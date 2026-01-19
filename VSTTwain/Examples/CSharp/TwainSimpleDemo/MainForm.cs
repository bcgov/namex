using System;
using System.Windows.Forms;
using Vintasoft.Twain;

namespace TwainSimpleDemo
{
    public partial class MainForm : Form
    {

        #region Constructor

        public MainForm()
        {
            InitializeComponent();

            this.Text = string.Format("VintaSoft TWAIN Simple Demo v{0}", TwainGlobalSettings.ProductVersion);
        }

        #endregion



        #region Methods

        /// <summary>
        /// Scans images.
        /// </summary>
        private void scanImagesButton_Click(object sender, EventArgs e)
        {
            try
            {
                // disable application UI
                scanImagesButton.Enabled = false;

                // create TWAIN device manager
                using (DeviceManager deviceManager = new DeviceManager(this))
                {
                    // try to find TWAIN device manager
                    deviceManager.IsTwain2Compatible = twain2CheckBox.Checked;
                    // if TWAIN device manager is not found
                    if (!deviceManager.IsTwainAvailable)
                    {
                        // try to find another TWAIN device manager
                        deviceManager.IsTwain2Compatible = !twain2CheckBox.Checked;
                        // if TWAIN device manager is not found
                        if (!deviceManager.IsTwainAvailable)
                        {
                            MessageBox.Show("TWAIN device manager is not found.");
                            return;
                        }
                    }

                    // open the device manager
                    deviceManager.Open();

                    // if devices are NOT found
                    if (deviceManager.Devices.Count == 0)
                    {
                        MessageBox.Show("Devices are not found.");
                        return;
                    }

                    // if device is NOT selected
                    if (!deviceManager.ShowDefaultDeviceSelectionDialog())
                    {
                        MessageBox.Show("Device is not selected.");
                        return;
                    }

                    // get reference to the selected device
                    Device device = deviceManager.DefaultDevice;

                    // set scan settings
                    device.ShowUI = showUiCheckBox.Checked;
                    device.ShowIndicators = showIndicatorsCheckBox.Checked;
                    device.DisableAfterAcquire = !device.ShowUI;
                    device.CloseAfterModalAcquire = false;

                    int totalImageCount = 0;
                    int imageCount = 0;
                    AcquireModalState acquireModalState = AcquireModalState.None;
                    do
                    {
                        // synchronously acquire image from device
                        acquireModalState = device.AcquireModal();
                        switch (acquireModalState)
                        {
                            case AcquireModalState.ImageAcquired:
                                // dispose previous bitmap in the picture box
                                if (pictureBox1.Image != null)
                                {
                                    pictureBox1.Image.Dispose();
                                    pictureBox1.Image = null;
                                }

                                // set a bitmap in the picture box
                                pictureBox1.Image = device.AcquiredImage.GetAsBitmap(true);

                                imageCount++;
                                totalImageCount++;

                                // dispose an acquired image
                                device.AcquiredImage.Dispose();

                                MessageBox.Show("Image is acquired.");
                                break;

                            case AcquireModalState.ScanCompleted:
                                MessageBox.Show(string.Format("Scan is completed. {0} images are acquired in session. Total {1} images are scanned.", imageCount, totalImageCount));
                                imageCount = 0;
                                break;

                            case AcquireModalState.ScanCanceled:
                                MessageBox.Show("Scan is canceled.");
                                break;

                            case AcquireModalState.ScanFailed:
                                MessageBox.Show(string.Format("Scan is failed: {0}", device.ErrorString));
                                break;

                            case AcquireModalState.UserInterfaceClosed:
                                MessageBox.Show("User interface is closed.");
                                break;
                        }
                    }
                    while (acquireModalState != AcquireModalState.None);

                    // close the device
                    device.Close();

                    // close the device manager
                    deviceManager.Close();
                }
            }
            catch (TwainException ex)
            {
                MessageBox.Show(ex.Message);
            }
            finally
            {
                // enable application UI
                scanImagesButton.Enabled = true;
            }
        }

        #endregion

    }
}