using ApiScanner;
using Microsoft.VisualBasic;
using Newtonsoft.Json.Linq;
using PdfSharp.Drawing.BarCodes;
using PdfSharp.Pdf;
using System;
using System.Collections.Generic;
using System.Data;
using System.Diagnostics.PerformanceData;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Security.Policy;
using System.Windows.Forms;

namespace RegScan
{
    public class DocumentObj
    {
        #region Properties and Constructors
        private DocumentModel ApiDocModel = new DocumentModel();
        private ScanningInfoModel ApiScanModel = new ScanningInfoModel();

        //DRS
        private string _documentURL;
        private string _documentClass;
        private string _documentServiceId;
        private string _documentExists;
        private string _documentTypeDescription;
        private DateTime _consumerFilingDate;
        private string _consumerIdentifier;
        private int _consumerReferenceId;
        private int _consumerDocumentId;
        object scanInfo;
        object scanDoc;

        //private long _documentId = UtilityObj.NOID;
        private string _documentId = "";
        private string _legalEntityKey;
        private string _ownerTypeCode;
        private string _documentTypeCode;
        private string _authorId;
        private string _description;
        private string _fileName;
        private string _fileExtension;
        private bool _isScanned;
        private bool _isPurged;
        private DateTime _createDateTime;
        private int _barCode;
        private int _pageCount;
        private long _accessionNumber;
        private int _batchId;
        private int _versionNumber;
        private string _owner;
        private int _eventId;
        private bool _eventIdIsNull;
        private string _scannerId;
        private DateTime _scannedDate;

        private Boolean _replaceFlag = false;
       

        // Calculated.
        private BoxObj _boxObj = null;        

        private PdfDocument _pdfDocument = null;
        private List<Bitmap> _imageList = new List<Bitmap>();

        // From document table
        public string DocumentURL { get { return _documentURL; } }
        public string DocumentId { get { return _documentId; } } //not used in data tables any longer
        public string LegalEntityKey { get { return _legalEntityKey; } }
        public string OwnerTypeCode { get { return _ownerTypeCode; } }
        public string DocumentTypeCode { get { return _documentTypeCode; } }
        public string AuthorId { get { return _authorId; } }
        public string Description { get { return _description; } set { _description = value; } }
        public string FileName { get { return _fileName; } }
        public string FileExtension { get { return _fileExtension; } }
        public bool IsScanned { get { return _isScanned; } }
        public bool IsPurged { get { return _isPurged; } }
        public DateTime CreateDateTime { get { return _createDateTime; } }
        public string BarCode { get { return _barCode.ToString(); } }
        public int PageCount { get { return _pageCount; } set { _pageCount = value; } }
        public long AccessionNumber { get { return _accessionNumber; } set { _accessionNumber = value; } }
        public string AccessionNumberString { get { return _accessionNumber.ToString().PadLeft(BoxObj.ACCESSION_NUMBER_LENGTH, '0'); } }
        public string AccessionNumberText { get { return AccessionNumberString.Substring(0, 2) + "-" + AccessionNumberString.Substring(2, 4) + "-" + AccessionNumberString.Substring(6, 4); } }
        public int BatchId { get { return _batchId; } set { _batchId = value; } }
        public int VersionNumber { get { return _versionNumber; } set { _versionNumber = value; } }
        public string ScannerId { get { return _scannerId; } set { _scannerId = value; } }
        public DateTime ScannedDate { get { return _scannedDate; } set { _scannedDate = value; } }

        public string Owner { get { return _owner; } }
        public BoxObj Box { get { return _boxObj; } set { _boxObj = value; } }

        // Calculated
        public PdfDocument PDFDocument { get { return _pdfDocument; } set { _pdfDocument = value; } }
        public List<Bitmap> ImageList { get { return _imageList; } set { _imageList = value; } }

        public int SequenceNumber { get { return int.Parse(AccessionNumberString.Substring(0, 2)); } }
        public int ScheduleNumber { get { return int.Parse(AccessionNumberString.Substring(2, 4)); } }
        public int BoxNumber { get { return int.Parse(AccessionNumberString.Substring(6, 4)); } }

        public int PagesInBox { get { return _boxObj == null ? 0 : _boxObj.PageCount; } }
        public int PdfPages { get { return _pdfDocument.PageCount; } }
        public string FQDocType { get { return DocTypeObj.Find(_documentTypeCode).FQDescription; } }

        public string Error = "";

        public DocumentObj()
        {
            _boxObj = new BoxObj();
        }

        #endregion

        #region dml
               
        private void Insert()
        {
            copyToModel();            
            byte[] pdfBytes = PDFObj.ConvertPdfToByteArray(_pdfDocument);
            string resp = DocumentApi.post(_fileName, pdfBytes, ApiDocModel);
            UpdateBoxPageCount();
        }
               
        private void Update()
        {
            copyToModel();

            byte[] pdfBytes = PDFObj.ConvertPdfToByteArray(_pdfDocument);
            
            string resp = DocumentApi.patch(ApiDocModel, _documentServiceId);
            if (resp.Contains("errorMessage")) {
                UtilityObj.writeLog("Scanned document Image failed PATCH to update information.");
                Environment.Exit(0);    
            }
            resp = DocumentApi.put(_fileName, pdfBytes, ApiDocModel);
            if (resp.Contains("errorMessage"))
            {
                MessageBox.Show("ERROR, scanned image failed to laod into database. Current data for " + BarCode + " may be inaccurrate.");
                UtilityObj.writeLog("Scanned document Image failed PUT to update old image.");
                Environment.Exit(0);
            }

            UpdateBoxPageCount();
        }

        public void UpdateInsert()
        {
            // Set some values before database requests.
            _isScanned = true;
            _fileExtension = "PDF";
            _fileName = _legalEntityKey + DateTime.Now.ToString("yyyy_MM_dd_hh_mm_ss");                    
            
            if (_replaceFlag)
                Update();
            else
                Insert();

            _replaceFlag = false;
        }

        private void UpdateBoxPageCount()
        {
            // Update Box Page Count
            _boxObj.PageCount += _pageCount;
            _boxObj.UpdatePageCount();
        }

        #endregion

        #region Utility 
        public void ConvertPDFToImageList()
        {
            // The document will be null if this is a new scan
            if (_pdfDocument == null)
                return;

            string fileName = System.IO.Path.GetTempPath() + Guid.NewGuid().ToString() + ".pdf";
            File.WriteAllBytes(fileName, PDFObj.ConvertPdfToByteArray(_pdfDocument));
            var pdf = new Cyotek.GhostScript.PdfConversion.Pdf2Image(fileName);
            _imageList = pdf.GetImages().ToList();
            File.Delete(fileName);
        }


        public void SetToNew()
        {
            //_documentId = "";          // _documentId = "" indicates a database insert, instead of an update.
            _replaceFlag = true;

            if (_documentClass == "SOCIETY")
            {
                _ownerTypeCode = "SOC";
            }
            else
            {
                _ownerTypeCode = _documentClass;
            }
            
            // Get the lates open box ... if one is not found, then one will be created.            
            _boxObj = BoxObj.Find(_ownerTypeCode);
            _accessionNumber = GetAccessionNumber(_boxObj);
            _batchId = 0;                           // Batch Id is reset to zero.
        }
        #endregion

        #region Static Find, Select and utility methods
        static public string ErrorMessage = "";


        //  _BarCode  == conDocId
        static public List<DocumentObj> Find(string _BarCode)
        {           
            ErrorMessage = "";
            List<DocumentObj> list = new List<DocumentObj>();           

            string resp = DocumentApi.get(_BarCode);

            if (resp.Contains("errorMessage"))
            {
                resp = "";
            }

            if (resp == "" )
            {                
                ErrorMessage = "No Documents Found For Barcode: " + _BarCode;
            }            
            else
            {
                var token = JToken.Parse(resp);
                string docClass = (string)token[0]["documentClass"];

                List<JObject> docList = DocumentApi.getDocObjectList(docClass, _BarCode);

                UtilityObj.writeLog("Fix3 API returned docList, Adding docs to list");
                foreach (JObject jDoc in docList)                   
                    list.Add(ExtractDocument(jDoc));
            }

            UtilityObj.writeLog("Return Ordered docs");

            // Return list ordered by Version Number Descending.
            return list.OrderByDescending(l => l.VersionNumber).ToList();

        }


        // Select the documents that match this barcode.
        static private DocumentObj ExtractDocument(JObject jDoc)
        {           
            UtilityObj.writeLog("Extract jDoc and scanning information.");

            DocumentObj docObj = new DocumentObj();
            copyFromModel(docObj, jDoc);

            if (jDoc["scanningInformation"] != null) {
                
                UtilityObj.writeLog("Extract jDoc and scanning information.");

                // If Accession Number
                if (docObj._accessionNumber == 0 )
                {
                    // Get the latest open box ... if one is not found, then one will be created.
                    docObj._boxObj = BoxObj.Find(docObj._ownerTypeCode);

                    // IF the box was not created
                    if (docObj._boxObj == null)
                    {
                        docObj.Error = BoxObj.ERROR_MESSAGE;
                    }
                    else
                        docObj.AccessionNumber = GetAccessionNumber(docObj._boxObj);
                }
                else
                {
                    // Get the existing box from the accession number.
                    string an = docObj._accessionNumber.ToString().PadLeft(BoxObj.ACCESSION_NUMBER_LENGTH, '0');
                    docObj._boxObj = BoxObj.Find(int.Parse(an.Substring(0, 2)), int.Parse(an.Substring(2, 4)), int.Parse(an.Substring(6, 4)));
                    docObj._accessionNumber = Convert.ToInt64(docObj._accessionNumber);
                }                               
            }
            else
            {
                UtilityObj.writeLog("No Scanning Information for Barcode " + docObj._consumerDocumentId);
            }

            // Make sure document exists
            if (docObj._documentURL != "")
            {
                Byte[] docBytes = DocumentApi.getDocBytes(docObj._documentURL);

                if (docBytes != null && docBytes.Length > 2000)
                {
                    docObj._pdfDocument = PDFObj.ConvertByteArrayToPDF(docBytes);
                }
            }
            return docObj;
        }
              

        // IF the document does not contain an assesion number, then get one based on the ower type code.
        static public long GetAccessionNumber(BoxObj _Box)
        {
            return long.Parse(_Box.SequenceNumber.ToString().PadLeft(2, '0') +
                              _Box.ScheduleNumber.ToString().PadLeft(4, '0') +
                              _Box.BoxNumber.ToString().PadLeft(4, '0'));

        }

        public void copyToModel()
        {
            ApiScanModel.accessionNumber = _accessionNumber;
            ApiScanModel.author = _authorId;
            ApiScanModel.batchId = _batchId;
            ApiScanModel.createDateTime = _createDateTime;
            ApiScanModel.pagecount = _pageCount;
            ApiScanModel.scannedDate = _scannedDate;

            ApiDocModel.author = _authorId;
            ApiDocModel.consumerDocumentId = _barCode;
            ApiDocModel.consumerFilename = _fileName;
            ApiDocModel.consumerFilingDate = DateTime.Now;
            ApiDocModel.consumerIdentifier = _consumerIdentifier;
            ApiDocModel.consumerReferenceId = "";
            ApiDocModel.createDateTime = _createDateTime;
            ApiDocModel.documentClass = _documentClass;
            ApiDocModel.documentExists = "";
            ApiDocModel.documentServiceId = _documentServiceId;
            ApiDocModel.documentType = _documentTypeCode;
            ApiDocModel.documentTypeDescription = "";
            ApiDocModel.documentURL = "";
            ApiDocModel.scanningInformation = ApiScanModel;
          
        }
        
        public void copyToModel(JObject temp, ScanningInfoModel scanInfo )
        {
            if (temp["accessionNumber"] != null) { ApiScanModel.accessionNumber = (long)temp["accessionNumber"]; }
            if (temp["authorId"] != null) { ApiScanModel.author = (string)temp["authorId"]; }
            if (temp["scannedDate"] != null) { ApiScanModel.scannedDate = (DateTime)temp["scannedDate"]; }
            if (temp["batchId"] != null) { ApiScanModel.batchId = (int)temp["batchId"]; }
            if (temp["createDateTime"] != null) { ApiScanModel.createDateTime = (DateTime)temp["createDateTime"]; }
            if (temp["pageCount"] != null) { ApiScanModel.pagecount = (int)temp["pageCount"]; }

            if (temp["author"] != null) { ApiDocModel.author = (string)temp["author"]; }
            if (temp["consumerDocumentId"] != null) { ApiDocModel.consumerDocumentId = (int)temp["consumerDocumentId"]; }
            if (temp["consumerFilename"] != null) { ApiDocModel.consumerFilename = (string)temp["consumerFilename"]; }
            if (temp["consumerFilingDate"] != null) { ApiDocModel.consumerFilingDate = (DateTime)temp["consumerFilingDate"]; }
            if (temp["consumerIdentifier"] != null) { ApiDocModel.consumerIdentifier = (string)temp["consumerIdentifier"]; }
            if (temp["consumerReferenceId"] != null) { ApiDocModel.consumerReferenceId = ""; }
            if (temp["createDateTime"] != null) { ApiDocModel.createDateTime = (DateTime)temp["createDateTime"]; }
            if (temp["documentClass"] != null) { ApiDocModel.documentClass = (string)temp["documentClass"]; }
            if (temp["documentExists"] != null) { ApiDocModel.documentExists = (string)temp["documentExists"]; }
            if (temp["documentId"] != null) { ApiDocModel.documentServiceId = (string)temp["documentId"]; }
            
            if (temp["documentType"] != null) { ApiDocModel.documentType = (string)temp["documentTypeCode"]; }
            //if (temp["documentType"] != null) { ApiDocModel.documentType = (string)temp["documentType"]; }


            if (temp["documentTypeDescription"] != null) { ApiDocModel.documentTypeDescription = (string)temp["documentTypeDescription"]; }
            if (temp["documentURL"] != null) { ApiDocModel.documentURL = (string)temp["documentURL"]; } 
                 
            ApiDocModel.scanningInformation = scanInfo;
        }

        
        static public void copyFromModel(DocumentObj docObj, JObject jDoc)
        {         
            if (jDoc["author"] != null) { docObj._authorId = (string)jDoc["author"]; }            
            if (jDoc["consumerDocumentId"] != null) { docObj._barCode = (int)jDoc["consumerDocumentId"]; }            
            if (jDoc["consumerFilename"] != null) { docObj._fileName = (string)jDoc["consumerFilename"]; }

            if (jDoc["consumerIdentifier"] != null) { docObj._legalEntityKey = (string)jDoc["consumerIdentifier"]; }
            if (jDoc["consumerIdentifier"] != null) { docObj._consumerIdentifier = (string)jDoc["consumerIdentifier"]; }

            if ( dataCheck(jDoc["consumerReferenceId"].ToString())) { docObj._consumerReferenceId = Int32.Parse(jDoc["consumerReferenceId"].ToString()); }
            if (jDoc["createDateTime"] != null) { docObj._createDateTime = (DateTime)jDoc["createDateTime"]; }

            if (jDoc["documentClass"] != null) { docObj._description = (string)jDoc["documentClass"]; }
            if (jDoc["documentClass"] != null) { docObj._documentClass = (string)jDoc["documentClass"]; }

            if (jDoc["documentServiceId"] != null) { docObj._documentServiceId = (string)jDoc["documentServiceId"]; }
            if (jDoc["documentType"] != null) { docObj._documentTypeCode = (string)jDoc["documentType"]; }
            if (jDoc["documentTypeDescription"] != null) { docObj._documentTypeDescription = (string)jDoc["documentTypeDescription"]; }
            if (jDoc["documentURL"] != null) { docObj._documentURL = (string)jDoc["documentURL"]; }

            if (jDoc["scanningInformation"] != null)
            {
                docObj.scanInfo = (object)jDoc["scanningInformation"];
                docObj.ApiScanModel = (ScanningInfoModel)docObj.scanInfo;

                docObj._accessionNumber = docObj.ApiScanModel.accessionNumber;
                docObj._authorId = docObj.ApiScanModel.author;
                docObj._batchId = docObj.ApiScanModel.batchId;
                docObj._createDateTime = docObj.ApiScanModel.createDateTime;
                docObj._pageCount = docObj.ApiScanModel.pagecount;
                docObj._scannedDate = docObj.ApiScanModel.scannedDate;                       
            }
        }        

        static private Boolean dataCheck(string jDoc)
        {
            if (jDoc == null || jDoc.ToString() == "") { return false; }
            return true;
        }

        #endregion      

    }
}
