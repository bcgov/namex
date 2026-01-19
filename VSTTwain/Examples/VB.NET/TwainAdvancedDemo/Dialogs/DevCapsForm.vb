Imports System.Windows.Forms
Imports System.Text
Imports Vintasoft.Twain

Public Partial Class DevCapsForm
	Inherits Form

	#Region "Internal structs"

	Private Structure DeviceCapabilityInfo
		Friend DeviceCapability As DeviceCapability

		Friend Sub New(deviceCapability__1 As DeviceCapability)
			DeviceCapability = deviceCapability__1
		End Sub

		Public Overrides Function ToString() As String
			Return DeviceCapability.Name
		End Function
	End Structure

	#End Region



	#Region "Fields"

	''' <summary>
	''' Current device.
	''' </summary>
	Private _device As Device

	#End Region



	#Region "Constructor"

	Public Sub New(device As Device)
		InitializeComponent()

		If device.State <> DeviceState.Closed Then
			Throw New ApplicationException("Device is used.")
		End If

		_device = device

		Me.Text = String.Format("{0} [TWAIN {1}] capabilities", _device.Info.ProductName, _device.Info.TwainVersion)
	End Sub

	#End Region



	#Region "Methods"

	''' <summary>
	''' Form is loaded.
	''' </summary>
	''' <param name="sender"></param>
	''' <param name="e"></param>
	Private Sub DevCapsForm_Load(sender As Object, e As EventArgs)
		Try
			_device.Open()

			For i As Integer = 0 To _device.Capabilities.Count - 1
				supportedCapabilitiesListBox.Items.Add(New DeviceCapabilityInfo(_device.Capabilities(i)))
			Next

			deviceManufacturerLabel.Text = String.Format("Manufacturer: {0}", _device.Info.Manufacturer)
			deviceProductFamilyLabel.Text = String.Format("Product family: {0}", _device.Info.ProductFamily)
			deviceProductNameLabel.Text = String.Format("Product name: {0}", _device.Info.ProductName)
			driverTwainVersionLabel.Text = String.Format("TWAIN version: {0}", _device.Info.TwainVersion)
			driverTwain2CompatibleLabel.Text = String.Format("TWAIN 2.0 compatible: {0}", _device.Info.IsTwain2Compatible)
			flatbedPresentLabel.Text = String.Format("Flatbed present: {0}", _device.HasFlatbed)
			feederPresentLabel.Text = String.Format("Feeder present: {0}", _device.HasFeeder)
		Catch ex As TwainDeviceException
			Close()
			MessageBox.Show(ex.Message, "Device error", MessageBoxButtons.OK, MessageBoxIcon.[Error])
		End Try
	End Sub

	''' <summary>
	''' Form is closing.
	''' </summary>
	''' <param name="sender"></param>
	''' <param name="e"></param>
	Private Sub DevCapsForm_FormClosing(sender As Object, e As FormClosingEventArgs)
		If _device.State = DeviceState.Opened Then
			_device.Close()
		End If
	End Sub


	#Region "Show capability value"

	''' <summary>
	''' Gets information about selected capability.
	''' </summary>
	''' <param name="sender"></param>
	''' <param name="e"></param>
	Private Sub supportedCapabilitiesListBox_SelectedIndexChanged(sender As Object, e As EventArgs)
		Cursor = Cursors.WaitCursor

		getMethodComboBox.Items.Clear()

		Dim deviceCapabilityInfo As DeviceCapabilityInfo = CType(supportedCapabilitiesListBox.SelectedItem, DeviceCapabilityInfo)
		Dim cap As DeviceCapability = deviceCapabilityInfo.DeviceCapability

		Dim usageMode As DeviceCapabilityUsageMode = DeviceCapabilityUsageMode.[Get]
		If getMethodComboBox.SelectedItem IsNot Nothing Then
			usageMode = DirectCast(getMethodComboBox.SelectedItem, DeviceCapabilityUsageMode)
		End If

		GetCapValue(cap, usageMode)

		Cursor = Cursors.[Default]
	End Sub

	''' <summary>
	''' Gets information about selected capability when the usage mode of capability is changed.
	''' </summary>
	''' <param name="sender"></param>
	''' <param name="e"></param>
	Private Sub getMethodComboBox_SelectedIndexChanged(sender As Object, e As EventArgs)
		Cursor = Cursors.WaitCursor

		Dim deviceCapabilityInfo As DeviceCapabilityInfo = CType(supportedCapabilitiesListBox.SelectedItem, DeviceCapabilityInfo)
		Dim cap As DeviceCapability = deviceCapabilityInfo.DeviceCapability

		Dim usageMode As DeviceCapabilityUsageMode = DeviceCapabilityUsageMode.[Get]
		If getMethodComboBox.SelectedItem IsNot Nothing Then
			usageMode = DirectCast(getMethodComboBox.SelectedItem, DeviceCapabilityUsageMode)
		End If

		GetCapValue(cap, usageMode)

		Cursor = Cursors.[Default]
	End Sub

	''' <summary>
	''' Gets information about value of specified capability in specified usage mode.
	''' </summary>
	''' <param name="deviceCapability"></param>
	''' <param name="usageMode"></param>
	Private Sub GetCapValue(deviceCapability As DeviceCapability, usageMode As DeviceCapabilityUsageMode)
		usageModeTextBox.Text = ""
		containerTypeTextBox.Text = ""
		valueTypeTextBox.Text = ""
		currentValueTextBox.Text = ""
		minValueTextBox.Text = ""
		maxValueTextBox.Text = ""
		defaultValueTextBox.Text = ""
		stepSizeTextBox.Text = ""
		supportedValuesListBox.Items.Clear()

		Try
			Dim deviceCapabilityValue As TwainValueContainerBase = Nothing
			If usageMode = DeviceCapabilityUsageMode.GetCurrent Then
				deviceCapabilityValue = deviceCapability.GetCurrentValue()
			ElseIf usageMode = DeviceCapabilityUsageMode.GetDefault Then
				deviceCapabilityValue = deviceCapability.GetDefaultValue()
			Else
				deviceCapabilityValue = deviceCapability.GetValue()
			End If

			If getMethodComboBox.Items.Count = 0 Then
				'
				usageModeTextBox.Text = deviceCapability.UsageMode.ToString()
				'
				If (deviceCapability.UsageMode And DeviceCapabilityUsageMode.[Get]) <> 0 Then
					getMethodComboBox.Items.Add(DeviceCapabilityUsageMode.[Get])
				End If
				If (deviceCapability.UsageMode And DeviceCapabilityUsageMode.GetCurrent) <> 0 Then
					getMethodComboBox.Items.Add(DeviceCapabilityUsageMode.GetCurrent)
				End If
				If (deviceCapability.UsageMode And DeviceCapabilityUsageMode.GetDefault) <> 0 Then
					getMethodComboBox.Items.Add(DeviceCapabilityUsageMode.GetDefault)
				End If
			End If

			If deviceCapabilityValue IsNot Nothing Then
				'
				containerTypeTextBox.Text = deviceCapabilityValue.ContainerType.ToString()
				valueTypeTextBox.Text = deviceCapability.ValueType.ToString()

				'
				Select Case deviceCapabilityValue.ContainerType
					Case TwainValueContainerType.OneValue
						Dim oneDeviceCapabilityValue As TwainOneValueContainer = DirectCast(deviceCapabilityValue, TwainOneValueContainer)
						AddCapOneCurrentValueToForm(oneDeviceCapabilityValue)
						Exit Select

					Case TwainValueContainerType.Range
						Dim rangeDeviceCapabilityValue As TwainRangeValueContainer = DirectCast(deviceCapabilityValue, TwainRangeValueContainer)
						AddCapRangeCurrentValueToForm(rangeDeviceCapabilityValue)
						AddCapRangeDefaultValueToForm(rangeDeviceCapabilityValue)
						AddCapMinValueToForm(rangeDeviceCapabilityValue)
						AddCapMaxValueToForm(rangeDeviceCapabilityValue)
						AddCapStepSizeToForm(rangeDeviceCapabilityValue)
						Exit Select

					Case TwainValueContainerType.[Enum]
						Dim enumDeviceCapabilityValue As TwainEnumValueContainer = DirectCast(deviceCapabilityValue, TwainEnumValueContainer)
						AddCapEnumCurrentValueToForm(enumDeviceCapabilityValue)
						AddCapEnumDefaultValueToForm(enumDeviceCapabilityValue)
						AddCapValuesToForm(enumDeviceCapabilityValue)
						Exit Select

					Case TwainValueContainerType.Array
						Dim arrayDeviceCapabilityValue As TwainArrayValueContainer = DirectCast(deviceCapabilityValue, TwainArrayValueContainer)
						AddCapValuesToForm(arrayDeviceCapabilityValue)
						Exit Select
				End Select
			End If
		Catch ex As TwainDeviceCapabilityException
			currentValueTextBox.Text = ex.Message
		End Try
	End Sub

	''' <summary>
	''' Gets information about the current value stored in OneValue container.
	''' </summary>
	''' <param name="deviceCapabilityValue"></param>
	Private Sub AddCapOneCurrentValueToForm(deviceCapabilityValue As TwainOneValueContainer)
		If deviceCapabilityValue.EnumValue IsNot Nothing Then
			currentValueTextBox.Text = String.Format("{0} [{1}]", deviceCapabilityValue.Value, deviceCapabilityValue.EnumValue)
		Else
			currentValueTextBox.Text = deviceCapabilityValue.Value.ToString()
		End If
	End Sub

	''' <summary>
	''' Gets information about the current value stored in Range container.
	''' </summary>
	''' <param name="deviceCapabilityValue"></param>
	Private Sub AddCapRangeCurrentValueToForm(deviceCapabilityValue As TwainRangeValueContainer)
		currentValueTextBox.Text = deviceCapabilityValue.Value.ToString()
	End Sub

	''' <summary>
	''' Gets information about the current value stored in Enum container.
	''' </summary>
	''' <param name="deviceCapabilityValue"></param>
	Private Sub AddCapEnumCurrentValueToForm(deviceCapabilityValue As TwainEnumValueContainer)
		Dim valueIndex As Integer = deviceCapabilityValue.ValueIndex

		If valueIndex >= 0 AndAlso valueIndex < deviceCapabilityValue.Values.Length Then
			If deviceCapabilityValue.EnumValues IsNot Nothing Then
				currentValueTextBox.Text = String.Format("{0} [{1}], Index={2}", deviceCapabilityValue.Values.GetValue(valueIndex), deviceCapabilityValue.EnumValues.GetValue(valueIndex), valueIndex)
			Else
				currentValueTextBox.Text = String.Format("{0}, Index={1}", deviceCapabilityValue.Values.GetValue(valueIndex), valueIndex)
			End If
		End If
	End Sub

	''' <summary>
	''' Gets information about the default value stored in Range container.
	''' </summary>
	''' <param name="deviceCapabilityValue"></param>
	Private Sub AddCapRangeDefaultValueToForm(deviceCapabilityValue As TwainRangeValueContainer)
		defaultValueTextBox.Text = deviceCapabilityValue.DefaultValue.ToString()
	End Sub

	''' <summary>
	''' Gets information about the default value stored in Enum container.
	''' </summary>
	''' <param name="deviceCapabilityValue"></param>
	Private Sub AddCapEnumDefaultValueToForm(deviceCapabilityValue As TwainEnumValueContainer)
		Dim defaultValueIndex As Integer = deviceCapabilityValue.DefaultValueIndex
		If deviceCapabilityValue.EnumValues IsNot Nothing Then
			If defaultValueIndex >= 0 AndAlso defaultValueIndex < deviceCapabilityValue.EnumValues.Length Then
				defaultValueTextBox.Text = String.Format("{0} [{1}]", defaultValueIndex, deviceCapabilityValue.EnumValues.GetValue(defaultValueIndex))
			End If
		Else
			defaultValueTextBox.Text = defaultValueIndex.ToString()
		End If
	End Sub

	''' <summary>
	''' Gets information about the minimal value stored in Enum container.
	''' </summary>
	''' <param name="deviceCapabilityValue"></param>
	Private Sub AddCapMinValueToForm(deviceCapabilityValue As TwainRangeValueContainer)
		minValueTextBox.Text = deviceCapabilityValue.MinValue.ToString()
	End Sub

	''' <summary>
	''' Gets information about the maximal value stored in Enum container.
	''' </summary>
	''' <param name="deviceCapabilityValue"></param>
	Private Sub AddCapMaxValueToForm(deviceCapabilityValue As TwainRangeValueContainer)
		maxValueTextBox.Text = deviceCapabilityValue.MaxValue.ToString()
	End Sub

	''' <summary>
	''' Gets information about the step size of value stored in Enum container.
	''' </summary>
	''' <param name="deviceCapabilityValue"></param>
	Private Sub AddCapStepSizeToForm(deviceCapabilityValue As TwainRangeValueContainer)
		stepSizeTextBox.Text = deviceCapabilityValue.StepSize.ToString()
	End Sub

	''' <summary>
	''' Gets information about the supported values stored in Array container.
	''' </summary>
	''' <param name="deviceCapabilityValue"></param>
	Private Sub AddCapValuesToForm(deviceCapabilityValue As TwainArrayValueContainer)
		If deviceCapabilityValue.Values Is Nothing Then
			Return
		End If

		If deviceCapabilityValue.EnumValues IsNot Nothing Then
			For i As Integer = 0 To deviceCapabilityValue.Values.Length - 1
				supportedValuesListBox.Items.Add(String.Format("{0} [{1}]", deviceCapabilityValue.Values.GetValue(i), deviceCapabilityValue.EnumValues.GetValue(i)))
			Next
		Else
			For i As Integer = 0 To deviceCapabilityValue.Values.Length - 1
				supportedValuesListBox.Items.Add(deviceCapabilityValue.Values.GetValue(i))
			Next
		End If
	End Sub

	#End Region


	#Region "Copy values of all capabilities to clipboard"

	''' <summary>
	''' Copies information about all capabilities to the clipboard.
	''' </summary>
	''' <param name="sender"></param>
	''' <param name="e"></param>
	Private Sub copyToClipboardButton_Click(sender As Object, e As EventArgs)
		If _device.State = DeviceState.Closed Then
			MessageBox.Show("Device is not open.")
			Return
		End If

		Cursor = Cursors.WaitCursor

		Dim capsInfo As New StringBuilder()

		' get main information about the device
		capsInfo.Append(String.Format("Manufacturer: {0}{1}", _device.Info.Manufacturer, Environment.NewLine))
		capsInfo.Append(String.Format("Product family: {0}{1}", _device.Info.ProductFamily, Environment.NewLine))
		capsInfo.Append(String.Format("Product name: {0}{1}", _device.Info.ProductName, Environment.NewLine))
		capsInfo.Append(String.Format("Driver version: {0}{1}", _device.Info.DriverVersion, Environment.NewLine))
		capsInfo.Append(String.Format("TWAIN version: {0}{1}", _device.Info.TwainVersion, Environment.NewLine))
		capsInfo.Append(String.Format("TWAIN 2.0 compatible: {0}{1}", _device.Info.IsTwain2Compatible, Environment.NewLine))
		capsInfo.Append(String.Format("Flatbed present: {0}{1}", _device.HasFlatbed, Environment.NewLine))
		capsInfo.Append(String.Format("Feeder present: {0}{1}{1}", _device.HasFeeder, Environment.NewLine))

		' get information about capabilities of device
		Dim deviceCapability As DeviceCapability
		For i As Integer = 0 To _device.Capabilities.Count - 1
			Try
				deviceCapability = _device.Capabilities(i)

				capsInfo.Append(String.Format("Capability: {0}{1}", deviceCapability, Environment.NewLine))

				Dim capValue As TwainValueContainerBase = deviceCapability.GetValue()

				Dim capUsageMode As DeviceCapabilityUsageMode = deviceCapability.UsageMode
				capsInfo.Append(String.Format("  Supported usage modes: {0}{1}", capUsageMode, Environment.NewLine))

				If capValue IsNot Nothing Then
					If (capUsageMode And DeviceCapabilityUsageMode.[Get]) <> 0 Then
						AddCapInfoToCapsInfo(DeviceCapabilityUsageMode.[Get], capValue, capsInfo)
					End If
					If (capUsageMode And DeviceCapabilityUsageMode.GetCurrent) <> 0 Then
						AddCapInfoToCapsInfo(DeviceCapabilityUsageMode.GetCurrent, deviceCapability.GetCurrentValue(), capsInfo)
					End If
					If (capUsageMode And DeviceCapabilityUsageMode.GetDefault) <> 0 Then
						AddCapInfoToCapsInfo(DeviceCapabilityUsageMode.GetDefault, deviceCapability.GetDefaultValue(), capsInfo)
					End If
				Else
					capsInfo.Append(String.Format("  Value: NULL{0}", Environment.NewLine))
				End If
			Catch generatedExceptionName As TwainDeviceException
			Catch generatedExceptionName As TwainDeviceCapabilityException
			End Try
			capsInfo.Append(Environment.NewLine)
		Next
		capsInfo.Append(Environment.NewLine)

		' get information about image layouts
		Try
			capsInfo.Append(String.Format("Default image layout: {0}{1}", _device.ImageLayout.GetDefault(), Environment.NewLine))
			capsInfo.Append(Environment.NewLine)
		Catch generatedExceptionName As TwainDeviceException
		End Try

        ' get information about cameras of device
        Dim deviceCameras As DeviceCamera() = _device.Cameras.GetCameras()
        If deviceCameras.Length > 0 Then
            For i As Integer = 0 To deviceCameras.Length - 1
                capsInfo.Append(String.Format("Camera{0}: {1}{2}", i, deviceCameras(i), Environment.NewLine))
            Next
            capsInfo.Append(Environment.NewLine)
        End If


		' copy info about device to clipboard
		Clipboard.SetText(capsInfo.ToString())

		Cursor = Cursors.[Default]

		MessageBox.Show("Information about device capabilities is copied to clipboard.")
	End Sub

	''' <summary>
	''' Adds information about the value of capability in specified usage mode to the string builder.
	''' </summary>
	''' <param name="capUsageMode"></param>
	''' <param name="capValue"></param>
	''' <param name="capsInfo"></param>
	Private Sub AddCapInfoToCapsInfo(capUsageMode As DeviceCapabilityUsageMode, capValue As TwainValueContainerBase, capsInfo As StringBuilder)
		capsInfo.Append(String.Format("  Usage mode: {0}{1}", capUsageMode, Environment.NewLine))
		capsInfo.Append(String.Format("    Value container type: {0}{1}", capValue.ContainerType, Environment.NewLine))

		Select Case capValue.ContainerType
			Case TwainValueContainerType.OneValue
				Dim oneDeviceCapabilityValue As TwainOneValueContainer = DirectCast(capValue, TwainOneValueContainer)
				AddCapOneCurrentValueInfoToCapsInfo(oneDeviceCapabilityValue, capsInfo)
				Exit Select

			Case TwainValueContainerType.Range
				Dim rangeDeviceCapabilityValue As TwainRangeValueContainer = DirectCast(capValue, TwainRangeValueContainer)
				AddCapRangeCurrentValueInfoToCapsInfo(rangeDeviceCapabilityValue, capsInfo)
				AddCapRangeDefaultValueInfoToCapsInfo(rangeDeviceCapabilityValue, capsInfo)
				AddCapMinValueInfoToCapsInfo(rangeDeviceCapabilityValue, capsInfo)
				AddCapMaxValueInfoToCapsInfo(rangeDeviceCapabilityValue, capsInfo)
				AddCapStepSizeInfoToCapsInfo(rangeDeviceCapabilityValue, capsInfo)
				Exit Select

			Case TwainValueContainerType.[Enum]
				Dim enumDeviceCapabilityValue As TwainEnumValueContainer = DirectCast(capValue, TwainEnumValueContainer)
				AddCapEnumCurrentValueInfoToCapsInfo(enumDeviceCapabilityValue, capsInfo)
				AddCapEnumDefaultValueInfoToCapsInfo(enumDeviceCapabilityValue, capsInfo)
				AddCapValuesInfoToCapsInfo(enumDeviceCapabilityValue, capsInfo)
				Exit Select

			Case TwainValueContainerType.Array
				Dim arrayDeviceCapabilityValue As TwainArrayValueContainer = DirectCast(capValue, TwainArrayValueContainer)
				AddCapValuesInfoToCapsInfo(arrayDeviceCapabilityValue, capsInfo)
				Exit Select
		End Select
	End Sub

	''' <summary>
	''' Gets information about the current value stored in OneValue container.
	''' </summary>
	''' <param name="deviceCapabilityValue"></param>
	''' <param name="capsInfo"></param>
	Private Sub AddCapOneCurrentValueInfoToCapsInfo(deviceCapabilityValue As TwainOneValueContainer, capsInfo As StringBuilder)
		If deviceCapabilityValue.EnumValue IsNot Nothing Then
			capsInfo.Append(String.Format("    Current value: {0}[{1}] ({2}){3}", deviceCapabilityValue.Value, deviceCapabilityValue.EnumValue, deviceCapabilityValue.Value.[GetType](), Environment.NewLine))
		Else
			capsInfo.Append(String.Format("    Current value: {0} ({1}){2}", deviceCapabilityValue.Value, deviceCapabilityValue.Value.[GetType](), Environment.NewLine))
		End If
	End Sub

	''' <summary>
	''' Gets information about the current value stored in Range container.
	''' </summary>
	''' <param name="deviceCapabilityValue"></param>
	''' <param name="capsInfo"></param>
	Private Sub AddCapRangeCurrentValueInfoToCapsInfo(deviceCapabilityValue As TwainRangeValueContainer, capsInfo As StringBuilder)
		capsInfo.Append(String.Format("    Current value: {0} ({1}){2}", deviceCapabilityValue.Value, deviceCapabilityValue.Value.[GetType](), Environment.NewLine))
	End Sub

	''' <summary>
	''' Gets information about the current value stored in Enum container.
	''' </summary>
	''' <param name="deviceCapabilityValue"></param>
	''' <param name="capsInfo"></param>
	Private Sub AddCapEnumCurrentValueInfoToCapsInfo(deviceCapabilityValue As TwainEnumValueContainer, capsInfo As StringBuilder)
		If deviceCapabilityValue.EnumValues IsNot Nothing Then
			If deviceCapabilityValue.ValueIndex >= 0 AndAlso deviceCapabilityValue.ValueIndex < deviceCapabilityValue.EnumValues.Length Then
				capsInfo.Append(String.Format("    Current value index: {0}[{1}]{2}", deviceCapabilityValue.ValueIndex, deviceCapabilityValue.EnumValues.GetValue(deviceCapabilityValue.ValueIndex), Environment.NewLine))
			Else
				capsInfo.Append(String.Format("    Current value index: {0}[WRONG VALUE INDEX]{1}", deviceCapabilityValue.ValueIndex, Environment.NewLine))
			End If
		Else
			capsInfo.Append(String.Format("    Current value index: {0}{1}", deviceCapabilityValue.ValueIndex, Environment.NewLine))
		End If
	End Sub

	''' <summary>
	''' Gets information about the default value stored in Range container.
	''' </summary>
	''' <param name="deviceCapabilityValue"></param>
	''' <param name="capsInfo"></param>
	Private Sub AddCapRangeDefaultValueInfoToCapsInfo(deviceCapabilityValue As TwainRangeValueContainer, capsInfo As StringBuilder)
		capsInfo.Append(String.Format("    Default value: {0} ({1}){2}", deviceCapabilityValue.DefaultValue, deviceCapabilityValue.DefaultValue.[GetType](), Environment.NewLine))
	End Sub

	''' <summary>
	''' Gets information about the default value stored in Enum container.
	''' </summary>
	''' <param name="deviceCapabilityValue"></param>
	''' <param name="capsInfo"></param>
	Private Sub AddCapEnumDefaultValueInfoToCapsInfo(deviceCapabilityValue As TwainEnumValueContainer, capsInfo As StringBuilder)
		If deviceCapabilityValue.EnumValues IsNot Nothing Then
			If deviceCapabilityValue.DefaultValueIndex >= 0 AndAlso deviceCapabilityValue.DefaultValueIndex < deviceCapabilityValue.EnumValues.Length Then
				capsInfo.Append(String.Format("    Default value index: {0}[{1}]{2}", deviceCapabilityValue.DefaultValueIndex, deviceCapabilityValue.EnumValues.GetValue(deviceCapabilityValue.DefaultValueIndex), Environment.NewLine))
			Else
				capsInfo.Append(String.Format("    Default value index: {0}[WRONG DEFAULT VALUE INDEX]{1}", deviceCapabilityValue.DefaultValueIndex, Environment.NewLine))
			End If
		Else
			capsInfo.Append(String.Format("    Default value index: {0}{1}", deviceCapabilityValue.DefaultValueIndex, Environment.NewLine))
		End If
	End Sub

	''' <summary>
	''' Gets information about the minimal value stored in Enum container.
	''' </summary>
	''' <param name="deviceCapabilityValue"></param>
	''' <param name="capsInfo"></param>
	Private Sub AddCapMinValueInfoToCapsInfo(deviceCapabilityValue As TwainRangeValueContainer, capsInfo As StringBuilder)
		capsInfo.Append(String.Format("    Min value: {0} ({1}){2}", deviceCapabilityValue.MinValue, deviceCapabilityValue.MinValue.[GetType](), Environment.NewLine))
	End Sub

	''' <summary>
	''' Gets information about the maximal value stored in Enum container.
	''' </summary>
	''' <param name="deviceCapabilityValue"></param>
	''' <param name="capsInfo"></param>
	Private Sub AddCapMaxValueInfoToCapsInfo(deviceCapabilityValue As TwainRangeValueContainer, capsInfo As StringBuilder)
		capsInfo.Append(String.Format("    Max value: {0} ({1}){2}", deviceCapabilityValue.MaxValue, deviceCapabilityValue.MaxValue.[GetType](), Environment.NewLine))
	End Sub

	''' <summary>
	''' Gets information about the step size of value stored in Enum container.
	''' </summary>
	''' <param name="deviceCapabilityValue"></param>
	''' <param name="capsInfo"></param>
	Private Sub AddCapStepSizeInfoToCapsInfo(deviceCapabilityValue As TwainRangeValueContainer, capsInfo As StringBuilder)
		capsInfo.Append(String.Format("    Step size: {0} ({1}){2}", deviceCapabilityValue.StepSize, deviceCapabilityValue.StepSize.[GetType](), Environment.NewLine))
	End Sub

	''' <summary>
	''' Gets information about the supported values stored in Array container.
	''' </summary>
	''' <param name="deviceCapabilityValue"></param>
	''' <param name="capsInfo"></param>
	Private Sub AddCapValuesInfoToCapsInfo(deviceCapabilityValue As TwainArrayValueContainer, capsInfo As StringBuilder)
		If deviceCapabilityValue.Values Is Nothing OrElse deviceCapabilityValue.Values.Length = 0 Then
			capsInfo.Append(String.Format("    Supported values[0]:{0}", Environment.NewLine))
			Return
		End If

		Dim values As New StringBuilder()

		If deviceCapabilityValue.Values.GetValue(0).[GetType]().Equals(GetType(String)) Then
			For j As Integer = 0 To deviceCapabilityValue.Values.Length - 1
				values.Append(String.Format("""{0}"", ", deviceCapabilityValue.Values.GetValue(j)))
			Next
		Else
			If deviceCapabilityValue.EnumValues IsNot Nothing Then
				For i As Integer = 0 To deviceCapabilityValue.Values.Length - 1
					values.Append(String.Format("{0} [{1}], ", deviceCapabilityValue.Values.GetValue(i), deviceCapabilityValue.EnumValues.GetValue(i)))
				Next
			Else
				For i As Integer = 0 To deviceCapabilityValue.Values.Length - 1
					values.Append(String.Format("{0}, ", deviceCapabilityValue.Values.GetValue(i)))
				Next
			End If
		End If

		capsInfo.Append(String.Format("    Supported values[{0}, {1}]: {2}{3}", deviceCapabilityValue.Values.Length, deviceCapabilityValue.Values.GetValue(0).[GetType](), values, Environment.NewLine))
	End Sub

	#End Region

	#End Region

End Class
