using System.Windows;
using System.Windows.Input;
using System.Windows.Controls;
using Vintasoft.WpfTwain;
using Vintasoft.WpfTwain.ImageEncoders;

namespace WpfTwainAdvancedDemo
{
    /// <summary>
    /// Interaction logic for PdfSaveSettingsForm.xaml
    /// </summary>
    public partial class PdfSaveSettingsWindow : Window
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

        public PdfSaveSettingsWindow(Window owner, bool isFileExist)
        {
            InitializeComponent();

            this.Owner = owner;

            if (!isFileExist)
            {
                rbCreateNewDocument.IsChecked = true;
                rbAddToDocument.IsEnabled = false;
            }
        }

        #endregion



        #region Methods

        private void bOk_Click(object sender, RoutedEventArgs e)
        {
            _saveAllImages = (bool)rbSaveAllImages.IsChecked;

            _multiPage = (bool)rbAddToDocument.IsChecked;
            _pdfACompatible = (bool)chkPdfACompatible.IsChecked;
            _pdfAuthor = txtPdfAuthor.Text;
            _pdfTitle = txtPdfTitle.Text;

            if ((bool)rbComprNone.IsChecked)
                _compression = PdfImageCompression.None;
            else if ((bool)rbComprCCITT.IsChecked)
                _compression = PdfImageCompression.CcittFax;
            else if ((bool)rbComprLzw.IsChecked)
                _compression = PdfImageCompression.LZW;
            else if ((bool)rbComprJpeg.IsChecked)
            {
                _compression = PdfImageCompression.JPEG;
                _jpegQuality = jpegQualityNumericUpDown.Value;
            }
            else if ((bool)rbComprZip.IsChecked)
                _compression = PdfImageCompression.ZIP;
            else if ((bool)rbComprAuto.IsChecked)
                _compression = PdfImageCompression.Auto;

            DialogResult = true;
        }

        private void EnableJpegCompressionQuality(object sender, RoutedEventArgs e)
        {
            if (!this.IsVisible)
                return;

            gbJpegCompression.IsEnabled = true;
        }

        private void DisableJpegCompressionQuality(object sender, RoutedEventArgs e)
        {
            if (!this.IsVisible)
                return;

            gbJpegCompression.IsEnabled = false;
        }

        private void bCancel_Click(object sender, RoutedEventArgs e)
        {
            DialogResult = false;
            Close();
        }

        #endregion

    }
}
