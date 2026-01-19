using System;
using System.Windows.Forms;
using Vintasoft.Twain;
using Vintasoft.Twain.ImageEncoders;

namespace TwainAdvancedDemo
{
	public partial class PdfSaveSettingsForm : Form
    {

        #region Fields & properties

        bool _saveAllImages = false;
        public bool SaveAllImages
        {
            get { return _saveAllImages; }
        }
        
        bool _multiPage = true;
		public bool MultiPage
		{
			get { return _multiPage; }
		}

		bool _pdfACompatible = true;
		public bool PdfACompatible
		{
			get { return _pdfACompatible; }
		}

		string _pdfAuthor = string.Empty;
		public string PdfAuthor
		{
			get { return _pdfAuthor; }
		}

		string _pdfTitle = string.Empty;
		public string PdfTitle
		{
			get { return _pdfTitle; }
		}

		PdfImageCompression _compression = PdfImageCompression.Auto;
		public PdfImageCompression Compression
		{
			get { return _compression; }
		}
		
		int _jpegQuality = 90;
		public int JpegQuality
		{
			get { return _jpegQuality; }
        }

        #endregion


        #region Constructor

        public PdfSaveSettingsForm(bool isFileExist)
		{
			InitializeComponent();

			if (!isFileExist)
			{
				createNewDocumentRadioButton.Checked = true;
				addToDocumentRadioButton.Enabled = false;
			}
        }

        #endregion


        #region Methods

        private void okButton_Click(object sender, EventArgs e)
		{
            _saveAllImages = saveAllImagesRadioButton.Checked;

			_multiPage = addToDocumentRadioButton.Checked;
			_pdfACompatible = pdfACompatibleCheckBox.Checked;
			_pdfAuthor = pdfAuthorTextBox.Text;
			_pdfTitle = pdfTitleTextBox.Text;

			if (noneCompressionRadioButton.Checked)
                _compression = PdfImageCompression.None;
			else if (ccittCompressionRadioButton.Checked)
                _compression = PdfImageCompression.CcittFax;
			else if (lzwCompressionRadioButton.Checked)
                _compression = PdfImageCompression.LZW;
			else if (jpegCompressionRadioButton.Checked)
			{
				_compression = PdfImageCompression.JPEG;
				_jpegQuality = (int)jpegQualityNumericUpDown.Value;
			}
			else if (zipCompressionRadioButton.Checked)
                _compression = PdfImageCompression.ZIP;
			else if (autoCompressionRadioButton.Checked)
                _compression = PdfImageCompression.Auto;

			DialogResult = DialogResult.OK;
		}

		private void EnableJpegCompressionQuality(object sender, EventArgs e)
		{
			gbJpegCompression.Enabled = true;
		}

		private void DisableJpegCompressionQuality(object sender, EventArgs e)
		{
			gbJpegCompression.Enabled = false;
        }

        #endregion

    }
}