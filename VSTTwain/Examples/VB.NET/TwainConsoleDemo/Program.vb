Imports System.IO
Imports Vintasoft.Twain

Class Program

    Friend Shared Sub Main(ByVal args As String())
        Try
            ' create TWAIN device manager
            Using deviceManager As New DeviceManager()
                ' try to use TWAIN device manager 2.x
                deviceManager.IsTwain2Compatible = True
                ' if TWAIN device manager 2.x is not available
                If Not deviceManager.IsTwainAvailable Then
                    ' try to use TWAIN device manager 1.x
                    deviceManager.IsTwain2Compatible = False
                    ' if TWAIN device manager 1.x is not available
                    If Not deviceManager.IsTwainAvailable Then
                        Console.WriteLine("TWAIN device manager is not available.")
                        Return
                    End If
                End If

                ' open the device manager
                deviceManager.Open()

                ' if no devices are found in the system
                If deviceManager.Devices.Count = 0 Then
                    Console.WriteLine("Devices are not found.")
                    Return
                End If

                ' select the device
                deviceManager.ShowDefaultDeviceSelectionDialog()

                ' get reference to the current device
                Dim device As Device = deviceManager.DefaultDevice

                device.ShowUI = False
                device.DisableAfterAcquire = True

                ' open the device
                device.Open()

                ' set acquisition parameters
                If device.TransferMode <> TransferMode.Native Then
                    device.TransferMode = TransferMode.Native
                End If
                If device.PixelType <> PixelType.BW Then
                    device.PixelType = PixelType.BW
                End If

                ' create directory for TIFF file
                Dim directoryForImages As String = Path.GetDirectoryName(Directory.GetCurrentDirectory())
                directoryForImages = Path.Combine(directoryForImages, "Images")
                If Not Directory.Exists(directoryForImages) Then
                    Directory.CreateDirectory(directoryForImages)
                End If

                Dim multipageTiffFilename As String = Path.Combine(directoryForImages, "multipage.tif")

                ' acquire image(s) from the device
                Dim imageIndex As Integer = 0
                Dim acquireModalState1 As AcquireModalState = AcquireModalState.None
                Do
                    acquireModalState1 = device.AcquireModal()
                    Select Case acquireModalState1
                        Case AcquireModalState.ImageAcquired
                            ' save acquired image to a file
                            device.AcquiredImage.Save(multipageTiffFilename)
                            ' dispose an acquired image
                            device.AcquiredImage.Dispose()

                            Console.WriteLine(String.Format("Image{0} is saved.", System.Math.Max(System.Threading.Interlocked.Increment(imageIndex), imageIndex - 1)))
                            Exit Select

                        Case AcquireModalState.ScanCompleted
                            Console.WriteLine("Scan is completed.")
                            Exit Select

                        Case AcquireModalState.ScanCanceled
                            Console.WriteLine("Scan is canceled.")
                            Exit Select

                        Case AcquireModalState.ScanFailed
                            Console.WriteLine(String.Format("Scan is failed: {0}", device.ErrorString))
                            Exit Select

                        Case AcquireModalState.UserInterfaceClosed
                            Console.WriteLine("User interface is closed.")
                            Exit Select
                    End Select
                Loop While acquireModalState1 <> AcquireModalState.None

                ' close the device
                device.Close()

                ' close the device manager
                deviceManager.Close()
            End Using
        Catch ex As TwainException
            Console.WriteLine("Error: " + ex.Message)
        End Try

        Console.WriteLine("Press any key to continue...")
        Console.ReadKey()
    End Sub

End Class
