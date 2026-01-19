Partial Class TiffSaveSettingsForm
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
		Me.jpegQualityNumericUpDown = New System.Windows.Forms.NumericUpDown()
		Me.label1 = New System.Windows.Forms.Label()
		Me.okButton = New System.Windows.Forms.Button()
		Me.cancelButton = New System.Windows.Forms.Button()
		Me.groupBox1 = New System.Windows.Forms.GroupBox()
		Me.zipCompressionRadioButton = New System.Windows.Forms.RadioButton()
		Me.autoCompressionRadioButton = New System.Windows.Forms.RadioButton()
		Me.jpegCompressionRadioButton = New System.Windows.Forms.RadioButton()
		Me.lzwCompressionRadioButton = New System.Windows.Forms.RadioButton()
		Me.ccittCompressionRadioButton = New System.Windows.Forms.RadioButton()
		Me.noneCompressionRadioButton = New System.Windows.Forms.RadioButton()
		Me.gbJpegCompression = New System.Windows.Forms.GroupBox()
		Me.createNewDocumentaddToDocumentRadioButton = New System.Windows.Forms.RadioButton()
		Me.addToDocumentRadioButton = New System.Windows.Forms.RadioButton()
		Me.groupBox2 = New System.Windows.Forms.GroupBox()
		Me.groupBox3 = New System.Windows.Forms.GroupBox()
		Me.saveAllImagesaddToDocumentRadioButton = New System.Windows.Forms.RadioButton()
		Me.saveCurrentImageaddToDocumentRadioButton = New System.Windows.Forms.RadioButton()
		DirectCast(Me.jpegQualityNumericUpDown, System.ComponentModel.ISupportInitialize).BeginInit()
		Me.groupBox1.SuspendLayout()
		Me.gbJpegCompression.SuspendLayout()
		Me.groupBox2.SuspendLayout()
		Me.groupBox3.SuspendLayout()
		Me.SuspendLayout()
		' 
		' jpegQualityNumericUpDown
		' 
		Me.jpegQualityNumericUpDown.Location = New System.Drawing.Point(81, 19)
		Me.jpegQualityNumericUpDown.Minimum = New Decimal(New Integer() {5, 0, 0, 0})
		Me.jpegQualityNumericUpDown.Name = "jpegQualityNumericUpDown"
		Me.jpegQualityNumericUpDown.Size = New System.Drawing.Size(89, 20)
		Me.jpegQualityNumericUpDown.TabIndex = 1
		Me.jpegQualityNumericUpDown.Value = New Decimal(New Integer() {90, 0, 0, 0})
		' 
		' label1
		' 
		Me.label1.AutoSize = True
		Me.label1.Location = New System.Drawing.Point(33, 21)
		Me.label1.Name = "label1"
		Me.label1.Size = New System.Drawing.Size(42, 13)
		Me.label1.TabIndex = 2
		Me.label1.Text = "Quality:"
		' 
		' okButton
		' 
		Me.okButton.Location = New System.Drawing.Point(40, 265)
		Me.okButton.Name = "okButton"
		Me.okButton.Size = New System.Drawing.Size(75, 23)
		Me.okButton.TabIndex = 3
		Me.okButton.Text = "Ok"
		Me.okButton.UseVisualStyleBackColor = True
		AddHandler Me.okButton.Click, New System.EventHandler(AddressOf Me.okButton_Click)
		' 
		' cancelButton
		' 
		Me.cancelButton.DialogResult = System.Windows.Forms.DialogResult.Cancel
		Me.cancelButton.Location = New System.Drawing.Point(127, 265)
		Me.cancelButton.Name = "cancelButton"
		Me.cancelButton.Size = New System.Drawing.Size(75, 23)
		Me.cancelButton.TabIndex = 4
		Me.cancelButton.Text = "Cancel"
		Me.cancelButton.UseVisualStyleBackColor = True
		' 
		' groupBox1
		' 
		Me.groupBox1.Controls.Add(Me.zipCompressionRadioButton)
		Me.groupBox1.Controls.Add(Me.autoCompressionRadioButton)
		Me.groupBox1.Controls.Add(Me.jpegCompressionRadioButton)
		Me.groupBox1.Controls.Add(Me.lzwCompressionRadioButton)
		Me.groupBox1.Controls.Add(Me.ccittCompressionRadioButton)
		Me.groupBox1.Controls.Add(Me.noneCompressionRadioButton)
		Me.groupBox1.Location = New System.Drawing.Point(8, 123)
		Me.groupBox1.Name = "groupBox1"
		Me.groupBox1.Size = New System.Drawing.Size(225, 80)
		Me.groupBox1.TabIndex = 5
		Me.groupBox1.TabStop = False
		Me.groupBox1.Text = "Compression"
		' 
		' zipCompressionRadioButton
		' 
		Me.zipCompressionRadioButton.AutoSize = True
		Me.zipCompressionRadioButton.Location = New System.Drawing.Point(145, 37)
		Me.zipCompressionRadioButton.Name = "zipCompressionRadioButton"
		Me.zipCompressionRadioButton.Size = New System.Drawing.Size(42, 17)
		Me.zipCompressionRadioButton.TabIndex = 5
		Me.zipCompressionRadioButton.Text = "ZIP"
		Me.zipCompressionRadioButton.UseVisualStyleBackColor = True
		AddHandler Me.zipCompressionRadioButton.CheckedChanged, New System.EventHandler(AddressOf Me.DisableJpegCompressionQuality)
		' 
		' autoCompressionRadioButton
		' 
		Me.autoCompressionRadioButton.AutoSize = True
		Me.autoCompressionRadioButton.Checked = True
		Me.autoCompressionRadioButton.Location = New System.Drawing.Point(12, 19)
		Me.autoCompressionRadioButton.Name = "autoCompressionRadioButton"
		Me.autoCompressionRadioButton.Size = New System.Drawing.Size(47, 17)
		Me.autoCompressionRadioButton.TabIndex = 4
		Me.autoCompressionRadioButton.TabStop = True
		Me.autoCompressionRadioButton.Text = "Auto"
		Me.autoCompressionRadioButton.UseVisualStyleBackColor = True
		AddHandler Me.autoCompressionRadioButton.CheckedChanged, New System.EventHandler(AddressOf Me.EnableJpegCompressionQuality)
		' 
		' jpegCompressionRadioButton
		' 
		Me.jpegCompressionRadioButton.AutoSize = True
		Me.jpegCompressionRadioButton.Location = New System.Drawing.Point(145, 55)
		Me.jpegCompressionRadioButton.Name = "jpegCompressionRadioButton"
		Me.jpegCompressionRadioButton.Size = New System.Drawing.Size(52, 17)
		Me.jpegCompressionRadioButton.TabIndex = 3
		Me.jpegCompressionRadioButton.Text = "JPEG"
		Me.jpegCompressionRadioButton.UseVisualStyleBackColor = True
		AddHandler Me.jpegCompressionRadioButton.CheckedChanged, New System.EventHandler(AddressOf Me.EnableJpegCompressionQuality)
		' 
		' lzwCompressionRadioButton
		' 
		Me.lzwCompressionRadioButton.AutoSize = True
		Me.lzwCompressionRadioButton.Location = New System.Drawing.Point(145, 19)
		Me.lzwCompressionRadioButton.Name = "lzwCompressionRadioButton"
		Me.lzwCompressionRadioButton.Size = New System.Drawing.Size(49, 17)
		Me.lzwCompressionRadioButton.TabIndex = 2
		Me.lzwCompressionRadioButton.Text = "LZW"
		Me.lzwCompressionRadioButton.UseVisualStyleBackColor = True
		AddHandler Me.lzwCompressionRadioButton.CheckedChanged, New System.EventHandler(AddressOf Me.DisableJpegCompressionQuality)
		' 
		' ccittCompressionRadioButton
		' 
		Me.ccittCompressionRadioButton.AutoSize = True
		Me.ccittCompressionRadioButton.Location = New System.Drawing.Point(12, 55)
		Me.ccittCompressionRadioButton.Name = "ccittCompressionRadioButton"
		Me.ccittCompressionRadioButton.Size = New System.Drawing.Size(117, 17)
		Me.ccittCompressionRadioButton.TabIndex = 1
		Me.ccittCompressionRadioButton.Text = "CCITT Group 4 Fax"
		Me.ccittCompressionRadioButton.UseVisualStyleBackColor = True
		AddHandler Me.ccittCompressionRadioButton.CheckedChanged, New System.EventHandler(AddressOf Me.DisableJpegCompressionQuality)
		' 
		' noneCompressionRadioButton
		' 
		Me.noneCompressionRadioButton.AutoSize = True
		Me.noneCompressionRadioButton.Location = New System.Drawing.Point(12, 37)
		Me.noneCompressionRadioButton.Name = "noneCompressionRadioButton"
		Me.noneCompressionRadioButton.Size = New System.Drawing.Size(51, 17)
		Me.noneCompressionRadioButton.TabIndex = 0
		Me.noneCompressionRadioButton.Text = "None"
		Me.noneCompressionRadioButton.UseVisualStyleBackColor = True
		AddHandler Me.noneCompressionRadioButton.CheckedChanged, New System.EventHandler(AddressOf Me.DisableJpegCompressionQuality)
		' 
		' gbJpegCompression
		' 
		Me.gbJpegCompression.Controls.Add(Me.jpegQualityNumericUpDown)
		Me.gbJpegCompression.Controls.Add(Me.label1)
		Me.gbJpegCompression.Enabled = False
		Me.gbJpegCompression.Location = New System.Drawing.Point(8, 206)
		Me.gbJpegCompression.Name = "gbJpegCompression"
		Me.gbJpegCompression.Size = New System.Drawing.Size(225, 51)
		Me.gbJpegCompression.TabIndex = 6
		Me.gbJpegCompression.TabStop = False
		Me.gbJpegCompression.Text = "JPEG compression"
		' 
		' createNewDocumentaddToDocumentRadioButton
		' 
		Me.createNewDocumentaddToDocumentRadioButton.AutoSize = True
		Me.createNewDocumentaddToDocumentRadioButton.Location = New System.Drawing.Point(12, 15)
		Me.createNewDocumentaddToDocumentRadioButton.Name = "createNewDocumentaddToDocumentRadioButton"
		Me.createNewDocumentaddToDocumentRadioButton.Size = New System.Drawing.Size(129, 17)
		Me.createNewDocumentaddToDocumentRadioButton.TabIndex = 14
		Me.createNewDocumentaddToDocumentRadioButton.Text = "Create new document"
		Me.createNewDocumentaddToDocumentRadioButton.UseVisualStyleBackColor = True
		' 
		' addToDocumentRadioButton
		' 
		Me.addToDocumentRadioButton.AutoSize = True
		Me.addToDocumentRadioButton.Checked = True
		Me.addToDocumentRadioButton.Location = New System.Drawing.Point(12, 32)
		Me.addToDocumentRadioButton.Name = "addToDocumentRadioButton"
		Me.addToDocumentRadioButton.Size = New System.Drawing.Size(144, 17)
		Me.addToDocumentRadioButton.TabIndex = 15
		Me.addToDocumentRadioButton.TabStop = True
		Me.addToDocumentRadioButton.Text = "Add to existing document"
		Me.addToDocumentRadioButton.UseVisualStyleBackColor = True
		' 
		' groupBox2
		' 
		Me.groupBox2.Controls.Add(Me.addToDocumentRadioButton)
		Me.groupBox2.Controls.Add(Me.createNewDocumentaddToDocumentRadioButton)
		Me.groupBox2.Location = New System.Drawing.Point(8, 64)
		Me.groupBox2.Name = "groupBox2"
		Me.groupBox2.Size = New System.Drawing.Size(225, 55)
		Me.groupBox2.TabIndex = 10
		Me.groupBox2.TabStop = False
		Me.groupBox2.Text = "Document settings"
		' 
		' groupBox3
		' 
		Me.groupBox3.Controls.Add(Me.saveAllImagesaddToDocumentRadioButton)
		Me.groupBox3.Controls.Add(Me.saveCurrentImageaddToDocumentRadioButton)
		Me.groupBox3.Location = New System.Drawing.Point(8, 4)
		Me.groupBox3.Name = "groupBox3"
		Me.groupBox3.Size = New System.Drawing.Size(225, 58)
		Me.groupBox3.TabIndex = 11
		Me.groupBox3.TabStop = False
		Me.groupBox3.Text = "Save settings"
		' 
		' saveAllImagesaddToDocumentRadioButton
		' 
		Me.saveAllImagesaddToDocumentRadioButton.AutoSize = True
		Me.saveAllImagesaddToDocumentRadioButton.Location = New System.Drawing.Point(15, 35)
		Me.saveAllImagesaddToDocumentRadioButton.Name = "saveAllImagesaddToDocumentRadioButton"
		Me.saveAllImagesaddToDocumentRadioButton.Size = New System.Drawing.Size(99, 17)
		Me.saveAllImagesaddToDocumentRadioButton.TabIndex = 1
		Me.saveAllImagesaddToDocumentRadioButton.Text = "Save all images"
		Me.saveAllImagesaddToDocumentRadioButton.UseVisualStyleBackColor = True
		' 
		' saveCurrentImageaddToDocumentRadioButton
		' 
		Me.saveCurrentImageaddToDocumentRadioButton.AutoSize = True
		Me.saveCurrentImageaddToDocumentRadioButton.Checked = True
		Me.saveCurrentImageaddToDocumentRadioButton.Location = New System.Drawing.Point(15, 17)
		Me.saveCurrentImageaddToDocumentRadioButton.Name = "saveCurrentImageaddToDocumentRadioButton"
		Me.saveCurrentImageaddToDocumentRadioButton.Size = New System.Drawing.Size(139, 17)
		Me.saveCurrentImageaddToDocumentRadioButton.TabIndex = 0
		Me.saveCurrentImageaddToDocumentRadioButton.TabStop = True
		Me.saveCurrentImageaddToDocumentRadioButton.Text = "Save only current image"
		Me.saveCurrentImageaddToDocumentRadioButton.UseVisualStyleBackColor = True
		' 
		' TiffSaveSettingsForm
		' 
		Me.AcceptButton = Me.okButton
		Me.AutoScaleDimensions = New System.Drawing.SizeF(6F, 13F)
		Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
		Me.CancelButton = Me.cancelButton
		Me.ClientSize = New System.Drawing.Size(242, 296)
		Me.Controls.Add(Me.groupBox3)
		Me.Controls.Add(Me.groupBox2)
		Me.Controls.Add(Me.gbJpegCompression)
		Me.Controls.Add(Me.groupBox1)
		Me.Controls.Add(Me.cancelButton)
		Me.Controls.Add(Me.okButton)
		Me.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle
		Me.MaximizeBox = False
		Me.MinimizeBox = False
		Me.Name = "TiffSaveSettingsForm"
		Me.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent
		Me.Text = "TIFF save settings"
		DirectCast(Me.jpegQualityNumericUpDown, System.ComponentModel.ISupportInitialize).EndInit()
		Me.groupBox1.ResumeLayout(False)
		Me.groupBox1.PerformLayout()
		Me.gbJpegCompression.ResumeLayout(False)
		Me.gbJpegCompression.PerformLayout()
		Me.groupBox2.ResumeLayout(False)
		Me.groupBox2.PerformLayout()
		Me.groupBox3.ResumeLayout(False)
		Me.groupBox3.PerformLayout()
		Me.ResumeLayout(False)

	End Sub

	#End Region

	Private WithEvents jpegQualityNumericUpDown As System.Windows.Forms.NumericUpDown
	Private WithEvents label1 As System.Windows.Forms.Label
	Private WithEvents okButton As System.Windows.Forms.Button
	Private WithEvents cancelButton As System.Windows.Forms.Button
	Private WithEvents groupBox1 As System.Windows.Forms.GroupBox
	Private WithEvents noneCompressionRadioButton As System.Windows.Forms.RadioButton
	Private WithEvents jpegCompressionRadioButton As System.Windows.Forms.RadioButton
	Private WithEvents lzwCompressionRadioButton As System.Windows.Forms.RadioButton
	Private WithEvents ccittCompressionRadioButton As System.Windows.Forms.RadioButton
	Private WithEvents gbJpegCompression As System.Windows.Forms.GroupBox
	Private WithEvents autoCompressionRadioButton As System.Windows.Forms.RadioButton
	Private WithEvents zipCompressionRadioButton As System.Windows.Forms.RadioButton
	Private WithEvents createNewDocumentaddToDocumentRadioButton As System.Windows.Forms.RadioButton
	Private WithEvents addToDocumentRadioButton As System.Windows.Forms.RadioButton
	Private WithEvents groupBox2 As System.Windows.Forms.GroupBox
	Private WithEvents groupBox3 As System.Windows.Forms.GroupBox
	Private WithEvents saveAllImagesaddToDocumentRadioButton As System.Windows.Forms.RadioButton
	Private WithEvents saveCurrentImageaddToDocumentRadioButton As System.Windows.Forms.RadioButton
End Class
