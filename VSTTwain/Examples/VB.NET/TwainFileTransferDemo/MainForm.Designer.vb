Partial Class MainForm
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
		Me.acquireImageWithUIButton = New System.Windows.Forms.Button()
		Me.label2 = New System.Windows.Forms.Label()
		Me.directoryForImagesTextBox = New System.Windows.Forms.TextBox()
		Me.selectDirectoryForImagesButton = New System.Windows.Forms.Button()
		Me.deviceSettingsGroupBox = New System.Windows.Forms.GroupBox()
		Me.supportedCompressionsComboBox = New System.Windows.Forms.ComboBox()
		Me.label4 = New System.Windows.Forms.Label()
		Me.supportedFileFormatsComboBox = New System.Windows.Forms.ComboBox()
		Me.label3 = New System.Windows.Forms.Label()
		Me.devicesComboBox = New System.Windows.Forms.ComboBox()
		Me.label1 = New System.Windows.Forms.Label()
		Me.statusTextBox = New System.Windows.Forms.TextBox()
		Me.folderBrowserDialog1 = New System.Windows.Forms.FolderBrowserDialog()
		Me.acquireImageWithoutUIButton = New System.Windows.Forms.Button()
		Me.deviceSettingsGroupBox.SuspendLayout()
		Me.SuspendLayout()
		' 
		' acquireImageWithUIButton
		' 
		Me.acquireImageWithUIButton.Location = New System.Drawing.Point(194, 143)
		Me.acquireImageWithUIButton.Name = "acquireImageWithUIButton"
		Me.acquireImageWithUIButton.Size = New System.Drawing.Size(175, 36)
		Me.acquireImageWithUIButton.TabIndex = 87
		Me.acquireImageWithUIButton.Text = "Acquire image with UI"
		AddHandler Me.acquireImageWithUIButton.Click, New System.EventHandler(AddressOf Me.acquireImageWithUIButton_Click)
		' 
		' label2
		' 
		Me.label2.AutoSize = True
		Me.label2.Location = New System.Drawing.Point(12, 11)
		Me.label2.Name = "label2"
		Me.label2.Size = New System.Drawing.Size(103, 13)
		Me.label2.TabIndex = 103
		Me.label2.Text = "Directory for images:"
		' 
		' directoryForImagesTextBox
		' 
		Me.directoryForImagesTextBox.Location = New System.Drawing.Point(121, 9)
		Me.directoryForImagesTextBox.Name = "directoryForImagesTextBox"
		Me.directoryForImagesTextBox.[ReadOnly] = True
		Me.directoryForImagesTextBox.Size = New System.Drawing.Size(584, 20)
		Me.directoryForImagesTextBox.TabIndex = 104
		' 
		' selectDirectoryForImagesButton
		' 
		Me.selectDirectoryForImagesButton.Location = New System.Drawing.Point(711, 9)
		Me.selectDirectoryForImagesButton.Name = "selectDirectoryForImagesButton"
		Me.selectDirectoryForImagesButton.Size = New System.Drawing.Size(26, 23)
		Me.selectDirectoryForImagesButton.TabIndex = 105
		Me.selectDirectoryForImagesButton.Text = "..."
		Me.selectDirectoryForImagesButton.UseVisualStyleBackColor = True
		AddHandler Me.selectDirectoryForImagesButton.Click, New System.EventHandler(AddressOf Me.selectDirectoryForImagesButton_Click)
		' 
		' deviceSettingsGroupBox
		' 
		Me.deviceSettingsGroupBox.Controls.Add(Me.supportedCompressionsComboBox)
		Me.deviceSettingsGroupBox.Controls.Add(Me.label4)
		Me.deviceSettingsGroupBox.Controls.Add(Me.supportedFileFormatsComboBox)
		Me.deviceSettingsGroupBox.Controls.Add(Me.label3)
		Me.deviceSettingsGroupBox.Location = New System.Drawing.Point(121, 62)
		Me.deviceSettingsGroupBox.Name = "deviceSettingsGroupBox"
		Me.deviceSettingsGroupBox.Size = New System.Drawing.Size(616, 71)
		Me.deviceSettingsGroupBox.TabIndex = 114
		Me.deviceSettingsGroupBox.TabStop = False
		Me.deviceSettingsGroupBox.Text = "Device settings"
		' 
		' supportedCompressionsComboBox
		' 
		Me.supportedCompressionsComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		Me.supportedCompressionsComboBox.FormattingEnabled = True
		Me.supportedCompressionsComboBox.Location = New System.Drawing.Point(149, 41)
		Me.supportedCompressionsComboBox.Name = "supportedCompressionsComboBox"
		Me.supportedCompressionsComboBox.Size = New System.Drawing.Size(449, 21)
		Me.supportedCompressionsComboBox.TabIndex = 22
		' 
		' label4
		' 
		Me.label4.AutoSize = True
		Me.label4.Location = New System.Drawing.Point(10, 44)
		Me.label4.Name = "label4"
		Me.label4.Size = New System.Drawing.Size(126, 13)
		Me.label4.TabIndex = 21
		Me.label4.Text = "Supported compressions:"
		' 
		' supportedFileFormatsComboBox
		' 
		Me.supportedFileFormatsComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		Me.supportedFileFormatsComboBox.FormattingEnabled = True
		Me.supportedFileFormatsComboBox.Location = New System.Drawing.Point(149, 15)
		Me.supportedFileFormatsComboBox.Name = "supportedFileFormatsComboBox"
		Me.supportedFileFormatsComboBox.Size = New System.Drawing.Size(449, 21)
		Me.supportedFileFormatsComboBox.TabIndex = 1
		' 
		' label3
		' 
		Me.label3.AutoSize = True
		Me.label3.Location = New System.Drawing.Point(10, 18)
		Me.label3.Name = "label3"
		Me.label3.Size = New System.Drawing.Size(112, 13)
		Me.label3.TabIndex = 0
		Me.label3.Text = "Supported file formats:"
		' 
		' devicesComboBox
		' 
		Me.devicesComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		Me.devicesComboBox.Location = New System.Drawing.Point(121, 35)
		Me.devicesComboBox.Name = "devicesComboBox"
		Me.devicesComboBox.Size = New System.Drawing.Size(616, 21)
		Me.devicesComboBox.TabIndex = 110
		AddHandler Me.devicesComboBox.SelectedIndexChanged, New System.EventHandler(AddressOf Me.devicesComboBox_SelectedIndexChanged)
		' 
		' label1
		' 
		Me.label1.Location = New System.Drawing.Point(59, 36)
		Me.label1.Name = "label1"
		Me.label1.Size = New System.Drawing.Size(56, 16)
		Me.label1.TabIndex = 112
		Me.label1.Text = "Devices:"
		' 
		' statusTextBox
		' 
		Me.statusTextBox.Location = New System.Drawing.Point(12, 185)
		Me.statusTextBox.Multiline = True
		Me.statusTextBox.Name = "statusTextBox"
		Me.statusTextBox.Size = New System.Drawing.Size(725, 425)
		Me.statusTextBox.TabIndex = 117
		' 
		' acquireImageWithoutUIButton
		' 
		Me.acquireImageWithoutUIButton.Location = New System.Drawing.Point(379, 143)
		Me.acquireImageWithoutUIButton.Name = "acquireImageWithoutUIButton"
		Me.acquireImageWithoutUIButton.Size = New System.Drawing.Size(175, 36)
		Me.acquireImageWithoutUIButton.TabIndex = 118
		Me.acquireImageWithoutUIButton.Text = "Acquire image without UI"
		AddHandler Me.acquireImageWithoutUIButton.Click, New System.EventHandler(AddressOf Me.acquireImageWithoutUIButton_Click)
		' 
		' MainForm
		' 
		Me.AutoScaleDimensions = New System.Drawing.SizeF(6F, 13F)
		Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
		Me.ClientSize = New System.Drawing.Size(748, 622)
		Me.Controls.Add(Me.acquireImageWithoutUIButton)
		Me.Controls.Add(Me.statusTextBox)
		Me.Controls.Add(Me.deviceSettingsGroupBox)
		Me.Controls.Add(Me.devicesComboBox)
		Me.Controls.Add(Me.label1)
		Me.Controls.Add(Me.selectDirectoryForImagesButton)
		Me.Controls.Add(Me.directoryForImagesTextBox)
		Me.Controls.Add(Me.label2)
		Me.Controls.Add(Me.acquireImageWithUIButton)
		Me.MaximizeBox = False
		Me.Name = "MainForm"
		Me.Text = "VintaSoft TWAIN File Transfer Demo"
		AddHandler Me.Shown, New System.EventHandler(AddressOf Me.MainForm_Shown)
		AddHandler Me.FormClosing, New System.Windows.Forms.FormClosingEventHandler(AddressOf Me.MainForm_FormClosing)
		Me.deviceSettingsGroupBox.ResumeLayout(False)
		Me.deviceSettingsGroupBox.PerformLayout()
		Me.ResumeLayout(False)
		Me.PerformLayout()

	End Sub

	#End Region

	Private WithEvents acquireImageWithUIButton As System.Windows.Forms.Button
	Private WithEvents label2 As System.Windows.Forms.Label
	Private WithEvents directoryForImagesTextBox As System.Windows.Forms.TextBox
	Private WithEvents selectDirectoryForImagesButton As System.Windows.Forms.Button
	Private WithEvents deviceSettingsGroupBox As System.Windows.Forms.GroupBox
	Private WithEvents devicesComboBox As System.Windows.Forms.ComboBox
	Private WithEvents label1 As System.Windows.Forms.Label
	Private WithEvents supportedFileFormatsComboBox As System.Windows.Forms.ComboBox
	Private WithEvents label3 As System.Windows.Forms.Label
	Private WithEvents statusTextBox As System.Windows.Forms.TextBox
	Private WithEvents folderBrowserDialog1 As System.Windows.Forms.FolderBrowserDialog
	Private WithEvents supportedCompressionsComboBox As System.Windows.Forms.ComboBox
	Private WithEvents label4 As System.Windows.Forms.Label
	Private WithEvents acquireImageWithoutUIButton As System.Windows.Forms.Button
End Class

