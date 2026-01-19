Imports System.Drawing
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
    ''' Determines that device is initialized.
    ''' </summary>
    Private _isDeviceInitialized As Boolean

    ''' <summary>
    ''' Current pixel type.
    ''' </summary>
    Private _pixelType As PixelType = PixelType.RGB
    ''' <summary>
    ''' Current unit of measure.
    ''' </summary>
    Private _unitOfMeasure As UnitOfMeasure = UnitOfMeasure.Inches
    ''' <summary>
    ''' Object that controls IAutoRotate capability.
    ''' </summary>
    Private _autoRotateCap As DeviceCapability
    ''' <summary>
    ''' Object that controls IAutoBorderDetection capability.
    ''' </summary>
    Private _autoBorderDetectionCap As DeviceCapability

    Private _isUnitOfMeasureAvailable As Boolean
    Private _isXResolutionAvailable As Boolean
    Private _isYResolutionAvailable As Boolean
    Private _isPageSizeAvailable As Boolean
    Private _isPageOrientationAvailable As Boolean
    Private _isImageLayoutAvailable As Boolean
    Private _isPixelTypeAvailable As Boolean
    Private _isBitDepthAvailable As Boolean
    Private _isThresholdAvailable As Boolean
    Private _isBrightnessAvailable As Boolean
    Private _isContrastAvailable As Boolean
    Private _isImageFilterAvailable As Boolean
    Private _isNoiseFilterAvailable As Boolean
    Private _isAutoRotateAvailable As Boolean
    Private _isAutoBorderDetectionAvailable As Boolean

    ''' <summary>
    ''' Acquired images count.
    ''' </summary>
    Private _imageCount As Integer = 1

    ''' <summary>
    ''' Determines that image acquistion must be canceled because application's form is closing.
    ''' </summary>
    Private _cancelTransferBecauseFormIsClosing As Boolean

#End Region



#Region "Constructor"

    Public Sub New()
        InitializeComponent()

        Me.Text = String.Format("VintaSoft TWAIN Custom UI Demo v{0}", TwainGlobalSettings.ProductVersion)

        _deviceManager = New DeviceManager(Me)
    End Sub

#End Region



#Region "Properties"

    Private _isDeviceChanging As Boolean
    Public Property IsDeviceChanging() As Boolean
        Get
            Return _isDeviceChanging
        End Get
        Set(ByVal value As Boolean)
            If _isDeviceChanging <> Value Then
                _isDeviceChanging = Value

                If Value Then
                    Me.Cursor = Cursors.WaitCursor
                Else
                    Me.Cursor = Cursors.[Default]
                End If

                UpdateUI()
            End If
        End Set
    End Property

    Private _isImageAcquiring As Boolean
    Public Property IsImageAcquiring() As Boolean
        Get
            Return _isImageAcquiring
        End Get
        Set(ByVal value As Boolean)
            If _isImageAcquiring <> Value Then
                _isImageAcquiring = Value
                UpdateUI()
            End If
        End Set
    End Property

#End Region



#Region "Methods"

    ''' <summary>
    ''' Application form is shown.
    ''' </summary>
    Private Sub MainForm_Shown(ByVal sender As Object, ByVal e As EventArgs)
        ' change the application status and update UI
        IsDeviceChanging = True
        ' init devices
        InitDevices()
    End Sub


#Region "Init"

    ''' <summary>
    ''' Opens TWAIN device manager.
    ''' </summary>
    Private Function OpenDeviceManager() As Boolean
        ' try to find the device manager specified by user
        _deviceManager.IsTwain2Compatible = twain2CompatibleCheckBox.Checked
        ' if TWAIN device manager is NOT available
        If Not _deviceManager.IsTwainAvailable Then
            ' try to use another TWAIN device manager
            _deviceManager.IsTwain2Compatible = Not twain2CompatibleCheckBox.Checked
            ' if TWAIN device manager is NOT available
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

        Return True
    End Function

    ''' <summary>
    ''' Inits devices.
    ''' </summary>
    Private Sub InitDevices()
        ' clear a list of devices
        devicesComboBox.Items.Clear()

        ' if TWAIN device manager is opened
        If OpenDeviceManager() Then
            twain2CompatibleCheckBox.Checked = _deviceManager.IsTwain2Compatible

            If _currentDevice IsNot Nothing Then
                UnsubscribeFromDeviceEvents()
            End If

            ' get a reference to the default device
            _currentDevice = _deviceManager.DefaultDevice
            SubscribeToDeviceEvents()

            ' init a list of devices
            Dim devices As DeviceCollection = _deviceManager.Devices
            For i As Integer = 0 To devices.Count - 1
                devicesComboBox.Items.Add(devices(i).Info.ProductName)

                If devices(i) Is _currentDevice Then
                    devicesComboBox.SelectedIndex = i
                End If
            Next

            ' init current device settings
            InitDeviceSettings()
        End If

        ' change the application status and update UI
        IsDeviceChanging = False
    End Sub

    ''' <summary>
    ''' Inits settings of device.
    ''' </summary>
    Private Sub InitDeviceSettings()
        _isDeviceInitialized = False

        If _currentDevice.State <> DeviceState.Opened Then
            Try
                ' open the device
                _currentDevice.Open()
            Catch ex As Exception
                MessageBox.Show(ex.Message)
                Return
            End Try
        End If


        ' get info about device capabilities

        ' unit of measure
        GetUnitOfMeasure()
        ' init resolution settings
        GetResolution()

        ' page size
        GetPageSize()
        ' page orientation
        GetPageOrientation()

        ' init image layout
        GetImageLayout()

        ' pixel type
        GetPixelType()
        ' bit depth
        GetBitDepth()
        ' threshold, contrast and brightness
        GetThresholdBrightnesContrast()

        ' image filter
        GetImageFilter()
        ' noise filter
        GetNoiseFilter()
        ' automatic rotate
        GetAutoRotate()
        ' automatic border detection
        GetAutoBorderDetection()


        '
        _isDeviceInitialized = True
    End Sub

    ''' <summary>
    ''' Inits combo box by array of values.
    ''' </summary>
    Private Sub InitComboBox(ByVal comboBox As ComboBox, ByVal values As Array, ByVal currentValue As Object)
        comboBox.Items.Clear()

        If values Is Nothing OrElse values.Length = 0 Then
            Return
        End If

        For i As Integer = 0 To values.Length - 1
            comboBox.Items.Add(values.GetValue(i))
        Next

        comboBox.SelectedItem = currentValue
    End Sub

    ''' <summary>
    ''' Inits track bar by values of device capability represented as range.
    ''' </summary>
    Private Sub InitRangeCapValue(ByVal capValue As TwainValueContainerBase, ByVal valuesTrackBar As TrackBar)
        If capValue Is Nothing Then
            Return
        End If

        Try
            ' if container type of capability is a range
            If capValue.ContainerType = TwainValueContainerType.Range Then
                ' convert base(abstract) object to real(non abstract) object
                Dim capValueAsRange As TwainRangeValueContainer = DirectCast(capValue, TwainRangeValueContainer)
                ' get range values as range struct (this action simplifies the convertation process of values)
                Dim range As Range(Of Single) = capValueAsRange.GetAsRangeOfFloatValues()

                Dim min As Integer = CInt(range.MinValue)
                Dim max As Integer = CInt(range.MaxValue)

                ' This is patch for bug in TWAIN drivers for HP ScanJet GXXXX scanners.
                If min > max Then
                    max = UInt16.MaxValue + max
                End If

                ' set the track bar values
                valuesTrackBar.Minimum = min
                valuesTrackBar.Maximum = max
                valuesTrackBar.SmallChange = CInt(range.StepSize)
                valuesTrackBar.TickFrequency = valuesTrackBar.SmallChange
                valuesTrackBar.Value = CInt(range.Value)
            Else
                ShowErrorMessage("Container type of capability is not a range.", "Device capability")
            End If
        Catch generatedExceptionName As TwainDeviceCapabilityException
        End Try
    End Sub

#End Region


#Region "UI"

    ''' <summary>
    ''' Updates UI.
    ''' </summary>
    Private Sub UpdateUI()
        Dim hasDevices As Boolean = False
        If _deviceManager.State = DeviceManagerState.Opened Then
            If _deviceManager.Devices.Count > 0 Then
                hasDevices = True
            End If
        End If
        Dim isDeviceChanging As Boolean = Me.IsDeviceChanging
        Dim isImageAcquiring As Boolean = Me.IsImageAcquiring

        twain2CompatibleCheckBox.Enabled = Not isImageAcquiring

        transferModeGroupBox.Enabled = Not isDeviceChanging AndAlso hasDevices AndAlso Not isImageAcquiring
        devicesComboBox.Enabled = Not isDeviceChanging AndAlso hasDevices AndAlso Not isImageAcquiring
        pageGroupBox.Enabled = Not isDeviceChanging AndAlso hasDevices AndAlso Not isImageAcquiring
        resolutionGroupBox.Enabled = Not isDeviceChanging AndAlso hasDevices AndAlso Not isImageAcquiring
        imageLayoutGroupBox.Enabled = Not isDeviceChanging AndAlso hasDevices AndAlso Not isImageAcquiring
        imagesToAcquireGroupBox.Enabled = Not isDeviceChanging AndAlso hasDevices AndAlso Not isImageAcquiring
        imageGroupBox.Enabled = Not isDeviceChanging AndAlso hasDevices AndAlso Not isImageAcquiring
        imageProcessingGroupBox.Enabled = Not isDeviceChanging AndAlso hasDevices AndAlso Not isImageAcquiring

        acquireImageButton.Enabled = hasDevices AndAlso Not isDeviceChanging
        If Not isDeviceChanging Then
            If isImageAcquiring Then
                acquireImageButton.Text = "Cancel"
            Else
                acquireImageButton.Text = "Acquire image(s)"
            End If
        End If


        ' unit of measure
        unitOfMeasureComboBox.Enabled = _isUnitOfMeasureAvailable

        ' resolution
        xResComboBox.Enabled = _isXResolutionAvailable
        xResTrackBar.Enabled = _isXResolutionAvailable
        yResComboBox.Enabled = _isYResolutionAvailable
        yResTrackBar.Enabled = _isYResolutionAvailable

        ' page size
        pageSizeComboBox.Enabled = _isPageSizeAvailable
        pageSizeLabel.Enabled = _isPageSizeAvailable

        ' page orientation
        pageOrientationComboBox.Enabled = _isPageOrientationAvailable
        pageOrientationLabel.Enabled = _isPageOrientationAvailable

        ' image layout
        leftTextBox.Enabled = _isImageLayoutAvailable
        topTextBox.Enabled = _isImageLayoutAvailable
        rightTextBox.Enabled = _isImageLayoutAvailable
        bottomTextBox.Enabled = _isImageLayoutAvailable

        ' pixel type
        pixelTypeComboBox.Enabled = _isPixelTypeAvailable
        pixelTypeLabel.Enabled = _isPixelTypeAvailable

        ' bit depth
        bitDepthComboBox.Enabled = _isBitDepthAvailable
        bitDepthLabel.Enabled = _isBitDepthAvailable

        ' threshold
        thresholdLabel.Enabled = _isThresholdAvailable
        thresholdComboBox.Enabled = _isThresholdAvailable
        thresholdTrackBar.Enabled = _isThresholdAvailable

        ' brightness
        brightnessLabel.Enabled = _isBrightnessAvailable
        brightnessComboBox.Enabled = _isBrightnessAvailable
        brightnessTrackBar.Enabled = _isBrightnessAvailable

        ' contrast
        contrastLabel.Enabled = _isContrastAvailable
        contrastComboBox.Enabled = _isContrastAvailable
        contrastTrackBar.Enabled = _isContrastAvailable

        ' image filter
        imageFilterComboBox.Enabled = _isImageFilterAvailable

        ' noise filter
        noiseFilterComboBox.Enabled = _isNoiseFilterAvailable

        ' auto rotate
        autoRotateCheckBox.Enabled = _isAutoRotateAvailable

        ' auto detect border
        autoBorderDetectionCheckBox.Enabled = _isAutoBorderDetectionAvailable
    End Sub

    ''' <summary>
    ''' TWAIN 2.0 compatibility is changed.
    ''' </summary>
    Private Sub twain2CompatibleCheckBox_CheckedChanged(ByVal sender As Object, ByVal e As EventArgs)
        ' if TWAIN 2.0 compatibility is not changed
        If _deviceManager.IsTwainAvailable AndAlso _deviceManager.IsTwain2Compatible = twain2CompatibleCheckBox.Checked Then
            Return
        End If

        ' change the application status and update UI
        IsDeviceChanging = True

        ' close device and device manager
        CloseDeviceAndDeviceManager()

        ' change TWAIN 2.0 compatibility
        _deviceManager.IsTwain2Compatible = twain2CompatibleCheckBox.Checked

        ' init devices
        InitDevices()
    End Sub

    ''' <summary>
    ''' Current device is changed.
    ''' </summary>
    Private Sub devicesComboBox_SelectedIndexChanged(ByVal sender As Object, ByVal e As EventArgs)
        If _deviceManager.State <> DeviceManagerState.Opened Then
            Return
        End If

        ' if current device is not changed
        If _currentDevice.Info.ProductName = DirectCast(devicesComboBox.SelectedItem, String) Then
            Return
        End If

        ' change the application status and update UI
        IsDeviceChanging = True

        ' close device if necessary
        If _currentDevice.State = DeviceState.Opened Then
            _currentDevice.Close()
        End If

        If _currentDevice IsNot Nothing Then
            UnsubscribeFromDeviceEvents()
        End If

        ' get a reference to current device
        _currentDevice = _deviceManager.Devices.Find(DirectCast(devicesComboBox.SelectedItem, String))
        SubscribeToDeviceEvents()

        Try
            ' init device settings
            InitDeviceSettings()

            ' change the application status and update UI
            IsDeviceChanging = False
        Catch ex As TwainDeviceException
            ShowErrorMessage(ex.Message, "Device error")
        Catch ex As TwainInvalidStateException
            ShowErrorMessage(ex.Message, "Device invalid state")
        End Try
    End Sub

    ''' <summary>
    ''' Acquire image button is clicked.
    ''' </summary>
    Private Sub acquireImageButton_Click(ByVal sender As Object, ByVal e As EventArgs)
        ' acquiring, need to cancel
        If IsImageAcquiring Then
            _currentDevice.CancelTransfer()
            Return
        End If

        ' acquire image(s)
        AcquireImage(nativeTransferRadioButton.Checked)
    End Sub

    ''' <summary>
    ''' Native transfer mode is selected.
    ''' </summary>
    Private Sub nativeTransferRadioButton_CheckedChanged(ByVal sender As Object, ByVal e As EventArgs)
        imageAcquisitionProgressBar.Visible = False
    End Sub

    ''' <summary>
    ''' Memory transfer mode is selected.
    ''' </summary>
    Private Sub memoryTransferRadioButton_CheckedChanged(ByVal sender As Object, ByVal e As EventArgs)
        imageAcquisitionProgressBar.Visible = True
    End Sub

    ''' <summary>
    ''' Pixel type is changed.
    ''' </summary>
    Private Sub pixelTypeComboBox_SelectedIndexChanged(ByVal sender As Object, ByVal e As EventArgs)
        If Not _isDeviceInitialized Then
            Return
        End If

        Me.Cursor = Cursors.WaitCursor

        ' if device is closed
        If _currentDevice.State = DeviceState.Closed Then
            ' open the device
            _currentDevice.Open()
        End If

        _pixelType = DirectCast(pixelTypeComboBox.SelectedItem, PixelType)
        _currentDevice.PixelType = _pixelType

        ' bit depth
        GetBitDepth()
        ' threshold, contrast and brightness
        GetThresholdBrightnesContrast()

        Me.Cursor = Cursors.[Default]

        UpdateUI()
    End Sub

    ''' <summary>
    ''' Unit of measure is changed.
    ''' </summary>
    Private Sub unitOfMeasureComboBox_SelectedIndexChanged(ByVal sender As Object, ByVal e As EventArgs)
        If Not _isDeviceInitialized Then
            Return
        End If

        Me.Cursor = Cursors.WaitCursor

        ' if device is closed
        If _currentDevice.State = DeviceState.Closed Then
            ' open the device
            _currentDevice.Open()
        End If

        _unitOfMeasure = DirectCast(unitOfMeasureComboBox.SelectedItem, UnitOfMeasure)
        _currentDevice.UnitOfMeasure = _unitOfMeasure
        GetResolution()
        ResetImageLayout()

        Me.Cursor = Cursors.[Default]

        UpdateUI()
    End Sub

    ''' <summary>
    ''' Reset the image layout.
    ''' </summary>
    Private Sub resetImageLayoutButton_Click(ByVal sender As Object, ByVal e As EventArgs)
        ResetImageLayout()
    End Sub

    ''' <summary>
    ''' Reset the image layout.
    ''' </summary>
    Private Sub ResetImageLayout()
        If _currentDevice Is Nothing Then
            Return
        End If

        Me.Cursor = Cursors.WaitCursor

        ' if device is closed
        If _currentDevice.State = DeviceState.Closed Then
            ' open the device
            _currentDevice.Open()
        End If

        Try
            _currentDevice.ImageLayout.Reset()
            GetImageLayout()
        Catch ex As TwainException
            ShowErrorMessage(ex.Message, "Error")
        End Try

        Me.Cursor = Cursors.[Default]
    End Sub

    ''' <summary>
    ''' Show tooltip when mouse hovers the track bar.
    ''' </summary>
    Private Sub trackBar_MouseHover(ByVal sender As Object, ByVal e As EventArgs)
        SetTooltip(DirectCast(sender, TrackBar))
    End Sub

    ''' <summary>
    ''' Show tooltip when track bar is scrolling.
    ''' </summary>
    Private Sub trackBar_Scroll(ByVal sender As Object, ByVal e As EventArgs)
        SetTooltip(DirectCast(sender, TrackBar))
    End Sub

    ''' <summary>
    ''' Associate ToolTip text with specified track bar.
    ''' </summary>
    Private Sub SetTooltip(ByVal trackBar As TrackBar)
        toolTip1.SetToolTip(trackBar, trackBar.Value.ToString())
    End Sub

    ''' <summary>
    ''' Clear images.
    ''' </summary>
    Private Sub clearImagesButton_Click(ByVal sender As Object, ByVal e As EventArgs)
        acquiredImagesTabControl.Controls.Clear()

        GC.Collect()
    End Sub

    ''' <summary>
    ''' Application form is closing.
    ''' </summary>
    Private Sub MainForm_FormClosing(ByVal sender As Object, ByVal e As FormClosingEventArgs)
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
        End If

        ' close the device and device manager
        CloseDeviceAndDeviceManager()
        ' dispose the device manager
        _deviceManager.Dispose()
        _deviceManager = Nothing
    End Sub

    Private Sub ShowErrorMessage(ByVal message As String, ByVal title As String)
        MessageBox.Show(message, title, MessageBoxButtons.OK, MessageBoxIcon.[Error])
    End Sub

#End Region


#Region "Acquire image(s)"

    ''' <summary>
    ''' Acquires image(s).
    ''' </summary>
    Private Sub AcquireImage(ByVal nativeTransferMode As Boolean)
        If _currentDevice Is Nothing Then
            Return
        End If

        ' change the application status and update UI
        IsImageAcquiring = True

        ' disable User Interface of device
        _currentDevice.ShowUI = False
        _currentDevice.ShowIndicators = False
        _currentDevice.DisableAfterAcquire = True


        ' if device is closed
        If _currentDevice.State = DeviceState.Closed Then
            ' open the device
            _currentDevice.Open()
        End If


        ' set device capabilities

        ' number of pages to acquire
        SetXferCount()

        ' pixel type
        SetPixelType()
        ' bit depth
        SetBitDepth()
        ' threshold, brightness and contrast
        If _pixelType = PixelType.BW Then
            SetThreshold()
        Else
            SetBrightness()
            SetContrast()
        End If

        ' unit of measure
        SetUnitOfMeasure()
        ' resolution
        SetResolution()

        ' page size
        SetPageSize()
        ' page orientation
        SetPageOrientation()

        ' image layout
        SetImageLayout()

        ' image filter
        SetImageFilter()
        ' noise filter
        SetNoiseFilter()
        ' auto rotate
        SetAutoRotate()
        ' auto border detection
        SetAutoBorderDetection()

        ' set the transfer mode
        Dim newTransferMode As TransferMode = TransferMode.Memory
        If nativeTransferMode Then
            _currentDevice.TransferMode = TransferMode.Native
        End If
        If _currentDevice.TransferMode <> newTransferMode Then
            _currentDevice.TransferMode = newTransferMode
        End If

        Try
            ' acquire image(s)
            _currentDevice.Acquire()
        Catch ex As Exception
            MessageBox.Show(String.Format("Error: {0}", ex.Message))
            ' change the application status and update UI
            IsImageAcquiring = False
        End Try
    End Sub

    ''' <summary>
    ''' Subscribes to device events.
    ''' </summary>
    Private Sub SubscribeToDeviceEvents()
        AddHandler _currentDevice.ImageAcquiringProgress, New EventHandler(Of ImageAcquiringProgressEventArgs)(AddressOf device_ImageAcquiringProgress)
        AddHandler _currentDevice.ImageAcquired, New EventHandler(Of ImageAcquiredEventArgs)(AddressOf device_ImageAcquired)
        AddHandler _currentDevice.ScanCanceled, New EventHandler(AddressOf device_ScanCanceled)
        AddHandler _currentDevice.ScanFailed, New EventHandler(Of ScanFailedEventArgs)(AddressOf device_ScanFailed)
        AddHandler _currentDevice.ScanFinished, New EventHandler(AddressOf device_ScanFinished)
    End Sub

    ''' <summary>
    ''' Unsubscribes from device events.
    ''' </summary>
    Private Sub UnsubscribeFromDeviceEvents()
        RemoveHandler _currentDevice.ImageAcquiringProgress, New EventHandler(Of ImageAcquiringProgressEventArgs)(AddressOf device_ImageAcquiringProgress)
        RemoveHandler _currentDevice.ImageAcquired, New EventHandler(Of ImageAcquiredEventArgs)(AddressOf device_ImageAcquired)
        RemoveHandler _currentDevice.ScanCanceled, New EventHandler(AddressOf device_ScanCanceled)
        RemoveHandler _currentDevice.ScanFailed, New EventHandler(Of ScanFailedEventArgs)(AddressOf device_ScanFailed)
        RemoveHandler _currentDevice.ScanFinished, New EventHandler(AddressOf device_ScanFinished)
    End Sub

    ''' <summary>
    ''' Image is acquiring.
    ''' </summary>
    Private Sub device_ImageAcquiringProgress(ByVal sender As Object, ByVal e As ImageAcquiringProgressEventArgs)
        ' image acquistion must be canceled because application's form is closing
        If _cancelTransferBecauseFormIsClosing Then
            ' cancel image acquisition
            _currentDevice.CancelTransfer()
            Return
        End If

        imageAcquisitionProgressBar.Value = e.Progress
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

        ' create panel for picture box with acquired image
        Dim tabPage1 As New TabPage()
        tabPage1.Location = New System.Drawing.Point(4, 22)
        tabPage1.Padding = New System.Windows.Forms.Padding(3)
        tabPage1.Size = New System.Drawing.Size(522, 318)
        tabPage1.Text = String.Format("Image {0} [{1}x{2}, {3}, {4}]", System.Math.Max(System.Threading.Interlocked.Increment(_imageCount), _imageCount - 1), e.Image.ImageInfo.Width, e.Image.ImageInfo.Height, e.Image.ImageInfo.PixelType, e.Image.ImageInfo.Resolution)

        ' create picture box for acquired image
        Dim pictureBox1 As New PictureBox()
        ' set the picture box size
        pictureBox1.Size = tabPage1.Size
        ' set a bitmap in the picture box
        pictureBox1.Image = e.Image.GetAsBitmap(True)
        ' set the picture box size mode
        pictureBox1.SizeMode = PictureBoxSizeMode.StretchImage

        ' add a picture box to a panel
        tabPage1.Controls.Add(pictureBox1)
        ' add a panel to a tab control with images
        acquiredImagesTabControl.Controls.Add(tabPage1)
        ' select new panel
        acquiredImagesTabControl.SelectedTab = tabPage1

        ' dispose an acquired image
        e.Image.Dispose()
    End Sub

    ''' <summary>
    ''' Scan is canceled.
    ''' </summary>
    Private Sub device_ScanCanceled(ByVal sender As Object, ByVal e As EventArgs)
        ' image acquistion must be canceled because application's form is closing
        If _cancelTransferBecauseFormIsClosing Then
            _cancelTransferBecauseFormIsClosing = False
            ' close the application's form
            Me.Close()
            Return
        End If

        MessageBox.Show("Scan is canceled.")
    End Sub

    ''' <summary>
    ''' Scan is failed.
    ''' </summary>
    Private Sub device_ScanFailed(ByVal sender As Object, ByVal e As ScanFailedEventArgs)
        ShowErrorMessage(e.ErrorString, "Scan is failed")
    End Sub

    ''' <summary>
    ''' Scan is finished.
    ''' </summary>
    Private Sub device_ScanFinished(ByVal sender As Object, ByVal e As EventArgs)
        ' close the device
        _currentDevice.Close()

        ' change the application status and update UI
        IsImageAcquiring = False

        '
        imageAcquisitionProgressBar.Value = 0
    End Sub

#End Region


#Region "Device capabilities"

#Region "Get"

    ''' <summary>
    ''' Get information about the current and supported units of measure of device.
    ''' </summary>
    Private Sub GetUnitOfMeasure()
        _isUnitOfMeasureAvailable = False
        Try
            _unitOfMeasure = _currentDevice.UnitOfMeasure
            InitComboBox(unitOfMeasureComboBox, _currentDevice.GetSupportedUnitsOfMeasure(), _unitOfMeasure)

            If unitOfMeasureComboBox.Items.Count > 0 Then
                _isUnitOfMeasureAvailable = True
            End If
        Catch generatedExceptionName As TwainDeviceCapabilityException
        End Try
    End Sub

    ''' <summary>
    ''' Get information about the current and supported resolutions of device.
    ''' </summary>
    Private Sub GetResolution()
        ' Horizontal resolution

        xResTrackBar.Visible = False
        xResComboBox.Visible = False
        _isXResolutionAvailable = False

        If _currentDevice.State = DeviceState.Closed Then
            _currentDevice.Open()
        End If

        ' get supported values of horizontal resolution
        Dim xResCapValue As TwainValueContainerBase = Nothing
        Try
            xResCapValue = _currentDevice.GetSupportedHorizontalResolutions()
        Catch generatedExceptionName As TwainDeviceCapabilityException
            Return
        End Try
        If xResCapValue Is Nothing Then
            Return
        End If

        ' if values are represented as range
        If xResCapValue.ContainerType = TwainValueContainerType.Range Then
            InitRangeCapValue(xResCapValue, xResTrackBar)

            xResTrackBar.Visible = True
        Else
            ' if values are represented as array or enumeration
            InitComboBox(xResComboBox, xResCapValue.GetAsFloatArray(), _currentDevice.Resolution.Horizontal)

            xResComboBox.Visible = True
        End If

        _isXResolutionAvailable = True


        ' Vertical resolution

        yResTrackBar.Visible = False
        yResComboBox.Visible = False
        _isYResolutionAvailable = False

        ' get supported values of vertical resolution
        Dim yResCapValue As TwainValueContainerBase
        Try
            yResCapValue = _currentDevice.GetSupportedVerticalResolutions()
        Catch generatedExceptionName As TwainDeviceCapabilityException
            Return
        End Try
        If yResCapValue Is Nothing Then
            Return
        End If

        ' if values are represented as range
        If yResCapValue.ContainerType = TwainValueContainerType.Range Then
            InitRangeCapValue(yResCapValue, yResTrackBar)

            yResTrackBar.Visible = True
        Else
            ' if values are represented as array or enumeration
            InitComboBox(yResComboBox, yResCapValue.GetAsFloatArray(), _currentDevice.Resolution.Vertical)

            yResComboBox.Visible = True
        End If

        _isYResolutionAvailable = True
    End Sub

    ''' <summary>
    ''' Get information about the current and supported page sizes of device.
    ''' </summary>
    Private Sub GetPageSize()
        _isPageSizeAvailable = False
        Try
            InitComboBox(pageSizeComboBox, _currentDevice.GetSupportedPageSizes(), _currentDevice.PageSize)

            If pageSizeComboBox.Items.Count > 0 Then
                _isPageSizeAvailable = True
            End If
        Catch generatedExceptionName As TwainDeviceCapabilityException
        End Try
    End Sub

    ''' <summary>
    ''' Get information about the page orientation of device.
    ''' </summary>
    Private Sub GetPageOrientation()
        _isPageOrientationAvailable = False
        Try
            Dim supportedPageOrientations As PageOrientation() = _currentDevice.GetSupportedPageOrientations()
            If supportedPageOrientations IsNot Nothing AndAlso _currentDevice.GetSupportedPageOrientations().Length > 0 Then
                InitComboBox(pageOrientationComboBox, supportedPageOrientations, _currentDevice.PageOrientation)

                _isPageOrientationAvailable = True
            End If
        Catch generatedExceptionName As TwainDeviceCapabilityException
        End Try
    End Sub

    ''' <summary>
    ''' Get information about the image layout of device.
    ''' </summary>
    Private Sub GetImageLayout()
        _isImageLayoutAvailable = False

        If _currentDevice.State = DeviceState.Closed Then
            _currentDevice.Open()
        End If

        ' Image layout
        leftTextBox.Text = ""
        topTextBox.Text = ""
        rightTextBox.Text = ""
        bottomTextBox.Text = ""
        Try
            Dim imageLayoutRect As RectangleF = _currentDevice.ImageLayout.[Get]()

            _isImageLayoutAvailable = True

            leftTextBox.Text = imageLayoutRect.Left.ToString()
            topTextBox.Text = imageLayoutRect.Top.ToString()
            rightTextBox.Text = imageLayoutRect.Right.ToString()
            bottomTextBox.Text = imageLayoutRect.Bottom.ToString()
        Catch generatedExceptionName As FormatException
        Catch generatedExceptionName As TwainDeviceException
        Catch generatedExceptionName As TwainDeviceCapabilityException
        End Try
    End Sub

    ''' <summary>
    ''' Get information about the current and supported pixel types of device.
    ''' </summary>
    Private Sub GetPixelType()
        _isPixelTypeAvailable = False
        Try
            _pixelType = _currentDevice.PixelType
            InitComboBox(pixelTypeComboBox, _currentDevice.GetSupportedPixelTypes(), _pixelType)

            _isPixelTypeAvailable = True
        Catch generatedExceptionName As TwainDeviceCapabilityException
        End Try
    End Sub

    ''' <summary>
    ''' Get information about the current and supported bit depths of device.
    ''' </summary>
    Private Sub GetBitDepth()
        _isBitDepthAvailable = False

        If _currentDevice.State = DeviceState.Closed Then
            _currentDevice.Open()
        End If

        Try
            InitComboBox(bitDepthComboBox, _currentDevice.GetSupportedBitDepths(), _currentDevice.BitDepth)

            _isBitDepthAvailable = True
        Catch generatedExceptionName As TwainDeviceCapabilityException
        End Try
    End Sub

    ''' <summary>
    ''' Get information about the current and supported thresholds OR brightnesses and contrasts of device.
    ''' </summary>
    Private Sub GetThresholdBrightnesContrast()
        thresholdComboBox.Visible = False
        thresholdTrackBar.Visible = False
        brightnessComboBox.Visible = False
        brightnessComboBox.Visible = False
        contrastComboBox.Visible = False
        contrastTrackBar.Visible = False

        If _currentDevice.State = DeviceState.Closed Then
            _currentDevice.Open()
        End If

        Dim capValue As TwainValueContainerBase
        If _pixelType = PixelType.BW Then
            ' init threshold values
            _isThresholdAvailable = False
            Try
                capValue = _currentDevice.GetSupportedThresholdValues()

                _isThresholdAvailable = True
            Catch generatedExceptionName As TwainDeviceCapabilityException
                Return
            End Try
            If capValue Is Nothing Then
                Return
            End If

            If capValue.ContainerType = TwainValueContainerType.Range Then
                InitRangeCapValue(capValue, thresholdTrackBar)

                thresholdTrackBar.Visible = True
            ElseIf capValue.ContainerType = TwainValueContainerType.[Enum] Then
                Dim capValueAsEnum As TwainEnumValueContainer = DirectCast(capValue, TwainEnumValueContainer)
                InitComboBox(thresholdComboBox, capValueAsEnum.GetAsFloatArray(), capValueAsEnum.GetAsFloat())

                thresholdComboBox.Visible = True
            End If
        Else
            ' init brightness values
            _isBrightnessAvailable = False
            Try
                capValue = _currentDevice.GetSupportedBrightnessValues()

                _isBrightnessAvailable = True
            Catch generatedExceptionName As TwainDeviceCapabilityException
                Return
            End Try
            If capValue Is Nothing Then
                Return
            End If

            If capValue.ContainerType = TwainValueContainerType.Range Then
                InitRangeCapValue(capValue, brightnessTrackBar)

                brightnessTrackBar.Visible = True
            ElseIf capValue.ContainerType = TwainValueContainerType.[Enum] Then
                Dim capValueAsEnum As TwainEnumValueContainer = DirectCast(capValue, TwainEnumValueContainer)
                InitComboBox(brightnessComboBox, capValueAsEnum.GetAsFloatArray(), capValueAsEnum.GetAsFloat())

                brightnessComboBox.Visible = True
            End If

            ' init contrast values
            _isContrastAvailable = False
            Try
                capValue = _currentDevice.GetSupportedContrastValues()

                _isContrastAvailable = True
            Catch generatedExceptionName As TwainDeviceCapabilityException
                Return
            End Try
            If capValue Is Nothing Then
                Return
            End If

            If capValue.ContainerType = TwainValueContainerType.Range Then
                InitRangeCapValue(capValue, contrastTrackBar)

                contrastTrackBar.Visible = True
            ElseIf capValue.ContainerType = TwainValueContainerType.[Enum] Then
                Dim capValueAsEnum As TwainEnumValueContainer = DirectCast(capValue, TwainEnumValueContainer)
                InitComboBox(contrastComboBox, capValueAsEnum.GetAsFloatArray(), capValueAsEnum.GetAsFloat())

                contrastComboBox.Visible = True
            End If
        End If
    End Sub

    ''' <summary>
    ''' Get information about the current and supported image filters of device.
    ''' </summary>
    Private Sub GetImageFilter()
        _isImageFilterAvailable = False
        Try
            Dim currentImageFilter As ImageFilter = _currentDevice.ImageFilter

            Dim supportedImageFilters As ImageFilter() = _currentDevice.GetSupportedImageFilters()
            InitComboBox(imageFilterComboBox, supportedImageFilters, currentImageFilter)

            _isImageFilterAvailable = True
        Catch generatedExceptionName As TwainDeviceCapabilityException
        End Try
    End Sub

    ''' <summary>
    ''' Get information about the current and supported noise filters of device.
    ''' </summary>
    Private Sub GetNoiseFilter()
        _isNoiseFilterAvailable = False
        Try
            InitComboBox(noiseFilterComboBox, _currentDevice.GetSupportedNoiseFilters(), _currentDevice.NoiseFilter)

            _isNoiseFilterAvailable = True
        Catch generatedExceptionName As TwainDeviceCapabilityException
        End Try
    End Sub

    ''' <summary>
    ''' Get information about the auto rotate capability of device.
    ''' </summary>
    Private Sub GetAutoRotate()
        _isAutoRotateAvailable = False
        _autoRotateCap = _currentDevice.Capabilities.Find(DeviceCapabilityId.IAutomaticRotate)
        If _autoRotateCap Is Nothing Then
            Return
        End If

        Try
            Dim autoRotateCapValue As TwainValueContainerBase = _autoRotateCap.GetValue()
            If autoRotateCapValue IsNot Nothing Then
                autoRotateCheckBox.Checked = autoRotateCapValue.GetAsBool()
            End If

            _isAutoRotateAvailable = True
        Catch generatedExceptionName As TwainDeviceCapabilityException
        End Try
    End Sub

    ''' <summary>
    ''' Get information about the auto border detection capability of device.
    ''' </summary>
    Private Sub GetAutoBorderDetection()
        _isAutoBorderDetectionAvailable = False
        _autoBorderDetectionCap = _currentDevice.Capabilities.Find(DeviceCapabilityId.IAutomaticBorderDetection)
        If _autoBorderDetectionCap Is Nothing Then
            Return
        End If

        Try
            Dim autoBorderDetectionCapValue As TwainValueContainerBase = _autoBorderDetectionCap.GetValue()
            If autoBorderDetectionCapValue IsNot Nothing Then
                autoBorderDetectionCheckBox.Checked = autoBorderDetectionCapValue.GetAsBool()
            End If

            _isAutoBorderDetectionAvailable = True
        Catch generatedExceptionName As TwainDeviceCapabilityException
        End Try
    End Sub

#End Region


#Region "Set"

    ''' <summary>
    ''' Specify how many images application wants to receive from the device.
    ''' </summary>
    Private Sub SetXferCount()
        Try
            Dim newXferCount As Short = CShort(Math.Truncate(pagesToAcquireNumericUpDown.Value))
            If _currentDevice.XferCount <> newXferCount Then
                _currentDevice.XferCount = newXferCount
            End If
        Catch generatedExceptionName As TwainDeviceCapabilityException
        End Try
    End Sub

    ''' <summary>
    ''' Set unit of measure of device.
    ''' </summary>
    Private Sub SetUnitOfMeasure()
        If _isUnitOfMeasureAvailable Then
            Try
                If _currentDevice.UnitOfMeasure <> _unitOfMeasure Then
                    _currentDevice.UnitOfMeasure = _unitOfMeasure
                End If
            Catch generatedExceptionName As TwainDeviceCapabilityException
            End Try
        End If
    End Sub

    ''' <summary>
    ''' Set resolution of device.
    ''' </summary>
    Private Sub SetResolution()
        If xResComboBox.Visible AndAlso yResComboBox.Visible Then
            Try
                Dim newXRes As Single = CSng(xResComboBox.SelectedItem)
                Dim newYRes As Single = CSng(yResComboBox.SelectedItem)
                If _currentDevice.UnitOfMeasure <> _unitOfMeasure OrElse _currentDevice.Resolution.Horizontal <> newXRes OrElse _currentDevice.Resolution.Vertical <> newYRes Then
                    _currentDevice.Resolution = New Resolution(newXRes, newYRes, _unitOfMeasure)
                End If
            Catch generatedExceptionName As TwainDeviceCapabilityException
            End Try
        End If
        If xResTrackBar.Visible AndAlso yResTrackBar.Visible Then
            Try
                Dim newXRes As Single = CSng(xResTrackBar.Value)
                Dim newYRes As Single = CSng(yResTrackBar.Value)
                If _currentDevice.UnitOfMeasure <> _unitOfMeasure OrElse _currentDevice.Resolution.Horizontal <> newXRes OrElse _currentDevice.Resolution.Vertical <> newYRes Then
                    _currentDevice.Resolution = New Resolution(newXRes, newYRes, _unitOfMeasure)
                End If
            Catch generatedExceptionName As TwainDeviceCapabilityException
            End Try
        End If
    End Sub

    ''' <summary>
    ''' Set page size of device.
    ''' </summary>
    Private Sub SetPageSize()
        If _isPageSizeAvailable Then
            Try
                Dim newPageSize As PageSize = DirectCast(pageSizeComboBox.SelectedItem, PageSize)
                If _currentDevice.PageSize <> newPageSize Then
                    _currentDevice.PageSize = newPageSize
                End If
            Catch generatedExceptionName As TwainDeviceCapabilityException
            End Try
        End If
    End Sub

    ''' <summary>
    ''' Set page orientation of device.
    ''' </summary>
    Private Sub SetPageOrientation()
        If _isPageOrientationAvailable Then
            Try
                Dim newPageOrientation As PageOrientation = DirectCast(pageOrientationComboBox.SelectedItem, PageOrientation)
                If _currentDevice.PageOrientation <> newPageOrientation Then
                    _currentDevice.PageOrientation = newPageOrientation
                End If
            Catch generatedExceptionName As TwainDeviceCapabilityException
            End Try
        End If
    End Sub

    ''' <summary>
    ''' Set image layout of device.
    ''' </summary>
    Private Sub SetImageLayout()
        If _isImageLayoutAvailable Then
            Try
                Dim newImageLayout As New RectangleF(Single.Parse(leftTextBox.Text), Single.Parse(topTextBox.Text), Single.Parse(rightTextBox.Text), Single.Parse(bottomTextBox.Text))
                Dim currentImageLayout As RectangleF = _currentDevice.ImageLayout.[Get]()
                If Math.Abs(newImageLayout.Left - currentImageLayout.Left) > 0.0001F OrElse Math.Abs(newImageLayout.Top - currentImageLayout.Top) > 0.0001F OrElse Math.Abs(newImageLayout.Width - currentImageLayout.Width) > 0.0001F OrElse Math.Abs(newImageLayout.Height - currentImageLayout.Height) > 0.0001F Then
                    _currentDevice.ImageLayout.[Set](newImageLayout)
                End If
            Catch ex As FormatException
                MessageBox.Show(ex.Message, "Set Image Layout Error")
            Catch ex As TwainDeviceException
                MessageBox.Show(ex.Message, "Set Image Layout Error")
            Catch ex As TwainDeviceCapabilityException
                MessageBox.Show(ex.Message, "Set Image Layout Error")
            End Try
        End If
    End Sub

    ''' <summary>
    ''' Set pixel type of device.
    ''' </summary>
    Private Sub SetPixelType()
        Try
            If _currentDevice.PixelType <> _pixelType Then
                _currentDevice.PixelType = _pixelType
            End If
        Catch generatedExceptionName As TwainDeviceCapabilityException
        End Try
    End Sub

    ''' <summary>
    ''' Set bit depth of device.
    ''' </summary>
    Private Sub SetBitDepth()
        If _isBitDepthAvailable Then
            Try
                Dim newBitDepth As Integer = CInt(bitDepthComboBox.SelectedItem)
                If _currentDevice.BitDepth <> newBitDepth Then
                    _currentDevice.BitDepth = newBitDepth
                End If
            Catch generatedExceptionName As TwainDeviceCapabilityException
            End Try
        End If
    End Sub

    ''' <summary>
    ''' Set threshold of device.
    ''' </summary>
    Private Sub SetThreshold()
        If _isThresholdAvailable Then
            Try
                Dim newThreshold As Single = CSng(thresholdTrackBar.Value)
                If _currentDevice.Threshold <> newThreshold Then
                    _currentDevice.Threshold = newThreshold
                End If
            Catch generatedExceptionName As TwainDeviceCapabilityException
            End Try
        End If
    End Sub

    ''' <summary>
    ''' Set brightness of device.
    ''' </summary>
    Private Sub SetBrightness()
        If _isBrightnessAvailable Then
            Try
                Dim newBrightness As Single = CSng(brightnessTrackBar.Value)
                If _currentDevice.Brightness <> newBrightness Then
                    _currentDevice.Brightness = newBrightness
                End If
            Catch generatedExceptionName As TwainDeviceCapabilityException
            End Try
        End If
    End Sub

    ''' <summary>
    ''' Set contrast of device.
    ''' </summary>
    Private Sub SetContrast()
        If _isContrastAvailable Then
            Try
                Dim newContrast As Single = CSng(contrastTrackBar.Value)
                If _currentDevice.Contrast <> newContrast Then
                    _currentDevice.Contrast = newContrast
                End If
            Catch generatedExceptionName As TwainDeviceCapabilityException
            End Try
        End If
    End Sub

    ''' <summary>
    ''' Set image filter of device.
    ''' </summary>
    Private Sub SetImageFilter()
        If _isImageFilterAvailable AndAlso imageFilterComboBox.SelectedItem IsNot Nothing Then
            Try
                Dim newImageFilter As ImageFilter = DirectCast(imageFilterComboBox.SelectedItem, ImageFilter)
                If _currentDevice.ImageFilter <> newImageFilter Then
                    _currentDevice.ImageFilter = newImageFilter
                End If
            Catch generatedExceptionName As TwainDeviceCapabilityException
            End Try
        End If
    End Sub

    ''' <summary>
    ''' Set noise filter of device.
    ''' </summary>
    Private Sub SetNoiseFilter()
        If _isNoiseFilterAvailable AndAlso noiseFilterComboBox.SelectedItem IsNot Nothing Then
            Try
                Dim newNoiseFilter As NoiseFilter = DirectCast(noiseFilterComboBox.SelectedItem, NoiseFilter)
                If _currentDevice.NoiseFilter <> newNoiseFilter Then
                    _currentDevice.NoiseFilter = newNoiseFilter
                End If
            Catch generatedExceptionName As TwainDeviceCapabilityException
            End Try
        End If
    End Sub

    ''' <summary>
    ''' Set auto rotate capability of device.
    ''' </summary>
    Private Sub SetAutoRotate()
        If _isAutoRotateAvailable Then
            Try
                Dim newAutoRotate As Boolean = autoRotateCheckBox.Checked
                Dim currentValue As TwainValueContainerBase = _autoRotateCap.GetCurrentValue()
                If currentValue IsNot Nothing AndAlso currentValue.GetAsBool() <> newAutoRotate Then
                    _autoRotateCap.SetValue(newAutoRotate)
                End If
            Catch generatedExceptionName As TwainDeviceCapabilityException
            End Try
        End If
    End Sub

    ''' <summary>
    ''' Set auto border detection capability of device.
    ''' </summary>
    Private Sub SetAutoBorderDetection()
        If _isAutoBorderDetectionAvailable Then
            Try
                Dim newAutoBorderDetection As Boolean = autoBorderDetectionCheckBox.Checked
                Dim currentValue As TwainValueContainerBase = _autoBorderDetectionCap.GetCurrentValue()
                If currentValue IsNot Nothing AndAlso currentValue.GetAsBool() <> newAutoBorderDetection Then
                    _autoBorderDetectionCap.SetValue(newAutoBorderDetection)
                End If
            Catch generatedExceptionName As TwainDeviceCapabilityException
            End Try
        End If
    End Sub

#End Region

#End Region


#Region "Close device"

    ''' <summary>
    ''' Closes the device and device manager.
    ''' </summary>
    Private Sub CloseDeviceAndDeviceManager()
        If _currentDevice IsNot Nothing Then
            ' close device if it is not closed
            If _currentDevice.State <> DeviceState.Closed Then
                _currentDevice.Close()
            End If
        End If

        ' close device manager if it is opened or loaded
        If _deviceManager.State <> DeviceManagerState.Closed Then
            _deviceManager.Close()
        End If
    End Sub

#End Region

#End Region

End Class
