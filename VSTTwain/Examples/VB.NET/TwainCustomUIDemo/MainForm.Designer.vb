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
		Me.components = New System.ComponentModel.Container()
		Me.devicesComboBox = New System.Windows.Forms.ComboBox()
		Me.label1 = New System.Windows.Forms.Label()
		Me.pageGroupBox = New System.Windows.Forms.GroupBox()
		Me.pageOrientationComboBox = New System.Windows.Forms.ComboBox()
		Me.pageOrientationLabel = New System.Windows.Forms.Label()
		Me.pageSizeComboBox = New System.Windows.Forms.ComboBox()
		Me.pageSizeLabel = New System.Windows.Forms.Label()
		Me.imageGroupBox = New System.Windows.Forms.GroupBox()
		Me.thresholdComboBox = New System.Windows.Forms.ComboBox()
		Me.contrastComboBox = New System.Windows.Forms.ComboBox()
		Me.brightnessComboBox = New System.Windows.Forms.ComboBox()
		Me.contrastLabel = New System.Windows.Forms.Label()
		Me.bitDepthComboBox = New System.Windows.Forms.ComboBox()
		Me.bitDepthLabel = New System.Windows.Forms.Label()
		Me.pixelTypeComboBox = New System.Windows.Forms.ComboBox()
		Me.pixelTypeLabel = New System.Windows.Forms.Label()
		Me.brightnessLabel = New System.Windows.Forms.Label()
		Me.thresholdLabel = New System.Windows.Forms.Label()
		Me.contrastTrackBar = New System.Windows.Forms.TrackBar()
		Me.thresholdTrackBar = New System.Windows.Forms.TrackBar()
		Me.brightnessTrackBar = New System.Windows.Forms.TrackBar()
		Me.imageProcessingGroupBox = New System.Windows.Forms.GroupBox()
		Me.autoBorderDetectionCheckBox = New System.Windows.Forms.CheckBox()
		Me.autoRotateCheckBox = New System.Windows.Forms.CheckBox()
		Me.noiseFilterComboBox = New System.Windows.Forms.ComboBox()
		Me.noiseFilterLabel = New System.Windows.Forms.Label()
		Me.imageFilterComboBox = New System.Windows.Forms.ComboBox()
		Me.imageFilterLabel = New System.Windows.Forms.Label()
		Me.resolutionGroupBox = New System.Windows.Forms.GroupBox()
		Me.unitOfMeasureComboBox = New System.Windows.Forms.ComboBox()
		Me.unitOfMeasureLabel = New System.Windows.Forms.Label()
		Me.yResComboBox = New System.Windows.Forms.ComboBox()
		Me.yResLabel = New System.Windows.Forms.Label()
		Me.xResLabel = New System.Windows.Forms.Label()
		Me.xResComboBox = New System.Windows.Forms.ComboBox()
		Me.yResTrackBar = New System.Windows.Forms.TrackBar()
		Me.xResTrackBar = New System.Windows.Forms.TrackBar()
		Me.twain2CompatibleCheckBox = New System.Windows.Forms.CheckBox()
		Me.imageLayoutGroupBox = New System.Windows.Forms.GroupBox()
		Me.resetImageLayoutButton = New System.Windows.Forms.Button()
		Me.bottomTextBox = New System.Windows.Forms.TextBox()
		Me.rightTextBox = New System.Windows.Forms.TextBox()
		Me.topTextBox = New System.Windows.Forms.TextBox()
		Me.leftTextBox = New System.Windows.Forms.TextBox()
		Me.label13 = New System.Windows.Forms.Label()
		Me.label14 = New System.Windows.Forms.Label()
		Me.label7 = New System.Windows.Forms.Label()
		Me.label12 = New System.Windows.Forms.Label()
		Me.acquireImageButton = New System.Windows.Forms.Button()
		Me.imageAcquisitionProgressBar = New System.Windows.Forms.ProgressBar()
		Me.acquiredImagesTabControl = New System.Windows.Forms.TabControl()
		Me.label15 = New System.Windows.Forms.Label()
		Me.pagesToAcquireNumericUpDown = New System.Windows.Forms.NumericUpDown()
		Me.comboBox1 = New System.Windows.Forms.ComboBox()
		Me.label16 = New System.Windows.Forms.Label()
		Me.comboBox2 = New System.Windows.Forms.ComboBox()
		Me.label17 = New System.Windows.Forms.Label()
		Me.imagesToAcquireGroupBox = New System.Windows.Forms.GroupBox()
		Me.transferModeGroupBox = New System.Windows.Forms.GroupBox()
		Me.memoryTransferRadioButton = New System.Windows.Forms.RadioButton()
		Me.nativeTransferRadioButton = New System.Windows.Forms.RadioButton()
		Me.clearImagesButton = New System.Windows.Forms.Button()
		Me.toolTip1 = New System.Windows.Forms.ToolTip(Me.components)
		Me.pageGroupBox.SuspendLayout()
		Me.imageGroupBox.SuspendLayout()
		DirectCast(Me.contrastTrackBar, System.ComponentModel.ISupportInitialize).BeginInit()
		DirectCast(Me.thresholdTrackBar, System.ComponentModel.ISupportInitialize).BeginInit()
		DirectCast(Me.brightnessTrackBar, System.ComponentModel.ISupportInitialize).BeginInit()
		Me.imageProcessingGroupBox.SuspendLayout()
		Me.resolutionGroupBox.SuspendLayout()
		DirectCast(Me.yResTrackBar, System.ComponentModel.ISupportInitialize).BeginInit()
		DirectCast(Me.xResTrackBar, System.ComponentModel.ISupportInitialize).BeginInit()
		Me.imageLayoutGroupBox.SuspendLayout()
		DirectCast(Me.pagesToAcquireNumericUpDown, System.ComponentModel.ISupportInitialize).BeginInit()
		Me.imagesToAcquireGroupBox.SuspendLayout()
		Me.transferModeGroupBox.SuspendLayout()
		Me.SuspendLayout()
		' 
		' devicesComboBox
		' 
		Me.devicesComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		Me.devicesComboBox.Location = New System.Drawing.Point(56, 29)
		Me.devicesComboBox.Name = "devicesComboBox"
		Me.devicesComboBox.Size = New System.Drawing.Size(286, 21)
		Me.devicesComboBox.TabIndex = 89
		AddHandler Me.devicesComboBox.SelectedIndexChanged, New System.EventHandler(AddressOf Me.devicesComboBox_SelectedIndexChanged)
		' 
		' label1
		' 
		Me.label1.Location = New System.Drawing.Point(6, 31)
		Me.label1.Name = "label1"
		Me.label1.Size = New System.Drawing.Size(56, 16)
		Me.label1.TabIndex = 99
		Me.label1.Text = "Device:"
		' 
		' pageGroupBox
		' 
		Me.pageGroupBox.Controls.Add(Me.pageOrientationComboBox)
		Me.pageGroupBox.Controls.Add(Me.pageOrientationLabel)
		Me.pageGroupBox.Controls.Add(Me.pageSizeComboBox)
		Me.pageGroupBox.Controls.Add(Me.pageSizeLabel)
		Me.pageGroupBox.Location = New System.Drawing.Point(9, 100)
		Me.pageGroupBox.Name = "pageGroupBox"
		Me.pageGroupBox.Size = New System.Drawing.Size(262, 67)
		Me.pageGroupBox.TabIndex = 100
		Me.pageGroupBox.TabStop = False
		Me.pageGroupBox.Text = "Page"
		' 
		' pageOrientationComboBox
		' 
		Me.pageOrientationComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		Me.pageOrientationComboBox.FormattingEnabled = True
		Me.pageOrientationComboBox.Location = New System.Drawing.Point(75, 40)
		Me.pageOrientationComboBox.Name = "pageOrientationComboBox"
		Me.pageOrientationComboBox.Size = New System.Drawing.Size(177, 21)
		Me.pageOrientationComboBox.TabIndex = 3
		' 
		' pageOrientationLabel
		' 
		Me.pageOrientationLabel.AutoSize = True
		Me.pageOrientationLabel.Location = New System.Drawing.Point(8, 43)
		Me.pageOrientationLabel.Name = "pageOrientationLabel"
		Me.pageOrientationLabel.Size = New System.Drawing.Size(61, 13)
		Me.pageOrientationLabel.TabIndex = 2
		Me.pageOrientationLabel.Text = "Orientation:"
		' 
		' pageSizeComboBox
		' 
		Me.pageSizeComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		Me.pageSizeComboBox.FormattingEnabled = True
		Me.pageSizeComboBox.Location = New System.Drawing.Point(75, 15)
		Me.pageSizeComboBox.Name = "pageSizeComboBox"
		Me.pageSizeComboBox.Size = New System.Drawing.Size(177, 21)
		Me.pageSizeComboBox.TabIndex = 1
		' 
		' pageSizeLabel
		' 
		Me.pageSizeLabel.AutoSize = True
		Me.pageSizeLabel.Location = New System.Drawing.Point(8, 18)
		Me.pageSizeLabel.Name = "pageSizeLabel"
		Me.pageSizeLabel.Size = New System.Drawing.Size(30, 13)
		Me.pageSizeLabel.TabIndex = 0
		Me.pageSizeLabel.Text = "Size:"
		' 
		' imageGroupBox
		' 
		Me.imageGroupBox.Controls.Add(Me.thresholdComboBox)
		Me.imageGroupBox.Controls.Add(Me.contrastComboBox)
		Me.imageGroupBox.Controls.Add(Me.brightnessComboBox)
		Me.imageGroupBox.Controls.Add(Me.contrastLabel)
		Me.imageGroupBox.Controls.Add(Me.bitDepthComboBox)
		Me.imageGroupBox.Controls.Add(Me.bitDepthLabel)
		Me.imageGroupBox.Controls.Add(Me.pixelTypeComboBox)
		Me.imageGroupBox.Controls.Add(Me.pixelTypeLabel)
		Me.imageGroupBox.Controls.Add(Me.brightnessLabel)
		Me.imageGroupBox.Controls.Add(Me.thresholdLabel)
		Me.imageGroupBox.Controls.Add(Me.contrastTrackBar)
		Me.imageGroupBox.Controls.Add(Me.thresholdTrackBar)
		Me.imageGroupBox.Controls.Add(Me.brightnessTrackBar)
		Me.imageGroupBox.Location = New System.Drawing.Point(277, 101)
		Me.imageGroupBox.Name = "imageGroupBox"
		Me.imageGroupBox.Size = New System.Drawing.Size(262, 124)
		Me.imageGroupBox.TabIndex = 101
		Me.imageGroupBox.TabStop = False
		Me.imageGroupBox.Text = "Image"
		' 
		' thresholdComboBox
		' 
		Me.thresholdComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		Me.thresholdComboBox.FormattingEnabled = True
		Me.thresholdComboBox.Location = New System.Drawing.Point(75, 70)
		Me.thresholdComboBox.Name = "thresholdComboBox"
		Me.thresholdComboBox.Size = New System.Drawing.Size(171, 21)
		Me.thresholdComboBox.TabIndex = 119
		' 
		' contrastComboBox
		' 
		Me.contrastComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		Me.contrastComboBox.FormattingEnabled = True
		Me.contrastComboBox.Location = New System.Drawing.Point(75, 97)
		Me.contrastComboBox.Name = "contrastComboBox"
		Me.contrastComboBox.Size = New System.Drawing.Size(171, 21)
		Me.contrastComboBox.TabIndex = 118
		' 
		' brightnessComboBox
		' 
		Me.brightnessComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		Me.brightnessComboBox.FormattingEnabled = True
		Me.brightnessComboBox.Location = New System.Drawing.Point(75, 70)
		Me.brightnessComboBox.Name = "brightnessComboBox"
		Me.brightnessComboBox.Size = New System.Drawing.Size(171, 21)
		Me.brightnessComboBox.TabIndex = 117
		' 
		' contrastLabel
		' 
		Me.contrastLabel.AutoSize = True
		Me.contrastLabel.Location = New System.Drawing.Point(9, 100)
		Me.contrastLabel.Name = "contrastLabel"
		Me.contrastLabel.Size = New System.Drawing.Size(49, 13)
		Me.contrastLabel.TabIndex = 6
		Me.contrastLabel.Text = "Contrast:"
		' 
		' bitDepthComboBox
		' 
		Me.bitDepthComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		Me.bitDepthComboBox.FormattingEnabled = True
		Me.bitDepthComboBox.Location = New System.Drawing.Point(74, 43)
		Me.bitDepthComboBox.Name = "bitDepthComboBox"
		Me.bitDepthComboBox.Size = New System.Drawing.Size(171, 21)
		Me.bitDepthComboBox.TabIndex = 3
		' 
		' bitDepthLabel
		' 
		Me.bitDepthLabel.AutoSize = True
		Me.bitDepthLabel.Location = New System.Drawing.Point(8, 46)
		Me.bitDepthLabel.Name = "bitDepthLabel"
		Me.bitDepthLabel.Size = New System.Drawing.Size(52, 13)
		Me.bitDepthLabel.TabIndex = 2
		Me.bitDepthLabel.Text = "Bit depth:"
		' 
		' pixelTypeComboBox
		' 
		Me.pixelTypeComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		Me.pixelTypeComboBox.FormattingEnabled = True
		Me.pixelTypeComboBox.Location = New System.Drawing.Point(74, 16)
		Me.pixelTypeComboBox.Name = "pixelTypeComboBox"
		Me.pixelTypeComboBox.Size = New System.Drawing.Size(171, 21)
		Me.pixelTypeComboBox.TabIndex = 1
		AddHandler Me.pixelTypeComboBox.SelectedIndexChanged, New System.EventHandler(AddressOf Me.pixelTypeComboBox_SelectedIndexChanged)
		' 
		' pixelTypeLabel
		' 
		Me.pixelTypeLabel.AutoSize = True
		Me.pixelTypeLabel.Location = New System.Drawing.Point(8, 18)
		Me.pixelTypeLabel.Name = "pixelTypeLabel"
		Me.pixelTypeLabel.Size = New System.Drawing.Size(55, 13)
		Me.pixelTypeLabel.TabIndex = 0
		Me.pixelTypeLabel.Text = "Pixel type:"
		' 
		' brightnessLabel
		' 
		Me.brightnessLabel.AutoSize = True
		Me.brightnessLabel.Location = New System.Drawing.Point(9, 73)
		Me.brightnessLabel.Name = "brightnessLabel"
		Me.brightnessLabel.Size = New System.Drawing.Size(59, 13)
		Me.brightnessLabel.TabIndex = 4
		Me.brightnessLabel.Text = "Brightness:"
		' 
		' thresholdLabel
		' 
		Me.thresholdLabel.AutoSize = True
		Me.thresholdLabel.Location = New System.Drawing.Point(8, 73)
		Me.thresholdLabel.Name = "thresholdLabel"
		Me.thresholdLabel.Size = New System.Drawing.Size(57, 13)
		Me.thresholdLabel.TabIndex = 8
		Me.thresholdLabel.Text = "Threshold:"
		' 
		' contrastTrackBar
		' 
		Me.contrastTrackBar.AutoSize = False
		Me.contrastTrackBar.Location = New System.Drawing.Point(71, 97)
		Me.contrastTrackBar.Name = "contrastTrackBar"
		Me.contrastTrackBar.Size = New System.Drawing.Size(181, 21)
		Me.contrastTrackBar.TabIndex = 115
		AddHandler Me.contrastTrackBar.Scroll, New System.EventHandler(AddressOf Me.trackBar_Scroll)
		AddHandler Me.contrastTrackBar.MouseHover, New System.EventHandler(AddressOf Me.trackBar_MouseHover)
		' 
		' thresholdTrackBar
		' 
		Me.thresholdTrackBar.AutoSize = False
		Me.thresholdTrackBar.Location = New System.Drawing.Point(71, 70)
		Me.thresholdTrackBar.Name = "thresholdTrackBar"
		Me.thresholdTrackBar.Size = New System.Drawing.Size(181, 21)
		Me.thresholdTrackBar.TabIndex = 116
		AddHandler Me.thresholdTrackBar.Scroll, New System.EventHandler(AddressOf Me.trackBar_Scroll)
		AddHandler Me.thresholdTrackBar.MouseHover, New System.EventHandler(AddressOf Me.trackBar_MouseHover)
		' 
		' brightnessTrackBar
		' 
		Me.brightnessTrackBar.AutoSize = False
		Me.brightnessTrackBar.Location = New System.Drawing.Point(71, 70)
		Me.brightnessTrackBar.Name = "brightnessTrackBar"
		Me.brightnessTrackBar.Size = New System.Drawing.Size(181, 21)
		Me.brightnessTrackBar.TabIndex = 114
		AddHandler Me.brightnessTrackBar.Scroll, New System.EventHandler(AddressOf Me.trackBar_Scroll)
		AddHandler Me.brightnessTrackBar.MouseHover, New System.EventHandler(AddressOf Me.trackBar_MouseHover)
		' 
		' imageProcessingGroupBox
		' 
		Me.imageProcessingGroupBox.Controls.Add(Me.autoBorderDetectionCheckBox)
		Me.imageProcessingGroupBox.Controls.Add(Me.autoRotateCheckBox)
		Me.imageProcessingGroupBox.Controls.Add(Me.noiseFilterComboBox)
		Me.imageProcessingGroupBox.Controls.Add(Me.noiseFilterLabel)
		Me.imageProcessingGroupBox.Controls.Add(Me.imageFilterComboBox)
		Me.imageProcessingGroupBox.Controls.Add(Me.imageFilterLabel)
		Me.imageProcessingGroupBox.Location = New System.Drawing.Point(277, 228)
		Me.imageProcessingGroupBox.Name = "imageProcessingGroupBox"
		Me.imageProcessingGroupBox.Size = New System.Drawing.Size(262, 108)
		Me.imageProcessingGroupBox.TabIndex = 102
		Me.imageProcessingGroupBox.TabStop = False
		Me.imageProcessingGroupBox.Text = "Image processing"
		' 
		' autoBorderDetectionCheckBox
		' 
		Me.autoBorderDetectionCheckBox.AutoSize = True
		Me.autoBorderDetectionCheckBox.Location = New System.Drawing.Point(11, 85)
		Me.autoBorderDetectionCheckBox.Name = "autoBorderDetectionCheckBox"
		Me.autoBorderDetectionCheckBox.Size = New System.Drawing.Size(153, 17)
		Me.autoBorderDetectionCheckBox.TabIndex = 6
		Me.autoBorderDetectionCheckBox.Text = "Automatic border detection"
		Me.autoBorderDetectionCheckBox.UseVisualStyleBackColor = True
		' 
		' autoRotateCheckBox
		' 
		Me.autoRotateCheckBox.AutoSize = True
		Me.autoRotateCheckBox.Location = New System.Drawing.Point(11, 68)
		Me.autoRotateCheckBox.Name = "autoRotateCheckBox"
		Me.autoRotateCheckBox.Size = New System.Drawing.Size(103, 17)
		Me.autoRotateCheckBox.TabIndex = 4
		Me.autoRotateCheckBox.Text = "Automatic rotate"
		Me.autoRotateCheckBox.UseVisualStyleBackColor = True
		' 
		' noiseFilterComboBox
		' 
		Me.noiseFilterComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		Me.noiseFilterComboBox.FormattingEnabled = True
		Me.noiseFilterComboBox.Location = New System.Drawing.Point(75, 42)
		Me.noiseFilterComboBox.Name = "noiseFilterComboBox"
		Me.noiseFilterComboBox.Size = New System.Drawing.Size(177, 21)
		Me.noiseFilterComboBox.TabIndex = 3
		' 
		' noiseFilterLabel
		' 
		Me.noiseFilterLabel.AutoSize = True
		Me.noiseFilterLabel.Location = New System.Drawing.Point(8, 45)
		Me.noiseFilterLabel.Name = "noiseFilterLabel"
		Me.noiseFilterLabel.Size = New System.Drawing.Size(59, 13)
		Me.noiseFilterLabel.TabIndex = 2
		Me.noiseFilterLabel.Text = "Noise filter:"
		' 
		' imageFilterComboBox
		' 
		Me.imageFilterComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		Me.imageFilterComboBox.FormattingEnabled = True
		Me.imageFilterComboBox.Location = New System.Drawing.Point(75, 16)
		Me.imageFilterComboBox.Name = "imageFilterComboBox"
		Me.imageFilterComboBox.Size = New System.Drawing.Size(177, 21)
		Me.imageFilterComboBox.TabIndex = 1
		' 
		' imageFilterLabel
		' 
		Me.imageFilterLabel.AutoSize = True
		Me.imageFilterLabel.Location = New System.Drawing.Point(8, 19)
		Me.imageFilterLabel.Name = "imageFilterLabel"
		Me.imageFilterLabel.Size = New System.Drawing.Size(61, 13)
		Me.imageFilterLabel.TabIndex = 0
		Me.imageFilterLabel.Text = "Image filter:"
		' 
		' resolutionGroupBox
		' 
		Me.resolutionGroupBox.Controls.Add(Me.unitOfMeasureComboBox)
		Me.resolutionGroupBox.Controls.Add(Me.unitOfMeasureLabel)
		Me.resolutionGroupBox.Controls.Add(Me.yResComboBox)
		Me.resolutionGroupBox.Controls.Add(Me.yResLabel)
		Me.resolutionGroupBox.Controls.Add(Me.xResLabel)
		Me.resolutionGroupBox.Controls.Add(Me.xResComboBox)
		Me.resolutionGroupBox.Controls.Add(Me.yResTrackBar)
		Me.resolutionGroupBox.Controls.Add(Me.xResTrackBar)
		Me.resolutionGroupBox.Location = New System.Drawing.Point(9, 169)
		Me.resolutionGroupBox.Name = "resolutionGroupBox"
		Me.resolutionGroupBox.Size = New System.Drawing.Size(262, 93)
		Me.resolutionGroupBox.TabIndex = 103
		Me.resolutionGroupBox.TabStop = False
		Me.resolutionGroupBox.Text = "Resolution"
		' 
		' unitOfMeasureComboBox
		' 
		Me.unitOfMeasureComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		Me.unitOfMeasureComboBox.FormattingEnabled = True
		Me.unitOfMeasureComboBox.Location = New System.Drawing.Point(96, 15)
		Me.unitOfMeasureComboBox.Name = "unitOfMeasureComboBox"
		Me.unitOfMeasureComboBox.Size = New System.Drawing.Size(156, 21)
		Me.unitOfMeasureComboBox.TabIndex = 5
		AddHandler Me.unitOfMeasureComboBox.SelectedIndexChanged, New System.EventHandler(AddressOf Me.unitOfMeasureComboBox_SelectedIndexChanged)
		' 
		' unitOfMeasureLabel
		' 
		Me.unitOfMeasureLabel.AutoSize = True
		Me.unitOfMeasureLabel.Location = New System.Drawing.Point(6, 18)
		Me.unitOfMeasureLabel.Name = "unitOfMeasureLabel"
		Me.unitOfMeasureLabel.Size = New System.Drawing.Size(84, 13)
		Me.unitOfMeasureLabel.TabIndex = 4
		Me.unitOfMeasureLabel.Text = "Unit of measure:"
		' 
		' yResComboBox
		' 
		Me.yResComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		Me.yResComboBox.FormattingEnabled = True
		Me.yResComboBox.Location = New System.Drawing.Point(96, 65)
		Me.yResComboBox.Name = "yResComboBox"
		Me.yResComboBox.Size = New System.Drawing.Size(156, 21)
		Me.yResComboBox.TabIndex = 3
		' 
		' yResLabel
		' 
		Me.yResLabel.AutoSize = True
		Me.yResLabel.Location = New System.Drawing.Point(7, 68)
		Me.yResLabel.Name = "yResLabel"
		Me.yResLabel.Size = New System.Drawing.Size(45, 13)
		Me.yResLabel.TabIndex = 2
		Me.yResLabel.Text = "Vertical:"
		' 
		' xResLabel
		' 
		Me.xResLabel.AutoSize = True
		Me.xResLabel.Location = New System.Drawing.Point(7, 43)
		Me.xResLabel.Name = "xResLabel"
		Me.xResLabel.Size = New System.Drawing.Size(57, 13)
		Me.xResLabel.TabIndex = 0
		Me.xResLabel.Text = "Horizontal:"
		' 
		' xResComboBox
		' 
		Me.xResComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		Me.xResComboBox.FormattingEnabled = True
		Me.xResComboBox.Location = New System.Drawing.Point(96, 40)
		Me.xResComboBox.Name = "xResComboBox"
		Me.xResComboBox.Size = New System.Drawing.Size(156, 21)
		Me.xResComboBox.TabIndex = 1
		' 
		' yResTrackBar
		' 
		Me.yResTrackBar.AutoSize = False
		Me.yResTrackBar.Location = New System.Drawing.Point(91, 65)
		Me.yResTrackBar.Name = "yResTrackBar"
		Me.yResTrackBar.Size = New System.Drawing.Size(168, 21)
		Me.yResTrackBar.TabIndex = 118
		AddHandler Me.yResTrackBar.Scroll, New System.EventHandler(AddressOf Me.trackBar_Scroll)
		AddHandler Me.yResTrackBar.MouseHover, New System.EventHandler(AddressOf Me.trackBar_MouseHover)
		' 
		' xResTrackBar
		' 
		Me.xResTrackBar.AutoSize = False
		Me.xResTrackBar.Location = New System.Drawing.Point(91, 40)
		Me.xResTrackBar.Name = "xResTrackBar"
		Me.xResTrackBar.Size = New System.Drawing.Size(168, 21)
		Me.xResTrackBar.TabIndex = 117
		AddHandler Me.xResTrackBar.Scroll, New System.EventHandler(AddressOf Me.trackBar_Scroll)
		AddHandler Me.xResTrackBar.MouseHover, New System.EventHandler(AddressOf Me.trackBar_MouseHover)
		' 
		' twain2CompatibleCheckBox
		' 
		Me.twain2CompatibleCheckBox.Checked = True
		Me.twain2CompatibleCheckBox.CheckState = System.Windows.Forms.CheckState.Checked
		Me.twain2CompatibleCheckBox.Location = New System.Drawing.Point(9, 6)
		Me.twain2CompatibleCheckBox.Name = "twain2CompatibleCheckBox"
		Me.twain2CompatibleCheckBox.Size = New System.Drawing.Size(136, 17)
		Me.twain2CompatibleCheckBox.TabIndex = 104
		Me.twain2CompatibleCheckBox.Text = "TWAIN 2.0 compatible"
		Me.twain2CompatibleCheckBox.UseVisualStyleBackColor = True
		AddHandler Me.twain2CompatibleCheckBox.CheckedChanged, New System.EventHandler(AddressOf Me.twain2CompatibleCheckBox_CheckedChanged)
		' 
		' imageLayoutGroupBox
		' 
		Me.imageLayoutGroupBox.Controls.Add(Me.resetImageLayoutButton)
		Me.imageLayoutGroupBox.Controls.Add(Me.bottomTextBox)
		Me.imageLayoutGroupBox.Controls.Add(Me.rightTextBox)
		Me.imageLayoutGroupBox.Controls.Add(Me.topTextBox)
		Me.imageLayoutGroupBox.Controls.Add(Me.leftTextBox)
		Me.imageLayoutGroupBox.Controls.Add(Me.label13)
		Me.imageLayoutGroupBox.Controls.Add(Me.label14)
		Me.imageLayoutGroupBox.Controls.Add(Me.label7)
		Me.imageLayoutGroupBox.Controls.Add(Me.label12)
		Me.imageLayoutGroupBox.Location = New System.Drawing.Point(9, 265)
		Me.imageLayoutGroupBox.Name = "imageLayoutGroupBox"
		Me.imageLayoutGroupBox.Size = New System.Drawing.Size(262, 94)
		Me.imageLayoutGroupBox.TabIndex = 105
		Me.imageLayoutGroupBox.TabStop = False
		Me.imageLayoutGroupBox.Text = "Image layout:"
		' 
		' resetImageLayoutButton
		' 
		Me.resetImageLayoutButton.Location = New System.Drawing.Point(177, 64)
		Me.resetImageLayoutButton.Name = "resetImageLayoutButton"
		Me.resetImageLayoutButton.Size = New System.Drawing.Size(75, 23)
		Me.resetImageLayoutButton.TabIndex = 14
		Me.resetImageLayoutButton.Text = "Reset"
		Me.resetImageLayoutButton.UseVisualStyleBackColor = True
		AddHandler Me.resetImageLayoutButton.Click, New System.EventHandler(AddressOf Me.resetImageLayoutButton_Click)
		' 
		' bottomTextBox
		' 
		Me.bottomTextBox.Location = New System.Drawing.Point(177, 40)
		Me.bottomTextBox.Name = "bottomTextBox"
		Me.bottomTextBox.Size = New System.Drawing.Size(75, 20)
		Me.bottomTextBox.TabIndex = 13
		' 
		' rightTextBox
		' 
		Me.rightTextBox.Location = New System.Drawing.Point(45, 40)
		Me.rightTextBox.Name = "rightTextBox"
		Me.rightTextBox.Size = New System.Drawing.Size(75, 20)
		Me.rightTextBox.TabIndex = 12
		' 
		' topTextBox
		' 
		Me.topTextBox.Location = New System.Drawing.Point(177, 16)
		Me.topTextBox.Name = "topTextBox"
		Me.topTextBox.Size = New System.Drawing.Size(75, 20)
		Me.topTextBox.TabIndex = 11
		' 
		' leftTextBox
		' 
		Me.leftTextBox.Location = New System.Drawing.Point(45, 17)
		Me.leftTextBox.Name = "leftTextBox"
		Me.leftTextBox.Size = New System.Drawing.Size(75, 20)
		Me.leftTextBox.TabIndex = 10
		' 
		' label13
		' 
		Me.label13.AutoSize = True
		Me.label13.Location = New System.Drawing.Point(129, 43)
		Me.label13.Name = "label13"
		Me.label13.Size = New System.Drawing.Size(43, 13)
		Me.label13.TabIndex = 7
		Me.label13.Text = "Bottom:"
		' 
		' label14
		' 
		Me.label14.AutoSize = True
		Me.label14.Location = New System.Drawing.Point(8, 43)
		Me.label14.Name = "label14"
		Me.label14.Size = New System.Drawing.Size(35, 13)
		Me.label14.TabIndex = 6
		Me.label14.Text = "Right:"
		' 
		' label7
		' 
		Me.label7.AutoSize = True
		Me.label7.Location = New System.Drawing.Point(129, 19)
		Me.label7.Name = "label7"
		Me.label7.Size = New System.Drawing.Size(29, 13)
		Me.label7.TabIndex = 2
		Me.label7.Text = "Top:"
		' 
		' label12
		' 
		Me.label12.AutoSize = True
		Me.label12.Location = New System.Drawing.Point(8, 19)
		Me.label12.Name = "label12"
		Me.label12.Size = New System.Drawing.Size(28, 13)
		Me.label12.TabIndex = 0
		Me.label12.Text = "Left:"
		' 
		' acquireImageButton
		' 
		Me.acquireImageButton.Location = New System.Drawing.Point(352, 6)
		Me.acquireImageButton.Name = "acquireImageButton"
		Me.acquireImageButton.Size = New System.Drawing.Size(187, 45)
		Me.acquireImageButton.TabIndex = 106
		Me.acquireImageButton.Text = "Acquire image(s)"
		Me.acquireImageButton.UseVisualStyleBackColor = True
		AddHandler Me.acquireImageButton.Click, New System.EventHandler(AddressOf Me.acquireImageButton_Click)
		' 
		' imageAcquisitionProgressBar
		' 
		Me.imageAcquisitionProgressBar.Location = New System.Drawing.Point(9, 676)
		Me.imageAcquisitionProgressBar.Name = "imageAcquisitionProgressBar"
		Me.imageAcquisitionProgressBar.Size = New System.Drawing.Size(530, 23)
		Me.imageAcquisitionProgressBar.TabIndex = 107
		' 
		' acquiredImagesTabControl
		' 
		Me.acquiredImagesTabControl.Location = New System.Drawing.Point(9, 364)
		Me.acquiredImagesTabControl.Name = "acquiredImagesTabControl"
		Me.acquiredImagesTabControl.SelectedIndex = 0
		Me.acquiredImagesTabControl.Size = New System.Drawing.Size(530, 306)
		Me.acquiredImagesTabControl.TabIndex = 108
		' 
		' label15
		' 
		Me.label15.AutoSize = True
		Me.label15.Location = New System.Drawing.Point(8, 16)
		Me.label15.Name = "label15"
		Me.label15.Size = New System.Drawing.Size(95, 13)
		Me.label15.TabIndex = 109
		Me.label15.Text = "Number of images:"
		' 
		' pagesToAcquireNumericUpDown
		' 
		Me.pagesToAcquireNumericUpDown.Location = New System.Drawing.Point(112, 15)
		Me.pagesToAcquireNumericUpDown.Maximum = New Decimal(New Integer() {255, 0, 0, 0})
		Me.pagesToAcquireNumericUpDown.Minimum = New Decimal(New Integer() {1, 0, 0, -2147483648})
		Me.pagesToAcquireNumericUpDown.Name = "pagesToAcquireNumericUpDown"
		Me.pagesToAcquireNumericUpDown.Size = New System.Drawing.Size(93, 20)
		Me.pagesToAcquireNumericUpDown.TabIndex = 110
		Me.pagesToAcquireNumericUpDown.Value = New Decimal(New Integer() {1, 0, 0, -2147483648})
		' 
		' comboBox1
		' 
		Me.comboBox1.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		Me.comboBox1.FormattingEnabled = True
		Me.comboBox1.Location = New System.Drawing.Point(75, 47)
		Me.comboBox1.Name = "comboBox1"
		Me.comboBox1.Size = New System.Drawing.Size(177, 21)
		Me.comboBox1.TabIndex = 3
		' 
		' label16
		' 
		Me.label16.AutoSize = True
		Me.label16.Location = New System.Drawing.Point(8, 50)
		Me.label16.Name = "label16"
		Me.label16.Size = New System.Drawing.Size(61, 13)
		Me.label16.TabIndex = 2
		Me.label16.Text = "Orientation:"
		' 
		' comboBox2
		' 
		Me.comboBox2.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		Me.comboBox2.FormattingEnabled = True
		Me.comboBox2.Location = New System.Drawing.Point(75, 20)
		Me.comboBox2.Name = "comboBox2"
		Me.comboBox2.Size = New System.Drawing.Size(177, 21)
		Me.comboBox2.TabIndex = 1
		' 
		' label17
		' 
		Me.label17.AutoSize = True
		Me.label17.Location = New System.Drawing.Point(8, 23)
		Me.label17.Name = "label17"
		Me.label17.Size = New System.Drawing.Size(30, 13)
		Me.label17.TabIndex = 0
		Me.label17.Text = "Size:"
		' 
		' imagesToAcquireGroupBox
		' 
		Me.imagesToAcquireGroupBox.Controls.Add(Me.pagesToAcquireNumericUpDown)
		Me.imagesToAcquireGroupBox.Controls.Add(Me.label15)
		Me.imagesToAcquireGroupBox.Location = New System.Drawing.Point(277, 57)
		Me.imagesToAcquireGroupBox.Name = "imagesToAcquireGroupBox"
		Me.imagesToAcquireGroupBox.Size = New System.Drawing.Size(262, 41)
		Me.imagesToAcquireGroupBox.TabIndex = 111
		Me.imagesToAcquireGroupBox.TabStop = False
		Me.imagesToAcquireGroupBox.Text = "Images to acquire"
		' 
		' transferModeGroupBox
		' 
		Me.transferModeGroupBox.Controls.Add(Me.memoryTransferRadioButton)
		Me.transferModeGroupBox.Controls.Add(Me.nativeTransferRadioButton)
		Me.transferModeGroupBox.Location = New System.Drawing.Point(9, 57)
		Me.transferModeGroupBox.Name = "transferModeGroupBox"
		Me.transferModeGroupBox.Size = New System.Drawing.Size(262, 41)
		Me.transferModeGroupBox.TabIndex = 112
		Me.transferModeGroupBox.TabStop = False
		Me.transferModeGroupBox.Text = "Transfer mode"
		' 
		' memoryTransferRadioButton
		' 
		Me.memoryTransferRadioButton.AutoSize = True
		Me.memoryTransferRadioButton.Checked = True
		Me.memoryTransferRadioButton.Location = New System.Drawing.Point(132, 16)
		Me.memoryTransferRadioButton.Name = "memoryTransferRadioButton"
		Me.memoryTransferRadioButton.Size = New System.Drawing.Size(62, 17)
		Me.memoryTransferRadioButton.TabIndex = 1
		Me.memoryTransferRadioButton.TabStop = True
		Me.memoryTransferRadioButton.Text = "Memory"
		Me.memoryTransferRadioButton.UseVisualStyleBackColor = True
		AddHandler Me.memoryTransferRadioButton.CheckedChanged, New System.EventHandler(AddressOf Me.memoryTransferRadioButton_CheckedChanged)
		' 
		' nativeTransferRadioButton
		' 
		Me.nativeTransferRadioButton.AutoSize = True
		Me.nativeTransferRadioButton.Location = New System.Drawing.Point(14, 16)
		Me.nativeTransferRadioButton.Name = "nativeTransferRadioButton"
		Me.nativeTransferRadioButton.Size = New System.Drawing.Size(56, 17)
		Me.nativeTransferRadioButton.TabIndex = 0
		Me.nativeTransferRadioButton.Text = "Native"
		Me.nativeTransferRadioButton.UseVisualStyleBackColor = True
		AddHandler Me.nativeTransferRadioButton.CheckedChanged, New System.EventHandler(AddressOf Me.nativeTransferRadioButton_CheckedChanged)
		' 
		' clearImagesButton
		' 
		Me.clearImagesButton.Location = New System.Drawing.Point(432, 342)
		Me.clearImagesButton.Name = "clearImagesButton"
		Me.clearImagesButton.Size = New System.Drawing.Size(107, 23)
		Me.clearImagesButton.TabIndex = 113
		Me.clearImagesButton.Text = "Clear images"
		Me.clearImagesButton.UseVisualStyleBackColor = True
		AddHandler Me.clearImagesButton.Click, New System.EventHandler(AddressOf Me.clearImagesButton_Click)
		' 
		' MainForm
		' 
		Me.AutoScaleDimensions = New System.Drawing.SizeF(6F, 13F)
		Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
		Me.ClientSize = New System.Drawing.Size(547, 704)
		Me.Controls.Add(Me.clearImagesButton)
		Me.Controls.Add(Me.transferModeGroupBox)
		Me.Controls.Add(Me.imagesToAcquireGroupBox)
		Me.Controls.Add(Me.acquiredImagesTabControl)
		Me.Controls.Add(Me.imageAcquisitionProgressBar)
		Me.Controls.Add(Me.acquireImageButton)
		Me.Controls.Add(Me.imageLayoutGroupBox)
		Me.Controls.Add(Me.twain2CompatibleCheckBox)
		Me.Controls.Add(Me.resolutionGroupBox)
		Me.Controls.Add(Me.imageProcessingGroupBox)
		Me.Controls.Add(Me.imageGroupBox)
		Me.Controls.Add(Me.pageGroupBox)
		Me.Controls.Add(Me.devicesComboBox)
		Me.Controls.Add(Me.label1)
		Me.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog
		Me.MaximizeBox = False
		Me.MinimizeBox = False
		Me.Name = "MainForm"
		Me.Text = "VintaSoft TWAIN Custom UI Demo"
		AddHandler Me.Shown, New System.EventHandler(AddressOf Me.MainForm_Shown)
		AddHandler Me.FormClosing, New System.Windows.Forms.FormClosingEventHandler(AddressOf Me.MainForm_FormClosing)
		Me.pageGroupBox.ResumeLayout(False)
		Me.pageGroupBox.PerformLayout()
		Me.imageGroupBox.ResumeLayout(False)
		Me.imageGroupBox.PerformLayout()
		DirectCast(Me.contrastTrackBar, System.ComponentModel.ISupportInitialize).EndInit()
		DirectCast(Me.thresholdTrackBar, System.ComponentModel.ISupportInitialize).EndInit()
		DirectCast(Me.brightnessTrackBar, System.ComponentModel.ISupportInitialize).EndInit()
		Me.imageProcessingGroupBox.ResumeLayout(False)
		Me.imageProcessingGroupBox.PerformLayout()
		Me.resolutionGroupBox.ResumeLayout(False)
		Me.resolutionGroupBox.PerformLayout()
		DirectCast(Me.yResTrackBar, System.ComponentModel.ISupportInitialize).EndInit()
		DirectCast(Me.xResTrackBar, System.ComponentModel.ISupportInitialize).EndInit()
		Me.imageLayoutGroupBox.ResumeLayout(False)
		Me.imageLayoutGroupBox.PerformLayout()
		DirectCast(Me.pagesToAcquireNumericUpDown, System.ComponentModel.ISupportInitialize).EndInit()
		Me.imagesToAcquireGroupBox.ResumeLayout(False)
		Me.imagesToAcquireGroupBox.PerformLayout()
		Me.transferModeGroupBox.ResumeLayout(False)
		Me.transferModeGroupBox.PerformLayout()
		Me.ResumeLayout(False)

	End Sub

	#End Region

	Private WithEvents devicesComboBox As System.Windows.Forms.ComboBox
	Private WithEvents label1 As System.Windows.Forms.Label
	Private WithEvents pageGroupBox As System.Windows.Forms.GroupBox
	Private WithEvents pageOrientationComboBox As System.Windows.Forms.ComboBox
	Private WithEvents pageOrientationLabel As System.Windows.Forms.Label
	Private WithEvents pageSizeComboBox As System.Windows.Forms.ComboBox
	Private WithEvents pageSizeLabel As System.Windows.Forms.Label
	Private WithEvents imageGroupBox As System.Windows.Forms.GroupBox
	Private WithEvents bitDepthComboBox As System.Windows.Forms.ComboBox
	Private WithEvents bitDepthLabel As System.Windows.Forms.Label
	Private WithEvents pixelTypeComboBox As System.Windows.Forms.ComboBox
	Private WithEvents pixelTypeLabel As System.Windows.Forms.Label
	Private WithEvents brightnessLabel As System.Windows.Forms.Label
	Private WithEvents imageProcessingGroupBox As System.Windows.Forms.GroupBox
	Private WithEvents noiseFilterComboBox As System.Windows.Forms.ComboBox
	Private WithEvents noiseFilterLabel As System.Windows.Forms.Label
	Private WithEvents imageFilterComboBox As System.Windows.Forms.ComboBox
	Private WithEvents imageFilterLabel As System.Windows.Forms.Label
	Private WithEvents thresholdLabel As System.Windows.Forms.Label
	Private WithEvents contrastLabel As System.Windows.Forms.Label
	Private WithEvents resolutionGroupBox As System.Windows.Forms.GroupBox
	Private WithEvents unitOfMeasureComboBox As System.Windows.Forms.ComboBox
	Private WithEvents unitOfMeasureLabel As System.Windows.Forms.Label
	Private WithEvents yResComboBox As System.Windows.Forms.ComboBox
	Private WithEvents yResLabel As System.Windows.Forms.Label
	Private WithEvents xResComboBox As System.Windows.Forms.ComboBox
	Private WithEvents xResLabel As System.Windows.Forms.Label
	Private WithEvents twain2CompatibleCheckBox As System.Windows.Forms.CheckBox
	Private WithEvents imageLayoutGroupBox As System.Windows.Forms.GroupBox
	Private WithEvents label7 As System.Windows.Forms.Label
	Private WithEvents label12 As System.Windows.Forms.Label
	Private WithEvents label13 As System.Windows.Forms.Label
	Private WithEvents label14 As System.Windows.Forms.Label
	Private WithEvents bottomTextBox As System.Windows.Forms.TextBox
	Private WithEvents rightTextBox As System.Windows.Forms.TextBox
	Private WithEvents topTextBox As System.Windows.Forms.TextBox
	Private WithEvents leftTextBox As System.Windows.Forms.TextBox
	Private WithEvents resetImageLayoutButton As System.Windows.Forms.Button
	Private WithEvents autoBorderDetectionCheckBox As System.Windows.Forms.CheckBox
	Private WithEvents autoRotateCheckBox As System.Windows.Forms.CheckBox
	Private WithEvents acquireImageButton As System.Windows.Forms.Button
	Private WithEvents imageAcquisitionProgressBar As System.Windows.Forms.ProgressBar
	Private WithEvents acquiredImagesTabControl As System.Windows.Forms.TabControl
	Private WithEvents label15 As System.Windows.Forms.Label
	Private WithEvents pagesToAcquireNumericUpDown As System.Windows.Forms.NumericUpDown
	Private WithEvents comboBox1 As System.Windows.Forms.ComboBox
	Private WithEvents label16 As System.Windows.Forms.Label
	Private WithEvents comboBox2 As System.Windows.Forms.ComboBox
	Private WithEvents label17 As System.Windows.Forms.Label
	Private WithEvents imagesToAcquireGroupBox As System.Windows.Forms.GroupBox
	Private WithEvents transferModeGroupBox As System.Windows.Forms.GroupBox
	Private WithEvents memoryTransferRadioButton As System.Windows.Forms.RadioButton
	Private WithEvents nativeTransferRadioButton As System.Windows.Forms.RadioButton
	Private WithEvents clearImagesButton As System.Windows.Forms.Button
	Private WithEvents brightnessTrackBar As System.Windows.Forms.TrackBar
	Private WithEvents contrastTrackBar As System.Windows.Forms.TrackBar
	Private WithEvents thresholdTrackBar As System.Windows.Forms.TrackBar
	Private WithEvents toolTip1 As System.Windows.Forms.ToolTip
	Private WithEvents xResTrackBar As System.Windows.Forms.TrackBar
	Private WithEvents yResTrackBar As System.Windows.Forms.TrackBar
	Private WithEvents brightnessComboBox As System.Windows.Forms.ComboBox
	Private WithEvents thresholdComboBox As System.Windows.Forms.ComboBox
	Private WithEvents contrastComboBox As System.Windows.Forms.ComboBox
End Class

