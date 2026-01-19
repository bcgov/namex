using System;
using System.Windows.Forms;
using Vintasoft.Twain;

namespace TwainExtendedImageInfoDemo
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

        #endregion



        #region Constructor

        public MainForm()
        {
            InitializeComponent();

            this.Text = String.Format("VintaSoft TWAIN Extended Image Info Demo v{0}", TwainGlobalSettings.ProductVersion);

            // create instance of the DeviceManager class
            _deviceManager = new DeviceManager(this);
        }

        #endregion



        #region Methods

        /// <summary>
        /// Application form is shown.
        /// </summary>
        private void MainForm_Shown(object sender, EventArgs e)
        {
            //
            string[] extendedImageInfoNames = Enum.GetNames(typeof(ExtendedImageInfoId));
            //
            for (int i = 0; i < extendedImageInfoNames.Length; i++)
                extendedImageInfoCheckedListBox.Items.Add(extendedImageInfoNames[i]);

            // select the standard extended image infos
            SelectStandardExtendedImageInfos();

            // open TWAIN device manager
            OpenDeviceManager();
        }


        /// <summary>
        /// Sets form's UI state.
        /// </summary>
        private void SetFormUiState(bool enabled)
        {
            acquireImageButton.Enabled = enabled;
        }


        /// <summary>
        /// Opens TWAIN device manager.
        /// </summary>
        private bool OpenDeviceManager()
        {
            SetFormUiState(false);

            // try to find the device manager 2.x
            _deviceManager.IsTwain2Compatible = true;
            // if TWAIN device manager 2.x is NOT available
            if (!_deviceManager.IsTwainAvailable)
            {
                // try to find the device manager 1.x
                _deviceManager.IsTwain2Compatible = true;
                // if TWAIN device manager 1.x is NOT available
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

            SetFormUiState(true);
            return true;
        }


        /// <summary>
        /// Acquires image.
        /// </summary>
        private void acquireImageButton_Click(object sender, EventArgs e)
        {
            try
            {
                // select the default device
                if (!_deviceManager.ShowDefaultDeviceSelectionDialog())
                {
                    MessageBox.Show("Device is not selected.");
                    return;
                }

                if (_currentDevice != null)
                    UnsubscribeFromDeviceEvents();

                // get reference to the selected device
                Device device = _deviceManager.DefaultDevice;

                _currentDevice = device;
                // subscribe to the device events
                SubscribeToDeviceEvents();

                // set acquisition parameters
                device.ShowUI = false;
                device.DisableAfterAcquire = true;

                // open the device
                device.Open();

                // determine if device supports the extended image info
                DeviceCapability extendedImageInfoCap = device.Capabilities.Find(DeviceCapabilityId.IExtImageInfo);
                if (extendedImageInfoCap == null)
                {
                    // close the device
                    device.Close();
                    MessageBox.Show("Device does not support extended image information.");
                    return;
                }

                // specify that image info is necessary
                AddExtendedImageInfoToRetrieveList(device);

                // start the asynchronous image acquisition process 
                device.Acquire();
            }
            catch (TwainException ex)
            {
                MessageBox.Show(ex.Message, "Error");
            }
        }

        /// <summary>
        /// Subscribes to the device events.
        /// </summary>
        private void SubscribeToDeviceEvents()
        {
            _currentDevice.ImageAcquired += new EventHandler<ImageAcquiredEventArgs>(device_ImageAcquired);
            _currentDevice.ScanCanceled += new EventHandler(device_ScanCanceled);
            _currentDevice.ScanFailed += new EventHandler<ScanFailedEventArgs>(device_ScanFailed);
            _currentDevice.ScanFinished += new EventHandler(device_ScanFinished);
        }

        /// <summary>
        /// Unsubscribes from the device events.
        /// </summary>
        private void UnsubscribeFromDeviceEvents()
        {
            _currentDevice.ImageAcquired -= new EventHandler<ImageAcquiredEventArgs>(device_ImageAcquired);
            _currentDevice.ScanCanceled -= new EventHandler(device_ScanCanceled);
            _currentDevice.ScanFailed -= new EventHandler<ScanFailedEventArgs>(device_ScanFailed);
            _currentDevice.ScanFinished -= new EventHandler(device_ScanFinished);
        }

        /// <summary>
        /// Image is acquired.
        /// </summary>
        private void device_ImageAcquired(object sender, ImageAcquiredEventArgs e)
        {
            // dispose an acquired image
            e.Image.Dispose();

            // output an extended image info

            extendedImageInfoAboutAcquiredImageTextBox.Text += "IMAGE IS ACQUIRED" + Environment.NewLine;
            extendedImageInfoAboutAcquiredImageTextBox.Text += Environment.NewLine;

            Device device = (Device)sender;
            for (int i = 0; i < device.ExtendedImageInfo.Count; i++)
            {
                AddExtendedImageInfoToResultTextBox(i, device.ExtendedImageInfo[i]);
            }
            extendedImageInfoAboutAcquiredImageTextBox.Text += Environment.NewLine;
        }

        /// <summary>
        /// Scan is canceled.
        /// </summary>
        private void device_ScanCanceled(object sender, EventArgs e)
        {
            MessageBox.Show("Scan is canceled.");
        }

        /// <summary>
        /// Scan is failed.
        /// </summary>
        private void device_ScanFailed(object sender, ScanFailedEventArgs e)
        {
            MessageBox.Show(e.ErrorString, "Scan is failed");
        }

        /// <summary>
        /// Scan is finished.
        /// </summary>
        void device_ScanFinished(object sender, EventArgs e)
        {
            // close the device
            _currentDevice.Close();
        }


        /// <summary>
        /// Select/unselect all types of extended image info.
        /// </summary>
        private void selectAllExtendedImageInfoButton_Click(object sender, EventArgs e)
        {
            bool selectAll = false;

            if (selectAllExtendedImageInfoButton.Text == "Select all")
            {
                selectAll = true;
                selectAllExtendedImageInfoButton.Text = "Unselect all";
            }
            else
            {
                selectAllExtendedImageInfoButton.Text = "Select all";
            }

            for (int i = 0; i < extendedImageInfoCheckedListBox.Items.Count; i++)
                extendedImageInfoCheckedListBox.SetItemChecked(i, selectAll);
        }

        /// <summary>
        /// Selects standard extended image infos (standard extended image infos always available
        /// if DeviceCapabilityId.IExtImageInfo capability is supported by device).
        /// </summary>
        private void SelectStandardExtendedImageInfos()
        {
            ExtendedImageInfoId[] standardExtendedImageInfoIds = new ExtendedImageInfoId[6] {
                ExtendedImageInfoId.DocumentNumber, ExtendedImageInfoId.PageNumber,
                ExtendedImageInfoId.Camera, ExtendedImageInfoId.FrameNumber,
                ExtendedImageInfoId.Frame, ExtendedImageInfoId.PixelFlavor };

            bool isStandardExtendedImageInfoFound;
            Type enumType = typeof(ExtendedImageInfoId);
            for (int i = 0; i < extendedImageInfoCheckedListBox.Items.Count; i++)
            {
                string extendedImageInfoIdAsString = (string)extendedImageInfoCheckedListBox.Items[i];
                ExtendedImageInfoId extendedImageInfoId = (ExtendedImageInfoId)Enum.Parse(enumType, extendedImageInfoIdAsString);

                isStandardExtendedImageInfoFound = false;
                for (int j = 0; j < standardExtendedImageInfoIds.Length; j++)
                {
                    if (extendedImageInfoId == standardExtendedImageInfoIds[j])
                    {
                        isStandardExtendedImageInfoFound = true;
                        break;
                    }
                }

                extendedImageInfoCheckedListBox.SetItemChecked(i, isStandardExtendedImageInfoFound);
            }
        }

        /// <summary>
        /// Adds type of extended image info to the list of necessary extended image infos.
        /// </summary>
        private void AddExtendedImageInfoToRetrieveList(Device device)
        {
            device.ExtendedImageInfo.Clear();

            Type enumType = typeof(ExtendedImageInfoId);
            for (int i = 0; i < extendedImageInfoCheckedListBox.Items.Count; i++)
            {
                if (extendedImageInfoCheckedListBox.GetItemChecked(i))
                {
                    string extendedImageInfoIdAsString = (string)extendedImageInfoCheckedListBox.Items[i];
                    ExtendedImageInfoId extendedImageInfoId = (ExtendedImageInfoId)Enum.Parse(enumType, extendedImageInfoIdAsString);

                    device.ExtendedImageInfo.Add(new ExtendedImageInfo(extendedImageInfoId));
                }
            }
        }

        /// <summary>
        /// Adds an extended image info to the result.
        /// </summary>
        private void AddExtendedImageInfoToResultTextBox(int index, ExtendedImageInfo info)
        {
            if (!info.IsValueValid)
                return;

            extendedImageInfoAboutAcquiredImageTextBox.Text += string.Format("Extended image info {0}", index);
            extendedImageInfoAboutAcquiredImageTextBox.Text += Environment.NewLine;

            extendedImageInfoAboutAcquiredImageTextBox.Text += string.Format("  Name={0}", Enum.GetName(typeof(ExtendedImageInfoId), info.InfoId));
            extendedImageInfoAboutAcquiredImageTextBox.Text += Environment.NewLine;

            extendedImageInfoAboutAcquiredImageTextBox.Text += string.Format("  Id={0}", info.InfoId);
            extendedImageInfoAboutAcquiredImageTextBox.Text += Environment.NewLine;

            extendedImageInfoAboutAcquiredImageTextBox.Text += string.Format("  Value type={0}", info.ValueType);
            extendedImageInfoAboutAcquiredImageTextBox.Text += Environment.NewLine;

            TwainOneValueContainer oneDeviceCapabilityValue = info.Value as TwainOneValueContainer;
            if (oneDeviceCapabilityValue != null)
            {
                extendedImageInfoAboutAcquiredImageTextBox.Text += string.Format("  Value={0}", oneDeviceCapabilityValue.Value);
                extendedImageInfoAboutAcquiredImageTextBox.Text += Environment.NewLine;
            }
            else
            {
                TwainArrayValueContainer arrayDeviceCapabilityValue = info.Value as TwainArrayValueContainer;
                if (arrayDeviceCapabilityValue != null)
                {
                    extendedImageInfoAboutAcquiredImageTextBox.Text += "Values: ";
                    if (arrayDeviceCapabilityValue.Values != null)
                    {
                        if (arrayDeviceCapabilityValue.Values.GetType() == typeof(byte[]))
                        {
                            extendedImageInfoAboutAcquiredImageTextBox.Text += string.Format("byte[{0}]", arrayDeviceCapabilityValue.Values.Length);
                        }
                        else
                        {
                            for (int i = 0; i < arrayDeviceCapabilityValue.Values.Length; i++)
                                extendedImageInfoAboutAcquiredImageTextBox.Text += string.Format("{0}, ", arrayDeviceCapabilityValue.Values.GetValue(i));
                        }
                    }
                    extendedImageInfoAboutAcquiredImageTextBox.Text += Environment.NewLine;
                }
            }
        }


        /// <summary>
        /// Application form is closing.
        /// </summary>
        private void MainForm_FormClosing(object sender, FormClosingEventArgs e)
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
        }

        #endregion

    }
}
