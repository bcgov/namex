Imports System.Windows
Imports System.Windows.Controls
Imports Vintasoft.WpfTwain

Public Partial Class MainWindow
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

	#End Region



	#Region "Constructor"

	Public Sub New()
		InitializeComponent()

		Me.Title = [String].Format("VintaSoft WPF TWAIN Extended Image Info Demo v{0}", TwainGlobalSettings.ProductVersion)

		' create instance of the DeviceManager class
		_deviceManager = New DeviceManager(Me)
	End Sub

	#End Region



	#Region "Methods"

	Private Sub Window_Loaded(sender As Object, e As EventArgs)
		'
		Dim extendedImageInfoNames As String() = [Enum].GetNames(GetType(ExtendedImageInfoId))
		'
		Dim checkBox As CheckBox
		For i As Integer = 0 To extendedImageInfoNames.Length - 1
			checkBox = New CheckBox()
			checkBox.Content = extendedImageInfoNames(i).Replace("_"C, " "C)

			extendedImageInfoToRetrievePanel.Children.Add(checkBox)
		Next

		' select the standard extended image infos
		SelectStandardExtendedImageInfos()

		' open TWAIN device manager
		OpenDeviceManager()
	End Sub

	''' <summary>
	''' Sets form's UI state.
	''' </summary>
	Private Sub SetFormUiState(enabled As Boolean)
		acquireImageButton.IsEnabled = enabled
	End Sub


	''' <summary>
	''' Opens TWAIN device manager.
	''' </summary>
	Private Function OpenDeviceManager() As Boolean
		SetFormUiState(False)

		' try to find the device manager 2.x
		_deviceManager.IsTwain2Compatible = True
		' if TWAIN device manager .x is not available
		If Not _deviceManager.IsTwainAvailable Then
			' try to use TWAIN device manager 1.x
			_deviceManager.IsTwain2Compatible = False
			' if TWAIN device manager 1.x is not available
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
	''' Acquire image.
	''' </summary>
	Private Sub acquireImageButton_Click(sender As Object, e As EventArgs)
		Try
			' select the device
			If Not _deviceManager.ShowDefaultDeviceSelectionDialog() Then
				MessageBox.Show("Device is not selected.")
				Return
			End If

			If _currentDevice IsNot Nothing Then
				UnsubscribeFromDeviceEvents()
			End If

			' get a reference to the selected device
            Dim device As Device = _deviceManager.DefaultDevice

			_currentDevice = device
			' subscribe to the device events
			SubscribeToDeviceEvents()

			' set acquisition parameters
			device.ShowUI = False
			device.DisableAfterAcquire = True

			' open the device
			device.Open()

			' determine if device supports the extended image info
			Dim extendedImageInfoCap As DeviceCapability = device.Capabilities.Find(DeviceCapabilityId.IExtImageInfo)
			If extendedImageInfoCap Is Nothing Then
				' close the device
				device.Close()
				MessageBox.Show("Device does not support extended image information.")
				Return
			End If

			' specify that image info is necessary
			AddExtendedImageInfoToRetrieveList(device)

			' start the asynchronous image acquisition process 
			device.Acquire()
		Catch ex As TwainException
			MessageBox.Show(ex.Message, "Error")
		End Try
	End Sub

	''' <summary>
	''' Subscribes to the device events.
	''' </summary>
	Private Sub SubscribeToDeviceEvents()
        AddHandler _currentDevice.ImageAcquired, New EventHandler(Of ImageAcquiredEventArgs)(AddressOf device_ImageAcquired)
        AddHandler _currentDevice.ScanCanceled, New EventHandler(AddressOf device_ScanCanceled)
        AddHandler _currentDevice.UserInterfaceClosed, New EventHandler(AddressOf device_UserInterfaceClosed)
        AddHandler _currentDevice.ScanFailed, New EventHandler(Of ScanFailedEventArgs)(AddressOf device_ScanFailed)
        AddHandler _currentDevice.ScanFinished, New EventHandler(AddressOf device_ScanFinished)
	End Sub

	''' <summary>
	''' Unsubscribes from the device events.
	''' </summary>
	Private Sub UnsubscribeFromDeviceEvents()
        RemoveHandler _currentDevice.ImageAcquired, New EventHandler(Of ImageAcquiredEventArgs)(AddressOf device_ImageAcquired)
        RemoveHandler _currentDevice.ScanCanceled, New EventHandler(AddressOf device_ScanCanceled)
        RemoveHandler _currentDevice.UserInterfaceClosed, New EventHandler(AddressOf device_UserInterfaceClosed)
        RemoveHandler _currentDevice.ScanFailed, New EventHandler(Of ScanFailedEventArgs)(AddressOf device_ScanFailed)
        RemoveHandler _currentDevice.ScanFinished, New EventHandler(AddressOf device_ScanFinished)
    End Sub

	''' <summary>
	''' Image is acquired.
	''' </summary>
	Private Sub device_ImageAcquired(sender As Object, e As ImageAcquiredEventArgs)
		' dispose an acquired image
		e.Image.Dispose()

		' output an extended image info

		extendedImageInfoAboutAcquiredImageTextBox.Text += "IMAGE IS ACQUIRED" & Environment.NewLine
		extendedImageInfoAboutAcquiredImageTextBox.Text += Environment.NewLine

		Dim device As Device = DirectCast(sender, Device)
		For i As Integer = 0 To device.ExtendedImageInfo.Count - 1
			AddExtendedImageInfoToResultTextBox(i, device.ExtendedImageInfo(i))
		Next
		extendedImageInfoAboutAcquiredImageTextBox.Text += Environment.NewLine
	End Sub

	''' <summary>
	''' Scan is canceled.
	''' </summary>
	Private Sub device_ScanCanceled(sender As Object, e As EventArgs)
        MessageBox.Show("Scan is canceled.")
	End Sub

	''' <summary>
	''' User interface of device is closed.
	''' </summary>
	Private Sub device_UserInterfaceClosed(sender As Object, e As EventArgs)
        MessageBox.Show("Scan is canceled.")
	End Sub

	''' <summary>
	''' Scan is failed.
	''' </summary>
	Private Sub device_ScanFailed(sender As Object, e As ScanFailedEventArgs)
        MessageBox.Show(e.ErrorString, "Scan is failed")
	End Sub

    ''' <summary>
    ''' Scan is finished.
    ''' </summary>
    Private Sub device_ScanFinished(ByVal sender As Object, ByVal e As EventArgs)
        ' close the device
        _currentDevice.Close()
    End Sub


	''' <summary>
	''' Select/unselect all types of extended image info.
	''' </summary>
	Private Sub selectAllExtendedImageInfoButton_Click(sender As Object, e As EventArgs)
		Dim selectAll As Boolean = False

		If DirectCast(selectAllExtendedImageInfoButton.Content, String) = "Select all" Then
			selectAll = True
			selectAllExtendedImageInfoButton.Content = "Unselect all"
		Else
			selectAllExtendedImageInfoButton.Content = "Select all"
		End If

		Dim checkBox As CheckBox
		For i As Integer = 0 To extendedImageInfoToRetrievePanel.Children.Count - 1
			checkBox = DirectCast(extendedImageInfoToRetrievePanel.Children(i), CheckBox)
			checkBox.IsChecked = selectAll
		Next
	End Sub

	''' <summary>
	''' Select standard extended image infos (standard extended image infos always available
	''' if DeviceCapabilityId.IExtImageInfo capability is supported by device).
	''' </summary>
	Private Sub SelectStandardExtendedImageInfos()
		Dim standardExtendedImageInfoIds As ExtendedImageInfoId() = New ExtendedImageInfoId(5) {ExtendedImageInfoId.DocumentNumber, ExtendedImageInfoId.PageNumber, ExtendedImageInfoId.Camera, ExtendedImageInfoId.FrameNumber, ExtendedImageInfoId.Frame, ExtendedImageInfoId.PixelFlavor}

		Dim isStandardExtendedImageInfoFound As Boolean
		Dim checkBox As CheckBox
		For i As Integer = 0 To extendedImageInfoToRetrievePanel.Children.Count - 1
			checkBox = DirectCast(extendedImageInfoToRetrievePanel.Children(i), CheckBox)
			Dim extendedImageInfoIdString As String = DirectCast(checkBox.Content, String).Replace(" "C, "_"C)
			Dim extendedImageInfoId__1 As ExtendedImageInfoId = DirectCast([Enum].Parse(GetType(ExtendedImageInfoId), extendedImageInfoIdString), ExtendedImageInfoId)

			isStandardExtendedImageInfoFound = False
			For j As Integer = 0 To standardExtendedImageInfoIds.Length - 1
				If extendedImageInfoId__1 = standardExtendedImageInfoIds(j) Then
					isStandardExtendedImageInfoFound = True
					Exit For
				End If
			Next

			checkBox.IsChecked = isStandardExtendedImageInfoFound
		Next
	End Sub

	''' <summary>
	''' Add type of extended image info to the list of necessary extended image infos.
	''' </summary>
	Private Sub AddExtendedImageInfoToRetrieveList(device As Device)
		device.ExtendedImageInfo.Clear()

		Dim checkBox As CheckBox
		For i As Integer = 0 To extendedImageInfoToRetrievePanel.Children.Count - 1
			checkBox = DirectCast(extendedImageInfoToRetrievePanel.Children(i), CheckBox)
			If checkBox.IsChecked = True Then
				Dim enumType As Type = GetType(ExtendedImageInfoId)
				Dim extendedImageInfoIdString As String = DirectCast(checkBox.Content, String).Replace(" "C, "_"C)
				Dim extendedImageInfoId As ExtendedImageInfoId = DirectCast([Enum].Parse(enumType, extendedImageInfoIdString), ExtendedImageInfoId)

				device.ExtendedImageInfo.Add(New ExtendedImageInfo(extendedImageInfoId))
			End If
		Next
	End Sub

	''' <summary>
	''' Add an extended image info to the result.
	''' </summary>
	Private Sub AddExtendedImageInfoToResultTextBox(index As Integer, info As ExtendedImageInfo)
		If Not info.IsValueValid Then
			Return
		End If

		extendedImageInfoAboutAcquiredImageTextBox.Text += String.Format("Extended image info {0}", index)
		extendedImageInfoAboutAcquiredImageTextBox.Text += Environment.NewLine

		extendedImageInfoAboutAcquiredImageTextBox.Text += String.Format("  Name={0}", [Enum].GetName(GetType(ExtendedImageInfoId), info.InfoId))
		extendedImageInfoAboutAcquiredImageTextBox.Text += Environment.NewLine

		extendedImageInfoAboutAcquiredImageTextBox.Text += String.Format("  Id={0}", info.InfoId)
		extendedImageInfoAboutAcquiredImageTextBox.Text += Environment.NewLine

		extendedImageInfoAboutAcquiredImageTextBox.Text += String.Format("  Value type={0}", info.ValueType)
		extendedImageInfoAboutAcquiredImageTextBox.Text += Environment.NewLine

		Dim oneDeviceCapabilityValue As TwainOneValueContainer = TryCast(info.Value, TwainOneValueContainer)
		If oneDeviceCapabilityValue IsNot Nothing Then
			extendedImageInfoAboutAcquiredImageTextBox.Text += String.Format("  Value={0}", oneDeviceCapabilityValue.Value)
			extendedImageInfoAboutAcquiredImageTextBox.Text += Environment.NewLine
		Else
			Dim arrayDeviceCapabilityValue As TwainArrayValueContainer = TryCast(info.Value, TwainArrayValueContainer)
			If arrayDeviceCapabilityValue IsNot Nothing Then
				extendedImageInfoAboutAcquiredImageTextBox.Text += "Values: "
				If arrayDeviceCapabilityValue.Values IsNot Nothing Then
                    If arrayDeviceCapabilityValue.Values.[GetType]() Is GetType(Byte()) Then
                        extendedImageInfoAboutAcquiredImageTextBox.Text += String.Format("byte[{0}]", arrayDeviceCapabilityValue.Values.Length)
                    Else
                        For i As Integer = 0 To arrayDeviceCapabilityValue.Values.Length - 1
                            extendedImageInfoAboutAcquiredImageTextBox.Text += String.Format("{0}, ", arrayDeviceCapabilityValue.Values.GetValue(i))
                        Next
                    End If
				End If
				extendedImageInfoAboutAcquiredImageTextBox.Text += Environment.NewLine
			End If
		End If
	End Sub

    Private Sub Window_Closing(ByVal sender As System.Object, ByVal e As System.ComponentModel.CancelEventArgs)
        If _currentDevice IsNot Nothing Then
            UnsubscribeFromDeviceEvents()
            _currentDevice = Nothing
        End If

        ' close the device manager
        _deviceManager.Close()
        ' dispose the device manager
        _deviceManager.Dispose()
        _deviceManager = Nothing
    End Sub

	#End Region

End Class
