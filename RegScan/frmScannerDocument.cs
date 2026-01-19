using AsyncRequests;
using PdfSharp.Drawing;
using PdfSharp.Pdf;
using System;
using System.Collections.Generic;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Windows.Forms;
using Vintasoft.Twain;

namespace RegScan
{
    public partial class frmScannerDocument : Form
    {

        #region Fields

        /// <summary>
        /// Current active document.
        /// </summary>
        DocumentObj _currentDocument = null;

        /// <summary>
        /// Current active batch number.
        /// </summary>
        BatchObj _currentBatchId = null;

        /// <summary>
        /// Options that control functions of application.
        /// </summary>
        private OptionsObj _options = null;

        /// <summary>
        /// Default setting for scanning parameters.
        /// </summary>
        private ScannerSettingObj _defaultSetting;

        /// <summary>
        /// List of all scananed images for the current document.
        /// </summary>
        private List<ImageObj> _scannedImageList = new List<ImageObj>();

        /// <summary>
        /// Index of current image being displayed.
        /// </summary>
        private int _currentImageIndex = -1;

        /// <summary>
        /// This is the list of bitmap images returned from the scanner from one scan session.
        ///     This may be one image or multiple images. 
        /// </summary>
        private List<string> _scanSessionFileList = new List<string>();

        /// <summary>
        /// image0 is the first page of the document and possibly contains a barcode.
        /// </summary>
        private Bitmap image0;

        /// <summary>
        /// PDF files created during viewing that can be deleted when form closes.
        /// </summary>
        List<string> _tempFileNameList = new List<string>();

        /// <summary>
        /// TWAIN device manager.
        /// </summary>
        DeviceManager _deviceManager = null;

        /// <summary>
        /// Current device.
        /// </summary>
        Device _currentDevice;

        /// <summary>
        /// Indicates that device is acquiring image(s).
        /// </summary>
        bool _isImageAcquiring;

        /// <summary>
        /// Determines that image acquistion must be canceled because application's form is closing.
        /// </summary>
        bool _cancelTransferBecauseFormIsClosing;

        #endregion
        public frmScannerDocument()
        {
            InitializeComponent();

            UtilityObj.createFolder("Images");

            // Set scanner defaults.
            _defaultSetting = new ScannerSettingObj();
            SetSettingValues();
            useAdfCheckBox_CheckedChanged(new object(), new EventArgs());

            // Load combo boxes
            cBoxOrientation.Items.Add(PdfSharp.PageOrientation.Landscape.ToString());
            cBoxOrientation.Items.Add(PdfSharp.PageOrientation.Portrait.ToString());
            cBoxOrientation.SelectedIndex = -1;

            cBoxPageSize.Items.Add(PdfSharp.PageSize.Letter.ToString());
            cBoxPageSize.Items.Add(PdfSharp.PageSize.Legal.ToString());
            cBoxPageSize.SelectedIndex = -1;

            // Get the options
            _options = new OptionsObj();
            TwainEnvironment.EnableDebugging("c:\\scanner25\\vstwain.log");
            TwainEnvironment.DebugLevel = DebugLevel.Debug;

            // create TWAIN device manager
            CreateTwainDeviceManager();
        }

        public void SetSettingValues()
        {
            useAdfCheckBox.Checked = _defaultSetting.UseDocumentFeeder;
            useDuplexCheckBox.Checked = _defaultSetting.UseDuplex;
            useUICheckBox.Checked = _defaultSetting.ShowTwainUI;
            showProgressIndicatorUICheckBox.Checked = _defaultSetting.ShowProgressIndicatorUI;
            ckBoxLowResolution.Checked = _defaultSetting.BlackAndWhiteCheckBox;
        }

        public void CreateTwainDeviceManager()
        {
            try
            {
                if (_deviceManager != null)
                    _deviceManager.Close();
                _deviceManager = new DeviceManager(this, CountryCode.Canada, LanguageType.EnglishCanadian);
                //Set the twaindsm path to the local folder if using 64 bit
                //_deviceManager.TwainDllPath = Directory.GetCurrentDirectory() + "\\TWAINDSM.dll";
            }
            catch { }
        }

        #region Scanning Session
        /// <summary>
        /// Process the scanned image.
        /// </summary>
        /// <param name="_Image"></param>
        private void ProcessScan(Bitmap _Image)
        {
            UtilityObj.writeLog("ProcessScan: Saving Scan");

            if (image0 == null)
            {
                image0 = _Image;
            }

            string fileName = "Images\\Bitmap_image " + Convert.ToString(_scanSessionFileList.Count) + ".bmp";
            UtilityObj.saveImageAsFile(fileName, _Image);

            // Save the image to file.
            _scanSessionFileList.Add(fileName);

            UtilityObj.writeLog("Scan List size: " + Convert.ToString(_scanSessionFileList.Count));
        }

        /// <summary>
        /// Process the completed scan session ... this contains most of the business logic of the application.
        /// </summary>
        private void ProcessCompleted()
        {
            UtilityObj.writeLog("Scanning finished");

            // Enable the form.
            Enabled = true;

            // If there is no scanned image (user might have clicked the close button)
            if (_scanSessionFileList.Count == 0)
                return;

            UtilityObj.writeLog("Fix Checking for barcode");
            // Scan for Barcodes
            var barcodes = BarCodeObj.Scan(image0);

            UtilityObj.writeLog("Fix Barcodes =" + barcodes.ToString());

            // IF we have a new document.
            if (_currentDocument == null)
            {
                UtilityObj.writeLog("Fix Current Doc is null");

                // IF we do not have a barcode.
                string barCode = "";
                if (barcodes.Count == 0)
                {
                    UtilityObj.writeLog("add barcode manually");
                    // Display the image.
                    SetImage(image0);

                    // Ask if a barcode shoulde be entered manually.
                    if (MessageBox.Show("No barcode found. Do you want to manually enter the barcode?", "Missing Barcode", MessageBoxButtons.YesNo) == System.Windows.Forms.DialogResult.Yes)
                    {
                        // Display dialog box to get manual entered barcode
                        var barCodeString = new BarCodeString();
                        var frm = new frmEnterBarCode(barCodeString);
                        frm.ShowDialog();
                        barCode = barCodeString.BarCode;
                    }
                }
                else
                {
                    UtilityObj.writeLog("Fix barcode found=" + barcodes[0].ToString());
                    // Assume the first bar code found is the correct one.
                    barCode = barcodes[0].ToString();
                }

                UtilityObj.writeLog("Fix Set List of Docs");
                // List to hold the documents.
                List<DocumentObj> docs = null;

                // If a bar code was found.
                if (barCode != "")
                {
                    UtilityObj.writeLog("Fix Barcode not null");
                    bool documentsFound = false;
                    bool neos = true;
                    while (neos)
                    {
                        UtilityObj.writeLog("Fix neos=true Searching for doc with associated barcode");
                        // Find the associated existing documents for this barcode ... There may be more than one document (known as versions)
                        docs = DocumentObj.Find(barCode);

                        // IF no documents were found
                        if (docs.Count == 0)
                        {
                            UtilityObj.writeLog("Fix No existing docs, SetImage(image0)");
                            // Display message that no documents(s) found for this barcode.
                            SetImage(image0);
                            // Ask if a barcode shoulde be entered manually.
                            if (MessageBox.Show("No documents found for barcode " + barCode + ". Do you want to manually enter the barcode?", "No Documents Found", MessageBoxButtons.YesNo) == System.Windows.Forms.DialogResult.Yes)
                            {
                                // Display dialog box to get manual entered barcode
                                var barCodeString = new BarCodeString();
                                var frm = new frmEnterBarCode(barCodeString);
                                frm.ShowDialog();
                                barCode = barCodeString.BarCode;
                            }
                            else
                                // Move on to next step.
                                neos = false;
                        }
                        else
                        {                           
                            // Indicate documents found and time to move onto next step.
                            documentsFound = true;
                            neos = false;
                        }
                    }            

                    if (documentsFound)
                    {
                        UtilityObj.writeLog("Fix Set current doc to docs[0]");
                        // The first document is the latest and is the one that will be displayed.
                        _currentDocument = docs[0];

                        // Display the warning if there was some sort of error getting the document.
                        if (_currentDocument.Error != "")
                            MessageBox.Show("Warning an error was found -> " + _currentDocument.Error);
                                            
                        // Will only be true, if it is an existing scan and new version is not required.
                        bool cancelScan = false;

                        // IF document has been purged.
                        if (_currentDocument.IsPurged)
                        {
                            // Cancel the scan and display a message.
                            cancelScan = true;
                            MessageBox.Show("This barcode number has already been used and deleted. It cannot be re-used.");
                        }
                        else
                        {
                            // IF document has already been scanned.
                            //if (_currentDocument.IsScanned)
                            if (_currentDocument.DocumentURL != "")
                            {
                                UtilityObj.writeLog("Document barcode already exists.");
                                // Turn off buttons for new box number.
                                btnNewBox.Enabled = false;

                                // Ask if this is a new version.
                                if (MessageBox.Show("Document with barcode " + barCode + " has already been scanned. Do you want to create a new version?", "Document Already Scanned", MessageBoxButtons.YesNo, MessageBoxIcon.Question) == System.Windows.Forms.DialogResult.Yes)
                                {
                                    // If a new version, then update the version number and set id to new
                                    _currentDocument.VersionNumber++;
                                    _currentDocument.SetToNew();
                                }
                                else
                                    // Cancel this scan if a new vesion is not required.
                                    cancelScan = true;
                            }
                            else
                            {
                                // Check for box full and display a message if it is full.
                                if ((_currentDocument.PageCount + _currentDocument.PagesInBox) > _options.MaximumPagesInBox)
                                    MessageBox.Show("Warning - Current Box will exceed limit of " + _options.MaximumPagesInBox.ToString() + " pages, after these pages are added");
                            }
                        }

                        // IF scan is to be cancelled
                        if (cancelScan)
                        {
                            // Set current document back to null.
                            _currentDocument = null;
                            UtilityObj.deleteFolder("Images");
                        }
                        else
                        {
                            // IF the current batch id is null
                            if (_currentBatchId == null)
                            {
                                // If the current document's batch is assigned.
                                if (_currentDocument.BatchId != 0)
                                {
                                    // Create a batch object and assigne current's document's values.
                                    _currentBatchId = new BatchObj();
                                    _currentBatchId.AccessionNumber = _currentDocument.AccessionNumber;
                                    _currentBatchId.BatchId = _currentDocument.BatchId;
                                }
                                else
                                {
                                    // Get the next batch id for this accession and assign it to the document.
                                    _currentBatchId = BatchObj.GetNextBatchId(_currentDocument.AccessionNumber);
                                    _currentDocument.BatchId = _currentBatchId.BatchId;
                                }
                            }
                            else
                            {
                                UtilityObj.writeLog("Fix No batchid");
                                // IF the accession number has changed, then get the next batch id and assign it.
                                if (_currentBatchId.AccessionNumber != _currentDocument.AccessionNumber)
                                    _currentBatchId = BatchObj.GetNextBatchId(_currentDocument.AccessionNumber);

                                // If the current document's batch is not assigned.
                                if (_currentDocument.BatchId == 0)
                                    _currentDocument.BatchId = _currentBatchId.BatchId;
                            }

                            UtilityObj.writeLog("Fix Display image");
                            // Display the document.
                            SetForm();

                            // Transfer images to our list of images for this document.
                            _scannedImageList.Clear();

                            // FOREACH of the pages scanned in this session.
                            foreach (var imageFile in _scanSessionFileList)
                            {
                                Bitmap image = UtilityObj.readFileAsImage(imageFile);
                                // Calculate the page size and add the image to the overall scanned list.
                                var pageSize = ImageObj.GetPageSize(image.Width, image.Height);

                                _scannedImageList.Add(new ImageObj(image, PdfSharp.PageOrientation.Portrait, pageSize));
                                image = null;
                            }

                            UtilityObj.writeLog("Fix SetImageNav");
                            // Display the first document.
                            _currentImageIndex = 0;
                            SetImageNav();
                        }                        
                    }                    
                }
                else
                {                    
                    // Clear Image
                    imageBox.Image = null;
                }                
            }

            // Existing docucment.
            else
            {
                // IF we have a barcode
                if (barcodes.Count != 0)
                {
                    // Display a warning message.
                    MessageBox.Show("Warning! A barcode was found on this page. Click OK to continue");
                }

                // Save the images.
                foreach (var imageFile in _scanSessionFileList)
                {
                    var image = UtilityObj.readFileAsImage(imageFile);
                    _currentImageIndex++;
                    var pageSize = ImageObj.GetPageSize(image.Width, image.Height);
                    _scannedImageList.Add(new ImageObj(image, PdfSharp.PageOrientation.Portrait, pageSize));
                }

                SetImageNav();

            }            
        }

        #endregion

        #region Image Display.

        /// <summary>
        ///  Sets the image on the image naviagtion panel.
        /// </summary>
        private void SetImageNav()
        {
            if (_currentImageIndex == -1)
                return;
            UpdateImageDisplay();
        }

        /// <summary>
        ///  Display next image.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnNextImage_Click(object sender, EventArgs e)
        {
            if (_currentImageIndex + 2 > _scannedImageList.Count)
                return;
            ++_currentImageIndex;
            UpdateImageDisplay();
        }

        /// <summary>
        /// Display previous image.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnPreviousImage_Click(object sender, EventArgs e)
        {
            if (_currentImageIndex - 1 < 0)
                return;
            --_currentImageIndex;
            UpdateImageDisplay();
        }

        /// <summary>
        /// Update the image display.
        /// </summary>
        private void UpdateImageDisplay()
        {
            if (_currentImageIndex > -1)
            {
                //SetImage(_scannedImageList[_currentImageIndex].Image);
                string imageFile = "Images\\Bitmap_image " + Convert.ToString(_currentImageIndex) + ".bmp";
                var image = UtilityObj.readFileAsImage(imageFile);
                SetImage(image);
                SetOrientation(_scannedImageList[_currentImageIndex].Orientation.ToString());
                SetPageSize(_scannedImageList[_currentImageIndex].PageSize.ToString());
            }

            lbPagesScanned.Text = "Pages Scanned: " + _scannedImageList.Count().ToString();
            string display = (_currentImageIndex + 1).ToString();
            lbDisplayImage.Text = display + " of " + _scannedImageList.Count.ToString();
            if (_currentImageIndex != 0)
                btnDeleteImage.Visible = true;
            else
                btnDeleteImage.Visible = false;

            btnViewAsPDF.Enabled = true;
            btnSharpen.Enabled = true;
            btnPrintBatchLabel.Enabled = true;
            btnNewBox.Enabled = true;
            cBoxOrientation.Enabled = true;
            cBoxPageSize.Enabled = true;
        }

        #endregion
        #region click events.
        private void btnRotate_Click(object sender, EventArgs e)
        {
            // Rotate current image and 
            _scannedImageList[_currentImageIndex].Rotate();
            UpdateImageDisplay();
        }

        /// <summary>
        /// View the scanned pages as a PDF.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnViewAsPDF_Click(object sender, EventArgs e)
        {
            // Nothing to view if no document
            if (_currentDocument == null)
                return;

            // Create a PDF document.
            var pdf = new PdfDocument();
            int updateCount = ((int)100 / _scannedImageList.Count) / 2;
            progressBar.Value = updateCount;
            progressBar.Visible = true;
            Application.DoEvents();

            UtilityObj.writeLog(Convert.ToString(_scannedImageList.Count) + " btnViewAsPDF_Click Scanner  Objects");

            // FOREACH image create a new page.
            foreach (var bp in _scannedImageList)
            {
                // Create a new page and add in the image.
                var pdfPage = new PdfPage();
                pdfPage.Size = bp.PageSize;
                pdfPage.Orientation = bp.Orientation;
                pdf.AddPage(pdfPage);
                var xgr = XGraphics.FromPdfPage(pdfPage);
                var img = XImage.FromGdiPlusImage(bp.Image);
                xgr.DrawImage(img, 0, 0);

                // Update progress bar
                txtMessage.Text += "\r\n" + "Page Size: " + pdfPage.Size.ToString();
                progressBar.Value += updateCount;
                Application.DoEvents();

            }

            _tempFileNameList.Add(PDFObj.DisplayPdf(pdf));
            progressBar.Visible = false;

        }

        /// <summary>
        ///  Save the document to the database.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnSave_Click(object sender, EventArgs e)
        {

            // Validation
            if (_currentDocument == null)
                return;

            if (_currentDocument.PageCount != _scannedImageList.Count)
            {
                if (MessageBox.Show("Number of pages scanned does not match number of pages expected ... Save?", "Page Mismatch", MessageBoxButtons.YesNo) == System.Windows.Forms.DialogResult.No)
                    return;
            }

            // Create a PDF document.
            var pdf = new PdfDocument();
            int updateCount = ((int)100 / _scannedImageList.Count) / 2;
            progressBar.Value = updateCount;
            progressBar.Visible = true;
            Application.DoEvents();

            UtilityObj.writeLog(Convert.ToString(_scannedImageList.Count) + " btnSave_Click Scanner  Objects");

            // FOREACH image create a new page.
            foreach (var bp in _scannedImageList)
            {

                // Create a new page and add in the image.
                var pdfPage = new PdfPage();
                pdfPage.Size = bp.PageSize;
                pdfPage.Orientation = bp.Orientation;
                pdf.AddPage(pdfPage);
                var xgr = XGraphics.FromPdfPage(pdfPage);
                var img = XImage.FromGdiPlusImage(bp.Image);
                xgr.DrawImage(img, 0, 0);

                // Update progress bar
                progressBar.Value += updateCount;
                Application.DoEvents();

            }

            // Update the document.
            _currentDocument.PDFDocument = pdf;
            _currentDocument.Description = txtDocumentDescription.Text;
            _currentDocument.PageCount = _scannedImageList.Count;
            _currentDocument.ScannerId = Environment.UserName;
            _currentDocument.ScannedDate = DateTime.Now;
            _currentDocument.ImageList = _scannedImageList.Select(i => i.Image).ToList();
            _currentDocument.UpdateInsert();

            // Reset the document and dispaly.
            ResetDocument();
            progressBar.Visible = false;

        }

        /// <summary>
        /// Cancel the scan.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnCancelScan_Click(object sender, EventArgs e)
        {
            // Reset the document and clear the display.
            ResetDocument();
        }

        /// <summary>
        /// Automated Document Feeder checkbox clicked.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void useAdfCheckBox_CheckedChanged(object sender, EventArgs e)
        {
            // If adf, then allow duplex.
            if (useAdfCheckBox.Checked)
                useDuplexCheckBox.Enabled = true;
            else
            {
                // otherwise insure not checked or can be checked.
                useDuplexCheckBox.Enabled = false;
                useDuplexCheckBox.Checked = false;
            }
        }

        /// <summary>
        /// Create a new box number.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnNewBox_Click(object sender, EventArgs e)
        {
            CreateNewBoxNumber();
        }

        /// <summary>
        /// Print the batch label.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnPrintBatchLabel_Click(object sender, EventArgs e)
        {

            // IF no document or batch, then don't proceed.
            if (_currentDocument == null || _currentBatchId == null)
                return;

            // Display the batch form.
            var frm = new frmBatchPrint(_currentBatchId, true);
            frm.ShowDialog();

            // If the batch ID was changed
            if (_currentBatchId.BatchId != int.Parse(txtBatchNumber.Text))
            {
                // Then update on the form and in the document object.
                txtBatchNumber.Text = _currentBatchId.BatchId.ToString();
                _currentDocument.BatchId = _currentBatchId.BatchId;
            }
        }

        /// <summary>
        ///  Delete the current image from teh list.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnDeleteImage_Click(object sender, EventArgs e)
        {
            // Confirm this image is to be deleted.
            if (MessageBox.Show("Are you sure you want to delete this page?", "Confirm Deletion", MessageBoxButtons.YesNo) == System.Windows.Forms.DialogResult.Yes)
            {
                _scannedImageList.RemoveAt(_currentImageIndex);
                _currentImageIndex--;
                UpdateImageDisplay();
            }
        }

        /// <summary>
        /// Fires when this forms becomes active.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void frmScanDocument_Activated(object sender, EventArgs e)
        {
            // Form is maximized.
            this.WindowState = FormWindowState.Maximized;                      

            // Scan button is set as the focus.
            btnScanPage.Focus();
        }

        /// <summary>
        /// The orientation was changed.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void cBoxOrientation_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (cBoxOrientation.Text == PdfSharp.PageOrientation.Landscape.ToString())
                _scannedImageList[_currentImageIndex].Orientation = PdfSharp.PageOrientation.Landscape;
            else if (cBoxOrientation.Text == PdfSharp.PageOrientation.Portrait.ToString())
                _scannedImageList[_currentImageIndex].Orientation = PdfSharp.PageOrientation.Portrait;
        }

        /// <summary>
        /// The Page size was changed.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void cBoxPageSize_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (cBoxPageSize.Text == PdfSharp.PageSize.Letter.ToString())
                _scannedImageList[_currentImageIndex].PageSize = PdfSharp.PageSize.Letter;
            else if (cBoxPageSize.Text == PdfSharp.PageSize.Legal.ToString())
                _scannedImageList[_currentImageIndex].PageSize = PdfSharp.PageSize.Legal;
        }
        #endregion

        #region house keeping methods

        /// <summary>
        /// Reset the document.
        /// </summary>
        private void ResetDocument()
        {
            // Clear document.
            _currentDocument = null;
            _scannedImageList.Clear();
            _currentImageIndex = -1;

            // Clear the document.
            txtBarCode.Text = "";
            txtDocumentId.Text = "";
            txtLegalEntityKey.Text = "";
            txtOwner.Text = "";
            txtDocumentDescription.Text = "";
            txtDocumentType.Text = "";
            txtVersionNumber.Text = "";
            txtPagesInDocument.Text = "";
            txtBatchNumber.Text = "";
            txtAccessionNumber.Text = "";
            txtPagesInBox.Text = "";
            imageBox.Image = null;
            heightLabel.Text = "";
            widthLabel.Text = "";
            lbDisplayImage.Text = "0 of 0";
            lbPagesScanned.Text = "Pages Scanned: 0";
            btnDeleteImage.Visible = false;
            btnNewBox.Enabled = false;
            btnPrintBatchLabel.Enabled = false;
            btnViewAsPDF.Enabled = false;
            btnSharpen.Enabled = false;
            cBoxOrientation.Enabled = false;
            cBoxOrientation.SelectedIndex = -1;
            cBoxPageSize.Enabled = false;

            // Delete any tempoary FileNames.
            try
            {
                foreach (var fileName in _tempFileNameList)
                    File.Delete(fileName);
                _tempFileNameList.Clear();
            }
            catch { }

            txtMessage.Text = "";
            imageBox.Image = null;
        }

        /// <summary>
        ///  Set the current selected Orientation in the combo box.
        /// </summary>
        /// <param name="_Orientation"></param>
        private void SetOrientation(string _Orientation)
        {

            for (int i = 0; i < cBoxOrientation.Items.Count; i++)
            {
                if (cBoxOrientation.Items[i].ToString() == _Orientation)
                    cBoxOrientation.SelectedIndex = i;
            }
        }

        /// <summary>
        /// Set the current selected Page Size in the combo box.
        /// </summary>
        /// <param name="_PageSize"></param>
        private void SetPageSize(string _PageSize)
        {
            for (int i = 0; i < cBoxPageSize.Items.Count; i++)
            {
                if (cBoxPageSize.Items[i].ToString() == _PageSize)
                    cBoxPageSize.SelectedIndex = i;
            }
        }

        /// <summary>
        /// Create a new box number.
        /// </summary>
        private void CreateNewBoxNumber()
        {
            // Dont' proceed if no current document.
            if (_currentDocument == null)
                return;

            // Create a copy of our box.
            var box = new BoxObj();
            BoxObj.CopyBox(_currentDocument.Box, box);

            // Make use of our existing form to create the new box.
            var frm = new frmBox();
            var status = frm.SetBoxNumber(box);
            if (status != "")
            {
                MessageBox.Show(status);
                frm.Dispose();
            }
            else
            {
                // Display the form.
                frm.ShowDialog();

                // IF a new box was created.
                if (!CompareBoxes(box, _currentDocument.Box))
                {
                    // Reset everything on this end.
                    _currentDocument.Box = box;
                    _currentDocument.AccessionNumber = long.Parse(box.AccessionNumber.Replace("-", ""));       // Remove formatting.
                    _currentBatchId.AccessionNumber = _currentDocument.AccessionNumber;
                    _currentBatchId.BatchId = 1;
                    _currentDocument.BatchId = _currentBatchId.BatchId;
                    txtBatchNumber.Text = _currentBatchId.BatchId.ToString();
                    txtAccessionNumber.Text = box.AccessionNumber;
                    txtPagesInBox.Text = box.PageCount.ToString();
                }
            }

        }

        /// <summary>
        /// Compare two boxes to see if they are the same
        /// </summary>
        /// <param name="_Box1"></param>
        /// <param name="_Box2"></param>
        /// <returns>False if they are not the same.</returns>
        private bool CompareBoxes(BoxObj _Box1, BoxObj _Box2)
        {
            bool result = false;

            if (_Box1.SequenceNumber == _Box2.SequenceNumber && _Box1.ScheduleNumber == _Box2.ScheduleNumber && _Box1.BoxNumber == _Box2.BoxNumber)
                result = true;

            return result;
        }

        /// <summary>
        /// Sets the image in the image box.
        /// </summary>
        /// <param name="_Image"></param>
        protected void SetImage(Bitmap _Image)
        {
            imageBox.SizeToFit = true;
            imageBox.Image = _Image;
            imageBox.SizeToFit = false;
        }

        /// <summary>
        /// Set the form from the document.
        /// </summary>
        protected void SetForm()
        {
            txtBarCode.Text = _currentDocument.BarCode;
            txtDocumentId.Text = _currentDocument.DocumentId == "" ? "[not assigned]" : _currentDocument.DocumentId.ToString();
            txtLegalEntityKey.Text = _currentDocument.LegalEntityKey;
            txtOwner.Text = _currentDocument.Owner;
            txtDocumentDescription.Text = _currentDocument.Description;
            txtDocumentType.Text = _currentDocument.FQDocType;
            txtVersionNumber.Text = _currentDocument.VersionNumber.ToString();
            txtPagesInDocument.Text = _currentDocument.PageCount.ToString();
            txtBatchNumber.Text = _currentDocument.BatchId.ToString();
            txtAccessionNumber.Text = _currentDocument.AccessionNumberText;
            txtPagesInBox.Text = _currentDocument.PagesInBox.ToString();
        }
        #endregion



        #region  Image Zoom Event Handlers

        /// <summary>
        /// Image was scrolled.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void imageBox_Scroll(object sender, ScrollEventArgs e)
        {
            this.UpdateStatusBar();
        }

        /// <summary>
        /// Update the status bar for the image.
        /// </summary>
        private void UpdateStatusBar()
        {
            positionToolStripStatusLabel.Text = imageBox.AutoScrollPosition.ToString();
            imageSizeToolStripStatusLabel.Text = imageBox.GetImageViewPort().ToString();
            zoomToolStripStatusLabel.Text = string.Format("{0}%", imageBox.Zoom);
        }

        /// <summary>
        /// Image was zoomed in or out.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void imageBox_ZoomChanged(object sender, EventArgs e)
        {
            this.UpdateStatusBar();
        }

        /// <summary>
        /// Image was resized.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void imageBox_Resize(object sender, EventArgs e)
        {
            this.UpdateStatusBar();
        }

        #endregion  Event Handlers

        #region Scanning Session.

        /// <summary>
        /// Subscribe to the device events.
        /// </summary>
        private void SubscribeToDeviceEvents(Device device)
        {
            try
            {
                device.ImageAcquiringProgress += new EventHandler<ImageAcquiringProgressEventArgs>(device_ImageAcquiringProgress);
                device.ImageAcquired += new EventHandler<ImageAcquiredEventArgs>(device_ImageAcquired);
                device.ScanFailed += new EventHandler<ScanFailedEventArgs>(device_ScanFailed);
                device.AsyncEvent += new EventHandler<DeviceAsyncEventArgs>(device_AsyncEvent);
                device.ScanFinished += new EventHandler(device_ScanFinished);
            }
            catch
            {
                MessageBox.Show("Error, scanner not found. Is the scanner turned on?", "TWAIN device error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                Environment.Exit(0);
            }
        }

        /// <summary>
        /// Unsubscribe from the device events.
        /// </summary>
        private void UnsubscribeFromDeviceEvents(Device device)
        {
            device.ImageAcquiringProgress -= new EventHandler<ImageAcquiringProgressEventArgs>(device_ImageAcquiringProgress);
            device.ImageAcquired -= new EventHandler<ImageAcquiredEventArgs>(device_ImageAcquired);
            device.ScanFailed -= new EventHandler<ScanFailedEventArgs>(device_ScanFailed);
            device.AsyncEvent -= new EventHandler<DeviceAsyncEventArgs>(device_AsyncEvent);
            device.ScanFinished -= new EventHandler(device_ScanFinished);
        }

        /// <summary>
        /// Image is being acquired.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void device_ImageAcquiringProgress(object sender, ImageAcquiringProgressEventArgs e)
        {
            // image acquistion must be canceled because application's form is closing
            if (_cancelTransferBecauseFormIsClosing)
            {
                // cancel image acquisition
                _currentDevice.CancelTransfer();
                return;
            }


            progressBar.Value = (int)e.Progress;

            //UtilityObj.writeLog(Convert.ToString(progressBar.Value) + " device_ImageAcquiringProgress");

            if (progressBar.Value == 100)
            {
                progressBar.Value = 0;
            }
        }

        private void device_ImageAcquired(object sender, ImageAcquiredEventArgs e)
        {
            // image acquistion must be canceled because application's form is closing
            if (_cancelTransferBecauseFormIsClosing)
            {
                // cancel image acquisition
                _currentDevice.CancelTransfer();
                return;
            }

            Bitmap acquiredImage = new Bitmap(e.Image.GetAsBitmap());

            ProcessScan(acquiredImage);

        }

        /// <summary>
        /// Device is running in async mode.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void device_AsyncEvent(object sender, DeviceAsyncEventArgs e)
        {
            UtilityObj.writeLog("device_AsyncEvent");
            switch (e.DeviceEvent)
            {
                case DeviceEventId.PaperJam:
                    MessageBox.Show("Paper is jammed.");
                    break;

                case DeviceEventId.CheckDeviceOnline:
                    MessageBox.Show("Check that device is online.");
                    break;

                case DeviceEventId.CheckBattery:
                    MessageBox.Show(string.Format("DeviceEvent: Device={0}, Event={1}, BatteryMinutes={2}, BatteryPercentage={3}",
                        e.DeviceName, e.DeviceEvent, e.BatteryMinutes, e.BatteryPercentage));
                    break;

                case DeviceEventId.CheckPowerSupply:
                    MessageBox.Show(string.Format("DeviceEvent: Device={0}, Event={1}, PowerSupply={2}",
                        e.DeviceName, e.DeviceEvent, e.PowerSupply));
                    break;

                case DeviceEventId.CheckResolution:
                    MessageBox.Show(string.Format("DeviceEvent: Device={0}, Event={1}, Resolution={2}",
                        e.DeviceName, e.DeviceEvent, e.Resolution));
                    break;

                case DeviceEventId.CheckFlash:
                    MessageBox.Show(string.Format("DeviceEvent: Device={0}, Event={1}, FlashUsed={2}",
                        e.DeviceName, e.DeviceEvent, e.FlashUsed));
                    break;

                case DeviceEventId.CheckAutomaticCapture:
                    MessageBox.Show(string.Format("DeviceEvent: Device={0}, Event={1}, AutomaticCapture={2}, TimeBeforeFirstCapture={3}, TimeBetweenCaptures={4}",
                        e.DeviceName, e.DeviceEvent, e.AutomaticCapture, e.TimeBeforeFirstCapture, e.TimeBetweenCaptures));
                    break;

                default:
                    MessageBox.Show(string.Format("DeviceEvent: Device={0}, Event={1}",
                        e.DeviceName, e.DeviceEvent));
                    break;
            }

            // if device is enabled or transferring images
            if (_currentDevice.State >= DeviceState.Enabled)
                return;

            // close the device
            _currentDevice.Close();
        }

        /// <summary>
        /// Scan failed event.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void device_ScanFailed(object sender, ScanFailedEventArgs e)
        {
            // show error message
            MessageBox.Show(e.ErrorString, "Scan failed", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }

        /// <summary>
        /// Scan session has finished event.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void device_ScanFinished(object sender, EventArgs e)
        {
            // close the device
            _currentDevice.Close();

            // specify that image acquisition is finished
            _isImageAcquiring = false;

            // Clear program bar.
            progressBar.Visible = false;

            // process the scanned images.
            ProcessCompleted();
        }

        /// <summary>
        /// Sets up the scanning session.
        /// </summary>
        /// <param name="sender"></param>p
        /// <param name="e"></param>
        private void btnScanPage_Click(object sender, EventArgs e)
        {            
            UtilityObj.deleteFolder("Images");
            _scanSessionFileList.Clear();
            image0 = null;
            UtilityObj.createFolder("Images");           

            // specify that image acquisition is started
            _isImageAcquiring = true;
            progressBar.Visible = true;

            try
            {

                // Open device manager, if not open.
                if (_deviceManager.State == DeviceManagerState.Closed)
                    _deviceManager.Open();

                if (_currentDevice != null)
                    // unsubscribe from the device events
                    UnsubscribeFromDeviceEvents(_currentDevice);

                // Get default device
                Device device = _deviceManager.DefaultDevice;
                _currentDevice = device;

                // subscribe to the device events
                SubscribeToDeviceEvents(_currentDevice);

                // set the image acquisition parameters
                device.ShowUI = useUICheckBox.Checked;
                device.ShowIndicators = showProgressIndicatorUICheckBox.Checked;
                device.ModalUI = false;
                device.DisableAfterAcquire = false;
                device.TransferMode = TransferMode.Memory;


                try
                {
                    // open the device
                    device.Open();
                }
                catch (Vintasoft.Twain.TwainException ex)
                {
                    // specify that image acquisition is finished
                    _isImageAcquiring = false;

                    MessageBox.Show(ex.Message.Replace("Unknown error 11.", "") + "Is the scanner " + device.Info.ProductName + " turned on?", "TWAIN device error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }
                catch(Exception ex2)
                {
                    MessageBox.Show(ex2.Message);
                    return;
                }

                // set device capabilities
                // unit of measure
                try
                {
                    if (device.UnitOfMeasure != UnitOfMeasure.Inches)
                        device.UnitOfMeasure = UnitOfMeasure.Inches;
                }
                catch (Vintasoft.Twain.TwainException)
                {
                }

                // resolution
                try
                {
                    if (ckBoxLowResolution.Checked)
                        device.Resolution = new Resolution(400, 400);
                    else
                        device.Resolution = new Resolution(600, 600);
                }
                catch (Vintasoft.Twain.TwainException)
                {
                }

                // ADF
                try
                {
                    device.DocumentFeeder.Enabled = useAdfCheckBox.Checked;
                }
                catch (TwainDeviceCapabilityException)
                {
                }

                // Duplex
                try
                {
                    device.DocumentFeeder.DuplexEnabled = useDuplexCheckBox.Checked;
                }
                catch (TwainDeviceCapabilityException)
                {
                }

                UtilityObj.writeLog("Checking for asynchronous scanning...");
                // if device supports asynchronous events
                if (device.IsAsyncEventsSupported)
                {
                    try
                    {
                        UtilityObj.writeLog("Device supports asynchronous scanning");
                        // enable all asynchronous events supported by device
                        device.AsyncEvents = device.GetSupportedAsyncEvents();
                    }
                    catch
                    {
                    }
                }


                try
                {
                    UtilityObj.writeLog("Start image acquisition");

                    // start image acquition process
                    device.Acquire();

                    UtilityObj.writeLog("End of image acquisition");
                }
                catch (Vintasoft.Twain.TwainException ex)
                {
                    // specify that image acquisition is finished
                    _isImageAcquiring = false;
                    UtilityObj.writeLog("Image acquisition error: " + ex);
                    MessageBox.Show(ex.Message, "TWAIN device", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }
            }
            finally
            {
               
            }
        }
        #endregion

    }
}
