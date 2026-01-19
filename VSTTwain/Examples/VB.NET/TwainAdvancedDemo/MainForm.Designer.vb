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
        Me.stretchImageCheckBox = New System.Windows.Forms.CheckBox
        Me.saveFileDialog1 = New System.Windows.Forms.SaveFileDialog
        Me.pictureBoxPanel = New System.Windows.Forms.Panel
        Me.pictureBox1 = New System.Windows.Forms.PictureBox
        Me.devicesLabel = New System.Windows.Forms.Label
        Me.selectDefaultDeviceButton = New System.Windows.Forms.Button
        Me.acquireImageButton = New System.Windows.Forms.Button
        Me.openDeviceManagerButton = New System.Windows.Forms.Button
        Me.showIndicatorsCheckBox = New System.Windows.Forms.CheckBox
        Me.imagesToAcquireNumericUpDown = New System.Windows.Forms.NumericUpDown
        Me.adfGroupBox = New System.Windows.Forms.GroupBox
        Me.label1 = New System.Windows.Forms.Label
        Me.imagesToAcquireRadioButton = New System.Windows.Forms.RadioButton
        Me.acquireAllImagesRadioButton = New System.Windows.Forms.RadioButton
        Me.useAdfCheckBox = New System.Windows.Forms.CheckBox
        Me.useDuplexCheckBox = New System.Windows.Forms.CheckBox
        Me.userInterfaceGroupBox = New System.Windows.Forms.GroupBox
        Me.showUICheckBox = New System.Windows.Forms.CheckBox
        Me.modalUICheckBox = New System.Windows.Forms.CheckBox
        Me.disableAfterScanCheckBox = New System.Windows.Forms.CheckBox
        Me.devicesComboBox = New System.Windows.Forms.ComboBox
        Me.twain2CompatibleCheckBox = New System.Windows.Forms.CheckBox
        Me.deleteImageButton = New System.Windows.Forms.Button
        Me.panel1 = New System.Windows.Forms.Panel
        Me.uploadImageButton = New System.Windows.Forms.Button
        Me.saveImageButton = New System.Windows.Forms.Button
        Me.getDeviceInfoButton = New System.Windows.Forms.Button
        Me.imageInfoLabel = New System.Windows.Forms.Label
        Me.nextImageButton = New System.Windows.Forms.Button
        Me.previousImageButton = New System.Windows.Forms.Button
        Me.processImageButton = New System.Windows.Forms.Button
        Me.imageAcquisitionProgressBar = New System.Windows.Forms.ProgressBar
        Me.imageGroupBox = New System.Windows.Forms.GroupBox
        Me.transferModeLabel = New System.Windows.Forms.Label
        Me.transferModeComboBox = New System.Windows.Forms.ComboBox
        Me.resolutionLabel = New System.Windows.Forms.Label
        Me.resolutionComboBox = New System.Windows.Forms.ComboBox
        Me.pixelTypeLabel = New System.Windows.Forms.Label
        Me.pixelTypeComboBox = New System.Windows.Forms.ComboBox
        Me.clearImagesButton = New System.Windows.Forms.Button
        Me.pictureBoxPanel.SuspendLayout()
        CType(Me.pictureBox1, System.ComponentModel.ISupportInitialize).BeginInit()
        CType(Me.imagesToAcquireNumericUpDown, System.ComponentModel.ISupportInitialize).BeginInit()
        Me.adfGroupBox.SuspendLayout()
        Me.userInterfaceGroupBox.SuspendLayout()
        Me.imageGroupBox.SuspendLayout()
        Me.SuspendLayout()
        '
        'stretchImageCheckBox
        '
        Me.stretchImageCheckBox.Checked = True
        Me.stretchImageCheckBox.CheckState = System.Windows.Forms.CheckState.Checked
        Me.stretchImageCheckBox.Location = New System.Drawing.Point(588, 167)
        Me.stretchImageCheckBox.Name = "stretchImageCheckBox"
        Me.stretchImageCheckBox.Size = New System.Drawing.Size(93, 17)
        Me.stretchImageCheckBox.TabIndex = 26
        Me.stretchImageCheckBox.Text = "Stretch image"
        Me.stretchImageCheckBox.UseVisualStyleBackColor = True
        '
        'saveFileDialog1
        '
        Me.saveFileDialog1.FileName = "doc1"
        Me.saveFileDialog1.Filter = "BMP image|*.bmp|GIF image|*.gif|JPEG image|*.jpg|PNG image|*.png|TIFF image|*.tif" & _
            "|PDF document|*.pdf"
        Me.saveFileDialog1.FilterIndex = 3
        '
        'pictureBoxPanel
        '
        Me.pictureBoxPanel.Anchor = CType((((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Bottom) _
                    Or System.Windows.Forms.AnchorStyles.Left) _
                    Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.pictureBoxPanel.AutoScroll = True
        Me.pictureBoxPanel.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle
        Me.pictureBoxPanel.Controls.Add(Me.pictureBox1)
        Me.pictureBoxPanel.Location = New System.Drawing.Point(9, 188)
        Me.pictureBoxPanel.Name = "pictureBoxPanel"
        Me.pictureBoxPanel.Size = New System.Drawing.Size(671, 382)
        Me.pictureBoxPanel.TabIndex = 81
        '
        'pictureBox1
        '
        Me.pictureBox1.Location = New System.Drawing.Point(-1, -1)
        Me.pictureBox1.Name = "pictureBox1"
        Me.pictureBox1.Size = New System.Drawing.Size(669, 380)
        Me.pictureBox1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage
        Me.pictureBox1.TabIndex = 0
        Me.pictureBox1.TabStop = False
        '
        'devicesLabel
        '
        Me.devicesLabel.Location = New System.Drawing.Point(169, 13)
        Me.devicesLabel.Name = "devicesLabel"
        Me.devicesLabel.Size = New System.Drawing.Size(56, 16)
        Me.devicesLabel.TabIndex = 76
        Me.devicesLabel.Text = "Devices:"
        '
        'selectDefaultDeviceButton
        '
        Me.selectDefaultDeviceButton.Location = New System.Drawing.Point(9, 67)
        Me.selectDefaultDeviceButton.Name = "selectDefaultDeviceButton"
        Me.selectDefaultDeviceButton.Size = New System.Drawing.Size(144, 26)
        Me.selectDefaultDeviceButton.TabIndex = 3
        Me.selectDefaultDeviceButton.Text = "Select default device"
        '
        'acquireImageButton
        '
        Me.acquireImageButton.Location = New System.Drawing.Point(9, 99)
        Me.acquireImageButton.Name = "acquireImageButton"
        Me.acquireImageButton.Size = New System.Drawing.Size(144, 26)
        Me.acquireImageButton.TabIndex = 4
        Me.acquireImageButton.Text = "Acquire image(s)"
        '
        'openDeviceManagerButton
        '
        Me.openDeviceManagerButton.Location = New System.Drawing.Point(9, 34)
        Me.openDeviceManagerButton.Name = "openDeviceManagerButton"
        Me.openDeviceManagerButton.Size = New System.Drawing.Size(144, 26)
        Me.openDeviceManagerButton.TabIndex = 2
        Me.openDeviceManagerButton.Text = "Open device manager"
        '
        'showIndicatorsCheckBox
        '
        Me.showIndicatorsCheckBox.Checked = True
        Me.showIndicatorsCheckBox.CheckState = System.Windows.Forms.CheckState.Checked
        Me.showIndicatorsCheckBox.Location = New System.Drawing.Point(8, 51)
        Me.showIndicatorsCheckBox.Name = "showIndicatorsCheckBox"
        Me.showIndicatorsCheckBox.Size = New System.Drawing.Size(104, 16)
        Me.showIndicatorsCheckBox.TabIndex = 9
        Me.showIndicatorsCheckBox.Text = "Show Indicators"
        '
        'imagesToAcquireNumericUpDown
        '
        Me.imagesToAcquireNumericUpDown.Location = New System.Drawing.Point(71, 63)
        Me.imagesToAcquireNumericUpDown.Maximum = New Decimal(New Integer() {1000, 0, 0, 0})
        Me.imagesToAcquireNumericUpDown.Minimum = New Decimal(New Integer() {1, 0, 0, 0})
        Me.imagesToAcquireNumericUpDown.Name = "imagesToAcquireNumericUpDown"
        Me.imagesToAcquireNumericUpDown.Size = New System.Drawing.Size(64, 20)
        Me.imagesToAcquireNumericUpDown.TabIndex = 18
        Me.imagesToAcquireNumericUpDown.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
        Me.imagesToAcquireNumericUpDown.Value = New Decimal(New Integer() {1, 0, 0, 0})
        '
        'adfGroupBox
        '
        Me.adfGroupBox.Controls.Add(Me.label1)
        Me.adfGroupBox.Controls.Add(Me.imagesToAcquireRadioButton)
        Me.adfGroupBox.Controls.Add(Me.acquireAllImagesRadioButton)
        Me.adfGroupBox.Controls.Add(Me.imagesToAcquireNumericUpDown)
        Me.adfGroupBox.Controls.Add(Me.useAdfCheckBox)
        Me.adfGroupBox.Controls.Add(Me.useDuplexCheckBox)
        Me.adfGroupBox.ForeColor = System.Drawing.SystemColors.ControlText
        Me.adfGroupBox.Location = New System.Drawing.Point(500, 37)
        Me.adfGroupBox.Name = "adfGroupBox"
        Me.adfGroupBox.Size = New System.Drawing.Size(182, 88)
        Me.adfGroupBox.TabIndex = 14
        Me.adfGroupBox.TabStop = False
        Me.adfGroupBox.Text = "Automatic Document Feeder"
        '
        'label1
        '
        Me.label1.AutoSize = True
        Me.label1.Location = New System.Drawing.Point(136, 66)
        Me.label1.Name = "label1"
        Me.label1.Size = New System.Drawing.Size(40, 13)
        Me.label1.TabIndex = 0
        Me.label1.Text = "images"
        '
        'imagesToAcquireRadioButton
        '
        Me.imagesToAcquireRadioButton.AutoSize = True
        Me.imagesToAcquireRadioButton.Location = New System.Drawing.Point(10, 64)
        Me.imagesToAcquireRadioButton.Name = "imagesToAcquireRadioButton"
        Me.imagesToAcquireRadioButton.Size = New System.Drawing.Size(61, 17)
        Me.imagesToAcquireRadioButton.TabIndex = 17
        Me.imagesToAcquireRadioButton.TabStop = True
        Me.imagesToAcquireRadioButton.Text = "Acquire"
        Me.imagesToAcquireRadioButton.UseVisualStyleBackColor = True
        '
        'acquireAllImagesRadioButton
        '
        Me.acquireAllImagesRadioButton.AutoSize = True
        Me.acquireAllImagesRadioButton.Checked = True
        Me.acquireAllImagesRadioButton.Location = New System.Drawing.Point(10, 43)
        Me.acquireAllImagesRadioButton.Name = "acquireAllImagesRadioButton"
        Me.acquireAllImagesRadioButton.Size = New System.Drawing.Size(112, 17)
        Me.acquireAllImagesRadioButton.TabIndex = 16
        Me.acquireAllImagesRadioButton.TabStop = True
        Me.acquireAllImagesRadioButton.Text = "Acquire All Images"
        Me.acquireAllImagesRadioButton.UseVisualStyleBackColor = True
        '
        'useAdfCheckBox
        '
        Me.useAdfCheckBox.Checked = True
        Me.useAdfCheckBox.CheckState = System.Windows.Forms.CheckState.Checked
        Me.useAdfCheckBox.Location = New System.Drawing.Point(10, 17)
        Me.useAdfCheckBox.Name = "useAdfCheckBox"
        Me.useAdfCheckBox.Size = New System.Drawing.Size(72, 16)
        Me.useAdfCheckBox.TabIndex = 14
        Me.useAdfCheckBox.Text = "Use ADF"
        '
        'useDuplexCheckBox
        '
        Me.useDuplexCheckBox.Location = New System.Drawing.Point(84, 17)
        Me.useDuplexCheckBox.Name = "useDuplexCheckBox"
        Me.useDuplexCheckBox.Size = New System.Drawing.Size(82, 16)
        Me.useDuplexCheckBox.TabIndex = 15
        Me.useDuplexCheckBox.Text = "Use Duplex"
        '
        'userInterfaceGroupBox
        '
        Me.userInterfaceGroupBox.Controls.Add(Me.showUICheckBox)
        Me.userInterfaceGroupBox.Controls.Add(Me.modalUICheckBox)
        Me.userInterfaceGroupBox.Controls.Add(Me.showIndicatorsCheckBox)
        Me.userInterfaceGroupBox.Controls.Add(Me.disableAfterScanCheckBox)
        Me.userInterfaceGroupBox.Location = New System.Drawing.Point(162, 38)
        Me.userInterfaceGroupBox.Name = "userInterfaceGroupBox"
        Me.userInterfaceGroupBox.Size = New System.Drawing.Size(139, 88)
        Me.userInterfaceGroupBox.TabIndex = 7
        Me.userInterfaceGroupBox.TabStop = False
        Me.userInterfaceGroupBox.Text = "User Interface"
        '
        'showUICheckBox
        '
        Me.showUICheckBox.Checked = True
        Me.showUICheckBox.CheckState = System.Windows.Forms.CheckState.Checked
        Me.showUICheckBox.ForeColor = System.Drawing.SystemColors.ControlText
        Me.showUICheckBox.Location = New System.Drawing.Point(8, 17)
        Me.showUICheckBox.Name = "showUICheckBox"
        Me.showUICheckBox.Size = New System.Drawing.Size(72, 16)
        Me.showUICheckBox.TabIndex = 7
        Me.showUICheckBox.Text = "Show UI"
        '
        'modalUICheckBox
        '
        Me.modalUICheckBox.Location = New System.Drawing.Point(8, 34)
        Me.modalUICheckBox.Name = "modalUICheckBox"
        Me.modalUICheckBox.Size = New System.Drawing.Size(72, 16)
        Me.modalUICheckBox.TabIndex = 8
        Me.modalUICheckBox.Text = "Modal UI"
        '
        'disableAfterScanCheckBox
        '
        Me.disableAfterScanCheckBox.Location = New System.Drawing.Point(8, 68)
        Me.disableAfterScanCheckBox.Name = "disableAfterScanCheckBox"
        Me.disableAfterScanCheckBox.Size = New System.Drawing.Size(128, 17)
        Me.disableAfterScanCheckBox.TabIndex = 10
        Me.disableAfterScanCheckBox.Text = "Disable after Scan"
        '
        'devicesComboBox
        '
        Me.devicesComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
        Me.devicesComboBox.Location = New System.Drawing.Point(217, 11)
        Me.devicesComboBox.Name = "devicesComboBox"
        Me.devicesComboBox.Size = New System.Drawing.Size(339, 21)
        Me.devicesComboBox.TabIndex = 5
        '
        'twain2CompatibleCheckBox
        '
        Me.twain2CompatibleCheckBox.Checked = True
        Me.twain2CompatibleCheckBox.CheckState = System.Windows.Forms.CheckState.Checked
        Me.twain2CompatibleCheckBox.Location = New System.Drawing.Point(17, 12)
        Me.twain2CompatibleCheckBox.Name = "twain2CompatibleCheckBox"
        Me.twain2CompatibleCheckBox.Size = New System.Drawing.Size(146, 17)
        Me.twain2CompatibleCheckBox.TabIndex = 1
        Me.twain2CompatibleCheckBox.Text = "TWAIN 2 compatible"
        Me.twain2CompatibleCheckBox.UseVisualStyleBackColor = True
        '
        'deleteImageButton
        '
        Me.deleteImageButton.Location = New System.Drawing.Point(500, 139)
        Me.deleteImageButton.Name = "deleteImageButton"
        Me.deleteImageButton.Size = New System.Drawing.Size(90, 23)
        Me.deleteImageButton.TabIndex = 24
        Me.deleteImageButton.Text = "Delete image"
        '
        'panel1
        '
        Me.panel1.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle
        Me.panel1.Location = New System.Drawing.Point(9, 131)
        Me.panel1.Name = "panel1"
        Me.panel1.Size = New System.Drawing.Size(671, 1)
        Me.panel1.TabIndex = 78
        '
        'uploadImageButton
        '
        Me.uploadImageButton.Location = New System.Drawing.Point(398, 139)
        Me.uploadImageButton.Name = "uploadImageButton"
        Me.uploadImageButton.Size = New System.Drawing.Size(90, 23)
        Me.uploadImageButton.TabIndex = 23
        Me.uploadImageButton.Text = "Upload image"
        '
        'saveImageButton
        '
        Me.saveImageButton.Location = New System.Drawing.Point(305, 139)
        Me.saveImageButton.Name = "saveImageButton"
        Me.saveImageButton.Size = New System.Drawing.Size(90, 23)
        Me.saveImageButton.TabIndex = 22
        Me.saveImageButton.Text = "Save image"
        '
        'getDeviceInfoButton
        '
        Me.getDeviceInfoButton.Location = New System.Drawing.Point(562, 9)
        Me.getDeviceInfoButton.Name = "getDeviceInfoButton"
        Me.getDeviceInfoButton.Size = New System.Drawing.Size(120, 23)
        Me.getDeviceInfoButton.TabIndex = 6
        Me.getDeviceInfoButton.Text = "Get source info"
        '
        'imageInfoLabel
        '
        Me.imageInfoLabel.Location = New System.Drawing.Point(162, 168)
        Me.imageInfoLabel.Name = "imageInfoLabel"
        Me.imageInfoLabel.Size = New System.Drawing.Size(367, 16)
        Me.imageInfoLabel.TabIndex = 77
        Me.imageInfoLabel.Text = "No images"
        Me.imageInfoLabel.TextAlign = System.Drawing.ContentAlignment.TopCenter
        '
        'nextImageButton
        '
        Me.nextImageButton.Location = New System.Drawing.Point(102, 139)
        Me.nextImageButton.Name = "nextImageButton"
        Me.nextImageButton.Size = New System.Drawing.Size(90, 23)
        Me.nextImageButton.TabIndex = 20
        Me.nextImageButton.Text = "Next image"
        '
        'previousImageButton
        '
        Me.previousImageButton.Location = New System.Drawing.Point(9, 139)
        Me.previousImageButton.Name = "previousImageButton"
        Me.previousImageButton.Size = New System.Drawing.Size(90, 23)
        Me.previousImageButton.TabIndex = 19
        Me.previousImageButton.Text = "Previous image"
        '
        'processImageButton
        '
        Me.processImageButton.Location = New System.Drawing.Point(205, 139)
        Me.processImageButton.Name = "processImageButton"
        Me.processImageButton.Size = New System.Drawing.Size(90, 23)
        Me.processImageButton.TabIndex = 21
        Me.processImageButton.Text = "Process image"
        '
        'imageAcquisitionProgressBar
        '
        Me.imageAcquisitionProgressBar.Anchor = CType(((System.Windows.Forms.AnchorStyles.Bottom Or System.Windows.Forms.AnchorStyles.Left) _
                    Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.imageAcquisitionProgressBar.Location = New System.Drawing.Point(9, 576)
        Me.imageAcquisitionProgressBar.Name = "imageAcquisitionProgressBar"
        Me.imageAcquisitionProgressBar.Size = New System.Drawing.Size(672, 23)
        Me.imageAcquisitionProgressBar.TabIndex = 87
        '
        'imageGroupBox
        '
        Me.imageGroupBox.Controls.Add(Me.transferModeLabel)
        Me.imageGroupBox.Controls.Add(Me.transferModeComboBox)
        Me.imageGroupBox.Controls.Add(Me.resolutionLabel)
        Me.imageGroupBox.Controls.Add(Me.resolutionComboBox)
        Me.imageGroupBox.Controls.Add(Me.pixelTypeLabel)
        Me.imageGroupBox.Controls.Add(Me.pixelTypeComboBox)
        Me.imageGroupBox.Location = New System.Drawing.Point(307, 37)
        Me.imageGroupBox.Name = "imageGroupBox"
        Me.imageGroupBox.Size = New System.Drawing.Size(187, 88)
        Me.imageGroupBox.TabIndex = 11
        Me.imageGroupBox.TabStop = False
        Me.imageGroupBox.Text = "Image:"
        '
        'transferModeLabel
        '
        Me.transferModeLabel.AutoSize = True
        Me.transferModeLabel.Location = New System.Drawing.Point(6, 18)
        Me.transferModeLabel.Name = "transferModeLabel"
        Me.transferModeLabel.Size = New System.Drawing.Size(76, 13)
        Me.transferModeLabel.TabIndex = 5
        Me.transferModeLabel.Text = "Transfer Mode"
        '
        'transferModeComboBox
        '
        Me.transferModeComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
        Me.transferModeComboBox.FormattingEnabled = True
        Me.transferModeComboBox.Items.AddRange(New Object() {"Native", "Memory"})
        Me.transferModeComboBox.Location = New System.Drawing.Point(88, 13)
        Me.transferModeComboBox.Name = "transferModeComboBox"
        Me.transferModeComboBox.Size = New System.Drawing.Size(89, 21)
        Me.transferModeComboBox.TabIndex = 11
        '
        'resolutionLabel
        '
        Me.resolutionLabel.AutoSize = True
        Me.resolutionLabel.Location = New System.Drawing.Point(6, 66)
        Me.resolutionLabel.Name = "resolutionLabel"
        Me.resolutionLabel.Size = New System.Drawing.Size(57, 13)
        Me.resolutionLabel.TabIndex = 3
        Me.resolutionLabel.Text = "Resolution"
        '
        'resolutionComboBox
        '
        Me.resolutionComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
        Me.resolutionComboBox.FormattingEnabled = True
        Me.resolutionComboBox.Items.AddRange(New Object() {"100", "150", "200", "300", "600"})
        Me.resolutionComboBox.Location = New System.Drawing.Point(88, 63)
        Me.resolutionComboBox.Name = "resolutionComboBox"
        Me.resolutionComboBox.Size = New System.Drawing.Size(89, 21)
        Me.resolutionComboBox.TabIndex = 13
        '
        'pixelTypeLabel
        '
        Me.pixelTypeLabel.AutoSize = True
        Me.pixelTypeLabel.Location = New System.Drawing.Point(6, 41)
        Me.pixelTypeLabel.Name = "pixelTypeLabel"
        Me.pixelTypeLabel.Size = New System.Drawing.Size(56, 13)
        Me.pixelTypeLabel.TabIndex = 1
        Me.pixelTypeLabel.Text = "Pixel Type"
        '
        'pixelTypeComboBox
        '
        Me.pixelTypeComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
        Me.pixelTypeComboBox.FormattingEnabled = True
        Me.pixelTypeComboBox.Items.AddRange(New Object() {"BW", "Gray", "Color"})
        Me.pixelTypeComboBox.Location = New System.Drawing.Point(88, 38)
        Me.pixelTypeComboBox.Name = "pixelTypeComboBox"
        Me.pixelTypeComboBox.Size = New System.Drawing.Size(89, 21)
        Me.pixelTypeComboBox.TabIndex = 12
        '
        'clearImagesButton
        '
        Me.clearImagesButton.Location = New System.Drawing.Point(592, 139)
        Me.clearImagesButton.Name = "clearImagesButton"
        Me.clearImagesButton.Size = New System.Drawing.Size(90, 23)
        Me.clearImagesButton.TabIndex = 25
        Me.clearImagesButton.Text = "Clear images"
        '
        'MainForm
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 13.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(691, 608)
        Me.Controls.Add(Me.clearImagesButton)
        Me.Controls.Add(Me.imageGroupBox)
        Me.Controls.Add(Me.processImageButton)
        Me.Controls.Add(Me.imageAcquisitionProgressBar)
        Me.Controls.Add(Me.stretchImageCheckBox)
        Me.Controls.Add(Me.pictureBoxPanel)
        Me.Controls.Add(Me.selectDefaultDeviceButton)
        Me.Controls.Add(Me.acquireImageButton)
        Me.Controls.Add(Me.openDeviceManagerButton)
        Me.Controls.Add(Me.adfGroupBox)
        Me.Controls.Add(Me.userInterfaceGroupBox)
        Me.Controls.Add(Me.devicesComboBox)
        Me.Controls.Add(Me.twain2CompatibleCheckBox)
        Me.Controls.Add(Me.deleteImageButton)
        Me.Controls.Add(Me.panel1)
        Me.Controls.Add(Me.uploadImageButton)
        Me.Controls.Add(Me.saveImageButton)
        Me.Controls.Add(Me.getDeviceInfoButton)
        Me.Controls.Add(Me.imageInfoLabel)
        Me.Controls.Add(Me.nextImageButton)
        Me.Controls.Add(Me.previousImageButton)
        Me.Controls.Add(Me.devicesLabel)
        Me.Name = "MainForm"
        Me.Text = "VintaSoft TWAIN Advanced Demo"
        Me.pictureBoxPanel.ResumeLayout(False)
        CType(Me.pictureBox1, System.ComponentModel.ISupportInitialize).EndInit()
        CType(Me.imagesToAcquireNumericUpDown, System.ComponentModel.ISupportInitialize).EndInit()
        Me.adfGroupBox.ResumeLayout(False)
        Me.adfGroupBox.PerformLayout()
        Me.userInterfaceGroupBox.ResumeLayout(False)
        Me.imageGroupBox.ResumeLayout(False)
        Me.imageGroupBox.PerformLayout()
        Me.ResumeLayout(False)

    End Sub

	#End Region

	Private WithEvents stretchImageCheckBox As System.Windows.Forms.CheckBox
	Private WithEvents saveFileDialog1 As System.Windows.Forms.SaveFileDialog
	Private WithEvents pictureBoxPanel As System.Windows.Forms.Panel
	Private WithEvents pictureBox1 As System.Windows.Forms.PictureBox
	Private WithEvents devicesLabel As System.Windows.Forms.Label
	Private WithEvents selectDefaultDeviceButton As System.Windows.Forms.Button
	Private WithEvents acquireImageButton As System.Windows.Forms.Button
	Private WithEvents openDeviceManagerButton As System.Windows.Forms.Button
	Private WithEvents showIndicatorsCheckBox As System.Windows.Forms.CheckBox
	Private WithEvents imagesToAcquireNumericUpDown As System.Windows.Forms.NumericUpDown
	Private WithEvents adfGroupBox As System.Windows.Forms.GroupBox
	Private WithEvents useAdfCheckBox As System.Windows.Forms.CheckBox
	Private WithEvents useDuplexCheckBox As System.Windows.Forms.CheckBox
	Private WithEvents userInterfaceGroupBox As System.Windows.Forms.GroupBox
	Private WithEvents showUICheckBox As System.Windows.Forms.CheckBox
	Private WithEvents modalUICheckBox As System.Windows.Forms.CheckBox
	Private WithEvents disableAfterScanCheckBox As System.Windows.Forms.CheckBox
	Private WithEvents devicesComboBox As System.Windows.Forms.ComboBox
	Private WithEvents twain2CompatibleCheckBox As System.Windows.Forms.CheckBox
	Private WithEvents deleteImageButton As System.Windows.Forms.Button
	Private WithEvents panel1 As System.Windows.Forms.Panel
	Private WithEvents uploadImageButton As System.Windows.Forms.Button
	Private WithEvents saveImageButton As System.Windows.Forms.Button
	Private WithEvents getDeviceInfoButton As System.Windows.Forms.Button
	Private WithEvents imageInfoLabel As System.Windows.Forms.Label
	Private WithEvents nextImageButton As System.Windows.Forms.Button
	Private WithEvents previousImageButton As System.Windows.Forms.Button
	Private WithEvents processImageButton As System.Windows.Forms.Button
	Private WithEvents imageAcquisitionProgressBar As System.Windows.Forms.ProgressBar
	Private WithEvents imageGroupBox As System.Windows.Forms.GroupBox
	Private WithEvents acquireAllImagesRadioButton As System.Windows.Forms.RadioButton
	Private WithEvents label1 As System.Windows.Forms.Label
	Private WithEvents imagesToAcquireRadioButton As System.Windows.Forms.RadioButton
	Private WithEvents pixelTypeComboBox As System.Windows.Forms.ComboBox
	Private WithEvents resolutionLabel As System.Windows.Forms.Label
	Private WithEvents resolutionComboBox As System.Windows.Forms.ComboBox
	Private WithEvents pixelTypeLabel As System.Windows.Forms.Label
	Private WithEvents transferModeLabel As System.Windows.Forms.Label
	Private WithEvents transferModeComboBox As System.Windows.Forms.ComboBox
	Private WithEvents clearImagesButton As System.Windows.Forms.Button


End Class

