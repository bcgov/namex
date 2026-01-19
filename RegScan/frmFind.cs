using System;
using System.Collections.Generic;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Windows.Forms;

namespace RegScan
{
    public partial class frmFind : Form
    {

        private int _versionIndex = 0;                                      // Index of current version being displayed.
        private List<DocumentObj> _docList = null;
        private int _imageIndex = 0;                                        // Index of current imagebeing displayed.
        List<string> _tempFileNameList = new List<string>();

        public frmFind()
        {
            InitializeComponent();
            txtBarCodeToFind.Focus();
            this.AcceptButton = btnFind;
        }

        private void btnClose_Click(object sender, EventArgs e)
        {
            // Delete any tempoary FileNames.
            try
            {
                foreach (var fileName in _tempFileNameList)
                    File.Delete(fileName);
                _tempFileNameList.Clear();
            }
            catch { }

            this.Close();
        }

        private void btnFind_Click(object sender, EventArgs e)
        {
            _versionIndex = 0;
            _docList = DocumentObj.Find(txtBarCodeToFind.Text).OrderBy(d => d.VersionNumber).ToList();
            if (_docList.Count() == 0)
                MessageBox.Show("No document(s) found for this barcode");
            else
            {
                if (_docList.Count > 1)
                {
                    pnlVersionDisplay.Visible = true;

                }
                else
                {
                    pnlVersionDisplay.Visible = false;
                }
                SetForm(_docList[_versionIndex]);
                SetImageButtons(_docList[_versionIndex]);
                UpdateDisplay();

            }

        }

        private void btnNext_Click(object sender, EventArgs e)
        {
            if (_versionIndex + 2 > _docList.Count)
                return;

            SetForm(_docList[++_versionIndex]);
            UpdateDisplay();
        }

        private void btnPrevious_Click(object sender, EventArgs e)
        {
            if (_versionIndex - 1 < 0)
                return;

            SetForm(_docList[--_versionIndex]);
            UpdateDisplay();
        }

        private void UpdateDisplay()
        {
            string display = (_versionIndex + 1).ToString();
            lbDisplayVersion.Text = display + " of " + _docList.Count.ToString();
            SetImageButtons(_docList[_versionIndex]);
        }

        private void SetImageButtons(DocumentObj _DocObj)
        {
            if (_DocObj.ImageList.Count > 1)
            {
                pnlNextPreviosImage.Visible = true;
            }
            else
            {
                pnlNextPreviosImage.Visible = false;
            }
            _imageIndex = 0;
            UpdateImageDisplay();
        }
        private void btnNextImage_Click(object sender, EventArgs e)
        {
            if (_docList == null)
                return;

            if (_imageIndex + 2 > _docList[_versionIndex].ImageList.Count)
                return;

            SetImage(_docList[_versionIndex].ImageList[++_imageIndex]);
            UpdateImageDisplay();
        }

        private void UpdateImageDisplay()
        {
            string display = (_imageIndex + 1).ToString();
            lbDisplayImage.Text = display + " of " + _docList[_versionIndex].ImageList.Count.ToString();
        }

        private void btnPreviousImage_Click(object sender, EventArgs e)
        {
            if (_docList == null)
                return;

            if (_imageIndex - 1 < 0)
                return;

            SetImage(_docList[_versionIndex].ImageList[--_imageIndex]);
            UpdateImageDisplay();
        }

        // Displays an Image.
        protected void SetImage(Bitmap _Image)
        {
            pbMainImageViewer.Image = _Image;
        }

        // Set the form from the document.
        protected void SetForm(DocumentObj _currentDocument)
        {
            txtBarCode.Text = _currentDocument.BarCode;
            txtDocumentId.Text = _currentDocument.DocumentId.ToString();
            txtLegalEntityKey.Text = _currentDocument.LegalEntityKey;
            txtOwner.Text = _currentDocument.Owner;
            txtDocumentDescription.Text = _currentDocument.Description;
            txtDocumentType.Text = _currentDocument.FQDocType;
            txtVersionNumber.Text = _currentDocument.VersionNumber.ToString();
            txtPagesInDocument.Text = _currentDocument.PageCount.ToString();
            txtBatchNumber.Text = _currentDocument.BatchId.ToString();
            txtAccessionNumber.Text = _currentDocument.AccessionNumberText;
            txtPagesInBox.Text = _currentDocument.PagesInBox.ToString();

            if (_currentDocument.IsScanned)
                _currentDocument.ConvertPDFToImageList();
            if (_currentDocument.ImageList.Count != 0)
                pbMainImageViewer.Image = _currentDocument.ImageList[0];
        }

        private void btnViewAsPDF_Click(object sender, EventArgs e)
        {
            if (_docList == null)
                return;

            if (_docList.Count() == 0)
                return;

            _tempFileNameList.Add(PDFObj.DisplayPdf(_docList[_versionIndex].PDFDocument));
        }

        private void frmFind_Load(object sender, EventArgs e)
        {
            txtBarCodeToFind.Focus();
        }

        private void frmFind_Activated(object sender, EventArgs e)
        {
            txtBarCodeToFind.Focus();
        }

    }
}
