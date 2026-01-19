using System;
using System.Windows.Forms;
using Vintasoft.Twain;
using Vintasoft.Twain.ImageEncoders;

namespace TwainAdvancedDemo
{
	public partial class TiffSaveSettingsForm : Form
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

		TiffCompression _compression = TiffCompression.Auto;
		public TiffCompression Compression
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

        public TiffSaveSettingsForm(bool isFileExist)
		{
			InitializeComponent();

			if (!isFileExist)
			{
				createNewDocumentaddToDocumentRadioButton.Checked = true;
				addToDocumentRadioButton.Enabled = false;
			}
        }

        #endregion


        #region Methods

        private void okButton_Click(object sender, EventArgs e)
		{
            _saveAllImages = saveAllImagesaddToDocumentRadioButton.Checked;

			_multiPage = addToDocumentRadioButton.Checked;

			if (noneCompressionRadioButton.Checked)
                _compression = TiffCompression.None;
			else if (ccittCompressionRadioButton.Checked)
                _compression = TiffCompression.CCITGroup4;
			else if (lzwCompressionRadioButton.Checked)
                _compression = TiffCompression.LZW;
			else if (jpegCompressionRadioButton.Checked)
			{
				_compression = TiffCompression.JPEG;
				_jpegQuality = (int)jpegQualityNumericUpDown.Value;
			}
			else if (zipCompressionRadioButton.Checked)
                _compression = TiffCompression.ZIP;
			else if (autoCompressionRadioButton.Checked)
                _compression = TiffCompression.Auto;

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