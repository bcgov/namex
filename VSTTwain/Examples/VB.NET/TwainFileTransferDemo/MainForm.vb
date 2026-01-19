Imports System.IO
Imports System.Windows.Forms
Imports Vintasoft.Twain

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
    ''' Path to directory where acquired images will be saved.
    ''' </summary>
    Private _directoryForImages As String
    ''' <summary>
    ''' Index of acquired image.
    ''' </summary>
    Private _imageIndex As Integer

#End Region



#Region "Constructors"

    Public Sub New()
        InitializeComponent()

        Me.Text = String.Format("VintaSoft TWAIN File Transfer Demo v{0}", TwainGlobalSettings.ProductVersion)

        ' create instance of the DeviceManager class
        _deviceManager = New DeviceManager(Me)
    End Sub

#End Region



#Region "Methods"

    ''' <summary>
    ''' Application form is shown.
    ''' </summary>
    Private Sub MainForm_Shown(ByVal sender As Object, ByVal e As EventArgs)
        ' get path to directory where acquired images will be saved

        _directoryForImages = Path.GetDirectoryName(Application.ExecutablePath)
        _directoryForImages = Path.Combine(_directoryForImages, "Images")
        If Not Directory.Exists(_directoryForImages) Then
            Directory.CreateDirectory(_directoryForImages)
        End If

        directoryForImagesTextBox.Text = _directoryForImages

        ' open TWAIN device manager
        If OpenDeviceManager() Then
            ' fill the device list

            devicesComboBox.Items.Clear()
            Dim devices As DeviceCollection = _deviceManager.Devices
            Dim deviceInfo As DeviceInfo
            For i As Integer = 0 To devices.Count - 1
                deviceInfo = devices(i).Info
                devicesComboBox.Items.Add(deviceInfo.ProductName)

                If devices(i) Is _deviceManager.DefaultDevice Then
                    devicesComboBox.SelectedIndex = i
                End If
            Next
        End If
    End Sub


    ''' <summary>
    ''' Sets form's UI state.
    ''' </summary>
    Private Sub SetFormUiState(ByVal enabled As Boolean)
        devicesComboBox.Enabled = enabled
        deviceSettingsGroupBox.Enabled = enabled
        acquireImageWithUIButton.Enabled = enabled
        acquireImageWithUIButton.Enabled = enabled
        acquireImageWithoutUIButton.Enabled = enabled
    End Sub


    ''' <summary>
    ''' Opens TWAIN device manager.
    ''' </summary>
    Private Function OpenDeviceManager() As Boolean
        SetFormUiState(False)

        ' try to find the device manager 2.x
        _deviceManager.IsTwain2Compatible = True
        ' if TWAIN device manager 2.x is NOT available
        If Not _deviceManager.IsTwainAvailable Then
            ' try to find the device manager 1.x
            _deviceManager.IsTwain2Compatible = True
            ' if TWAIN device manager 1.x is NOT available
            If Not _deviceManager.IsTwainAvailable Then
                MessageBox.Show("TWAIN device manager is not found.")
                Return False
            End If
        End If

        ' open the device manager
        _deviceManager.Open()

        ' if no devices are found in the system
        If _deviceManager.Devices.Count = 0 Then
            MessageBox.Show("No devices found.")
            Return False
        End If

        SetFormUiState(True)
        Return True
    End Function


    ''' <summary>
    ''' Selects directory for acquired images.
    ''' </summary>
    Private Sub selectDirectoryForImagesButton_Click(ByVal sender As Object, ByVal e As EventArgs)
        folderBrowserDialog1.SelectedPath = _directoryForImages
        If folderBrowserDialog1.ShowDialog() <> DialogResult.OK Then
            Return
        End If

        _directoryForImages = folderBrowserDialog1.SelectedPath
        directoryForImagesTextBox.Text = _directoryForImages
    End Sub

    ''' <summary>
    ''' Current device is changed.
    ''' </summary>
    Private Sub devicesComboBox_SelectedIndexChanged(ByVal sender As Object, ByVal e As EventArgs)
        SetFormUiState(False)

        ' get device
        Dim device As Device = _deviceManager.Devices.Find(DirectCast(devicesComboBox.SelectedItem, String))

        ' get file formats and compressions supported by device
        GetSupportedFileFormatsAndCompressions(device)

        SetFormUiState(True)
    End Sub

    ''' <summary>
    ''' Gets file formats and compressions supported by device in File Transfer mode.
    ''' </summary>
    Private Sub GetSupportedFileFormatsAndCompressions(ByVal device As Device)
        ' open the device
        device.Open()

        Try
            ' get supported file formats

            Dim currentFileFormat As TwainImageFileFormat = device.FileFormat
            Dim fileFormats As TwainImageFileFormat() = device.GetSupportedImageFileFormats()

            supportedFileFormatsComboBox.Items.Clear()
            For i As Integer = 0 To fileFormats.Length - 1
                supportedFileFormatsComboBox.Items.Add(fileFormats(i))

                If currentFileFormat = fileFormats(i) Then
                    supportedFileFormatsComboBox.SelectedIndex = i
                End If
            Next

            ' get supported compressions

            Dim currentCompression As TwainImageCompression = device.ImageCompression
            Dim compressions As TwainImageCompression() = device.GetSupportedImageCompressions()

            supportedCompressionsComboBox.Items.Clear()
            For i As Integer = 0 To compressions.Length - 1
                supportedCompressionsComboBox.Items.Add(compressions(i))

                If currentCompression = compressions(i) Then
                    supportedCompressionsComboBox.SelectedIndex = i
                End If
            Next
        Catch ex As Exception
            MessageBox.Show(ex.Message)
        Finally
            ' close the device
            device.Close()
        End Try

    End Sub


    ''' <summary>
    ''' Acquires image with UI.
    ''' </summary>
    Private Sub acquireImageWithUIButton_Click(ByVal sender As Object, ByVal e As EventArgs)
        AcquireImage(True)
    End Sub

    ''' <summary>
    ''' Acquires image without UI.
    ''' </summary>
    Private Sub acquireImageWithoutUIButton_Click(ByVal sender As Object, ByVal e As EventArgs)
        AcquireImage(False)
    End Sub

    ''' <summary>
    ''' Acquires image.
    ''' </summary>
    Private Sub AcquireImage(ByVal showUI As Boolean)
        SetFormUiState(False)

        If _currentDevice IsNot Nothing Then
            UnsubscribeFromDeviceEvents()
        End If

        Dim device As Device = _deviceManager.Devices.Find(DirectCast(devicesComboBox.SelectedItem, String))

        _currentDevice = device
        ' subscribe to the device events
        SubscribeToDeviceEvents()

        Try
            ' set settings of scan session
            device.TransferMode = TransferMode.File
            device.ShowUI = showUI
            device.DisableAfterAcquire = Not showUI

            ' open the device
            device.Open()

            Try
                ' set the file format in which acquired images must be saved
                Dim newFileFormat As TwainImageFileFormat = TwainImageFileFormat.Bmp
                If supportedFileFormatsComboBox.Items.Count > 0 Then
                    device.FileFormat = DirectCast(supportedFileFormatsComboBox.SelectedItem, TwainImageFileFormat)
                End If
                If device.FileFormat <> newFileFormat Then
                    device.FileFormat = newFileFormat
                End If
            Catch ex As Exception

            End Try

            ' start the asynchronous image acquisition process
            device.Acquire()
        Catch ex As TwainDeviceException
            ' close the device
            _currentDevice.Close()
            MessageBox.Show(ex.Message)
            SetFormUiState(True)
            Return
        End Try
    End Sub

    ''' <summary>
    ''' Subscribes to the device events.
    ''' </summary>
    Private Sub SubscribeToDeviceEvents()
        AddHandler _currentDevice.ImageAcquiring, New EventHandler(Of ImageAcquiringEventArgs)(AddressOf device_ImageAcquiring)
        AddHandler _currentDevice.ImageAcquired, New EventHandler(Of ImageAcquiredEventArgs)(AddressOf device_ImageAcquired)
        AddHandler _currentDevice.ScanCompleted, New EventHandler(AddressOf device_ScanCompleted)
        AddHandler _currentDevice.ScanCanceled, New EventHandler(AddressOf device_ScanCanceled)
        AddHandler _currentDevice.UserInterfaceClosed, New EventHandler(AddressOf device_UserInterfaceClosed)
        AddHandler _currentDevice.ScanFailed, New EventHandler(Of ScanFailedEventArgs)(AddressOf device_ScanFailed)
        AddHandler _currentDevice.ScanFinished, New EventHandler(AddressOf device_ScanFinished)
    End Sub

    ''' <summary>
    ''' Unsubscribes from the device events.
    ''' </summary>
    Private Sub UnsubscribeFromDeviceEvents()
        RemoveHandler _currentDevice.ImageAcquiring, New EventHandler(Of ImageAcquiringEventArgs)(AddressOf device_ImageAcquiring)
        RemoveHandler _currentDevice.ImageAcquired, New EventHandler(Of ImageAcquiredEventArgs)(AddressOf device_ImageAcquired)
        RemoveHandler _currentDevice.ScanCompleted, New EventHandler(AddressOf device_ScanCompleted)
        RemoveHandler _currentDevice.ScanCanceled, New EventHandler(AddressOf device_ScanCanceled)
        RemoveHandler _currentDevice.UserInterfaceClosed, New EventHandler(AddressOf device_UserInterfaceClosed)
        RemoveHandler _currentDevice.ScanFailed, New EventHandler(Of ScanFailedEventArgs)(AddressOf device_ScanFailed)
        RemoveHandler _currentDevice.ScanFinished, New EventHandler(AddressOf device_ScanFinished)
    End Sub

    ''' <summary>
    ''' Image is acquiring.
    ''' </summary>
    Private Sub device_ImageAcquiring(ByVal sender As Object, ByVal e As ImageAcquiringEventArgs)
        Dim fileExtension As String = "bmp"
        Select Case e.FileFormat
            Case TwainImageFileFormat.Tiff
                fileExtension = "tif"
                Exit Select

            Case TwainImageFileFormat.Jpeg
                fileExtension = "jpg"
                Exit Select
        End Select

        e.Filename = Path.Combine(_directoryForImages, String.Format("page{0}.{1}", _imageIndex, fileExtension))
    End Sub

    ''' <summary>
    ''' Image is acquired.
    ''' </summary>
    Private Sub device_ImageAcquired(ByVal sender As Object, ByVal e As ImageAcquiredEventArgs)
        statusTextBox.Text += String.Format("Image is saved to file '{0}'{1}", Path.GetFileName(e.Filename), Environment.NewLine)
        _imageIndex += 1
    End Sub

    ''' <summary>
    ''' Scan is completed.
    ''' </summary>
    Private Sub device_ScanCompleted(ByVal sender As Object, ByVal e As EventArgs)
        statusTextBox.Text += String.Format("Scan is completed{0}", Environment.NewLine)
    End Sub

    ''' <summary>
    ''' Scan is canceled.
    ''' </summary>
    Private Sub device_ScanCanceled(ByVal sender As Object, ByVal e As EventArgs)
        statusTextBox.Text += String.Format("Scan is canceled{0}", Environment.NewLine)
    End Sub

    ''' <summary>
    ''' User interface of device is closed.
    ''' </summary>
    Private Sub device_UserInterfaceClosed(ByVal sender As Object, ByVal e As EventArgs)
        statusTextBox.Text += String.Format("User Interface is closed{0}", Environment.NewLine)
    End Sub

    ''' <summary>
    ''' Scan is failed.
    ''' </summary>
    Private Sub device_ScanFailed(ByVal sender As Object, ByVal e As ScanFailedEventArgs)
        statusTextBox.Text += String.Format("Scan is failed: {0}{1}", e.ErrorString, Environment.NewLine)
    End Sub

    ''' <summary>
    ''' Scan is finished.
    ''' </summary>
    Private Sub device_ScanFinished(ByVal sender As Object, ByVal e As EventArgs)
        ' close the device
        _currentDevice.Close()

        statusTextBox.Text += String.Format("Scan is finished{0}", Environment.NewLine)

        SetFormUiState(True)
    End Sub


    ''' <summary>
    ''' Application form is closing.
    ''' </summary>
    Private Sub MainForm_FormClosing(ByVal sender As Object, ByVal e As FormClosingEventArgs)
        If _currentDevice IsNot Nothing Then
            UnsubscribeFromDeviceEvents()
            _currentDevice = Nothing
        End If

        ' close the device manager
        _deviceManager.Close()
        ' dispose the device manager
        _deviceManager.Dispose()
    End Sub

#End Region

End Class
