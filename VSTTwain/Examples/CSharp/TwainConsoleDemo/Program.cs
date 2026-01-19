using System;
using System.IO;
using Vintasoft.Twain;

namespace TwainConsoleDemo
{
    class Program
    {

        static void Main(string[] args)
        {
            try
            {
                // create TWAIN device manager
                using (DeviceManager deviceManager = new DeviceManager())
                {
                    // try to use TWAIN device manager 2.x
                    deviceManager.IsTwain2Compatible = true;
                    // if TWAIN device manager 2.x is not available
                    if (!deviceManager.IsTwainAvailable)
                    {
                        // try to use TWAIN device manager 1.x
                        deviceManager.IsTwain2Compatible = false;
                        // if TWAIN device manager 1.x is not available
                        if (!deviceManager.IsTwainAvailable)
                        {
                            Console.WriteLine("TWAIN device manager is not available.");
                            return;
                        }
                    }

                    // open the device manager
                    deviceManager.Open();

                    // if no devices are found in the system
                    if (deviceManager.Devices.Count == 0)
                    {
                        Console.WriteLine("Devices are not found.");
                        return;
                    }

                    // select the device
                    deviceManager.ShowDefaultDeviceSelectionDialog();

                    // get reference to the current device
                    Device device = deviceManager.DefaultDevice;

                    device.ShowUI = false;
                    device.DisableAfterAcquire = true;

                    // open the device
                    device.Open();

                    // set acquisition parameters
                    if (device.TransferMode != TransferMode.Native)
                        device.TransferMode = TransferMode.Native;
                    if (device.PixelType != PixelType.BW)
                        device.PixelType = PixelType.BW;

                    // create directory for TIFF file
                    string directoryForImages = Path.GetDirectoryName(Directory.GetCurrentDirectory());
                    directoryForImages = Path.Combine(directoryForImages, "Images");
                    if (!Directory.Exists(directoryForImages))
                        Directory.CreateDirectory(directoryForImages);

                    string multipageTiffFilename = Path.Combine(directoryForImages, "multipage.tif");

                    // acquire image(s) from the device
                    int imageIndex = 0;
                    AcquireModalState acquireModalState = AcquireModalState.None;
                    do
                    {
                        acquireModalState = device.AcquireModal();
                        switch (acquireModalState)
                        {
                            case AcquireModalState.ImageAcquired:
                                // save acquired image to a file
                                device.AcquiredImage.Save(multipageTiffFilename);
                                // dispose an acquired image
                                device.AcquiredImage.Dispose();

                                Console.WriteLine(string.Format("Image{0} is saved.", imageIndex++));
                                break;

                            case AcquireModalState.ScanCompleted:
                                Console.WriteLine("Scan is completed.");
                                break;

                            case AcquireModalState.ScanCanceled:
                                Console.WriteLine("Scan is canceled.");
                                break;

                            case AcquireModalState.ScanFailed:
                                Console.WriteLine(string.Format("Scan is failed: {0}", device.ErrorString));
                                break;

                            case AcquireModalState.UserInterfaceClosed:
                                Console.WriteLine("User interface is closed.");
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
                Console.WriteLine("Error: " + ex.Message);
            }

            Console.WriteLine("Press any key to continue...");
            Console.ReadKey();
        }

    }
}