using System;
using System.ComponentModel;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Threading;
using Vintasoft.WpfTwain;

namespace WpfTwainCustomUIDemo
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
        /// Determines that device is initialized.
        /// </summary>
        bool _isDeviceInitialized;

        /// <summary>
        /// Current pixel type.
        /// </summary>
        PixelType _pixelType = PixelType.RGB;
        /// <summary>
        /// Current unit of measure.
        /// </summary>
        UnitOfMeasure _unitOfMeasure = UnitOfMeasure.Inches;
        /// <summary>
        /// Object that controls IAutoRotate capability.
        /// </summary>
        DeviceCapability _autoRotateCap;
        /// <summary>
        /// Object that controls IAutoBorderDetection capability.
        /// </summary>
        DeviceCapability _autoBorderDetectionCap;

        bool _isUnitOfMeasureAvailable;
        bool _isXResolutionAvailable;
        bool _isYResolutionAvailable;
        bool _isPageSizeAvailable;
        bool _isPageOrientationAvailable;
        bool _isImageLayoutAvailable;
        bool _isPixelTypeAvailable;
        bool _isBitDepthAvailable;
        bool _isThresholdAvailable;
        bool _isBrightnessAvailable;
        bool _isContrastAvailable;
        bool _isImageFilterAvailable;
        bool _isNoiseFilterAvailable;
        bool _isAutoRotateAvailable;
        bool _isAutoBorderDetectionAvailable;

        /// <summary>
        /// Acquired images count.
        /// </summary>
        int _imageCount = 1;

        /// <summary>
        /// Determines that image acquistion must be canceled because application's window is closing.
        /// </summary>
        bool _cancelTransferBecauseWindowIsClosing;

        #endregion



        #region Constructors

        public MainWindow()
        {
            InitializeComponent();

            this.Title = string.Format("VintaSoft WPF TWAIN Custom UI Demo v{0}", TwainGlobalSettings.ProductVersion);

            _deviceManager = new DeviceManager(this);
        }

        #endregion



        #region Properties

        bool _isDeviceChanging;
        public bool IsDeviceChanging
        {
            get { return _isDeviceChanging; }
            set
            {
                if (_isDeviceChanging != value)
                {
                    _isDeviceChanging = value;

                    if (value)
                        this.Cursor = Cursors.Wait;
                    else
                        this.Cursor = Cursors.Arrow;

                    UpdateUI();
                }
            }
        }

        bool _isImageAcquiring;
        public bool IsImageAcquiring
        {
            get { return _isImageAcquiring; }
            set
            {
                if (_isImageAcquiring != value)
                {
                    _isImageAcquiring = value;
                    UpdateUI();
                }
            }
        }

        #endregion



        #region Methods

        /// <summary>
        /// Window of application is loaded.
        /// </summary>
        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            // change the application status and update UI
            IsDeviceChanging = true;
            // init devices
            InitDevices();
        }


        #region Init

        /// <summary>
        /// Open TWAIN device manager.
        /// </summary>
        private bool OpenDeviceManager()
        {
            // try to find the device manager specified by user
            _deviceManager.IsTwain2Compatible = (bool)twain2CompatibleCheckBox.IsChecked;
            // if TWAIN device manager is NOT available
            if (!_deviceManager.IsTwainAvailable)
            {
                // try to use another TWAIN device manager
                _deviceManager.IsTwain2Compatible = (bool)!twain2CompatibleCheckBox.IsChecked;
                // if TWAIN device manager is NOT available
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

            return true;
        }

        /// <summary>
        /// Init devices.
        /// </summary>
        private void InitDevices()
        {
            // clear a list of devices
            devicesComboBox.Items.Clear();

            // if TWAIN device manager is opened
            if (OpenDeviceManager())
            {
                twain2CompatibleCheckBox.IsChecked = _deviceManager.IsTwain2Compatible;

                if (_currentDevice != null)
                    UnsubscribeFromDeviceEvents();

                // get a reference to the default device
                _currentDevice = _deviceManager.DefaultDevice;
                // subscribe to device events
                SubscribeToDeviceEvents();

                // init a list of devices
                DeviceCollection devices = _deviceManager.Devices;
                for (int i = 0; i < devices.Count; i++)
                {
                    devicesComboBox.Items.Add(devices[i].Info.ProductName);

                    if (devices[i] == _currentDevice)
                        devicesComboBox.SelectedIndex = i;
                }

                // init device settings
                InitDeviceSettings();
            }

            // change the application status and update UI
            IsDeviceChanging = false;
        }

        /// <summary>
        /// Init device settings.
        /// </summary>
        private void InitDeviceSettings()
        {
            _isDeviceInitialized = false;

            if (_currentDevice.State != DeviceState.Opened)
            {
                try
                {
                    // open the device
                    _currentDevice.Open();
                }
                catch (TwainDeviceException ex)
                {
                    MessageBox.Show(ex.Message);
                    return;
                }
            }


            // get info about device capabilities

            // unit of measure
            GetUnitOfMeasure();
            // init resolution settings
            GetResolution();

            // page size
            GetPageSize();
            // page orientation
            GetPageOrientation();

            // init image layout
            GetImageLayout();

            // pixel type
            GetPixelType();
            // bit depth
            GetBitDepth();
            // threshold, contrast and brightness
            GetThresholdBrightnessContrast();

            // image filter
            GetImageFilter();
            // noise filter
            GetNoiseFilter();
            // automatic rotate
            GetAutoRotate();
            // automatic border detection
            GetAutoBorderDetection();


            //
            _isDeviceInitialized = true;
        }

        /// <summary>
        /// Init combo box by array of values.
        /// </summary>
        private void InitComboBox(ComboBox comboBox, Array values, object currentValue)
        {
            comboBox.IsEnabled = false;

            comboBox.Items.Clear();

            for (int i = 0; i < values.Length; i++)
                comboBox.Items.Add(values.GetValue(i));

            comboBox.SelectedItem = currentValue;
        }

        /// <summary>
        /// Inits track bar by values of device capability represented as range.
        /// </summary>
        private void InitRangeCapValue(TwainValueContainerBase capValue, Slider valuesSlider)
        {
            if (capValue == null)
                return;

            try
            {
                // if container type of capability is a range
                if (capValue.ContainerType == TwainValueContainerType.Range)
                {
                    // convert base(abstract) object to real(non abstract) object
                    TwainRangeValueContainer capValueAsRange = (TwainRangeValueContainer)capValue;
                    // get range values as range struct (this action simplifies the convertation process of values)
                    Range<float> range = capValueAsRange.GetAsRangeOfFloatValues();

                    int min = (int)range.MinValue;
                    int max = (int)range.MaxValue;

                    // This is patch for bug in TWAIN drivers for HP ScanJet GXXXX scanners.
                    if (min > max)
                        max = UInt16.MaxValue + max;

                    // set the track bar values
                    valuesSlider.Minimum = min;
                    valuesSlider.Maximum = max;
                    valuesSlider.SmallChange = (int)range.StepSize;
                    valuesSlider.TickFrequency = valuesSlider.SmallChange;
                    valuesSlider.Value = (int)range.Value;
                }
                else
                {
                    ShowErrorMessage("Container type of capability is not a range.", "Device capability");
                }
            }
            catch (TwainDeviceCapabilityException)
            {
            }
        }

        #endregion


        #region UI

        /// <summary>
        /// Updates UI.
        /// </summary>
        private void UpdateUI()
        {
            bool hasDevices = false;
            if (_deviceManager.State == DeviceManagerState.Opened)
            {
                if (_deviceManager.Devices.Count > 0)
                    hasDevices = true;
            }
            bool isDeviceChanging = this.IsDeviceChanging;
            bool isImageAcquiring = this.IsImageAcquiring;

            twain2CompatibleCheckBox.IsEnabled = !isImageAcquiring;

            transferModeGroupBox.IsEnabled = !isDeviceChanging && hasDevices && !isImageAcquiring;
            devicesComboBox.IsEnabled = !isDeviceChanging && hasDevices && !isImageAcquiring;
            pageGroupBox.IsEnabled = !isDeviceChanging && hasDevices && !isImageAcquiring;
            resolutionGroupBox.IsEnabled = !isDeviceChanging && hasDevices && !isImageAcquiring;
            imageLayoutGroupBox.IsEnabled = !isDeviceChanging && hasDevices && !isImageAcquiring;
            imagesToAcquireGroupBox.IsEnabled = !isDeviceChanging && hasDevices && !isImageAcquiring;
            imageGroupBox.IsEnabled = !isDeviceChanging && hasDevices && !isImageAcquiring;
            imageProcessingGroupBox.IsEnabled = !isDeviceChanging && hasDevices && !isImageAcquiring;

            acquireImagesButton.IsEnabled = hasDevices && !isDeviceChanging;
            if (!isDeviceChanging)
            {
                if (isImageAcquiring)
                    acquireImagesButton.Content = "Cancel";
                else
                    acquireImagesButton.Content = "Acquire image(s)";
            }


            // unit of measure
            unitOfMeasureComboBox.IsEnabled = _isUnitOfMeasureAvailable;

            // resolution
            xResComboBox.IsEnabled = _isXResolutionAvailable;
            xResSlider.IsEnabled = _isXResolutionAvailable;
            yResComboBox.IsEnabled = _isYResolutionAvailable;
            yResSlider.IsEnabled = _isYResolutionAvailable;

            // page size
            pageSizeComboBox.IsEnabled = _isPageSizeAvailable;
            pageSizeLabel.IsEnabled = _isPageSizeAvailable;

            // page orientation
            pageOrientationComboBox.IsEnabled = _isPageOrientationAvailable;
            pageOrientationLabel.IsEnabled = _isPageOrientationAvailable;

            // image layout
            leftTextBox.IsEnabled = _isImageLayoutAvailable;
            topTextBox.IsEnabled = _isImageLayoutAvailable;
            rightTextBox.IsEnabled = _isImageLayoutAvailable;
            bottomTextBox.IsEnabled = _isImageLayoutAvailable;

            // pixel type
            pixelTypeComboBox.IsEnabled = _isPixelTypeAvailable;
            pixelTypeLabel.IsEnabled = _isPixelTypeAvailable;

            // bit depth
            bitDepthComboBox.IsEnabled = _isBitDepthAvailable;
            bitDepthLabel.IsEnabled = _isBitDepthAvailable;

            // threshold
            thresholdLabel.IsEnabled = _isThresholdAvailable;
            thresholdComboBox.IsEnabled = _isThresholdAvailable;
            thresholdSlider.IsEnabled = _isThresholdAvailable;

            // brightness
            brightnessLabel.IsEnabled = _isBrightnessAvailable;
            brightnessComboBox.IsEnabled = _isBrightnessAvailable;
            brightnessSlider.IsEnabled = _isBrightnessAvailable;

            // contrast
            contrastLabel.IsEnabled = _isContrastAvailable;
            contrastComboBox.IsEnabled = _isContrastAvailable;
            contrastSlider.IsEnabled = _isContrastAvailable;

            // image filter
            imageFilterComboBox.IsEnabled = _isImageFilterAvailable;

            // noise filter
            noiseFilterComboBox.IsEnabled = _isNoiseFilterAvailable;

            // auto rotate
            autoRotateCheckBox.IsEnabled = _isAutoRotateAvailable;

            // auto detect border
            autoBorderDetectionCheckBox.IsEnabled = _isAutoBorderDetectionAvailable;
        }

        /// <summary>
        /// Enables/disables TWAIN 2.0 compatibility.
        /// </summary>
        private void twain2CompatibleCheckBox_CheckedChanged(object sender, RoutedEventArgs e)
        {
            if (_deviceManager == null)
                return;

            // if TWAIN 2.0 compatibility is not changed
            if (_deviceManager.IsTwainAvailable &&
                _deviceManager.IsTwain2Compatible == twain2CompatibleCheckBox.IsChecked)
                return;

            // change the application status and update UI
            IsDeviceChanging = true;

            // close device and device manager
            CloseDeviceAndDeviceManager();

            // change TWAIN 2.0 compatibility
            _deviceManager.IsTwain2Compatible = (bool)twain2CompatibleCheckBox.IsChecked;

            // init devices
            InitDevices();
        }

        /// <summary>
        /// Current device is changed.
        /// </summary>
        private void devicesComboBox_SelectedIndexChanged(object sender, SelectionChangedEventArgs e)
        {
            if (_deviceManager.State != DeviceManagerState.Opened)
                return;

            // if current device is not changed
            if (_currentDevice.Info.ProductName == (string)devicesComboBox.SelectedItem)
                return;

            // change the application status and update UI
            IsDeviceChanging = true;

            // close device if necessary
            if (_currentDevice.State == DeviceState.Opened)
                _currentDevice.Close();

            if (_currentDevice != null)
                UnsubscribeFromDeviceEvents();

            // get a reference to current device
            _currentDevice = _deviceManager.Devices.Find((string)devicesComboBox.SelectedItem);
            SubscribeToDeviceEvents();

            try
            {
                // init device settings
                InitDeviceSettings();

                // change the application status and update UI
                IsDeviceChanging = false;
            }
            catch (TwainDeviceException ex)
            {
                ShowErrorMessage(ex.Message, "Device error");
            }
            catch (TwainInvalidStateException ex)
            {
                ShowErrorMessage(ex.Message, "Device invalid state");
            }
        }

        /// <summary>
        /// Acquire image button is clicked.
        /// </summary>
        private void acquireImagesButton_Click(object sender, RoutedEventArgs e)
        {
            // acquiring, need to cancel
            if (IsImageAcquiring)
            {
                _currentDevice.CancelTransfer();
                return;
            }

            // acquire image(s)
            AcquireImage(nativeTransferRadioButton.IsChecked == true);
        }

        private void nativeTransferRadioButton_Checked(object sender, RoutedEventArgs e)
        {
            if (imageAcquisitionProgressBar != null)
                imageAcquisitionProgressBar.Visibility = Visibility.Hidden;
        }

        private void memoryTransferRadioButton_Checked(object sender, RoutedEventArgs e)
        {
            if (imageAcquisitionProgressBar != null)
                imageAcquisitionProgressBar.Visibility = Visibility.Visible;
        }

        /// <summary>
        /// Pixel type is changed.
        /// </summary>
        private void pixelTypeComboBox_SelectedIndexChanged(object sender, SelectionChangedEventArgs e)
        {
            if (!_isDeviceInitialized)
                return;

            this.Cursor = Cursors.Wait;

            // if device is closed
            if (_currentDevice.State == DeviceState.Closed)
                // open the device
                _currentDevice.Open();

            _pixelType = (PixelType)pixelTypeComboBox.SelectedItem;
            _currentDevice.PixelType = _pixelType;

            GetBitDepth();
            GetThresholdBrightnessContrast();

            this.Cursor = Cursors.Arrow;

            UpdateUI();
        }

        /// <summary>
        /// Unit of measure is changed.
        /// </summary>
        private void unitOfMeasureComboBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (!_isDeviceInitialized)
                return;

            this.Cursor = Cursors.Wait;

            // if device is closed
            if (_currentDevice.State == DeviceState.Closed)
                // open the device
                _currentDevice.Open();

            _unitOfMeasure = (UnitOfMeasure)unitOfMeasureComboBox.SelectedItem;
            _currentDevice.UnitOfMeasure = _unitOfMeasure;
            GetResolution();
            ResetImageLayout();

            this.Cursor = Cursors.Arrow;

            UpdateUI();
        }

        /// <summary>
        /// Reset the image layout.
        /// </summary>
        private void resetImageLayoutButton_Click(object sender, RoutedEventArgs e)
        {
            ResetImageLayout();
        }

        /// <summary>
        /// Reset the image layout.
        /// </summary>
        private void ResetImageLayout()
        {
            if (_currentDevice == null)
                return;

            this.Cursor = Cursors.Wait;

            // if device is closed
            if (_currentDevice.State == DeviceState.Closed)
                // open the device
                _currentDevice.Open();

            try
            {
                _currentDevice.ImageLayout.Reset();
                GetImageLayout();
            }
            catch (TwainException ex)
            {
                ShowErrorMessage(ex.Message, "Error");
            }

            this.Cursor = Cursors.Arrow;
        }

        /// <summary>
        /// Clears acquired images.
        /// </summary>
        private void clearImagesButton_Click(object sender, RoutedEventArgs e)
        {
            acquiredImagesTabControl.Items.Clear();

            GC.Collect();
        }

        /// <summary>
        /// Window of application is closing.
        /// </summary>
        private void Window_Closing(object sender, CancelEventArgs e)
        {
            if (_currentDevice != null)
            {
                // if image is acquiring
                if (_currentDevice.State > DeviceState.Enabled)
                {
                    // cancel image acquisition
                    _currentDevice.CancelTransfer();
                    // specify that window must be closed when image acquisition is canceled
                    _cancelTransferBecauseWindowIsClosing = true;
                    // cancel form closing
                    e.Cancel = true;
                    return;
                }
            }

            // close the device and device manager
            CloseDeviceAndDeviceManager();
            // dispose the device manager
            _deviceManager.Dispose();
        }

        /// <summary>
        /// Update tooltip of slider.
        /// </summary>
        private void slider_ToolTipOpening(object sender, ToolTipEventArgs e)
        {
            Slider slider1 = (Slider)sender;
            ToolTip ttprogbar = new ToolTip();
            ttprogbar.Content = slider1.Value.ToString();
            slider1.ToolTip = ttprogbar;
        }

        private void textBoxShortFilter_PreviewTextInput(object sender, TextCompositionEventArgs e)
        {
            if (e.Source is TextBox)
            {
                TextBox textControl = (TextBox)e.Source;
                short tmp;
                string newText = textControl.Text + e.Text;
                if (!short.TryParse(newText, out tmp))
                    e.Handled = true;
            }
        }

        private void textBoxVoidTextFilter_LostFocus(object sender, RoutedEventArgs e)
        {
            if (e.Source is TextBox)
            {
                TextBox control = (TextBox)e.Source;
                if (control.Text.Trim() == "")
                {
                    control.Text = "0";
                }
            }
        }

        private void ShowErrorMessage(string message, string title)
        {
            MessageBox.Show(message, title, MessageBoxButton.OK, MessageBoxImage.Error);
        }

        #endregion


        #region Acquire image(s)

        /// <summary>
        /// Acquire image(s).
        /// </summary>
        private void AcquireImage(bool nativeTransferMode)
        {
            if (_currentDevice == null)
                return;

            // change the application status and update UI
            IsImageAcquiring = true;

            // disable User Interface of device
            _currentDevice.ShowUI = false;
            _currentDevice.ShowIndicators = false;
            _currentDevice.DisableAfterAcquire = true;


            // if device is closed
            if (_currentDevice.State == DeviceState.Closed)
                // open the device
                _currentDevice.Open();


            // set device capabilities

            // number of pages to acquire
            SetXferCount();

            // pixel type
            SetPixelType();
            // bit depth
            SetBitDepth();
            // threshold, brightness and contrast
            if (_pixelType == PixelType.BW)
            {
                SetThreshold();
            }
            else
            {
                SetBrightness();
                SetContrast();
            }

            // unit of measure
            SetUnitOfMeasure();
            // resolution
            SetResolution();

            // page size
            SetPageSize();
            // page orientation
            SetPageOrientation();

            // image layout
            SetImageLayout();

            // image filter
            SetImageFilter();
            // noise filter
            SetNoiseFilter();
            // auto rotate
            SetAutoRotate();
            // auto border detection
            SetAutoBorderDetection();

            // set the transfer mode
            TransferMode newTransferMode = TransferMode.Memory;
            if (nativeTransferMode)
                _currentDevice.TransferMode = TransferMode.Native;
            if (_currentDevice.TransferMode != newTransferMode)
                _currentDevice.TransferMode = newTransferMode;

            try
            {
                // acquire image(s)
                _currentDevice.Acquire();
            }
            catch (Exception ex)
            {
                MessageBox.Show(string.Format("Error: {0}", ex.Message));
                // change the application status and update UI
                IsImageAcquiring = false;
            }
        }

        /// <summary>
        /// Subscribe to device events.
        /// </summary>
        void SubscribeToDeviceEvents()
        {
            _currentDevice.ImageAcquiringProgress += new EventHandler<ImageAcquiringProgressEventArgs>(_device_ImageAcquiringProgress);
            _currentDevice.ImageAcquired += new EventHandler<ImageAcquiredEventArgs>(_device_ImageAcquired);
            _currentDevice.ScanFailed += new EventHandler<ScanFailedEventArgs>(_device_ScanFailed);
            _currentDevice.ScanFinished += new EventHandler(_currentDevice_ScanFinished);
        }

        /// <summary>
        /// Unsubscribe from device events.
        /// </summary>
        void UnsubscribeFromDeviceEvents()
        {
            _currentDevice.ImageAcquiringProgress -= new EventHandler<ImageAcquiringProgressEventArgs>(_device_ImageAcquiringProgress);
            _currentDevice.ImageAcquired -= new EventHandler<ImageAcquiredEventArgs>(_device_ImageAcquired);
            _currentDevice.ScanFailed -= new EventHandler<ScanFailedEventArgs>(_device_ScanFailed);
            _currentDevice.ScanFinished -= new EventHandler(_currentDevice_ScanFinished);
        }

        /// <summary>
        /// Image acquiring progress is changed.
        /// </summary>
        void _device_ImageAcquiringProgress(object sender, ImageAcquiringProgressEventArgs e)
        {
            // image acquistion must be canceled because application's window is closing
            if (_cancelTransferBecauseWindowIsClosing)
            {
                // cancel image acquisition
                _currentDevice.CancelTransfer();
                return;
            }

            imageAcquisitionProgressBar.Value = e.Progress;
        }

        /// <summary>
        /// Image is acquired.
        /// </summary>
        void _device_ImageAcquired(object sender, ImageAcquiredEventArgs e)
        {
            // image acquistion must be canceled because application's window is closing
            if (_cancelTransferBecauseWindowIsClosing)
            {
                // cancel image acquisition
                _currentDevice.CancelTransfer();
                return;
            }

            // create panel for picture box with acquired image
            TabItem tabPage1 = new TabItem();
            tabPage1.Width = double.NaN;
            tabPage1.Height = double.NaN;
            tabPage1.VerticalAlignment = VerticalAlignment.Stretch;
            tabPage1.HorizontalAlignment = HorizontalAlignment.Stretch;
            tabPage1.Header = string.Format("Image {0} [{1}x{2}, {3}, {4}]", _imageCount++,
                                            e.Image.ImageInfo.Width,
                                            e.Image.ImageInfo.Height,
                                            e.Image.ImageInfo.PixelType,
                                            e.Image.ImageInfo.Resolution);

            // create an image control for acquired image
            Image image1 = new Image();
            // set a bitmap source in the image control
            image1.Source = e.Image.GetAsBitmapSource();
            // set the image control size mode
            image1.Stretch = Stretch.Fill;

            // add an image control to a panel
            tabPage1.Content = image1;
            // add a panel to a tab control with images
            acquiredImagesTabControl.Items.Add(tabPage1);
            // select new panel
            acquiredImagesTabControl.SelectedItem = tabPage1;

            // dispose an acquired image
            e.Image.Dispose();
        }

        /// <summary>
        /// Scan is failed.
        /// </summary>
        void _device_ScanFailed(object sender, ScanFailedEventArgs e)
        {
            ShowErrorMessage(e.ErrorString, "Scan is failed");
        }

        /// <summary>
        /// Scan is finished.
        /// </summary>
        void _currentDevice_ScanFinished(object sender, EventArgs e)
        {
            // close the device
            _currentDevice.Close();

            // change the application status and update UI
            IsImageAcquiring = false;

            //
            imageAcquisitionProgressBar.Value = 0;
        }

        #endregion


        #region Device capabilities

        #region Get

        /// <summary>
        /// Get information about the current and supported units of measure of device.
        /// </summary>
        private void GetUnitOfMeasure()
        {
            _isUnitOfMeasureAvailable = false;
            try
            {
                _unitOfMeasure = _currentDevice.UnitOfMeasure;
                InitComboBox(unitOfMeasureComboBox, _currentDevice.GetSupportedUnitsOfMeasure(), _unitOfMeasure);

                _isUnitOfMeasureAvailable = true;
            }
            catch (TwainDeviceCapabilityException)
            {
            }
        }

        /// <summary>
        /// Get information about the current and supported resolutions of device.
        /// </summary>
        private void GetResolution()
        {
            // Horizontal resolution
            xResComboBox.Visibility = Visibility.Hidden;
            xResSlider.Visibility = Visibility.Hidden;
            _isXResolutionAvailable = false;

            // get supported values of horizontal resolution
            TwainValueContainerBase xResCapValue;
            try
            {
                xResCapValue = _currentDevice.GetSupportedHorizontalResolutions();
            }
            catch (TwainDeviceCapabilityException)
            {
                return;
            }
            if (xResCapValue == null)
            {
                return;
            }

            // if values are represented as range
            if (xResCapValue.ContainerType == TwainValueContainerType.Range)
            {
                InitRangeCapValue(xResCapValue, xResSlider);

                xResSlider.Visibility = Visibility.Visible;
            }
            // if values are represented as array or enumeration
            else
            {
                InitComboBox(xResComboBox, xResCapValue.GetAsFloatArray(), _currentDevice.Resolution.Horizontal);

                xResComboBox.Visibility = Visibility.Visible;
            }

            _isXResolutionAvailable = true;


            // Vertical resolution
            yResComboBox.Visibility = Visibility.Hidden;
            yResSlider.Visibility = Visibility.Hidden;
            _isYResolutionAvailable = false;

            // get supported values of horizontal resolution
            TwainValueContainerBase yResCapValue;
            try
            {
                yResCapValue = _currentDevice.GetSupportedVerticalResolutions();
            }
            catch (TwainDeviceCapabilityException)
            {
                return;
            }
            if (yResCapValue == null)
            {
                return;
            }

            // if values are represented as range
            if (yResCapValue.ContainerType == TwainValueContainerType.Range)
            {
                InitRangeCapValue(yResCapValue, yResSlider);

                yResSlider.Visibility = Visibility.Visible;
            }
            // if values are represented as array or enumeration
            else
            {
                InitComboBox(yResComboBox, yResCapValue.GetAsFloatArray(), _currentDevice.Resolution.Vertical);

                yResComboBox.Visibility = Visibility.Visible;
            }

            _isYResolutionAvailable = true;
        }

        /// <summary>
        /// Get information about the current and supported page sizes of device.
        /// </summary>
        private void GetPageSize()
        {
            _isPageSizeAvailable = false;
            try
            {
                InitComboBox(pageSizeComboBox, _currentDevice.GetSupportedPageSizes(), _currentDevice.PageSize);

                _isPageSizeAvailable = true;
            }
            catch (TwainDeviceCapabilityException)
            {
            }
        }

        /// <summary>
        /// Get information about the page orientation of device.
        /// </summary>
        private void GetPageOrientation()
        {
            _isPageOrientationAvailable = false;
            try
            {
                PageOrientation[] supportedPageOrientations = _currentDevice.GetSupportedPageOrientations();
                if (supportedPageOrientations != null && supportedPageOrientations.Length > 0)
                {
                    InitComboBox(pageOrientationComboBox, supportedPageOrientations, _currentDevice.PageOrientation);

                    _isPageOrientationAvailable = true;
                }
            }
            catch (TwainDeviceCapabilityException)
            {
            }
        }

        /// <summary>
        /// Get information about the current and supported thresholds OR brightnesses and contrasts of device.
        /// </summary>
        private void GetImageLayout()
        {
            _isImageLayoutAvailable = false;

            // Image layout
            leftTextBox.Text = "";
            topTextBox.Text = "";
            rightTextBox.Text = "";
            bottomTextBox.Text = "";
            try
            {
                RectangleF imageLayoutRect = _currentDevice.ImageLayout.Get();

                _isImageLayoutAvailable = true;

                leftTextBox.Text = imageLayoutRect.Left.ToString();
                topTextBox.Text = imageLayoutRect.Top.ToString();
                rightTextBox.Text = imageLayoutRect.Right.ToString();
                bottomTextBox.Text = imageLayoutRect.Bottom.ToString();
            }
            catch (FormatException)
            {
            }
            catch (TwainDeviceException)
            {
            }
            catch (TwainDeviceCapabilityException)
            {
            }
        }

        /// <summary>
        /// Get information about the current and supported pixel types of device.
        /// </summary>
        private void GetPixelType()
        {
            _isPixelTypeAvailable = false;
            try
            {
                _pixelType = _currentDevice.PixelType;
                InitComboBox(pixelTypeComboBox, _currentDevice.GetSupportedPixelTypes(), _pixelType);

                _isPixelTypeAvailable = true;
            }
            catch (TwainDeviceCapabilityException)
            {
            }
        }

        /// <summary>
        /// Get information about the current and supported bit depths of device.
        /// </summary>
        private void GetBitDepth()
        {
            _isBitDepthAvailable = false;
            try
            {
                InitComboBox(bitDepthComboBox, _currentDevice.GetSupportedBitDepths(), _currentDevice.BitDepth);

                _isBitDepthAvailable = true;
            }
            catch (TwainDeviceCapabilityException)
            {
            }
        }

        /// <summary>
        /// Get information about the current and supported thresholds OR brightnesses and contrasts of device.
        /// </summary>
        private void GetThresholdBrightnessContrast()
        {
            thresholdComboBox.Visibility = Visibility.Hidden;
            thresholdSlider.Visibility = Visibility.Hidden;
            brightnessComboBox.Visibility = Visibility.Hidden;
            brightnessSlider.Visibility = Visibility.Hidden;
            contrastComboBox.Visibility = Visibility.Hidden;
            contrastSlider.Visibility = Visibility.Hidden;

            TwainValueContainerBase capValue;
            if (_pixelType == PixelType.BW)
            {
                // init threshold values
                _isThresholdAvailable = false;
                try
                {
                    capValue = _currentDevice.GetSupportedThresholdValues();

                    _isThresholdAvailable = true;
                }
                catch (TwainDeviceCapabilityException)
                {
                    return;
                }
                if (capValue == null)
                {
                    return;
                }

                if (capValue.ContainerType == TwainValueContainerType.Range)
                {
                    InitRangeCapValue(capValue, thresholdSlider);

                    thresholdSlider.Visibility = Visibility.Visible;
                }
                else if (capValue.ContainerType == TwainValueContainerType.Enum)
                {
                    TwainEnumValueContainer capValueAsEnum = (TwainEnumValueContainer)capValue;
                    InitComboBox(thresholdComboBox, capValueAsEnum.GetAsFloatArray(), capValueAsEnum.GetAsFloat());

                    thresholdComboBox.Visibility = Visibility.Visible;
                }
            }
            else
            {
                // init brightness values
                _isBrightnessAvailable = false;
                try
                {
                    capValue = _currentDevice.GetSupportedBrightnessValues();

                    _isBrightnessAvailable = true;
                }
                catch (TwainDeviceCapabilityException)
                {
                    return;
                }
                if (capValue == null)
                {
                    return;
                }

                if (capValue.ContainerType == TwainValueContainerType.Range)
                {
                    InitRangeCapValue(capValue, brightnessSlider);

                    brightnessSlider.Visibility = Visibility.Visible;
                }
                else if (capValue.ContainerType == TwainValueContainerType.Enum)
                {
                    TwainEnumValueContainer capValueAsEnum = (TwainEnumValueContainer)capValue;
                    InitComboBox(brightnessComboBox, capValueAsEnum.GetAsFloatArray(), capValueAsEnum.GetAsFloat());

                    brightnessComboBox.Visibility = Visibility.Visible;
                }

                // init contrast values
                _isContrastAvailable = false;
                try
                {
                    capValue = _currentDevice.GetSupportedContrastValues();

                    _isContrastAvailable = true;
                }
                catch (TwainDeviceCapabilityException)
                {
                    return;
                }
                if (capValue == null)
                {
                    return;
                }

                if (capValue.ContainerType == TwainValueContainerType.Range)
                {
                    InitRangeCapValue(capValue, contrastSlider);

                    contrastSlider.Visibility = Visibility.Visible;
                }
                else if (capValue.ContainerType == TwainValueContainerType.Enum)
                {
                    TwainEnumValueContainer capValueAsEnum = (TwainEnumValueContainer)capValue;
                    InitComboBox(contrastComboBox, capValueAsEnum.GetAsFloatArray(), capValueAsEnum.GetAsFloat());

                    contrastComboBox.Visibility = Visibility.Visible;
                }
            }
        }

        /// <summary>
        /// Get information about the current and supported image filters of device.
        /// </summary>
        private void GetImageFilter()
        {
            _isImageFilterAvailable = false;
            try
            {
                ImageFilter currentImageFilter = _currentDevice.ImageFilter;

                ImageFilter[] supportedImageFilters = _currentDevice.GetSupportedImageFilters();
                InitComboBox(imageFilterComboBox, supportedImageFilters, currentImageFilter);

                _isImageFilterAvailable = true;
            }
            catch (TwainDeviceCapabilityException)
            {
            }
        }

        /// <summary>
        /// Get information about the current and supported noise filters of device.
        /// </summary>
        private void GetNoiseFilter()
        {
            _isNoiseFilterAvailable = false;
            try
            {
                InitComboBox(noiseFilterComboBox, _currentDevice.GetSupportedNoiseFilters(), _currentDevice.NoiseFilter);

                _isNoiseFilterAvailable = true;
            }
            catch (TwainDeviceCapabilityException)
            {
            }
        }

        /// <summary>
        /// Get information about the auto rotate capability of device.
        /// </summary>
        private void GetAutoRotate()
        {
            _isAutoRotateAvailable = false;
            
            _autoRotateCap = _currentDevice.Capabilities.Find(DeviceCapabilityId.IAutomaticRotate);
            if (_autoRotateCap == null)
            {
                return;
            }

            try
            {
                TwainValueContainerBase autoRotateCapValue = _autoRotateCap.GetValue();
                if (autoRotateCapValue != null)
                    autoRotateCheckBox.IsChecked = autoRotateCapValue.GetAsBool();

                _isAutoRotateAvailable = true;
            }
            catch (TwainDeviceCapabilityException)
            {
            }
        }

        /// <summary>
        /// Get information about the auto border detection capability of device.
        /// </summary>
        private void GetAutoBorderDetection()
        {
            _isAutoBorderDetectionAvailable = false;

            _autoBorderDetectionCap = _currentDevice.Capabilities.Find(DeviceCapabilityId.IAutomaticBorderDetection);
            if (_autoBorderDetectionCap == null)
            {
                return;
            }

            try
            {
                TwainValueContainerBase autoBorderDetectionCapValue = _autoBorderDetectionCap.GetValue();
                if (autoBorderDetectionCapValue != null)
                    autoBorderDetectionCheckBox.IsChecked = autoBorderDetectionCapValue.GetAsBool();

                _isAutoBorderDetectionAvailable = true;
            }
            catch (TwainDeviceCapabilityException)
            {
            }
        }

        #endregion


        #region Set

        /// <summary>
        /// Specify how many images application wants to receive from the device.
        /// </summary>
        private void SetXferCount()
        {
            try
            {
                short newXferCount = (short)pagesToAcquireNumericUpDown.Value;
                if (_currentDevice.XferCount != newXferCount)
                    _currentDevice.XferCount = newXferCount;
            }
            catch (TwainDeviceCapabilityException)
            {
            }
        }

        /// <summary>
        /// Set unit of measure of device.
        /// </summary>
        private void SetUnitOfMeasure()
        {
            if (_isUnitOfMeasureAvailable)
            {
                try
                {
                    if (_currentDevice.UnitOfMeasure != _unitOfMeasure)
                        _currentDevice.UnitOfMeasure = _unitOfMeasure;
                }
                catch (TwainDeviceCapabilityException)
                {
                }
            }
        }

        /// <summary>
        /// Set resolution of device.
        /// </summary>
        private void SetResolution()
        {
            if (xResComboBox.IsEnabled && yResComboBox.IsEnabled)
            {
                try
                {
                    float newXRes = (float)xResComboBox.SelectedItem;
                    float newYRes = (float)yResComboBox.SelectedItem;
                    if (_currentDevice.UnitOfMeasure != _unitOfMeasure ||
                        _currentDevice.Resolution.Horizontal != newXRes ||
                        _currentDevice.Resolution.Vertical != newYRes)
                        _currentDevice.Resolution = new Resolution(newXRes, newYRes, _unitOfMeasure);
                }
                catch (TwainDeviceCapabilityException)
                {
                }
            }
            if (xResSlider.IsEnabled && yResSlider.IsEnabled)
            {
                try
                {
                    float newXRes = (float)xResSlider.Value;
                    float newYRes = (float)yResSlider.Value;
                    if (_currentDevice.UnitOfMeasure != _unitOfMeasure ||
                        _currentDevice.Resolution.Horizontal != newXRes ||
                        _currentDevice.Resolution.Vertical != newYRes)
                        _currentDevice.Resolution = new Resolution(newXRes, newYRes, _unitOfMeasure);
                }
                catch (TwainDeviceCapabilityException)
                {
                }
            }
        }

        /// <summary>
        /// Set page size of device.
        /// </summary>
        private void SetPageSize()
        {
            if (_isPageSizeAvailable)
            {
                try
                {
                    PageSize newPageSize = (PageSize)pageSizeComboBox.SelectedItem;
                    if (_currentDevice.PageSize != newPageSize)
                        _currentDevice.PageSize = newPageSize;
                }
                catch (TwainDeviceCapabilityException)
                {
                }
            }
        }

        /// <summary>
        /// Set page orientation of device.
        /// </summary>
        private void SetPageOrientation()
        {
            if (_isPageOrientationAvailable)
            {
                try
                {
                    PageOrientation newPageOrientation = (PageOrientation)pageOrientationComboBox.SelectedItem;
                    if (_currentDevice.PageOrientation != newPageOrientation)
                        _currentDevice.PageOrientation = newPageOrientation;
                }
                catch (TwainDeviceCapabilityException)
                {
                }
            }
        }

        /// <summary>
        /// Set image layout of device.
        /// </summary>
        private void SetImageLayout()
        {
            if (_isImageLayoutAvailable)
            {
                try
                {
                    RectangleF newImageLayout = new RectangleF(float.Parse(leftTextBox.Text),
                                                           float.Parse(topTextBox.Text),
                                                           float.Parse(rightTextBox.Text),
                                                           float.Parse(bottomTextBox.Text));
                    RectangleF currentImageLayout = _currentDevice.ImageLayout.Get();
                    if (Math.Abs(newImageLayout.Left - currentImageLayout.Left) > 0.0001f ||
                        Math.Abs(newImageLayout.Top - currentImageLayout.Top) > 0.0001f ||
                        Math.Abs(newImageLayout.Width - currentImageLayout.Width) > 0.0001f ||
                        Math.Abs(newImageLayout.Height - currentImageLayout.Height) > 0.0001f)
                        _currentDevice.ImageLayout.Set(newImageLayout);
                }
                catch (FormatException)
                {
                }
                catch (TwainDeviceException)
                {
                }
                catch (TwainDeviceCapabilityException)
                {
                }
            }
        }

        /// <summary>
        /// Set pixel type of device.
        /// </summary>
        private void SetPixelType()
        {
            try
            {
                if (_currentDevice.PixelType != _pixelType)
                    _currentDevice.PixelType = _pixelType;
            }
            catch (TwainDeviceCapabilityException)
            {
            }
        }

        /// <summary>
        /// Set bit depth of device.
        /// </summary>
        private void SetBitDepth()
        {
            if (_isBitDepthAvailable)
            {
                try
                {
                    int newBitDepth = (int)bitDepthComboBox.SelectedItem;
                    if (_currentDevice.BitDepth != newBitDepth)
                        _currentDevice.BitDepth = newBitDepth;
                }
                catch (TwainDeviceCapabilityException)
                {
                }
            }
        }

        /// <summary>
        /// Set threshold of device.
        /// </summary>
        private void SetThreshold()
        {
            if (_isThresholdAvailable)
            {
                try
                {
                    float newThreshold = (float)thresholdSlider.Value;
                    if (_currentDevice.Threshold != newThreshold)
                        _currentDevice.Threshold = newThreshold;
                }
                catch (TwainDeviceCapabilityException)
                {
                }
            }
        }

        /// <summary>
        /// Set brightness of device.
        /// </summary>
        private void SetBrightness()
        {
            if (_isBrightnessAvailable)
            {
                try
                {
                    float newBrightness = (float)brightnessSlider.Value;
                    if (_currentDevice.Brightness != newBrightness)
                        _currentDevice.Brightness = newBrightness;
                }
                catch (TwainDeviceCapabilityException)
                {
                }
            }
        }

        /// <summary>
        /// Set contrast of device.
        /// </summary>
        private void SetContrast()
        {
            if (_isContrastAvailable)
            {
                try
                {
                    float newContrast = (float)contrastSlider.Value;
                    if (_currentDevice.Contrast != newContrast)
                        _currentDevice.Contrast = newContrast;
                }
                catch (TwainDeviceCapabilityException)
                {
                }
            }
        }

        /// <summary>
        /// Set image filter of device.
        /// </summary>
        private void SetImageFilter()
        {
            if (_isImageFilterAvailable && imageFilterComboBox.SelectedItem != null)
            {
                try
                {
                    ImageFilter newImageFilter = (ImageFilter)imageFilterComboBox.SelectedItem;
                    if (_currentDevice.ImageFilter != newImageFilter)
                        _currentDevice.ImageFilter = newImageFilter;
                }
                catch (TwainDeviceCapabilityException)
                {
                }
            }
        }

        /// <summary>
        /// Set noise filter of device.
        /// </summary>
        private void SetNoiseFilter()
        {
            if (_isNoiseFilterAvailable && noiseFilterComboBox.SelectedItem != null)
            {
                try
                {
                    NoiseFilter newNoiseFilter = (NoiseFilter)noiseFilterComboBox.SelectedItem;
                    if (_currentDevice.NoiseFilter != newNoiseFilter)
                        _currentDevice.NoiseFilter = newNoiseFilter;
                }
                catch (TwainDeviceCapabilityException)
                {
                }
            }
        }

        /// <summary>
        /// Set auto rotate capability of device.
        /// </summary>
        private void SetAutoRotate()
        {
            if (_isAutoRotateAvailable)
            {
                try
                {
                    bool newAutoRotate = (bool)autoRotateCheckBox.IsChecked;
                    TwainValueContainerBase currentValue = _autoRotateCap.GetCurrentValue();
                    if (currentValue != null && currentValue.GetAsBool() != newAutoRotate)
                        _autoRotateCap.SetValue(newAutoRotate);
                }
                catch (TwainDeviceCapabilityException)
                {
                }
            }
        }

        /// <summary>
        /// Set auto border detection capability of device.
        /// </summary>
        private void SetAutoBorderDetection()
        {
            if (_isAutoBorderDetectionAvailable)
            {
                try
                {
                    bool newAutoBorderDetection = (bool)autoBorderDetectionCheckBox.IsChecked;
                    TwainValueContainerBase currentValue = _autoBorderDetectionCap.GetCurrentValue();
                    if (currentValue != null && currentValue.GetAsBool() != newAutoBorderDetection)
                        _autoBorderDetectionCap.SetValue(newAutoBorderDetection);
                }
                catch (TwainDeviceCapabilityException)
                {
                }
            }
        }

        #endregion

        #endregion


        #region Close device

        /// <summary>
        /// Closes the device and device manager.
        /// </summary>
        private void CloseDeviceAndDeviceManager()
        {
            if (_currentDevice != null)
            {
                // close device if it is not closed
                if (_currentDevice.State != DeviceState.Closed)
                    _currentDevice.Close();
            }

            // close device manager if it is opened or loaded
            if (_deviceManager.State != DeviceManagerState.Closed)
                _deviceManager.Close();
        }

        #endregion

        #endregion

    }
}
