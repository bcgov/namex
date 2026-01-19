Imports System.Diagnostics
Imports System.Drawing
Imports System.Globalization
Imports System.IO
Imports System.Windows.Forms
Imports Vintasoft.Twain
Imports Vintasoft.Twain.ImageEncoders

Partial Public Class MainForm
    Inherits Form

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
    ''' Determines that image acquistion must be canceled because application's form is closing.
    ''' </summary>
    Private _cancelTransferBecauseFormIsClosing As Boolean

#End Region



#Region "Constructors"

    Public Sub New()
        InitializeComponent()

        Me.Text = String.Format("VintaSoft TWAIN Advanced Demo v{0}", TwainGlobalSettings.ProductVersion)

        transferModeComboBox.SelectedIndex = 1
        pixelTypeComboBox.SelectedIndex = 1
        resolutionComboBox.SelectedIndex = 1

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
    ''' Opens the TWAIN device manager.
    ''' </summary>
    Private Sub openDeviceManagerButton_Click(ByVal sender As Object, ByVal e As EventArgs) Handles openDeviceManagerButton.Click
        ' clear list of devices
        devicesComboBox.Items.Clear()

        ' if device manager is open - close the device manager
        If _deviceManager.State = DeviceManagerState.Opened Then
            ' close the device manager
            _deviceManager.Close()

            ' change text on this button
            openDeviceManagerButton.Text = "Open device manager"
        Else

            ' if device manager is closed - open the device manager
            ' try to find the device manager specified by user
            _deviceManager.IsTwain2Compatible = twain2CompatibleCheckBox.Checked
            ' if device manager is not found
            If Not _deviceManager.IsTwainAvailable Then
                ' try to find another device manager
                _deviceManager.IsTwain2Compatible = Not _deviceManager.IsTwain2Compatible
                ' if device manager is not found again
                If Not _deviceManager.IsTwainAvailable Then
                    ' show dialog with error message
                    MessageBox.Show("TWAIN device manager is not found.", "TWAIN device manager", MessageBoxButtons.OK, MessageBoxIcon.[Error])

                    ' open a HTML page with article describing how to solve the problem
                    Process.Start("http://www.vintasoft.com/docs/vstwain-dotnet/index.html?Programming-Twain-Device_Manager.html")

                    Return
                End If
            End If

            ' device manager is found

            ' if check box value should be updated
            If twain2CompatibleCheckBox.Checked <> _deviceManager.IsTwain2Compatible Then
                ' update check box value 
                twain2CompatibleCheckBox.Checked = _deviceManager.IsTwain2Compatible
            End If

            Try
                ' open the device manager
                _deviceManager.Open()
            Catch ex As TwainDeviceManagerException
                ' close the device manager
                _deviceManager.Close()

                ' show dialog with error message
                MessageBox.Show(ex.Message, "TWAIN device manager", MessageBoxButtons.OK, MessageBoxIcon.[Error])

                ' open a HTML page with article describing how to solve the problem
                Process.Start("http://www.vintasoft.com/docs/vstwain-dotnet/index.html?Programming-Twain-Device_Manager.html")

                Return
            End Try

            ' for each available device
            Dim devices As DeviceCollection = _deviceManager.Devices
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
            openDeviceManagerButton.Text = "Close device manager"
        End If

        UpdateUI()
    End Sub

#End Region


#Region "Devices"

    ''' <summary>
    ''' Selects the default device.
    ''' </summary>
    Private Sub selectDefaultDeviceButton_Click(ByVal sender As Object, ByVal e As EventArgs) Handles selectDefaultDeviceButton.Click
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
    Private Sub getDeviceInfoButton_Click(ByVal sender As Object, ByVal e As EventArgs) Handles getDeviceInfoButton.Click
        Try
            ' find a device by device name
            Dim device As Device = _deviceManager.Devices.Find(DirectCast(devicesComboBox.SelectedItem, String))

            ' show dialog with information about device and device capabilities
            Dim deviceCapabilitiesForm As New DevCapsForm(device)
            deviceCapabilitiesForm.ShowDialog()
        Catch ex As TwainDeviceException
            MessageBox.Show(ex.Message, "Device error", MessageBoxButtons.OK, MessageBoxIcon.[Error])
        Catch ex As TwainDeviceCapabilityException
            MessageBox.Show(ex.Message, "Device capability error", MessageBoxButtons.OK, MessageBoxIcon.[Error])
        End Try
    End Sub

    ''' <summary>
    ''' Enables/disables User Interface of device.
    ''' </summary>
    Private Sub showUICheckBox_CheckedChanged(ByVal sender As Object, ByVal e As EventArgs) Handles showUICheckBox.CheckedChanged
        modalUICheckBox.Enabled = showUICheckBox.Checked
        disableAfterScanCheckBox.Enabled = showUICheckBox.Checked

        adfGroupBox.Enabled = Not showUICheckBox.Checked
    End Sub

    ''' <summary>
    ''' Transfer mode is changed.
    ''' </summary>
    Private Sub transferModeComboBox_SelectedIndexChanged(ByVal sender As Object, ByVal e As EventArgs) Handles transferModeComboBox.SelectedIndexChanged
        If transferModeComboBox.SelectedIndex = 0 Then
            imageAcquisitionProgressBar.Visible = False
        Else
            imageAcquisitionProgressBar.Visible = True
        End If
    End Sub

    ''' <summary>
    ''' Enables/disables the automatic document feeder.
    ''' </summary>
    Private Sub useAdfCheckBox_CheckedChanged(ByVal sender As Object, ByVal e As EventArgs) Handles useAdfCheckBox.CheckedChanged
        useDuplexCheckBox.Enabled = useAdfCheckBox.Checked
        imagesToAcquireNumericUpDown.Enabled = useAdfCheckBox.Checked
    End Sub

#End Region


#Region "Image acquisition"

    ''' <summary>
    ''' Starts the image acquisition.
    ''' </summary>
    Private Sub acquireImageButton_Click(ByVal sender As Object, ByVal e As EventArgs) Handles acquireImageButton.Click
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

                MessageBox.Show(String.Format("Device '{0}' is not found.", deviceName), "TWAIN device", MessageBoxButtons.OK, MessageBoxIcon.[Error])
                Return
            End If

            _currentDevice = device
            ' subscribe to the device events
            SubscribeToDeviceEvents(_currentDevice)

            ' set the image acquisition parameters
            device.ShowUI = showUICheckBox.Checked
            device.ModalUI = modalUICheckBox.Checked
            device.ShowIndicators = showIndicatorsCheckBox.Checked
            device.DisableAfterAcquire = disableAfterScanCheckBox.Checked

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

                MessageBox.Show(ex.Message, "TWAIN device", MessageBoxButtons.OK, MessageBoxIcon.[Error])
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
                MessageBox.Show(String.Format("Pixel type '{0}' is not supported.", pixelType__1), "TWAIN device")
            End Try

            ' unit of measure
            Try
                If device.UnitOfMeasure <> UnitOfMeasure.Inches Then
                    device.UnitOfMeasure = UnitOfMeasure.Inches
                End If
            Catch generatedExceptionName As TwainException
                MessageBox.Show("Unit of measure 'Inches' is not supported.", "TWAIN device")
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
                        If device.DocumentFeeder.Enabled <> useAdfCheckBox.Checked Then
                            device.DocumentFeeder.Enabled = useAdfCheckBox.Checked
                        End If
                    Catch generatedExceptionName As TwainDeviceCapabilityException
                    End Try

                    ' enable/disable duplex if necessary
                    Try
                        If device.DocumentFeeder.DuplexEnabled <> useDuplexCheckBox.Checked Then
                            device.DocumentFeeder.DuplexEnabled = useDuplexCheckBox.Checked
                        End If
                    Catch generatedExceptionName As TwainDeviceCapabilityException
                    End Try
                End If

                If Not acquireAllImagesRadioButton.Checked Then
                    device.XferCount = CType(Math.Truncate(imagesToAcquireNumericUpDown.Value), Int16)
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

                MessageBox.Show(ex.Message, "TWAIN device", MessageBoxButtons.OK, MessageBoxIcon.[Error])
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
        AddHandler device.ImageAcquiringProgress, New EventHandler(Of ImageAcquiringProgressEventArgs)(AddressOf device_ImageAcquiringProgress)
        AddHandler device.ImageAcquired, New EventHandler(Of ImageAcquiredEventArgs)(AddressOf device_ImageAcquired)
        AddHandler device.ScanFailed, New EventHandler(Of ScanFailedEventArgs)(AddressOf device_ScanFailed)
        AddHandler device.AsyncEvent, New EventHandler(Of DeviceAsyncEventArgs)(AddressOf device_AsyncEvent)
        AddHandler device.ScanFinished, New EventHandler(AddressOf device_ScanFinished)
    End Sub

    ''' <summary>
    ''' Unsubscribe from the device events.
    ''' </summary>
    Private Sub UnsubscribeFromDeviceEvents(ByVal device As Device)
        RemoveHandler device.ImageAcquiringProgress, New EventHandler(Of ImageAcquiringProgressEventArgs)(AddressOf device_ImageAcquiringProgress)
        RemoveHandler device.ImageAcquired, New EventHandler(Of ImageAcquiredEventArgs)(AddressOf device_ImageAcquired)
        RemoveHandler device.ScanFailed, New EventHandler(Of ScanFailedEventArgs)(AddressOf device_ScanFailed)
        RemoveHandler device.AsyncEvent, New EventHandler(Of DeviceAsyncEventArgs)(AddressOf device_AsyncEvent)
        RemoveHandler device.ScanFinished, New EventHandler(AddressOf device_ScanFinished)
    End Sub

    ''' <summary>
    ''' Image acquiring progress is changed.
    ''' </summary>
    Private Sub device_ImageAcquiringProgress(ByVal sender As Object, ByVal e As ImageAcquiringProgressEventArgs)
        ' image acquistion must be canceled because application's form is closing
        If _cancelTransferBecauseFormIsClosing Then
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
    Private Sub device_ImageAcquired(ByVal sender As Object, ByVal e As ImageAcquiredEventArgs)
        ' image acquistion must be canceled because application's form is closing
        If _cancelTransferBecauseFormIsClosing Then
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
    Private Sub device_ScanFailed(ByVal sender As Object, ByVal e As ScanFailedEventArgs)
        ' show error message
        MessageBox.Show(e.ErrorString, "Scan is failed", MessageBoxButtons.OK, MessageBoxIcon.[Error])
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

#Region "Navigate"

    ''' <summary>
    ''' Shows previous acquired image.
    ''' </summary>
    Private Sub previousImageButton_Click(ByVal sender As Object, ByVal e As EventArgs) Handles previousImageButton.Click
        SetCurrentImage(_imageIndex - 1)

        UpdateUI()
    End Sub

    ''' <summary>
    ''' Shows next acquired image.
    ''' </summary>
    Private Sub nextImageButton_Click(ByVal sender As Object, ByVal e As EventArgs) Handles nextImageButton.Click
        SetCurrentImage(_imageIndex + 1)

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
            If pictureBox1.Image IsNot Nothing Then
                pictureBox1.Image.Dispose()
                pictureBox1.Image = Nothing
            End If

            ' get the image from the internal buffer of the device if image is present
            If index >= 0 Then
                Dim acquiredImage As AcquiredImage = _images(index)

                pictureBox1.Image = acquiredImage.GetAsBitmap(True)
                SetImageScrolls()

                imageInfoLabel.Text = GetCurrentImageInfo(index, acquiredImage)

                _imageIndex = index
            Else
                ' show "No images" text
                imageInfoLabel.Text = "No images"

                _imageIndex = -1
            End If

            '
            UpdateUI()
        End SyncLock
    End Sub

    ''' <summary>
    ''' Sets image scrolls.
    ''' </summary>
    Private Sub SetImageScrolls()
        If stretchImageCheckBox.Checked Then
            pictureBox1.Size = New Size(pictureBoxPanel.Size.Width - 2, pictureBoxPanel.Size.Height - 2)
            pictureBox1.SizeMode = PictureBoxSizeMode.StretchImage
        Else
            pictureBox1.Size = New Size(pictureBox1.Image.Width, pictureBox1.Image.Height)
            pictureBox1.SizeMode = PictureBoxSizeMode.AutoSize
        End If
    End Sub

    ''' <summary>
    ''' Changes preview mode of current image.
    ''' </summary>
    Private Sub stretchImageCheckBox_CheckedChanged(ByVal sender As Object, ByVal e As EventArgs) Handles stretchImageCheckBox.CheckedChanged
        SetImageScrolls()
    End Sub

    ''' <summary>
    ''' Form of application is resized.
    ''' </summary>
    Private Sub MainForm_Resize(ByVal sender As Object, ByVal e As EventArgs) Handles MyBase.Resize
        SetImageScrolls()
    End Sub

#End Region


#Region "Process"

    ''' <summary>
    ''' Processes acquired image.
    ''' </summary>
    Private Sub rotateImageButton_Click(ByVal sender As Object, ByVal e As EventArgs) Handles processImageButton.Click
        ' get reference to current image
        Dim currentImage As AcquiredImage = _images(_imageIndex)

        ' process current image
        Dim form1 As New ImageProcessingForm(currentImage)
        form1.ShowDialog()

        ' update current image
        SetCurrentImage(_imageIndex)
    End Sub

#End Region


#Region "Save"

    ''' <summary>
    ''' Saves acquired image.
    ''' </summary>
    Private Sub saveImageButton_Click(ByVal sender As Object, ByVal e As EventArgs) Handles saveImageButton.Click
        saveFileDialog1.FileName = ""
        If saveFileDialog1.ShowDialog() <> DialogResult.OK Then
            Return
        End If

        Dim isFileExist As Boolean = File.Exists(saveFileDialog1.FileName)
        Dim saveAllImages As Boolean = False
        Try
            Dim encoderSettings As TwainImageEncoderSettings = Nothing

            Select Case saveFileDialog1.FilterIndex
                Case 3
                    ' JPEG
                    Dim jpegSettingsDlg As New JpegSaveSettingsForm()
                    If jpegSettingsDlg.ShowDialog() <> DialogResult.OK Then
                        Return
                    End If

                    encoderSettings = New TwainJpegEncoderSettings()
                    DirectCast(encoderSettings, TwainJpegEncoderSettings).JpegQuality = jpegSettingsDlg.Quality
                    Exit Select

                Case 5
                    ' TIFF
                    Dim tiffSettingsDlg As New TiffSaveSettingsForm(isFileExist)
                    If tiffSettingsDlg.ShowDialog() <> DialogResult.OK Then
                        Return
                    End If

                    saveAllImages = tiffSettingsDlg.SaveAllImages
                    encoderSettings = New TwainTiffEncoderSettings()
                    Dim twainTiffEncoderSettings As TwainTiffEncoderSettings = DirectCast(encoderSettings, TwainTiffEncoderSettings)
                    twainTiffEncoderSettings.TiffMultiPage = tiffSettingsDlg.MultiPage
                    twainTiffEncoderSettings.TiffCompression = tiffSettingsDlg.Compression
                    twainTiffEncoderSettings.JpegQuality = tiffSettingsDlg.JpegQuality
                    Exit Select

                Case 6
                    ' PDF
                    Dim pdfSettingsDlg As New PdfSaveSettingsForm(isFileExist)
                    If pdfSettingsDlg.ShowDialog() <> DialogResult.OK Then
                        Return
                    End If

                    saveAllImages = pdfSettingsDlg.SaveAllImages
                    encoderSettings = New TwainPdfEncoderSettings()
                    Dim twainPdfEncoderSettings As TwainPdfEncoderSettings = DirectCast(encoderSettings, TwainPdfEncoderSettings)
                    twainPdfEncoderSettings.PdfMultiPage = pdfSettingsDlg.MultiPage
                    twainPdfEncoderSettings.PdfImageCompression = pdfSettingsDlg.Compression
                    twainPdfEncoderSettings.PdfACompatible = pdfSettingsDlg.PdfACompatible
                    twainPdfEncoderSettings.PdfDocumentInfo.Author = pdfSettingsDlg.PdfAuthor
                    twainPdfEncoderSettings.PdfDocumentInfo.Title = pdfSettingsDlg.PdfTitle
                    twainPdfEncoderSettings.JpegQuality = pdfSettingsDlg.JpegQuality
                    Exit Select
            End Select

            Cursor = Cursors.WaitCursor

            Dim filename As String = saveFileDialog1.FileName
            ' save all images to specified file
            If saveAllImages Then
                ' save first image
                _images(0).Save(filename, encoderSettings)

                ' enable multipage support if necessary
                If saveFileDialog1.FilterIndex = 5 Then
                    DirectCast(encoderSettings, TwainTiffEncoderSettings).TiffMultiPage = True
                ElseIf saveFileDialog1.FilterIndex = 6 Then
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

            Cursor = Cursors.[Default]

            MessageBox.Show("Image(s) saved successfully!")
        Catch ex As Exception
            Cursor = Cursors.[Default]
            MessageBox.Show(ex.Message, "Saving error")
        End Try
    End Sub

#End Region


#Region "Upload"

    ''' <summary>
    ''' Uploads acquired image.
    ''' </summary>
    Private Sub uploadImageButton_Click(ByVal sender As Object, ByVal e As EventArgs) Handles uploadImageButton.Click
        Dim uploadForm As New UploadForm(_images(_imageIndex))
        uploadForm.ShowDialog()
    End Sub

#End Region


#Region "Delete, clear"

    ''' <summary>
    ''' Removes image from acquired image collection.
    ''' </summary>
    Private Sub deleteImageButton_Click(ByVal sender As Object, ByVal e As EventArgs) Handles deleteImageButton.Click
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
    Private Sub clearImagesButton_Click(ByVal sender As Object, ByVal e As EventArgs) Handles clearImagesButton.Click
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
    ''' Update UI.
    ''' </summary>
    Private Sub UpdateUI()
        Dim isDeviceManagerOpened As Boolean = _deviceManager.State = DeviceManagerState.Opened
        Dim hasDevices As Boolean = False
        If isDeviceManagerOpened Then
            If _deviceManager.Devices.Count > 0 Then
                hasDevices = True
            End If
        End If

        openDeviceManagerButton.Enabled = Not _isImageAcquiring
        selectDefaultDeviceButton.Enabled = isDeviceManagerOpened AndAlso Not _isImageAcquiring

        acquireImageButton.Enabled = isDeviceManagerOpened AndAlso hasDevices AndAlso Not _isImageAcquiring

        devicesComboBox.Enabled = isDeviceManagerOpened AndAlso Not _isImageAcquiring
        getDeviceInfoButton.Enabled = isDeviceManagerOpened AndAlso hasDevices AndAlso Not _isImageAcquiring

        imageGroupBox.Enabled = isDeviceManagerOpened AndAlso hasDevices AndAlso Not _isImageAcquiring
        userInterfaceGroupBox.Enabled = isDeviceManagerOpened AndAlso hasDevices AndAlso Not _isImageAcquiring
        adfGroupBox.Enabled = isDeviceManagerOpened AndAlso hasDevices AndAlso Not _isImageAcquiring


        ' image navigation/processing

        If _imageIndex > 0 Then
            previousImageButton.Enabled = True
        Else
            previousImageButton.Enabled = False
        End If

        If _imageIndex < (_images.Count - 1) Then
            nextImageButton.Enabled = True
        Else
            nextImageButton.Enabled = False
        End If

        processImageButton.Enabled = _images.Count > 0
        saveImageButton.Enabled = _images.Count > 0
        uploadImageButton.Enabled = _images.Count > 0
        deleteImageButton.Enabled = _images.Count > 0
        clearImagesButton.Enabled = _images.Count > 0

        stretchImageCheckBox.Enabled = _images.Count > 0
    End Sub

    ''' <summary>
    ''' Application's form is closing.
    ''' </summary>
    Private Sub MainForm_FormClosing(ByVal sender As Object, ByVal e As FormClosingEventArgs) Handles MyBase.FormClosing
        If Not _currentDevice Is Nothing Then

            ' if image is acquiring
            If _currentDevice.State > DeviceState.Enabled Then
                ' cancel image acquisition
                _currentDevice.CancelTransfer()
                ' specify that form must be closed when image acquisition is canceled
                _cancelTransferBecauseFormIsClosing = True
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
