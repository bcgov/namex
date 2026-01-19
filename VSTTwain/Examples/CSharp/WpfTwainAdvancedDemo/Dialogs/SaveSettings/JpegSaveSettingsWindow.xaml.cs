using System.Windows;
using System.Windows.Input;
using System.Windows.Controls;

namespace WpfTwainAdvancedDemo
{
    /// <summary>
    /// Interaction logic for JpegSaveSettingForm.xaml
    /// </summary>
    public partial class JpegSaveSettingsWindow : Window
    {

        #region Properties

        int _quality = 90;
        public int Quality
        {
            get { return _quality; }
        }

        #endregion



        #region Constructors

        public JpegSaveSettingsWindow(Window owner)
        {
            InitializeComponent();

            this.Owner = owner;
        }

        #endregion



        #region Methods

        private void bOk_Click(object sender, RoutedEventArgs e)
        {
            _quality = nJpegQuality.Value;
            DialogResult = true;
        }

        private void bCancel_Click(object sender, RoutedEventArgs e)
        {
            DialogResult = false;
            Close();
        }

        #endregion

    }
}
