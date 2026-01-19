Partial Class DevCapsForm
	''' <summary>
	''' Required designer variable.
	''' </summary>
	Private components As System.ComponentModel.IContainer = Nothing

	''' <summary>
	''' Clean up any resources being used.
	''' </summary>
	''' <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
	Protected Overrides Sub Dispose(disposing As Boolean)
		If disposing AndAlso (components IsNot Nothing) Then
			components.Dispose()
		End If
		MyBase.Dispose(disposing)
	End Sub

	#Region "Windows Form Designer generated code"

	''' <summary>
	''' Required method for Designer support - do not modify
	''' the contents of this method with the code editor.
	''' </summary>
	Private Sub InitializeComponent()
		Me.supportedCapabilitiesListBox = New System.Windows.Forms.ListBox()
		Me.label1 = New System.Windows.Forms.Label()
		Me.closeButton = New System.Windows.Forms.Button()
		Me.label2 = New System.Windows.Forms.Label()
		Me.currentValueTextBox = New System.Windows.Forms.TextBox()
		Me.defaultValueTextBox = New System.Windows.Forms.TextBox()
		Me.label3 = New System.Windows.Forms.Label()
		Me.label4 = New System.Windows.Forms.Label()
		Me.supportedValuesListBox = New System.Windows.Forms.ListBox()
		Me.usageModeTextBox = New System.Windows.Forms.TextBox()
		Me.label5 = New System.Windows.Forms.Label()
		Me.copyToClipboardButton = New System.Windows.Forms.Button()
		Me.deviceManufacturerLabel = New System.Windows.Forms.Label()
		Me.deviceProductFamilyLabel = New System.Windows.Forms.Label()
		Me.deviceProductNameLabel = New System.Windows.Forms.Label()
		Me.driverTwainVersionLabel = New System.Windows.Forms.Label()
		Me.driverTwain2CompatibleLabel = New System.Windows.Forms.Label()
		Me.feederPresentLabel = New System.Windows.Forms.Label()
		Me.flatbedPresentLabel = New System.Windows.Forms.Label()
		Me.maxValueTextBox = New System.Windows.Forms.TextBox()
		Me.label6 = New System.Windows.Forms.Label()
		Me.minValueTextBox = New System.Windows.Forms.TextBox()
		Me.label7 = New System.Windows.Forms.Label()
		Me.containerTypeTextBox = New System.Windows.Forms.TextBox()
		Me.label8 = New System.Windows.Forms.Label()
		Me.getMethodComboBox = New System.Windows.Forms.ComboBox()
		Me.label9 = New System.Windows.Forms.Label()
		Me.stepSizeTextBox = New System.Windows.Forms.TextBox()
		Me.label10 = New System.Windows.Forms.Label()
		Me.valueTypeTextBox = New System.Windows.Forms.TextBox()
		Me.label11 = New System.Windows.Forms.Label()
		Me.SuspendLayout()
		' 
		' supportedCapabilitiesListBox
		' 
		Me.supportedCapabilitiesListBox.FormattingEnabled = True
		Me.supportedCapabilitiesListBox.Location = New System.Drawing.Point(12, 124)
		Me.supportedCapabilitiesListBox.Name = "supportedCapabilitiesListBox"
		Me.supportedCapabilitiesListBox.Size = New System.Drawing.Size(231, 511)
		Me.supportedCapabilitiesListBox.TabIndex = 0
		AddHandler Me.supportedCapabilitiesListBox.SelectedIndexChanged, New System.EventHandler(AddressOf Me.supportedCapabilitiesListBox_SelectedIndexChanged)
		' 
		' label1
		' 
		Me.label1.AutoSize = True
		Me.label1.Location = New System.Drawing.Point(9, 108)
		Me.label1.Name = "label1"
		Me.label1.Size = New System.Drawing.Size(114, 13)
		Me.label1.TabIndex = 1
		Me.label1.Text = "Supported capabilities:"
		' 
		' closeButton
		' 
		Me.closeButton.DialogResult = System.Windows.Forms.DialogResult.Cancel
		Me.closeButton.Location = New System.Drawing.Point(342, 643)
		Me.closeButton.Name = "closeButton"
		Me.closeButton.Size = New System.Drawing.Size(156, 30)
		Me.closeButton.TabIndex = 2
		Me.closeButton.Text = "Close"
		Me.closeButton.UseVisualStyleBackColor = True
		' 
		' label2
		' 
		Me.label2.AutoSize = True
		Me.label2.Location = New System.Drawing.Point(257, 188)
		Me.label2.Name = "label2"
		Me.label2.Size = New System.Drawing.Size(73, 13)
		Me.label2.TabIndex = 3
		Me.label2.Text = "Current value:"
		' 
		' currentValueTextBox
		' 
		Me.currentValueTextBox.Location = New System.Drawing.Point(260, 204)
		Me.currentValueTextBox.Name = "currentValueTextBox"
		Me.currentValueTextBox.[ReadOnly] = True
		Me.currentValueTextBox.Size = New System.Drawing.Size(401, 20)
		Me.currentValueTextBox.TabIndex = 4
		' 
		' defaultValueTextBox
		' 
		Me.defaultValueTextBox.Location = New System.Drawing.Point(260, 285)
		Me.defaultValueTextBox.Name = "defaultValueTextBox"
		Me.defaultValueTextBox.[ReadOnly] = True
		Me.defaultValueTextBox.Size = New System.Drawing.Size(172, 20)
		Me.defaultValueTextBox.TabIndex = 6
		' 
		' label3
		' 
		Me.label3.AutoSize = True
		Me.label3.Location = New System.Drawing.Point(257, 269)
		Me.label3.Name = "label3"
		Me.label3.Size = New System.Drawing.Size(73, 13)
		Me.label3.TabIndex = 5
		Me.label3.Text = "Default value:"
		' 
		' label4
		' 
		Me.label4.AutoSize = True
		Me.label4.Location = New System.Drawing.Point(257, 314)
		Me.label4.Name = "label4"
		Me.label4.Size = New System.Drawing.Size(93, 13)
		Me.label4.TabIndex = 7
		Me.label4.Text = "Supported values:"
		' 
		' supportedValuesListBox
		' 
		Me.supportedValuesListBox.Location = New System.Drawing.Point(260, 332)
		Me.supportedValuesListBox.Name = "supportedValuesListBox"
		Me.supportedValuesListBox.Size = New System.Drawing.Size(401, 303)
		Me.supportedValuesListBox.TabIndex = 8
		' 
		' usageModeTextBox
		' 
		Me.usageModeTextBox.Location = New System.Drawing.Point(260, 125)
		Me.usageModeTextBox.Name = "usageModeTextBox"
		Me.usageModeTextBox.[ReadOnly] = True
		Me.usageModeTextBox.Size = New System.Drawing.Size(401, 20)
		Me.usageModeTextBox.TabIndex = 10
		' 
		' label5
		' 
		Me.label5.AutoSize = True
		Me.label5.Location = New System.Drawing.Point(257, 108)
		Me.label5.Name = "label5"
		Me.label5.Size = New System.Drawing.Size(70, 13)
		Me.label5.TabIndex = 9
		Me.label5.Text = "Usage mode:"
		' 
		' copyToClipboardButton
		' 
		Me.copyToClipboardButton.Location = New System.Drawing.Point(174, 643)
		Me.copyToClipboardButton.Name = "copyToClipboardButton"
		Me.copyToClipboardButton.Size = New System.Drawing.Size(156, 30)
		Me.copyToClipboardButton.TabIndex = 11
		Me.copyToClipboardButton.Text = "Copy to clipboard"
		Me.copyToClipboardButton.UseVisualStyleBackColor = True
		AddHandler Me.copyToClipboardButton.Click, New System.EventHandler(AddressOf Me.copyToClipboardButton_Click)
		' 
		' deviceManufacturerLabel
		' 
		Me.deviceManufacturerLabel.AutoSize = True
		Me.deviceManufacturerLabel.Location = New System.Drawing.Point(9, 9)
		Me.deviceManufacturerLabel.Name = "deviceManufacturerLabel"
		Me.deviceManufacturerLabel.Size = New System.Drawing.Size(73, 13)
		Me.deviceManufacturerLabel.TabIndex = 12
		Me.deviceManufacturerLabel.Text = "Manufacturer:"
		' 
		' deviceProductFamilyLabel
		' 
		Me.deviceProductFamilyLabel.AutoSize = True
		Me.deviceProductFamilyLabel.Location = New System.Drawing.Point(9, 27)
		Me.deviceProductFamilyLabel.Name = "deviceProductFamilyLabel"
		Me.deviceProductFamilyLabel.Size = New System.Drawing.Size(76, 13)
		Me.deviceProductFamilyLabel.TabIndex = 13
		Me.deviceProductFamilyLabel.Text = "Product family:"
		' 
		' deviceProductNameLabel
		' 
		Me.deviceProductNameLabel.AutoSize = True
		Me.deviceProductNameLabel.Location = New System.Drawing.Point(9, 45)
		Me.deviceProductNameLabel.Name = "deviceProductNameLabel"
		Me.deviceProductNameLabel.Size = New System.Drawing.Size(76, 13)
		Me.deviceProductNameLabel.TabIndex = 14
		Me.deviceProductNameLabel.Text = "Product name:"
		' 
		' driverTwainVersionLabel
		' 
		Me.driverTwainVersionLabel.AutoSize = True
		Me.driverTwainVersionLabel.Location = New System.Drawing.Point(9, 63)
		Me.driverTwainVersionLabel.Name = "driverTwainVersionLabel"
		Me.driverTwainVersionLabel.Size = New System.Drawing.Size(83, 13)
		Me.driverTwainVersionLabel.TabIndex = 15
		Me.driverTwainVersionLabel.Text = "TWAIN version:"
		' 
		' driverTwain2CompatibleLabel
		' 
		Me.driverTwain2CompatibleLabel.AutoSize = True
		Me.driverTwain2CompatibleLabel.Location = New System.Drawing.Point(254, 63)
		Me.driverTwain2CompatibleLabel.Name = "driverTwain2CompatibleLabel"
		Me.driverTwain2CompatibleLabel.Size = New System.Drawing.Size(118, 13)
		Me.driverTwain2CompatibleLabel.TabIndex = 16
		Me.driverTwain2CompatibleLabel.Text = "TWAIN 2.0 compatible:"
		' 
		' feederPresentLabel
		' 
		Me.feederPresentLabel.AutoSize = True
		Me.feederPresentLabel.Location = New System.Drawing.Point(254, 82)
		Me.feederPresentLabel.Name = "feederPresentLabel"
		Me.feederPresentLabel.Size = New System.Drawing.Size(81, 13)
		Me.feederPresentLabel.TabIndex = 18
		Me.feederPresentLabel.Text = "Feeder present:"
		' 
		' flatbedPresentLabel
		' 
		Me.flatbedPresentLabel.AutoSize = True
		Me.flatbedPresentLabel.Location = New System.Drawing.Point(9, 82)
		Me.flatbedPresentLabel.Name = "flatbedPresentLabel"
		Me.flatbedPresentLabel.Size = New System.Drawing.Size(83, 13)
		Me.flatbedPresentLabel.TabIndex = 17
		Me.flatbedPresentLabel.Text = "Flatbed present:"
		' 
		' maxValueTextBox
		' 
		Me.maxValueTextBox.Location = New System.Drawing.Point(489, 245)
		Me.maxValueTextBox.Name = "maxValueTextBox"
		Me.maxValueTextBox.[ReadOnly] = True
		Me.maxValueTextBox.Size = New System.Drawing.Size(172, 20)
		Me.maxValueTextBox.TabIndex = 22
		' 
		' label6
		' 
		Me.label6.AutoSize = True
		Me.label6.Location = New System.Drawing.Point(486, 229)
		Me.label6.Name = "label6"
		Me.label6.Size = New System.Drawing.Size(59, 13)
		Me.label6.TabIndex = 21
		Me.label6.Text = "Max value:"
		' 
		' minValueTextBox
		' 
		Me.minValueTextBox.Location = New System.Drawing.Point(260, 245)
		Me.minValueTextBox.Name = "minValueTextBox"
		Me.minValueTextBox.[ReadOnly] = True
		Me.minValueTextBox.Size = New System.Drawing.Size(172, 20)
		Me.minValueTextBox.TabIndex = 20
		' 
		' label7
		' 
		Me.label7.AutoSize = True
		Me.label7.Location = New System.Drawing.Point(257, 229)
		Me.label7.Name = "label7"
		Me.label7.Size = New System.Drawing.Size(56, 13)
		Me.label7.TabIndex = 19
		Me.label7.Text = "Min value:"
		' 
		' containerTypeTextBox
		' 
		Me.containerTypeTextBox.Location = New System.Drawing.Point(454, 163)
		Me.containerTypeTextBox.Name = "containerTypeTextBox"
		Me.containerTypeTextBox.[ReadOnly] = True
		Me.containerTypeTextBox.Size = New System.Drawing.Size(92, 20)
		Me.containerTypeTextBox.TabIndex = 24
		' 
		' label8
		' 
		Me.label8.AutoSize = True
		Me.label8.Location = New System.Drawing.Point(451, 147)
		Me.label8.Name = "label8"
		Me.label8.Size = New System.Drawing.Size(78, 13)
		Me.label8.TabIndex = 23
		Me.label8.Text = "Container type:"
		' 
		' getMethodComboBox
		' 
		Me.getMethodComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		Me.getMethodComboBox.FormattingEnabled = True
		Me.getMethodComboBox.Location = New System.Drawing.Point(260, 162)
		Me.getMethodComboBox.Name = "getMethodComboBox"
		Me.getMethodComboBox.Size = New System.Drawing.Size(172, 21)
		Me.getMethodComboBox.TabIndex = 25
		AddHandler Me.getMethodComboBox.SelectedIndexChanged, New System.EventHandler(AddressOf Me.getMethodComboBox_SelectedIndexChanged)
		' 
		' label9
		' 
		Me.label9.AutoSize = True
		Me.label9.Location = New System.Drawing.Point(257, 148)
		Me.label9.Name = "label9"
		Me.label9.Size = New System.Drawing.Size(56, 13)
		Me.label9.TabIndex = 26
		Me.label9.Text = "Operation:"
		' 
		' stepSizeTextBox
		' 
		Me.stepSizeTextBox.Location = New System.Drawing.Point(489, 285)
		Me.stepSizeTextBox.Name = "stepSizeTextBox"
		Me.stepSizeTextBox.[ReadOnly] = True
		Me.stepSizeTextBox.Size = New System.Drawing.Size(172, 20)
		Me.stepSizeTextBox.TabIndex = 28
		' 
		' label10
		' 
		Me.label10.AutoSize = True
		Me.label10.Location = New System.Drawing.Point(486, 269)
		Me.label10.Name = "label10"
		Me.label10.Size = New System.Drawing.Size(53, 13)
		Me.label10.TabIndex = 27
		Me.label10.Text = "Step size:"
		' 
		' valueTypeTextBox
		' 
		Me.valueTypeTextBox.Location = New System.Drawing.Point(569, 163)
		Me.valueTypeTextBox.Name = "valueTypeTextBox"
		Me.valueTypeTextBox.[ReadOnly] = True
		Me.valueTypeTextBox.Size = New System.Drawing.Size(92, 20)
		Me.valueTypeTextBox.TabIndex = 30
		' 
		' label11
		' 
		Me.label11.AutoSize = True
		Me.label11.Location = New System.Drawing.Point(566, 147)
		Me.label11.Name = "label11"
		Me.label11.Size = New System.Drawing.Size(60, 13)
		Me.label11.TabIndex = 29
		Me.label11.Text = "Value type:"
		' 
		' DevCapsForm
		' 
		Me.AutoScaleDimensions = New System.Drawing.SizeF(6F, 13F)
		Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
		Me.CancelButton = Me.closeButton
		Me.ClientSize = New System.Drawing.Size(673, 681)
		Me.Controls.Add(Me.valueTypeTextBox)
		Me.Controls.Add(Me.label11)
		Me.Controls.Add(Me.stepSizeTextBox)
		Me.Controls.Add(Me.label10)
		Me.Controls.Add(Me.label9)
		Me.Controls.Add(Me.getMethodComboBox)
		Me.Controls.Add(Me.containerTypeTextBox)
		Me.Controls.Add(Me.label8)
		Me.Controls.Add(Me.maxValueTextBox)
		Me.Controls.Add(Me.label6)
		Me.Controls.Add(Me.minValueTextBox)
		Me.Controls.Add(Me.label7)
		Me.Controls.Add(Me.feederPresentLabel)
		Me.Controls.Add(Me.flatbedPresentLabel)
		Me.Controls.Add(Me.driverTwain2CompatibleLabel)
		Me.Controls.Add(Me.driverTwainVersionLabel)
		Me.Controls.Add(Me.deviceProductNameLabel)
		Me.Controls.Add(Me.deviceProductFamilyLabel)
		Me.Controls.Add(Me.deviceManufacturerLabel)
		Me.Controls.Add(Me.copyToClipboardButton)
		Me.Controls.Add(Me.usageModeTextBox)
		Me.Controls.Add(Me.label5)
		Me.Controls.Add(Me.supportedValuesListBox)
		Me.Controls.Add(Me.label4)
		Me.Controls.Add(Me.defaultValueTextBox)
		Me.Controls.Add(Me.label3)
		Me.Controls.Add(Me.currentValueTextBox)
		Me.Controls.Add(Me.label2)
		Me.Controls.Add(Me.closeButton)
		Me.Controls.Add(Me.label1)
		Me.Controls.Add(Me.supportedCapabilitiesListBox)
		Me.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog
		Me.MaximizeBox = False
		Me.MinimizeBox = False
		Me.Name = "DevCapsForm"
		Me.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent
		Me.Text = "Device capabilities"
		AddHandler Me.Load, New System.EventHandler(AddressOf Me.DevCapsForm_Load)
		AddHandler Me.FormClosing, New System.Windows.Forms.FormClosingEventHandler(AddressOf Me.DevCapsForm_FormClosing)
		Me.ResumeLayout(False)
		Me.PerformLayout()

	End Sub

	#End Region

	Private WithEvents supportedCapabilitiesListBox As System.Windows.Forms.ListBox
	Private WithEvents label1 As System.Windows.Forms.Label
	Private WithEvents closeButton As System.Windows.Forms.Button
	Private WithEvents label2 As System.Windows.Forms.Label
	Private WithEvents currentValueTextBox As System.Windows.Forms.TextBox
	Private WithEvents defaultValueTextBox As System.Windows.Forms.TextBox
	Private WithEvents label3 As System.Windows.Forms.Label
	Private WithEvents label4 As System.Windows.Forms.Label
	Private WithEvents supportedValuesListBox As System.Windows.Forms.ListBox
	Private WithEvents usageModeTextBox As System.Windows.Forms.TextBox
	Private WithEvents label5 As System.Windows.Forms.Label
	Private WithEvents copyToClipboardButton As System.Windows.Forms.Button
	Private WithEvents deviceManufacturerLabel As System.Windows.Forms.Label
	Private WithEvents deviceProductFamilyLabel As System.Windows.Forms.Label
	Private WithEvents deviceProductNameLabel As System.Windows.Forms.Label
	Private WithEvents driverTwainVersionLabel As System.Windows.Forms.Label
	Private WithEvents driverTwain2CompatibleLabel As System.Windows.Forms.Label
	Private WithEvents feederPresentLabel As System.Windows.Forms.Label
	Private WithEvents flatbedPresentLabel As System.Windows.Forms.Label
	Private WithEvents maxValueTextBox As System.Windows.Forms.TextBox
	Private WithEvents label6 As System.Windows.Forms.Label
	Private WithEvents minValueTextBox As System.Windows.Forms.TextBox
	Private WithEvents label7 As System.Windows.Forms.Label
	Private WithEvents containerTypeTextBox As System.Windows.Forms.TextBox
	Private WithEvents label8 As System.Windows.Forms.Label
	Private WithEvents getMethodComboBox As System.Windows.Forms.ComboBox
	Private WithEvents label9 As System.Windows.Forms.Label
	Private WithEvents stepSizeTextBox As System.Windows.Forms.TextBox
	Private WithEvents label10 As System.Windows.Forms.Label
	Private WithEvents valueTypeTextBox As System.Windows.Forms.TextBox
	Private WithEvents label11 As System.Windows.Forms.Label
End Class
