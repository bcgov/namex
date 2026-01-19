using System;
using System.IO;
using System.Reflection;
using System.Windows;
using Vintasoft.WpfTwain;

namespace WpfTwainFileTransferDemo
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {

        #region Fields

        /// <summary>
        /// TWAIN device manager.
        /// </summary>
        DeviceManager _deviceManager;

        /// <summary>
        /// Current device.
        /// </summary>
        Device _currentDevice;

        /// <summary>
        /// Index of acquired image.
        /// </summary>
        int _imageIndex;

        #endregion



        #region Constructors

        public MainWindow()
        {
            InitializeComponent();

            this.Title = string.Format("VintaSoft WPF TWAIN File Transfer Demo v{0}", TwainGlobalSettings.ProductVersion);

            // create instance of the DeviceManager class
            _deviceManager = new DeviceManager(this);
        }

        #endregion



        #region Methods

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            // get path to directory where acquired images will be saved

            string directoryForImages = System.IO.Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
            directoryForImages = Path.Combine(directoryForImages, "Images");
            if (!Directory.Exists(directoryForImages))
                Directory.CreateDirectory(directoryForImages);
            directoryForImagesTextBox.Text = directoryForImages;


            // open TWAIN device manager
            if (OpenDeviceManager())
            {
                // fill the device list

                devicesComboBox.Items.Clear();
                DeviceInfo deviceInfo;
                DeviceCollection devices = _deviceManager.Devices;
                for (int i = 0; i < devices.Count; i++)
                {
                    deviceInfo = devices[i].Info;
                    devicesComboBox.Items.Add(deviceInfo.ProductName);

                    if (devices[i] == _deviceManager.DefaultDevice)
                        devicesComboBox.SelectedIndex = i;
                }
            }
        }

        /// <summary>
        /// Sets window's UI state.
        /// </summary>
        private void SetWindowUiState(bool enabled)
        {
            devicesComboBox.IsEnabled = enabled;
            deviceSettingsGroupBox.IsEnabled = enabled;
            acquireImageWithUIButton.IsEnabled = enabled;
            acquireImageWithUIButton.IsEnabled = enabled;
            acquireImageWithoutUIButton.IsEnabled = enabled;
        }


        /// <summary>
        /// Opens TWAIN device manager.
        /// </summary>
        private bool OpenDeviceManager()
        {
            SetWindowUiState(false);

            // try to find the device manager 2.x
            _deviceManager.IsTwain2Compatible = true;
            // if TWAIN device manager 2.x is not available
            if (!_deviceManager.IsTwainAvailable)
            {
                // try to use TWAIN device manager 1.x
                _deviceManager.IsTwain2Compatible = false;
                // if TWAIN device manager 1.x is not available
                if (!_deviceManager.IsTwainAvailable)
                {
                    MessageBox.Show("TWAIN device manager is not found.");
                    return false;
                }
            }

            // open the device manager
            _deviceManager.Open();

            // if no devices are found in the system
            if (_deviceManager.Devices.Count == 0)
            {
                MessageBox.Show("No devices found.");
                return false;
            }

            SetWindowUiState(true);
            return true;
        }


        /// <summary>
        /// Current device is changed.
        /// </summary>
        private void devicesComboBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            SetWindowUiState(false);

            // get device
            Device device = _deviceManager.Devices.Find((string)devicesComboBox.SelectedItem);

            // get file formats and compressions supported by device
            GetSupportedFileFormatsAndCompressions(device);

            SetWindowUiState(true);
        }

        /// <summary>
        /// Gets file formats and compressions supported by device in File Transfer mode.
        /// </summary>
        private void GetSupportedFileFormatsAndCompressions(Device device)
        {
            // open the device
            device.Open();

            try
            {
                // get supported file formats

                TwainImageFileFormat currentFileFormat = device.FileFormat;
                TwainImageFileFormat[] fileFormats = device.GetSupportedImageFileFormats();

                supportedFileFormatsComboBox.Items.Clear();
                for (int i = 0; i < fileFormats.Length; i++)
                {
                    supportedFileFormatsComboBox.Items.Add(fileFormats[i]);

                    if (currentFileFormat == fileFormats[i])
                        supportedFileFormatsComboBox.SelectedIndex = i;
                }

                // get supported compressions

                TwainImageCompression currentCompression = device.ImageCompression;
                TwainImageCompression[] compressions = device.GetSupportedImageCompressions();

                supportedCompressionsComboBox.Items.Clear();
                for (int i = 0; i < compressions.Length; i++)
                {
                    supportedCompressionsComboBox.Items.Add(compressions[i]);

                    if (currentCompression == compressions[i])
                        supportedCompressionsComboBox.SelectedIndex = i;
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
            finally
            {
                // close the device
                device.Close();
            }
        }


        /// <summary>
        /// Acquire image with UI.
        /// </summary>
        private void acquireImageWithUIButton_Click(object sender, EventArgs e)
        {
            AcquireImage(true);
        }

        /// <summary>
        /// Acquire image without UI.
        /// </summary>
        private void acquireImageWithoutUIButton_Click(object sender, EventArgs e)
        {
            AcquireImage(false);
        }

        /// <summary>
        /// Acquire image.
        /// </summary>
        private void AcquireImage(bool showUI)
        {
            SetWindowUiState(false);

            if (_currentDevice != null)
                UnsubscribeFromDeviceEvents();

            Device device = _deviceManager.Devices.Find((string)devicesComboBox.SelectedItem);

            _currentDevice = device;
            // subscribe to the device events
            SubscribeToDeviceEvents();

            try
            {
                // set settings of scan session
                device.TransferMode = TransferMode.File;
                device.ShowUI = showUI;
                device.DisableAfterAcquire = !showUI;

                // open the device
                device.Open();

                try
                {
                    // set the file format in which acquired images must be saved
                    TwainImageFileFormat newFileFormat = TwainImageFileFormat.Bmp;
                    if (supportedFileFormatsComboBox.Items.Count > 0)
                        device.FileFormat = (TwainImageFileFormat)supportedFileFormatsComboBox.SelectedItem;
                    if (device.FileFormat != newFileFormat)
                        device.FileFormat = newFileFormat;
                }
                catch
                {
                }

                // start the asynchronous image acquisition process
                device.Acquire();
            }
            catch (Exception ex)
            {
                // close the device
                _currentDevice.Close();
                MessageBox.Show(ex.Message);
                SetWindowUiState(true);
                return;
            }
        }

        /// <summary>
        /// Subscribes to the device events.
        /// </summary>
        private void SubscribeToDeviceEvents()
        {
            _currentDevice.ImageAcquiring += new EventHandler<ImageAcquiringEventArgs>(device_ImageAcquiring);
            _currentDevice.ImageAcquired += new EventHandler<ImageAcquiredEventArgs>(device_ImageAcquired);
            _currentDevice.ScanCompleted += new EventHandler(device_ScanCompleted);
            _currentDevice.ScanCanceled += new EventHandler(device_ScanCanceled);
            _currentDevice.UserInterfaceClosed += new EventHandler(device_UserInterfaceClosed);
            _currentDevice.ScanFailed += new EventHandler<ScanFailedEventArgs>(device_ScanFailed);
            _currentDevice.ScanFinished += new EventHandler(_currentDevice_ScanFinished);
        }

        /// <summary>
        /// Unsubscribes from the device events.
        /// </summary>
        private void UnsubscribeFromDeviceEvents()
        {
            _currentDevice.ImageAcquiring -= new EventHandler<ImageAcquiringEventArgs>(device_ImageAcquiring);
            _currentDevice.ImageAcquired -= new EventHandler<ImageAcquiredEventArgs>(device_ImageAcquired);
            _currentDevice.ScanCompleted -= new EventHandler(device_ScanCompleted);
            _currentDevice.ScanCanceled -= new EventHandler(device_ScanCanceled);
            _currentDevice.UserInterfaceClosed -= new EventHandler(device_UserInterfaceClosed);
            _currentDevice.ScanFailed -= new EventHandler<ScanFailedEventArgs>(device_ScanFailed);
            _currentDevice.ScanFinished -= new EventHandler(_currentDevice_ScanFinished);
        }

        /// <summary>
        /// Image is acquiring.
        /// </summary>
        void device_ImageAcquiring(object sender, ImageAcquiringEventArgs e)
        {
            Device device = (Device)sender;
            string fileExtension = "bmp";
            switch (e.FileFormat)
            {
                case TwainImageFileFormat.Tiff:
                    fileExtension = "tif";
                    break;

                case TwainImageFileFormat.Jpeg:
                    fileExtension = "jpg";
                    break;
            }

            e.Filename = Path.Combine(directoryForImagesTextBox.Text, string.Format("page{0}.{1}", _imageIndex, fileExtension));
        }

        /// <summary>
        /// Image is acquired.
        /// </summary>
        void device_ImageAcquired(object sender, ImageAcquiredEventArgs e)
        {
            statusTextBox.Text += string.Format("Image is saved to file '{0}'{1}", Path.GetFileName(e.Filename), Environment.NewLine);
            _imageIndex++;

        }

        /// <summary>
        /// Scan is completed.
        /// </summary>
        void device_ScanCompleted(object sender, EventArgs e)
        {
            statusTextBox.Text += string.Format("Scan completed{0}", Environment.NewLine);
        }

        /// <summary>
        /// Scan is canceled.
        /// </summary>
        void device_ScanCanceled(object sender, EventArgs e)
        {
            statusTextBox.Text += string.Format("Scan is canceled{0}", Environment.NewLine);
        }

        /// <summary>
        /// User interface of device is closed.
        /// </summary>
        void device_UserInterfaceClosed(object sender, EventArgs e)
        {
            statusTextBox.Text += string.Format("User Interface is closed{0}", Environment.NewLine);
        }

        /// <summary>
        /// Scan is failed.
        /// </summary>
        void device_ScanFailed(object sender, ScanFailedEventArgs e)
        {
            statusTextBox.Text += string.Format("Scan is failed: {0}{1}", e.ErrorString, Environment.NewLine);
        }

        /// <summary>
        /// Scan is finished.
        /// </summary>
        void _currentDevice_ScanFinished(object sender, EventArgs e)
        {
            // close the device
            _currentDevice.Close();

            statusTextBox.Text += string.Format("Scan is finished{0}", Environment.NewLine);

            SetWindowUiState(true);
        }

        private void Window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            if (_currentDevice != null)
            {
                UnsubscribeFromDeviceEvents();
                _currentDevice = null;
            }

            // close the device manager
            _deviceManager.Close();
            // dispose the device manager
            _deviceManager.Dispose();
            _deviceManager = null;
        }

        #endregion

    }
}
