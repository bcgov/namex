Imports System.ComponentModel
Imports System.Diagnostics
Imports System.Globalization
Imports System.IO
Imports System.Windows
Imports System.Windows.Input
Imports System.Windows.Media
Imports System.Windows.Threading
Imports Microsoft.Win32
Imports Vintasoft.WpfTwain
Imports Vintasoft.WpfTwain.ImageEncoders
Imports Vintasoft.WpfTwain.ImageProcessing

''' <summary>
''' Interaction logic for MainWindow.xaml
''' </summary>
Partial Public Class MainWindow
    Inherits Window

#Region "Fields"

    ''' <summary>
    ''' TWAIN device manager.
    ''' </summary>
    Private _deviceManager As DeviceManager

    ''' <summary>
    ''' Current device.
    ''' </summary>
    Private _currentDevice As Device

    ''' <summary>
    ''' Indicates that device is acquiring image(s).
    ''' </summary>
    Private _isImageAcquiring As Boolean

    ''' <summary>
    ''' Acquired image collection.
    ''' </summary>
    Private _images As New AcquiredImageCollection()

    ''' <summary>
    ''' Current image index in acquired image collection.
    ''' </summary>
    Private _imageIndex As Integer = -1

    ''' <summary>
    ''' Determines that image acquistion must be canceled because application's window is closing.
    ''' </summary>
    Private _cancelTransferBecauseWindowIsClosing As Boolean

    Private _saveFileDialog1 As New SaveFileDialog()

#End Region



#Region "Constructors"

    Public Sub New()
        InitializeComponent()

        Me.Title = String.Format("VintaSoft WPF TWAIN Advanced Demo v{0}", TwainGlobalSettings.ProductVersion)

        _saveFileDialog1.FileName = "doc1"
        _saveFileDialog1.Filter = "BMP image|*.bmp|GIF image|*.gif|JPEG image|*.jpg|PNG image|*.png|TIFF image|*.tif|PDF document|*.pdf"
        _saveFileDialog1.FilterIndex = 3

        ' get country and language for TWAIN device manager
        Dim country As CountryCode
        Dim language As LanguageType
        GetCountryAndLanguage(country, language)

        ' create TWAIN device manager
        _deviceManager = New DeviceManager(Me, country, language)

        UpdateUI()
    End Sub

#End Region



#Region "Methods"

#Region "Device manager"

    ''' <summary>
    ''' Opens TWAIN device manager.
    ''' </summary>
    Private Sub openDeviceManagerButton_Click(ByVal sender As Object, ByVal e As RoutedEventArgs)
        ' clear list of devices
        devicesComboBox.Items.Clear()

        ' if device manager is opened
        If _deviceManager.State = DeviceManagerState.Opened Then
            ' close the device manager
            _deviceManager.Close()

            ' change text on this button
            openDeviceManagerButton.Content = "Open device manager"
        Else

            ' if device manager is closed
            ' try to find the device manager specified by user
            If twain2CompatibleCheckBox.IsChecked = True Then
                _deviceManager.IsTwain2Compatible = True
            Else
                _deviceManager.IsTwain2Compatible = False
            End If
            ' if device manager is not found
            If Not _deviceManager.IsTwainAvailable Then
                ' try to find another version of device manager
                _deviceManager.IsTwain2Compatible = Not _deviceManager.IsTwain2Compatible
                ' if device manager is not found again
                If Not _deviceManager.IsTwainAvailable Then
                    ' show dialog with error message
                    MessageBox.Show("TWAIN device manager is not found.", "TWAIN device manager", MessageBoxButton.OK, MessageBoxImage.[Error])

                    ' open a HTML page with article describing how to solve the problem
                    Process.Start("http://www.vintasoft.com/docs/vstwain-dotnet/index.html?Programming-Twain-Device_Manager.html")

                    Return
                End If
            End If

            ' device manager is found

            ' if check box value should be updated
            If twain2CompatibleCheckBox.IsChecked <> _deviceManager.IsTwain2Compatible Then
                ' update check box value 
                twain2CompatibleCheckBox.IsChecked = _deviceManager.IsTwain2Compatible
            End If

            Try
                ' open the device manager
                _deviceManager.Open()
            Catch ex As TwainDeviceManagerException
                ' close the device manager
                _deviceManager.Close()

                ' show dialog with error message
                MessageBox.Show(ex.Message, "TWAIN device manager", MessageBoxButton.OK, MessageBoxImage.[Error])

                ' open a HTML page with article describing how to solve the problem
                Process.Start("http://www.vintasoft.com/docs/vstwain-dotnet/index.html?Programming-Twain-Device_Manager.html")

                Return
            End Try

            Dim devices As DeviceCollection = _deviceManager.Devices
            ' for each available device
            For i As Integer = 0 To devices.Count - 1
                ' add the device name to a combo box
                devicesComboBox.Items.Add(devices(i).Info.ProductName)

                ' if device is default device
                If devices(i) Is _deviceManager.DefaultDevice Then
                    ' select device in a combo box
                    devicesComboBox.SelectedIndex = i
                End If
            Next

            ' change text on this button
            openDeviceManagerButton.Content = "Close device manager"
        End If

        ' update UI
        UpdateUI()
    End Sub

#End Region


#Region "Devices"

    ''' <summary>
    ''' Selects the active device using TWAIN standard selection dialog.
    ''' </summary>
    Private Sub selectDeviceButton_Click(ByVal sender As Object, ByVal e As RoutedEventArgs)
        ' show the TWAIN device selection dialog
        If _deviceManager.ShowDefaultDeviceSelectionDialog() Then
            Dim devices As DeviceCollection = _deviceManager.Devices
            ' for each device
            For i As Integer = 0 To devices.Count - 1
                ' if device is default device
                If devices(i) Is _deviceManager.DefaultDevice Then
                    ' select device in a combo box
                    devicesComboBox.SelectedIndex = i
                End If
            Next
        End If
    End Sub

#End Region


#Region "Device"

    ''' <summary>
    ''' Gets information about device and device capabilities.
    ''' </summary>
    Private Sub getDeviceInfoButton_Click(ByVal sender As Object, ByVal e As RoutedEventArgs)
        Try
            ' find a device by device name
            Dim device As Device = _deviceManager.Devices.Find(DirectCast(devicesComboBox.SelectedItem, String))

            ' show dialog with information about device and device capabilities
            Dim deviceCapabilitiesWindow As New DevCapsWindow(Me, device)
            deviceCapabilitiesWindow.ShowDialog()
        Catch ex As TwainDeviceException
            MessageBox.Show(ex.Message, "Device error", MessageBoxButton.OK, MessageBoxImage.[Error])
        Catch ex As TwainDeviceCapabilityException
            MessageBox.Show(ex.Message, "Device capability rror", MessageBoxButton.OK, MessageBoxImage.[Error])
        End Try
    End Sub

    ''' <summary>
    ''' Enables/disables User Interface of device.
    ''' </summary>
    Private Sub showUICheckBox_CheckedChanged(ByVal sender As Object, ByVal e As RoutedEventArgs)
        If showIndicatorsCheckBox Is Nothing Then
            Return
        End If

        modalUICheckBox.IsEnabled = CBool(showUICheckBox.IsChecked)
        disableAfterAcquireCheckBox.IsEnabled = CBool(showUICheckBox.IsChecked)

        adfGroupBox.IsEnabled = CBool(Not showUICheckBox.IsChecked)
    End Sub

    ''' <summary>
    ''' Transfer mode is changed.
    ''' </summary>
    Private Sub transferModeComboBox_SelectionChanged(ByVal sender As Object, ByVal e As System.Windows.Controls.SelectionChangedEventArgs)
        If imageAcquisitionProgressBar Is Nothing Then
            Return
        End If

        If transferModeComboBox.SelectedIndex = 0 Then
            imageAcquisitionProgressBar.Visibility = Visibility.Hidden
        Else
            imageAcquisitionProgressBar.Visibility = Visibility.Visible
        End If
    End Sub

    ''' <summary>
    ''' Enables/disables usage of ADF.
    ''' </summary>
    Private Sub useAdfCheckBox_CheckedChanged(ByVal sender As Object, ByVal e As RoutedEventArgs)
        If useDuplexCheckBox IsNot Nothing Then
            useDuplexCheckBox.IsEnabled = CBool(useAdfCheckBox.IsChecked)
            imagesToAcquireNumericUpDown.IsEnabled = CBool(useAdfCheckBox.IsChecked)
        End If
    End Sub

#End Region


#Region "Image acquisition"

    ''' <summary>
    ''' Starts the image acquisition.
    ''' </summary>
    Private Sub acquireImageButton_Click(ByVal sender As Object, ByVal e As RoutedEventArgs)
        ' specify that image acquisition is started
        _isImageAcquiring = True
        ' update UI
        UpdateUI()

        Try
            If _currentDevice IsNot Nothing Then
                ' unsubscribe from the device events
                UnsubscribeFromDeviceEvents(_currentDevice)
            End If

            ' find the device by device name
            Dim deviceName As String = DirectCast(devicesComboBox.SelectedItem, String)
            Dim device As Device = _deviceManager.Devices.Find(deviceName)
            If device Is Nothing Then
                ' specify that image acquisition is finished
                _isImageAcquiring = False

                MessageBox.Show(String.Format("Device '{0}' is not found.", deviceName), "TWAIN device", MessageBoxButton.OK, MessageBoxImage.[Error])
                Return
            End If

            _currentDevice = device
            ' subscribe to the device events
            SubscribeToDeviceEvents(_currentDevice)

            ' set the image acquisition parameters
            device.ShowUI = CBool(showUICheckBox.IsChecked)
            device.ModalUI = CBool(modalUICheckBox.IsChecked)
            device.ShowIndicators = CBool(showIndicatorsCheckBox.IsChecked)
            device.DisableAfterAcquire = CBool(disableAfterAcquireCheckBox.IsChecked)

            ' trasfer mode
            If transferModeComboBox.SelectedIndex = 0 Then
                device.TransferMode = TransferMode.Native
            Else
                device.TransferMode = TransferMode.Memory
            End If

            Try
                ' open the device
                device.Open()
            Catch ex As TwainException
                ' specify that image acquisition is finished
                _isImageAcquiring = False

                MessageBox.Show(ex.Message, "TWAIN device", MessageBoxButton.OK, MessageBoxImage.[Error])
                Return
            End Try

            ' set device capabilities

            ' pixel type
            Dim pixelType__1 As PixelType = PixelType.BW
            Try
                If pixelTypeComboBox.SelectedIndex = 1 Then
                    pixelType__1 = PixelType.Gray
                ElseIf pixelTypeComboBox.SelectedIndex = 2 Then
                    pixelType__1 = PixelType.RGB
                End If

                If device.PixelType <> pixelType__1 Then
                    device.PixelType = pixelType__1
                End If
            Catch generatedExceptionName As TwainException
                MessageBox.Show(String.Format("Pixel type ""{0}"" is not supported.", pixelType__1), "TWAIN device")
            End Try

            ' unit of measure
            Try
                If device.UnitOfMeasure <> UnitOfMeasure.Inches Then
                    device.UnitOfMeasure = UnitOfMeasure.Inches
                End If
            Catch generatedExceptionName As TwainException
                MessageBox.Show("Unit of measure ""Inches"" is not supported.", "TWAIN device")
            End Try

            ' resolution
            Dim resolution As New Resolution(100, 100)
            Try
                If resolutionComboBox.SelectedIndex = 1 Then
                    resolution = New Resolution(150, 150)
                ElseIf resolutionComboBox.SelectedIndex = 2 Then
                    resolution = New Resolution(200, 200)
                ElseIf resolutionComboBox.SelectedIndex = 3 Then
                    resolution = New Resolution(300, 300)
                ElseIf resolutionComboBox.SelectedIndex = 4 Then
                    resolution = New Resolution(600, 600)
                End If

                If device.Resolution.Horizontal <> resolution.Horizontal OrElse device.Resolution.Vertical <> resolution.Vertical Then
                    device.Resolution = resolution
                End If
            Catch generatedExceptionName As TwainException
                MessageBox.Show(String.Format("Resolution ""{0}"" is not supported.", resolution), "TWAIN device")
            End Try

            ' if device is Fujitsu scanner
            If device.Info.ProductName.ToUpper().StartsWith("FUJITSU") Then
                Dim undefinedImageSizeCap As DeviceCapability = device.Capabilities.Find(DeviceCapabilityId.IUndefinedImageSize)
                ' if undefined image size is supported
                If undefinedImageSizeCap IsNot Nothing Then
                    Try
                        ' enable undefined image size feature
                        undefinedImageSizeCap.SetValue(True)
                    Catch generatedExceptionName As TwainDeviceCapabilityException
                    End Try
                End If
            End If

            Try
                ' if ADF present
                If Not device.Info.IsWIA AndAlso device.HasFeeder Then
                    ' enable/disable ADF if necessary
                    Try
                        If device.DocumentFeeder.Enabled <> useAdfCheckBox.IsChecked Then
                            device.DocumentFeeder.Enabled = CBool(useAdfCheckBox.IsChecked)
                        End If
                    Catch generatedExceptionName As TwainDeviceCapabilityException
                    End Try

                    ' enable/disable duplex if necessary
                    Try
                        If device.DocumentFeeder.DuplexEnabled <> useDuplexCheckBox.IsChecked Then
                            device.DocumentFeeder.DuplexEnabled = CBool(useDuplexCheckBox.IsChecked)
                        End If
                    Catch generatedExceptionName As TwainDeviceCapabilityException
                    End Try
                End If

                If acquireAllImagesRadioButton.IsChecked = False Then
                    device.XferCount = CType(imagesToAcquireNumericUpDown.Value, Int16)
                End If
            Catch ex As TwainException
                MessageBox.Show(ex.Message, "TWAIN device")
            End Try

            ' if device supports asynchronous events
            If device.IsAsyncEventsSupported Then
                Try
                    ' enable all asynchronous events supported by device
                    device.AsyncEvents = device.GetSupportedAsyncEvents()
                Catch
                End Try
            End If


            Try
                ' start image acquition process
                device.Acquire()
            Catch ex As TwainException
                ' specify that image acquisition is finished
                _isImageAcquiring = False

                MessageBox.Show(ex.Message, "TWAIN device", MessageBoxButton.OK, MessageBoxImage.[Error])
                Return
            End Try
        Finally
            ' update UI
            UpdateUI()
        End Try
    End Sub

    ''' <summary>
    ''' Subscribe to the device events.
    ''' </summary>
    Private Sub SubscribeToDeviceEvents(ByVal device As Device)
        AddHandler device.ImageAcquiringProgress, New EventHandler(Of ImageAcquiringProgressEventArgs)(AddressOf _device_ImageAcquiringProgress)
        AddHandler device.ImageAcquired, New EventHandler(Of ImageAcquiredEventArgs)(AddressOf _device_ImageAcquired)
        AddHandler device.ScanFailed, New EventHandler(Of ScanFailedEventArgs)(AddressOf _device_ScanFailed)
        AddHandler device.AsyncEvent, New EventHandler(Of DeviceAsyncEventArgs)(AddressOf device_AsyncEvent)
        AddHandler device.ScanFinished, New EventHandler(AddressOf device_ScanFinished)
    End Sub

    ''' <summary>
    ''' Unsubscribe from the device events.
    ''' </summary>
    Private Sub UnsubscribeFromDeviceEvents(ByVal device As Device)
        RemoveHandler device.ImageAcquiringProgress, New EventHandler(Of ImageAcquiringProgressEventArgs)(AddressOf _device_ImageAcquiringProgress)
        RemoveHandler device.ImageAcquired, New EventHandler(Of ImageAcquiredEventArgs)(AddressOf _device_ImageAcquired)
        RemoveHandler device.ScanFailed, New EventHandler(Of ScanFailedEventArgs)(AddressOf _device_ScanFailed)
        RemoveHandler device.AsyncEvent, New EventHandler(Of DeviceAsyncEventArgs)(AddressOf device_AsyncEvent)
        RemoveHandler device.ScanFinished, New EventHandler(AddressOf device_ScanFinished)
    End Sub

    ''' <summary>
    ''' Image acquiring progress is changed.
    ''' </summary>
    Private Sub _device_ImageAcquiringProgress(ByVal sender As Object, ByVal e As ImageAcquiringProgressEventArgs)
        ' image acquistion must be canceled because application's window is closing
        If _cancelTransferBecauseWindowIsClosing Then
            ' cancel image acquisition
            _currentDevice.CancelTransfer()
            Return
        End If

        imageAcquisitionProgressBar.Value = CInt(e.Progress)

        If imageAcquisitionProgressBar.Value = 100 Then
            imageAcquisitionProgressBar.Value = 0
        End If
    End Sub

    ''' <summary>
    ''' Image is acquired.
    ''' </summary>
    Private Sub _device_ImageAcquired(ByVal sender As Object, ByVal e As ImageAcquiredEventArgs)
        ' image acquistion must be canceled because application's window is closing
        If _cancelTransferBecauseWindowIsClosing Then
            ' cancel image acquisition
            _currentDevice.CancelTransfer()
            Return
        End If

        _images.Add(e.Image)

        SetCurrentImage(_images.Count - 1)
    End Sub

    ''' <summary>
    ''' Scan is failed.
    ''' </summary>
    Private Sub _device_ScanFailed(ByVal sender As Object, ByVal e As ScanFailedEventArgs)
        ' show error message
        MessageBox.Show(e.ErrorString, "Scan is failed", MessageBoxButton.OK, MessageBoxImage.[Error])
    End Sub

    ''' <summary>
    ''' An asynchronous event was generated by device.
    ''' </summary>
    Private Sub device_AsyncEvent(ByVal sender As Object, ByVal e As DeviceAsyncEventArgs)
        Select Case e.DeviceEvent
            Case DeviceEventId.PaperJam
                MessageBox.Show("Paper is jammed.")
                Exit Select

            Case DeviceEventId.CheckDeviceOnline
                MessageBox.Show("Check that device is online.")
                Exit Select

            Case DeviceEventId.CheckBattery
                MessageBox.Show(String.Format("DeviceEvent: Device={0}, Event={1}, BatteryMinutes={2}, BatteryPercentage={3}", e.DeviceName, e.DeviceEvent, e.BatteryMinutes, e.BatteryPercentage))
                Exit Select

            Case DeviceEventId.CheckPowerSupply
                MessageBox.Show(String.Format("DeviceEvent: Device={0}, Event={1}, PowerSupply={2}", e.DeviceName, e.DeviceEvent, e.PowerSupply))
                Exit Select

            Case DeviceEventId.CheckResolution
                MessageBox.Show(String.Format("DeviceEvent: Device={0}, Event={1}, Resolution={2}", e.DeviceName, e.DeviceEvent, e.Resolution))
                Exit Select

            Case DeviceEventId.CheckFlash
                MessageBox.Show(String.Format("DeviceEvent: Device={0}, Event={1}, FlashUsed={2}", e.DeviceName, e.DeviceEvent, e.FlashUsed))
                Exit Select

            Case DeviceEventId.CheckAutomaticCapture
                MessageBox.Show(String.Format("DeviceEvent: Device={0}, Event={1}, AutomaticCapture={2}, TimeBeforeFirstCapture={3}, TimeBetweenCaptures={4}", e.DeviceName, e.DeviceEvent, e.AutomaticCapture, e.TimeBeforeFirstCapture, e.TimeBetweenCaptures))
                Exit Select
            Case Else

                MessageBox.Show(String.Format("DeviceEvent: Device={0}, Event={1}", e.DeviceName, e.DeviceEvent))
                Exit Select
        End Select

        ' if device is enabled or transferring images
        If _currentDevice.State >= DeviceState.Enabled Then
            Return
        End If

        ' close the device
        _currentDevice.Close()
    End Sub

    ''' <summary>
    ''' Scan is finished.
    ''' </summary>
    Private Sub device_ScanFinished(ByVal sender As Object, ByVal e As EventArgs)
        ' close the device
        _currentDevice.Close()

        ' specify that image acquisition is finished
        _isImageAcquiring = False
        ' update UI
        UpdateUI()
    End Sub

#End Region


#Region "Acquired images"

#Region "Navigation"

    ''' <summary>
    ''' Shows previous acquired image.
    ''' </summary>
    Private Sub previousImageButton_Click(ByVal sender As Object, ByVal e As RoutedEventArgs)
        SetCurrentImage(_imageIndex - 1)
        ' update UI
        UpdateUI()
    End Sub

    ''' <summary>
    ''' Shows next acquired image.
    ''' </summary>
    Private Sub nextImageButton_Click(ByVal sender As Object, ByVal e As RoutedEventArgs)
        SetCurrentImage(_imageIndex + 1)
        ' update UI
        UpdateUI()
    End Sub

#End Region


#Region "Preview"

    ''' <summary>
    ''' Gets the information about current image.
    ''' </summary>
    Private Function GetCurrentImageInfo(ByVal index As Integer, ByVal acquiredImage As AcquiredImage) As String
        Dim imageInfo As ImageInfo = acquiredImage.ImageInfo
        Return String.Format("Image {0} from {1} ({2} x {3}, {4} bpp, {5})", index, _images.Count, imageInfo.Width, imageInfo.Height, imageInfo.BitCount, _
         imageInfo.Resolution)
    End Function

    ''' <summary>
    ''' Sets the current image.
    ''' </summary>
    Private Sub SetCurrentImage(ByVal index As Integer)
        SyncLock Me
            ' dispose previous image if necessary
            If image1.Source IsNot Nothing Then
                image1.Source = Nothing
            End If

            ' get the image from the internal buffer of the device if image is present
            If index >= 0 Then
                Dim acquiredImage As AcquiredImage = _images(index)

                image1.Source = acquiredImage.GetAsBitmapSource()
                SetImageScrolls()

                imageInfoLabel.Content = GetCurrentImageInfo(index, acquiredImage)

                _imageIndex = index
            Else
                ' show "No images" text
                imageInfoLabel.Content = "No images"

                _imageIndex = -1
            End If

            ' update UI
            UpdateUI()
        End SyncLock
    End Sub

    ''' <summary>
    ''' Changes preview mode of current image.
    ''' </summary>
    Private Sub stretchImageCheckBox_CheckedChanged(ByVal sender As Object, ByVal e As RoutedEventArgs)
        SetImageScrolls()
    End Sub

    ''' <summary>
    ''' Sets scrolls of image.
    ''' </summary>
    Private Sub SetImageScrolls()
        If image1 IsNot Nothing Then
            If stretchImageCheckBox.IsChecked = True Then
                image1.Width = imageScrollViewer.ViewportWidth - 5
                image1.Height = imageScrollViewer.ViewportHeight - 5
                image1.Stretch = Stretch.Fill
            Else
                image1.Width = image1.Source.Width
                image1.Height = image1.Source.Height
                image1.Stretch = Stretch.None
            End If
        End If
    End Sub

    ''' <summary>
    ''' Window of application is resized.
    ''' </summary>
    Private Sub MainWindow_Resize(ByVal sender As Object, ByVal e As SizeChangedEventArgs)
        If stretchImageCheckBox.IsChecked = True Then
            image1.Margin = New Thickness(2, 2, 2, 2)
        End If
    End Sub

#End Region


#Region "Processing"

    ''' <summary>
    ''' Processes acquired image.
    ''' </summary>
    Private Sub processImageButton_Click(ByVal sender As Object, ByVal e As RoutedEventArgs)
        ' get reference to current image
        Dim currentImage As AcquiredImage = _images(_imageIndex)

        ' process current image
        Dim window1 As New ImageProcessingWindow(currentImage)
        window1.ShowDialog()

        ' update current image
        SetCurrentImage(_imageIndex)
    End Sub

    ''' <summary>
    ''' Shows information about progress of image processing function.
    ''' </summary>
    Private Sub currentImage_ImageProcessingProgress(ByVal sender As Object, ByVal e As AcquiredImageProcessingProgressEventArgs)
        imageAcquisitionProgressBar.Value = CInt(e.Progress)
        If imageAcquisitionProgressBar.Value = 100 Then
            imageAcquisitionProgressBar.Value = 0
        End If
    End Sub

#End Region


#Region "Save"

    ''' <summary>
    ''' Saves acquired image.
    ''' </summary>
    Private Sub saveImageButton_Click(ByVal sender As Object, ByVal e As RoutedEventArgs)
        _saveFileDialog1.FileName = ""
        If _saveFileDialog1.ShowDialog() = True Then
            Dim isFileExist As Boolean = File.Exists(_saveFileDialog1.FileName)
            Dim saveAllImages As Boolean = False
            Try
                Dim encoderSettings As TwainImageEncoderSettings = Nothing

                Select Case _saveFileDialog1.FilterIndex
                    Case 3
                        ' JPEG
                        Dim jpegSettingsDlg As New JpegSaveSettingsWindow(Me)
                        If Not CBool(jpegSettingsDlg.ShowDialog()) Then
                            Return
                        End If

                        encoderSettings = New TwainJpegEncoderSettings()
                        DirectCast(encoderSettings, TwainJpegEncoderSettings).JpegQuality = jpegSettingsDlg.Quality
                        Exit Select

                    Case 5
                        ' TIFF
                        Dim tiffSettingsDlg As New TiffSaveSettingsWindow(Me, isFileExist)
                        If Not CBool(tiffSettingsDlg.ShowDialog()) Then
                            Return
                        End If

                        saveAllImages = tiffSettingsDlg.SaveAllImages
                        encoderSettings = New TwainTiffEncoderSettings()
                        DirectCast(encoderSettings, TwainTiffEncoderSettings).TiffMultiPage = tiffSettingsDlg.MultiPage
                        DirectCast(encoderSettings, TwainTiffEncoderSettings).TiffCompression = tiffSettingsDlg.Compression
                        DirectCast(encoderSettings, TwainTiffEncoderSettings).JpegQuality = tiffSettingsDlg.JpegQuality
                        Exit Select

                    Case 6
                        ' PDF
                        Dim pdfSettingsDlg As New PdfSaveSettingsWindow(Me, isFileExist)
                        If Not CBool(pdfSettingsDlg.ShowDialog()) Then
                            Return
                        End If

                        saveAllImages = pdfSettingsDlg.SaveAllImages
                        encoderSettings = New TwainPdfEncoderSettings()
                        DirectCast(encoderSettings, TwainPdfEncoderSettings).PdfMultiPage = pdfSettingsDlg.MultiPage
                        DirectCast(encoderSettings, TwainPdfEncoderSettings).PdfImageCompression = pdfSettingsDlg.Compression
                        DirectCast(encoderSettings, TwainPdfEncoderSettings).PdfACompatible = pdfSettingsDlg.PdfACompatible
                        DirectCast(encoderSettings, TwainPdfEncoderSettings).PdfDocumentInfo.Author = pdfSettingsDlg.PdfAuthor
                        DirectCast(encoderSettings, TwainPdfEncoderSettings).PdfDocumentInfo.Title = pdfSettingsDlg.PdfTitle
                        DirectCast(encoderSettings, TwainPdfEncoderSettings).JpegQuality = pdfSettingsDlg.JpegQuality
                        Exit Select
                End Select

                Cursor = Cursors.Wait

                Dim filename As String = _saveFileDialog1.FileName
                ' save all images to specified file
                If saveAllImages Then
                    ' save first image
                    _images(0).Save(filename, encoderSettings)

                    ' enable multipage support if necessary
                    If _saveFileDialog1.FilterIndex = 5 Then
                        DirectCast(encoderSettings, TwainTiffEncoderSettings).TiffMultiPage = True
                    ElseIf _saveFileDialog1.FilterIndex = 6 Then
                        DirectCast(encoderSettings, TwainPdfEncoderSettings).PdfMultiPage = True
                    End If

                    ' save second and next images
                    For i As Integer = 1 To _images.Count - 1
                        _images(i).Save(filename, encoderSettings)
                    Next
                Else
                    ' save only current image to specified file
                    _images(_imageIndex).Save(filename, encoderSettings)
                End If

                Cursor = Cursors.Arrow

                MessageBox.Show("Image(s) saved successfully!")
            Catch ex As Exception
                Cursor = Cursors.Arrow
                MessageBox.Show(ex.Message, "Saving error")
            End Try
        End If
    End Sub

#End Region


#Region "Upload"

    ''' <summary>
    ''' Uploads acquired image.
    ''' </summary>
    Private Sub uploadImageButton_Click(ByVal sender As Object, ByVal e As RoutedEventArgs)
        Dim uploadWindow As New UploadWindow(Me, _images(_imageIndex))
        uploadWindow.ShowDialog()
    End Sub

#End Region


#Region "Delete, clear"

    ''' <summary>
    ''' Removes image from collection of acquired images
    ''' </summary>
    Private Sub deleteImageButton_Click(ByVal sender As Object, ByVal e As RoutedEventArgs)
        ' dispose the image
        _images(_imageIndex).Dispose()

        ' remove image from image collection
        _images.RemoveAt(_imageIndex)

        If _imageIndex >= (_images.Count - 1) Then
            _imageIndex = _images.Count - 1
        End If

        SetCurrentImage(_imageIndex)
    End Sub

    ''' <summary>
    ''' Clears acquired image collection.
    ''' </summary>
    Private Sub clearImagesButton_Click(ByVal sender As Object, ByVal e As RoutedEventArgs)
        ' dispose all images from image collection and clear the image collection
        _images.ClearAndDisposeItems()

        _imageIndex = -1

        SetCurrentImage(_imageIndex)
    End Sub

#End Region

#End Region


    ''' <summary>
    ''' Returns country and language for TWAIN device manager.
    ''' </summary>
    ''' <remarks>
    ''' Unfortunately only KODAK scanners allow to set country and language.
    ''' </remarks>
    Private Sub GetCountryAndLanguage(ByRef country As CountryCode, ByRef language As LanguageType)
        country = CountryCode.Usa
        language = LanguageType.EnglishUsa

        Select Case CultureInfo.CurrentUICulture.Parent.IetfLanguageTag
            Case "de"
                country = CountryCode.Germany
                language = LanguageType.German

            Case "es"
                country = CountryCode.Spain
                language = LanguageType.Spanish

            Case "fr"
                country = CountryCode.France
                language = LanguageType.French

            Case "it"
                country = CountryCode.Italy
                language = LanguageType.Italian

            Case "pt"
                country = CountryCode.Portugal
                language = LanguageType.Portuguese

            Case "ru"
                country = CountryCode.Russia
                language = LanguageType.Russian
        End Select
    End Sub


    ''' <summary>
    ''' Updates UI.
    ''' </summary>
    Private Sub UpdateUI()
        Dim isDeviceManagerOpened As Boolean = _deviceManager.State = DeviceManagerState.Opened
        Dim hasDevices As Boolean = False
        If isDeviceManagerOpened Then
            If _deviceManager.Devices.Count > 0 Then
                hasDevices = True
            End If
        End If

        openDeviceManagerButton.IsEnabled = Not _isImageAcquiring
        selectDeviceButton.IsEnabled = isDeviceManagerOpened AndAlso Not _isImageAcquiring

        acquireImageButton.IsEnabled = isDeviceManagerOpened AndAlso hasDevices AndAlso Not _isImageAcquiring

        devicesComboBox.IsEnabled = isDeviceManagerOpened AndAlso Not _isImageAcquiring
        getDeviceInfoButton.IsEnabled = isDeviceManagerOpened AndAlso hasDevices AndAlso Not _isImageAcquiring

        imageGroupBox.IsEnabled = isDeviceManagerOpened AndAlso hasDevices AndAlso Not _isImageAcquiring
        userInterfaceGroupBox.IsEnabled = isDeviceManagerOpened AndAlso hasDevices AndAlso Not _isImageAcquiring
        adfGroupBox.IsEnabled = isDeviceManagerOpened AndAlso hasDevices AndAlso Not _isImageAcquiring


        ' image navigation/processing

        If _imageIndex > 0 Then
            previousImageButton.IsEnabled = True
        Else
            previousImageButton.IsEnabled = False
        End If

        If _imageIndex < (_images.Count - 1) Then
            nextImageButton.IsEnabled = True
        Else
            nextImageButton.IsEnabled = False
        End If

        processImageButton.IsEnabled = _images.Count > 0
        saveImageButton.IsEnabled = _images.Count > 0
        uploadImageButton.IsEnabled = _images.Count > 0
        deleteImageButton.IsEnabled = _images.Count > 0
        clearImagesButton.IsEnabled = _images.Count > 0

        stretchImageCheckBox.IsEnabled = _images.Count > 0
    End Sub

    ''' <summary>
    ''' Application window is closing.
    ''' </summary>
    Private Sub MainWindow_Closing(ByVal sender As Object, ByVal e As CancelEventArgs)
        If Not _currentDevice Is Nothing Then
            ' if image is acquiring
            If _currentDevice.State > DeviceState.Enabled Then
                ' cancel image acquisition
                _currentDevice.CancelTransfer()
                ' specify that form must be closed when image acquisition is canceled
                _cancelTransferBecauseWindowIsClosing = True
                ' cancel form closing
                e.Cancel = True
                Return
            End If

            ' unsubscribe from device events
            UnsubscribeFromDeviceEvents(_currentDevice)
            ' close the device
            _currentDevice.Close()
            _currentDevice = Nothing
        End If

        ' close the device manager
        _deviceManager.Close()
        ' dispose the device manager
        _deviceManager.Dispose()

        ' dispose all images from image collection and clear the image collection
        _images.ClearAndDisposeItems()
    End Sub

#End Region

End Class
