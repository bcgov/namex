using System;
using System.Drawing;
using System.Windows.Forms;
using Vintasoft.Twain;

namespace TwainCustomUIDemo
{
    public partial class MainForm : Form
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
        /// Determines that image acquistion must be canceled because application's form is closing.
        /// </summary>
        bool _cancelTransferBecauseFormIsClosing;

        #endregion



        #region Constructor

        public MainForm()
        {
            InitializeComponent();

            this.Text = string.Format("VintaSoft TWAIN Custom UI Demo v{0}", TwainGlobalSettings.ProductVersion);

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
                        this.Cursor = Cursors.WaitCursor;
                    else
                        this.Cursor = Cursors.Default;

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
        /// Application form is shown.
        /// </summary>
        private void MainForm_Shown(object sender, EventArgs e)
        {
            // change the application status and update UI
            IsDeviceChanging = true;
            // init devices
            InitDevices();
        }


        #region Init

        /// <summary>
        /// Opens TWAIN device manager.
        /// </summary>
        private bool OpenDeviceManager()
        {
            // try to find the device manager specified by user
            _deviceManager.IsTwain2Compatible = twain2CompatibleCheckBox.Checked;
            // if TWAIN device manager is NOT available
            if (!_deviceManager.IsTwainAvailable)
            {
                // try to use another TWAIN device manager
                _deviceManager.IsTwain2Compatible = !twain2CompatibleCheckBox.Checked;
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
        /// Inits devices.
        /// </summary>
        private void InitDevices()
        {
            // clear a list of devices
            devicesComboBox.Items.Clear();

            // if TWAIN device manager is opened
            if (OpenDeviceManager())
            {
                twain2CompatibleCheckBox.Checked = _deviceManager.IsTwain2Compatible;

                if (_currentDevice != null)
                    UnsubscribeFromDeviceEvents();

                // get a reference to the default device
                _currentDevice = _deviceManager.DefaultDevice;
                SubscribeToDeviceEvents();

                // init a list of devices
                DeviceCollection devices = _deviceManager.Devices;
                for (int i = 0; i < devices.Count; i++)
                {
                    devicesComboBox.Items.Add(devices[i].Info.ProductName);

                    if (devices[i] == _currentDevice)
                        devicesComboBox.SelectedIndex = i;
                }

                // init current device settings
                InitDeviceSettings();
            }

            // change the application status and update UI
            IsDeviceChanging = false;
        }

        /// <summary>
        /// Inits settings of device.
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
                catch (Exception ex)
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
            GetThresholdBrightnesContrast();

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
        /// Inits combo box by array of values.
        /// </summary>
        private void InitComboBox(ComboBox comboBox, Array values, object currentValue)
        {
            comboBox.Items.Clear();

            if (values == null || values.Length == 0)
                return;

            for (int i = 0; i < values.Length; i++)
                comboBox.Items.Add(values.GetValue(i));

            comboBox.SelectedItem = currentValue;
        }

        /// <summary>
        /// Inits track bar by values of device capability represented as range.
        /// </summary>
        private void InitRangeCapValue(TwainValueContainerBase capValue, TrackBar valuesTrackBar)
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
                    valuesTrackBar.Minimum = min;
                    valuesTrackBar.Maximum = max;
                    valuesTrackBar.SmallChange = (int)range.StepSize;
                    valuesTrackBar.TickFrequency = valuesTrackBar.SmallChange;
                    valuesTrackBar.Value = (int)range.Value;
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

            twain2CompatibleCheckBox.Enabled = !isImageAcquiring;

            transferModeGroupBox.Enabled = !isDeviceChanging && hasDevices && !isImageAcquiring;
            devicesComboBox.Enabled = !isDeviceChanging && hasDevices && !isImageAcquiring;
            pageGroupBox.Enabled = !isDeviceChanging && hasDevices && !isImageAcquiring;
            resolutionGroupBox.Enabled = !isDeviceChanging && hasDevices && !isImageAcquiring;
            imageLayoutGroupBox.Enabled = !isDeviceChanging && hasDevices && !isImageAcquiring;
            imagesToAcquireGroupBox.Enabled = !isDeviceChanging && hasDevices && !isImageAcquiring;
            imageGroupBox.Enabled = !isDeviceChanging && hasDevices && !isImageAcquiring;
            imageProcessingGroupBox.Enabled = !isDeviceChanging && hasDevices && !isImageAcquiring;

            acquireImageButton.Enabled = hasDevices && !isDeviceChanging;
            if (!isDeviceChanging)
            {
                if (isImageAcquiring)
                    acquireImageButton.Text = "Cancel";
                else
                    acquireImageButton.Text = "Acquire image(s)";
            }


            // unit of measure
            unitOfMeasureComboBox.Enabled = _isUnitOfMeasureAvailable;

            // resolution
            xResComboBox.Enabled = _isXResolutionAvailable;
            xResTrackBar.Enabled = _isXResolutionAvailable;
            yResComboBox.Enabled = _isYResolutionAvailable;
            yResTrackBar.Enabled = _isYResolutionAvailable;

            // page size
            pageSizeComboBox.Enabled = _isPageSizeAvailable;
            pageSizeLabel.Enabled = _isPageSizeAvailable;

            // page orientation
            pageOrientationComboBox.Enabled = _isPageOrientationAvailable;
            pageOrientationLabel.Enabled = _isPageOrientationAvailable;

            // image layout
            leftTextBox.Enabled = _isImageLayoutAvailable;
            topTextBox.Enabled = _isImageLayoutAvailable;
            rightTextBox.Enabled = _isImageLayoutAvailable;
            bottomTextBox.Enabled = _isImageLayoutAvailable;

            // pixel type
            pixelTypeComboBox.Enabled = _isPixelTypeAvailable;
            pixelTypeLabel.Enabled = _isPixelTypeAvailable;

            // bit depth
            bitDepthComboBox.Enabled = _isBitDepthAvailable;
            bitDepthLabel.Enabled = _isBitDepthAvailable;

            // threshold
            thresholdLabel.Enabled = _isThresholdAvailable;
            thresholdComboBox.Enabled = _isThresholdAvailable;
            thresholdTrackBar.Enabled = _isThresholdAvailable;

            // brightness
            brightnessLabel.Enabled = _isBrightnessAvailable;
            brightnessComboBox.Enabled = _isBrightnessAvailable;
            brightnessTrackBar.Enabled = _isBrightnessAvailable;

            // contrast
            contrastLabel.Enabled = _isContrastAvailable;
            contrastComboBox.Enabled = _isContrastAvailable;
            contrastTrackBar.Enabled = _isContrastAvailable;

            // image filter
            imageFilterComboBox.Enabled = _isImageFilterAvailable;

            // noise filter
            noiseFilterComboBox.Enabled = _isNoiseFilterAvailable;

            // auto rotate
            autoRotateCheckBox.Enabled = _isAutoRotateAvailable;

            // auto detect border
            autoBorderDetectionCheckBox.Enabled = _isAutoBorderDetectionAvailable;
        }

        /// <summary>
        /// TWAIN 2.0 compatibility is changed.
        /// </summary>
        private void twain2CompatibleCheckBox_CheckedChanged(object sender, EventArgs e)
        {
            // if TWAIN 2.0 compatibility is not changed
            if (_deviceManager.IsTwainAvailable &&
                _deviceManager.IsTwain2Compatible == twain2CompatibleCheckBox.Checked)
                return;

            // change the application status and update UI
            IsDeviceChanging = true;

            // close device and device manager
            CloseDeviceAndDeviceManager();

            // change TWAIN 2.0 compatibility
            _deviceManager.IsTwain2Compatible = twain2CompatibleCheckBox.Checked;

            // init devices
            InitDevices();
        }

        /// <summary>
        /// Current device is changed.
        /// </summary>
        private void devicesComboBox_SelectedIndexChanged(object sender, EventArgs e)
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
        private void acquireImageButton_Click(object sender, EventArgs e)
        {
            // acquiring, need to cancel
            if (IsImageAcquiring)
            {
                _currentDevice.CancelTransfer();
                return;
            }

            // acquire image(s)
            AcquireImage(nativeTransferRadioButton.Checked);
        }

        /// <summary>
        /// Native transfer mode is selected.
        /// </summary>
        private void nativeTransferRadioButton_CheckedChanged(object sender, EventArgs e)
        {
            imageAcquisitionProgressBar.Visible = false;
        }

        /// <summary>
        /// Memory transfer mode is selected.
        /// </summary>
        private void memoryTransferRadioButton_CheckedChanged(object sender, EventArgs e)
        {
            imageAcquisitionProgressBar.Visible = true;
        }

        /// <summary>
        /// Pixel type is changed.
        /// </summary>
        private void pixelTypeComboBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (!_isDeviceInitialized)
                return;

            this.Cursor = Cursors.WaitCursor;

            // if device is closed
            if (_currentDevice.State == DeviceState.Closed)
                // open the device
                _currentDevice.Open();

            _pixelType = (PixelType)pixelTypeComboBox.SelectedItem;
            _currentDevice.PixelType = _pixelType;

            // bit depth
            GetBitDepth();
            // threshold, contrast and brightness
            GetThresholdBrightnesContrast();

            this.Cursor = Cursors.Default;

            UpdateUI();
        }

        /// <summary>
        /// Unit of measure is changed.
        /// </summary>
        private void unitOfMeasureComboBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (!_isDeviceInitialized)
                return;

            this.Cursor = Cursors.WaitCursor;

            // if device is closed
            if (_currentDevice.State == DeviceState.Closed)
                // open the device
                _currentDevice.Open();

            _unitOfMeasure = (UnitOfMeasure)unitOfMeasureComboBox.SelectedItem;
            _currentDevice.UnitOfMeasure = _unitOfMeasure;
            GetResolution();
            ResetImageLayout();

            this.Cursor = Cursors.Default;

            UpdateUI();
        }

        /// <summary>
        /// Reset the image layout.
        /// </summary>
        private void resetImageLayoutButton_Click(object sender, EventArgs e)
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

            this.Cursor = Cursors.WaitCursor;

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

            this.Cursor = Cursors.Default;
        }

        /// <summary>
        /// Show tooltip when mouse hovers the track bar.
        /// </summary>
        private void trackBar_MouseHover(object sender, EventArgs e)
        {
            SetTooltip((TrackBar)sender);
        }

        /// <summary>
        /// Show tooltip when track bar is scrolling.
        /// </summary>
        private void trackBar_Scroll(object sender, EventArgs e)
        {
            SetTooltip((TrackBar)sender);
        }

        /// <summary>
        /// Associate ToolTip text with specified track bar.
        /// </summary>
        private void SetTooltip(TrackBar trackBar)
        {
            toolTip1.SetToolTip(trackBar, trackBar.Value.ToString());
        }

        /// <summary>
        /// Clear images.
        /// </summary>
        private void clearImagesButton_Click(object sender, EventArgs e)
        {
            acquiredImagesTabControl.Controls.Clear();

            GC.Collect();
        }

        /// <summary>
        /// Application form is closing.
        /// </summary>
        private void MainForm_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (_currentDevice != null)
            {
                // if image is acquiring
                if (_currentDevice.State > DeviceState.Enabled)
                {
                    // cancel image acquisition
                    _currentDevice.CancelTransfer();
                    // specify that form must be closed when image acquisition is canceled
                    _cancelTransferBecauseFormIsClosing = true;
                    // cancel form closing
                    e.Cancel = true;
                    return;
                }
            }

            // close the device and device manager
            CloseDeviceAndDeviceManager();
            // dispose the device manager
            _deviceManager.Dispose();
            _deviceManager = null;
        }

        private void ShowErrorMessage(string message, string title)
        {
            MessageBox.Show(message, title, MessageBoxButtons.OK, MessageBoxIcon.Error);
        }

        #endregion


        #region Acquire image(s)

        /// <summary>
        /// Acquires image(s).
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
        /// Subscribes to device events.
        /// </summary>
        private void SubscribeToDeviceEvents()
        {
            _currentDevice.ImageAcquiringProgress += new EventHandler<ImageAcquiringProgressEventArgs>(device_ImageAcquiringProgress);
            _currentDevice.ImageAcquired += new EventHandler<ImageAcquiredEventArgs>(device_ImageAcquired);
            _currentDevice.ScanFailed += new EventHandler<ScanFailedEventArgs>(device_ScanFailed);
            _currentDevice.ScanFinished += new EventHandler(device_ScanFinished);
        }

        /// <summary>
        /// Unsubscribes from device events.
        /// </summary>
        private void UnsubscribeFromDeviceEvents()
        {
            _currentDevice.ImageAcquiringProgress -= new EventHandler<ImageAcquiringProgressEventArgs>(device_ImageAcquiringProgress);
            _currentDevice.ImageAcquired -= new EventHandler<ImageAcquiredEventArgs>(device_ImageAcquired);
            _currentDevice.ScanFailed -= new EventHandler<ScanFailedEventArgs>(device_ScanFailed);
            _currentDevice.ScanFinished -= new EventHandler(device_ScanFinished);
        }

        /// <summary>
        /// Image is acquiring.
        /// </summary>
        private void device_ImageAcquiringProgress(object sender, ImageAcquiringProgressEventArgs e)
        {
            // image acquistion must be canceled because application's form is closing
            if (_cancelTransferBecauseFormIsClosing)
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
        private void device_ImageAcquired(object sender, ImageAcquiredEventArgs e)
        {
            // image acquistion must be canceled because application's form is closing
            if (_cancelTransferBecauseFormIsClosing)
            {
                // cancel image acquisition
                _currentDevice.CancelTransfer();
                return;
            }

            // create panel for picture box with acquired image
            TabPage tabPage1 = new TabPage();
            tabPage1.Location = new System.Drawing.Point(4, 22);
            tabPage1.Padding = new System.Windows.Forms.Padding(3);
            tabPage1.Size = new System.Drawing.Size(522, 318);
            tabPage1.Text = string.Format("Image {0} [{1}x{2}, {3}, {4}]", _imageCount++,
                                            e.Image.ImageInfo.Width,
                                            e.Image.ImageInfo.Height,
                                            e.Image.ImageInfo.PixelType,
                                            e.Image.ImageInfo.Resolution);

            // create picture box for acquired image
            PictureBox pictureBox1 = new PictureBox();
            // set the picture box size
            pictureBox1.Size = tabPage1.Size;
            // set a bitmap in the picture box
            pictureBox1.Image = e.Image.GetAsBitmap(true);
            // set the picture box size mode
            pictureBox1.SizeMode = PictureBoxSizeMode.StretchImage;

            // add a picture box to a panel
            tabPage1.Controls.Add(pictureBox1);
            // add a panel to a tab control with images
            acquiredImagesTabControl.Controls.Add(tabPage1);
            // select new panel
            acquiredImagesTabControl.SelectedTab = tabPage1;

            // dispose an acquired image
            e.Image.Dispose();
        }

        /// <summary>
        /// Scan is failed.
        /// </summary>
        private void device_ScanFailed(object sender, ScanFailedEventArgs e)
        {
            ShowErrorMessage(e.ErrorString, "Scan is failed");
        }

        /// <summary>
        /// Scan is finished.
        /// </summary>
        private void device_ScanFinished(object sender, EventArgs e)
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

                if (unitOfMeasureComboBox.Items.Count > 0)
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

            xResTrackBar.Visible = false;
            xResComboBox.Visible = false;
            _isXResolutionAvailable = false;

            if (_currentDevice.State == DeviceState.Closed)
                _currentDevice.Open();

            // get supported values of horizontal resolution
            TwainValueContainerBase xResCapValue = null;
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
                InitRangeCapValue(xResCapValue, xResTrackBar);

                xResTrackBar.Visible = true;
            }
            // if values are represented as array or enumeration
            else
            {
                InitComboBox(xResComboBox, xResCapValue.GetAsFloatArray(), _currentDevice.Resolution.Horizontal);

                xResComboBox.Visible = true;
            }

            _isXResolutionAvailable = true;


            // Vertical resolution

            yResTrackBar.Visible = false;
            yResComboBox.Visible = false;
            _isYResolutionAvailable = false;

            // get supported values of vertical resolution
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
                InitRangeCapValue(yResCapValue, yResTrackBar);

                yResTrackBar.Visible = true;
            }
            // if values are represented as array or enumeration
            else
            {
                InitComboBox(yResComboBox, yResCapValue.GetAsFloatArray(), _currentDevice.Resolution.Vertical);

                yResComboBox.Visible = true;
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

                if (pageSizeComboBox.Items.Count > 0)
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
                if (supportedPageOrientations != null && _currentDevice.GetSupportedPageOrientations().Length > 0)
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
        /// Get information about the image layout of device.
        /// </summary>
        private void GetImageLayout()
        {
            _isImageLayoutAvailable = false;

            if (_currentDevice.State == DeviceState.Closed)
                _currentDevice.Open();

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

            if (_currentDevice.State == DeviceState.Closed)
                _currentDevice.Open();

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
        private void GetThresholdBrightnesContrast()
        {
            thresholdComboBox.Visible = false;
            thresholdTrackBar.Visible = false;
            brightnessComboBox.Visible = false;
            brightnessComboBox.Visible = false;
            contrastComboBox.Visible = false;
            contrastTrackBar.Visible = false;

            if (_currentDevice.State == DeviceState.Closed)
                _currentDevice.Open();

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
                    InitRangeCapValue(capValue, thresholdTrackBar);

                    thresholdTrackBar.Visible = true;
                }
                else if (capValue.ContainerType == TwainValueContainerType.Enum)
                {
                    TwainEnumValueContainer capValueAsEnum = (TwainEnumValueContainer)capValue;
                    InitComboBox(thresholdComboBox, capValueAsEnum.GetAsFloatArray(), capValueAsEnum.GetAsFloat());

                    thresholdComboBox.Visible = true;
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
                    InitRangeCapValue(capValue, brightnessTrackBar);

                    brightnessTrackBar.Visible = true;
                }
                else if (capValue.ContainerType == TwainValueContainerType.Enum)
                {
                    TwainEnumValueContainer capValueAsEnum = (TwainEnumValueContainer)capValue;
                    InitComboBox(brightnessComboBox, capValueAsEnum.GetAsFloatArray(), capValueAsEnum.GetAsFloat());

                    brightnessComboBox.Visible = true;
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
                    InitRangeCapValue(capValue, contrastTrackBar);

                    contrastTrackBar.Visible = true;
                }
                else if (capValue.ContainerType == TwainValueContainerType.Enum)
                {
                    TwainEnumValueContainer capValueAsEnum = (TwainEnumValueContainer)capValue;
                    InitComboBox(contrastComboBox, capValueAsEnum.GetAsFloatArray(), capValueAsEnum.GetAsFloat());

                    contrastComboBox.Visible = true;
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
                    autoRotateCheckBox.Checked = autoRotateCapValue.GetAsBool();

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
                    autoBorderDetectionCheckBox.Checked = autoBorderDetectionCapValue.GetAsBool();

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
            if (xResComboBox.Visible && yResComboBox.Visible)
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
            if (xResTrackBar.Visible && yResTrackBar.Visible)
            {
                try
                {
                    float newXRes = (float)xResTrackBar.Value;
                    float newYRes = (float)yResTrackBar.Value;
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
                catch (FormatException ex)
                {
                    MessageBox.Show(ex.Message, "Set Image Layout Error");
                }
                catch (TwainDeviceException ex)
                {
                    MessageBox.Show(ex.Message, "Set Image Layout Error");
                }
                catch (TwainDeviceCapabilityException ex)
                {
                    MessageBox.Show(ex.Message, "Set Image Layout Error");
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
                    float newThreshold = (float)thresholdTrackBar.Value;
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
                    float newBrightness = (float)brightnessTrackBar.Value;
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
                    float newContrast = (float)contrastTrackBar.Value;
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
                    bool newAutoRotate = autoRotateCheckBox.Checked;
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
                    bool newAutoBorderDetection = autoBorderDetectionCheckBox.Checked;
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
