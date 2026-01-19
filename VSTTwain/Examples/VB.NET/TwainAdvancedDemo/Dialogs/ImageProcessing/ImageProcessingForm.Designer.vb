Partial Class ImageProcessingForm
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
		Me.pictureBox1 = New System.Windows.Forms.PictureBox()
		Me.groupBox1 = New System.Windows.Forms.GroupBox()
		Me.processingCommandProgressBar = New System.Windows.Forms.ProgressBar()
		Me.runCommandButton = New System.Windows.Forms.Button()
		Me.param4NumericUpDown = New System.Windows.Forms.NumericUpDown()
		Me.param4Label = New System.Windows.Forms.Label()
		Me.param3NumericUpDown = New System.Windows.Forms.NumericUpDown()
		Me.param3Label = New System.Windows.Forms.Label()
		Me.param2NumericUpDown = New System.Windows.Forms.NumericUpDown()
		Me.param2Label = New System.Windows.Forms.Label()
		Me.param1NumericUpDown = New System.Windows.Forms.NumericUpDown()
		Me.param1Label = New System.Windows.Forms.Label()
		Me.commandsComboBox = New System.Windows.Forms.ComboBox()
		Me.pictureBoxPanel = New System.Windows.Forms.Panel()
		Me.stretchImageCheckBox = New System.Windows.Forms.CheckBox()
		DirectCast(Me.pictureBox1, System.ComponentModel.ISupportInitialize).BeginInit()
		Me.groupBox1.SuspendLayout()
		DirectCast(Me.param4NumericUpDown, System.ComponentModel.ISupportInitialize).BeginInit()
		DirectCast(Me.param3NumericUpDown, System.ComponentModel.ISupportInitialize).BeginInit()
		DirectCast(Me.param2NumericUpDown, System.ComponentModel.ISupportInitialize).BeginInit()
		DirectCast(Me.param1NumericUpDown, System.ComponentModel.ISupportInitialize).BeginInit()
		Me.pictureBoxPanel.SuspendLayout()
		Me.SuspendLayout()
		' 
		' pictureBox1
		' 
		Me.pictureBox1.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle
		Me.pictureBox1.Location = New System.Drawing.Point(0, 0)
		Me.pictureBox1.Name = "pictureBox1"
		Me.pictureBox1.Size = New System.Drawing.Size(501, 511)
		Me.pictureBox1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage
		Me.pictureBox1.TabIndex = 0
		Me.pictureBox1.TabStop = False
		' 
		' groupBox1
		' 
		Me.groupBox1.Anchor = CType(((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Bottom) Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
		Me.groupBox1.Controls.Add(Me.processingCommandProgressBar)
		Me.groupBox1.Controls.Add(Me.runCommandButton)
		Me.groupBox1.Controls.Add(Me.param4NumericUpDown)
		Me.groupBox1.Controls.Add(Me.param4Label)
		Me.groupBox1.Controls.Add(Me.param3NumericUpDown)
		Me.groupBox1.Controls.Add(Me.param3Label)
		Me.groupBox1.Controls.Add(Me.param2NumericUpDown)
		Me.groupBox1.Controls.Add(Me.param2Label)
		Me.groupBox1.Controls.Add(Me.param1NumericUpDown)
		Me.groupBox1.Controls.Add(Me.param1Label)
		Me.groupBox1.Controls.Add(Me.commandsComboBox)
		Me.groupBox1.Location = New System.Drawing.Point(521, 32)
		Me.groupBox1.Name = "groupBox1"
		Me.groupBox1.Size = New System.Drawing.Size(200, 490)
		Me.groupBox1.TabIndex = 1
		Me.groupBox1.TabStop = False
		Me.groupBox1.Text = "Processing Command"
		' 
		' processingCommandProgressBar
		' 
		Me.processingCommandProgressBar.Location = New System.Drawing.Point(11, 223)
		Me.processingCommandProgressBar.Name = "processingCommandProgressBar"
		Me.processingCommandProgressBar.Size = New System.Drawing.Size(175, 23)
		Me.processingCommandProgressBar.TabIndex = 12
		' 
		' runCommandButton
		' 
		Me.runCommandButton.Location = New System.Drawing.Point(11, 182)
		Me.runCommandButton.Name = "runCommandButton"
		Me.runCommandButton.Size = New System.Drawing.Size(175, 35)
		Me.runCommandButton.TabIndex = 11
		Me.runCommandButton.Text = "Run command"
		Me.runCommandButton.UseVisualStyleBackColor = True
		AddHandler Me.runCommandButton.Click, New System.EventHandler(AddressOf Me.runCommandButton_Click)
		' 
		' param4NumericUpDown
		' 
		Me.param4NumericUpDown.Location = New System.Drawing.Point(125, 132)
		Me.param4NumericUpDown.Name = "param4NumericUpDown"
		Me.param4NumericUpDown.Size = New System.Drawing.Size(61, 20)
		Me.param4NumericUpDown.TabIndex = 10
		Me.param4NumericUpDown.Visible = False
		' 
		' param4Label
		' 
		Me.param4Label.AutoSize = True
		Me.param4Label.Location = New System.Drawing.Point(8, 134)
		Me.param4Label.Name = "param4Label"
		Me.param4Label.Size = New System.Drawing.Size(46, 13)
		Me.param4Label.TabIndex = 9
		Me.param4Label.Text = "Param4:"
		Me.param4Label.Visible = False
		' 
		' param3NumericUpDown
		' 
		Me.param3NumericUpDown.Location = New System.Drawing.Point(125, 106)
		Me.param3NumericUpDown.Name = "param3NumericUpDown"
		Me.param3NumericUpDown.Size = New System.Drawing.Size(61, 20)
		Me.param3NumericUpDown.TabIndex = 8
		Me.param3NumericUpDown.Visible = False
		' 
		' param3Label
		' 
		Me.param3Label.AutoSize = True
		Me.param3Label.Location = New System.Drawing.Point(8, 108)
		Me.param3Label.Name = "param3Label"
		Me.param3Label.Size = New System.Drawing.Size(46, 13)
		Me.param3Label.TabIndex = 7
		Me.param3Label.Text = "Param3:"
		Me.param3Label.Visible = False
		' 
		' param2NumericUpDown
		' 
		Me.param2NumericUpDown.Location = New System.Drawing.Point(125, 80)
		Me.param2NumericUpDown.Name = "param2NumericUpDown"
		Me.param2NumericUpDown.Size = New System.Drawing.Size(61, 20)
		Me.param2NumericUpDown.TabIndex = 6
		Me.param2NumericUpDown.Visible = False
		' 
		' param2Label
		' 
		Me.param2Label.AutoSize = True
		Me.param2Label.Location = New System.Drawing.Point(8, 82)
		Me.param2Label.Name = "param2Label"
		Me.param2Label.Size = New System.Drawing.Size(46, 13)
		Me.param2Label.TabIndex = 5
		Me.param2Label.Text = "Param2:"
		Me.param2Label.Visible = False
		' 
		' param1NumericUpDown
		' 
		Me.param1NumericUpDown.Location = New System.Drawing.Point(125, 54)
		Me.param1NumericUpDown.Name = "param1NumericUpDown"
		Me.param1NumericUpDown.Size = New System.Drawing.Size(61, 20)
		Me.param1NumericUpDown.TabIndex = 4
		Me.param1NumericUpDown.Visible = False
		' 
		' param1Label
		' 
		Me.param1Label.AutoSize = True
		Me.param1Label.Location = New System.Drawing.Point(8, 56)
		Me.param1Label.Name = "param1Label"
		Me.param1Label.Size = New System.Drawing.Size(46, 13)
		Me.param1Label.TabIndex = 2
		Me.param1Label.Text = "Param1:"
		Me.param1Label.Visible = False
		' 
		' commandsComboBox
		' 
		Me.commandsComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		Me.commandsComboBox.FormattingEnabled = True
		Me.commandsComboBox.Items.AddRange(New Object() {"Is Image Blank?", "Invert", "Change Brightness", "Change Contrast", "Crop", "Resize Canvas", _
			"Rotate", "Despeckle", "Deskew", "Remove Border"})
		Me.commandsComboBox.Location = New System.Drawing.Point(11, 23)
		Me.commandsComboBox.Name = "commandsComboBox"
		Me.commandsComboBox.Size = New System.Drawing.Size(175, 21)
		Me.commandsComboBox.TabIndex = 1
		AddHandler Me.commandsComboBox.SelectedIndexChanged, New System.EventHandler(AddressOf Me.commandsComboBox_SelectedIndexChanged)
		' 
		' pictureBoxPanel
		' 
		Me.pictureBoxPanel.Anchor = CType((((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Bottom) Or System.Windows.Forms.AnchorStyles.Left) Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
		Me.pictureBoxPanel.AutoScroll = True
		Me.pictureBoxPanel.Controls.Add(Me.pictureBox1)
		Me.pictureBoxPanel.Location = New System.Drawing.Point(12, 9)
		Me.pictureBoxPanel.Name = "pictureBoxPanel"
		Me.pictureBoxPanel.Size = New System.Drawing.Size(503, 513)
		Me.pictureBoxPanel.TabIndex = 2
		' 
		' stretchImageCheckBox
		' 
		Me.stretchImageCheckBox.Anchor = CType((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
		Me.stretchImageCheckBox.AutoSize = True
		Me.stretchImageCheckBox.Checked = True
		Me.stretchImageCheckBox.CheckState = System.Windows.Forms.CheckState.Checked
		Me.stretchImageCheckBox.Location = New System.Drawing.Point(521, 9)
		Me.stretchImageCheckBox.Name = "stretchImageCheckBox"
		Me.stretchImageCheckBox.Size = New System.Drawing.Size(92, 17)
		Me.stretchImageCheckBox.TabIndex = 3
		Me.stretchImageCheckBox.Text = "Stretch Image"
		Me.stretchImageCheckBox.UseVisualStyleBackColor = True
		AddHandler Me.stretchImageCheckBox.CheckedChanged, New System.EventHandler(AddressOf Me.stretchImageCheckBox_CheckedChanged)
		' 
		' ImageProcessingForm
		' 
		Me.AutoScaleDimensions = New System.Drawing.SizeF(6F, 13F)
		Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
		Me.ClientSize = New System.Drawing.Size(733, 534)
		Me.Controls.Add(Me.stretchImageCheckBox)
		Me.Controls.Add(Me.pictureBoxPanel)
		Me.Controls.Add(Me.groupBox1)
		Me.Name = "ImageProcessingForm"
		Me.Text = "Image Processing"
		AddHandler Me.Resize, New System.EventHandler(AddressOf Me.ImageProcessingForm_Resize)
		DirectCast(Me.pictureBox1, System.ComponentModel.ISupportInitialize).EndInit()
		Me.groupBox1.ResumeLayout(False)
		Me.groupBox1.PerformLayout()
		DirectCast(Me.param4NumericUpDown, System.ComponentModel.ISupportInitialize).EndInit()
		DirectCast(Me.param3NumericUpDown, System.ComponentModel.ISupportInitialize).EndInit()
		DirectCast(Me.param2NumericUpDown, System.ComponentModel.ISupportInitialize).EndInit()
		DirectCast(Me.param1NumericUpDown, System.ComponentModel.ISupportInitialize).EndInit()
		Me.pictureBoxPanel.ResumeLayout(False)
		Me.ResumeLayout(False)
		Me.PerformLayout()

	End Sub

	#End Region

	Private WithEvents pictureBox1 As System.Windows.Forms.PictureBox
	Private WithEvents groupBox1 As System.Windows.Forms.GroupBox
	Private WithEvents pictureBoxPanel As System.Windows.Forms.Panel
	Private WithEvents commandsComboBox As System.Windows.Forms.ComboBox
	Private WithEvents param4NumericUpDown As System.Windows.Forms.NumericUpDown
	Private WithEvents param4Label As System.Windows.Forms.Label
	Private WithEvents param3NumericUpDown As System.Windows.Forms.NumericUpDown
	Private WithEvents param3Label As System.Windows.Forms.Label
	Private WithEvents param2NumericUpDown As System.Windows.Forms.NumericUpDown
	Private WithEvents param2Label As System.Windows.Forms.Label
	Private WithEvents param1NumericUpDown As System.Windows.Forms.NumericUpDown
	Private WithEvents param1Label As System.Windows.Forms.Label
	Private WithEvents runCommandButton As System.Windows.Forms.Button
	Private WithEvents stretchImageCheckBox As System.Windows.Forms.CheckBox
	Private WithEvents processingCommandProgressBar As System.Windows.Forms.ProgressBar
End Class
