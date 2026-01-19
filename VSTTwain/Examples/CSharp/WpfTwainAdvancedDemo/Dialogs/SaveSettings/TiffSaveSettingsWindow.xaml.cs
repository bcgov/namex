using System.Windows;
using System.Windows.Input;
using System.Windows.Controls;
using Vintasoft.WpfTwain;
using Vintasoft.WpfTwain.ImageEncoders;

namespace WpfTwainAdvancedDemo
{
    /// <summary>
    /// Interaction logic for TiffSaveSettingsForm.xaml
    /// </summary>
    public partial class TiffSaveSettingsWindow : Window
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

        public TiffSaveSettingsWindow(Window owner, bool isFileExist)
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
            
            if ((bool)rbComprNone.IsChecked)
                _compression = TiffCompression.None;
            else if ((bool)rbComprCCITT.IsChecked)
                _compression = TiffCompression.CCITGroup4;
            else if ((bool)rbComprLzw.IsChecked)
                _compression = TiffCompression.LZW;
            else if ((bool)rbComprJpeg.IsChecked)
            {
                _compression = TiffCompression.JPEG;
                _jpegQuality = nJpegQuality.Value;
            }
            else if ((bool)rbComprZip.IsChecked)
                _compression = TiffCompression.ZIP;
            else if ((bool)rbComprAuto.IsChecked)
                _compression = TiffCompression.Auto;

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
