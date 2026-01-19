Partial Class PdfSaveSettingsForm
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
		Me.pdfACompatibleCheckBox = New System.Windows.Forms.CheckBox()
		Me.groupBox2 = New System.Windows.Forms.GroupBox()
		Me.addToDocumentRadioButton = New System.Windows.Forms.RadioButton()
		Me.createNewDocumentRadioButton = New System.Windows.Forms.RadioButton()
		Me.pdfTitleTextBox = New System.Windows.Forms.TextBox()
		Me.label3 = New System.Windows.Forms.Label()
		Me.pdfAuthorTextBox = New System.Windows.Forms.TextBox()
		Me.label2 = New System.Windows.Forms.Label()
		Me.groupBox3 = New System.Windows.Forms.GroupBox()
		Me.saveAllImagesRadioButton = New System.Windows.Forms.RadioButton()
		Me.saveCurrentImageRadioButton = New System.Windows.Forms.RadioButton()
		DirectCast(Me.jpegQualityNumericUpDown, System.ComponentModel.ISupportInitialize).BeginInit()
		Me.groupBox1.SuspendLayout()
		Me.gbJpegCompression.SuspendLayout()
		Me.groupBox2.SuspendLayout()
		Me.groupBox3.SuspendLayout()
		Me.SuspendLayout()
		' 
		' jpegQualityNumericUpDown
		' 
		Me.jpegQualityNumericUpDown.Location = New System.Drawing.Point(108, 19)
		Me.jpegQualityNumericUpDown.Minimum = New Decimal(New Integer() {5, 0, 0, 0})
		Me.jpegQualityNumericUpDown.Name = "jpegQualityNumericUpDown"
		Me.jpegQualityNumericUpDown.Size = New System.Drawing.Size(89, 20)
		Me.jpegQualityNumericUpDown.TabIndex = 1
		Me.jpegQualityNumericUpDown.Value = New Decimal(New Integer() {90, 0, 0, 0})
		' 
		' label1
		' 
		Me.label1.AutoSize = True
		Me.label1.Location = New System.Drawing.Point(60, 21)
		Me.label1.Name = "label1"
		Me.label1.Size = New System.Drawing.Size(42, 13)
		Me.label1.TabIndex = 2
		Me.label1.Text = "Quality:"
		' 
		' okButton
		' 
		Me.okButton.Location = New System.Drawing.Point(57, 346)
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
		Me.cancelButton.Location = New System.Drawing.Point(144, 346)
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
		Me.groupBox1.Location = New System.Drawing.Point(10, 202)
		Me.groupBox1.Name = "groupBox1"
		Me.groupBox1.Size = New System.Drawing.Size(256, 80)
		Me.groupBox1.TabIndex = 5
		Me.groupBox1.TabStop = False
		Me.groupBox1.Text = "Compression"
		' 
		' zipCompressionRadioButton
		' 
		Me.zipCompressionRadioButton.AutoSize = True
		Me.zipCompressionRadioButton.Location = New System.Drawing.Point(157, 37)
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
		Me.jpegCompressionRadioButton.Location = New System.Drawing.Point(157, 55)
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
		Me.lzwCompressionRadioButton.Location = New System.Drawing.Point(157, 19)
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
		Me.gbJpegCompression.Location = New System.Drawing.Point(10, 286)
		Me.gbJpegCompression.Name = "gbJpegCompression"
		Me.gbJpegCompression.Size = New System.Drawing.Size(256, 51)
		Me.gbJpegCompression.TabIndex = 6
		Me.gbJpegCompression.TabStop = False
		Me.gbJpegCompression.Text = "JPEG compression"
		' 
		' pdfACompatibleCheckBox
		' 
		Me.pdfACompatibleCheckBox.AutoSize = True
		Me.pdfACompatibleCheckBox.Checked = True
		Me.pdfACompatibleCheckBox.CheckState = System.Windows.Forms.CheckState.Checked
		Me.pdfACompatibleCheckBox.Location = New System.Drawing.Point(12, 56)
		Me.pdfACompatibleCheckBox.Name = "pdfACompatibleCheckBox"
		Me.pdfACompatibleCheckBox.Size = New System.Drawing.Size(113, 17)
		Me.pdfACompatibleCheckBox.TabIndex = 8
		Me.pdfACompatibleCheckBox.Text = "PDF/A compatible"
		Me.pdfACompatibleCheckBox.UseVisualStyleBackColor = True
		' 
		' groupBox2
		' 
		Me.groupBox2.Controls.Add(Me.addToDocumentRadioButton)
		Me.groupBox2.Controls.Add(Me.createNewDocumentRadioButton)
		Me.groupBox2.Controls.Add(Me.pdfTitleTextBox)
		Me.groupBox2.Controls.Add(Me.label3)
		Me.groupBox2.Controls.Add(Me.pdfAuthorTextBox)
		Me.groupBox2.Controls.Add(Me.label2)
		Me.groupBox2.Controls.Add(Me.pdfACompatibleCheckBox)
		Me.groupBox2.Location = New System.Drawing.Point(10, 65)
		Me.groupBox2.Name = "groupBox2"
		Me.groupBox2.Size = New System.Drawing.Size(256, 133)
		Me.groupBox2.TabIndex = 9
		Me.groupBox2.TabStop = False
		Me.groupBox2.Text = "Document settings"
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
		' createNewDocumentRadioButton
		' 
		Me.createNewDocumentRadioButton.AutoSize = True
		Me.createNewDocumentRadioButton.Location = New System.Drawing.Point(12, 15)
		Me.createNewDocumentRadioButton.Name = "createNewDocumentRadioButton"
		Me.createNewDocumentRadioButton.Size = New System.Drawing.Size(129, 17)
		Me.createNewDocumentRadioButton.TabIndex = 14
		Me.createNewDocumentRadioButton.Text = "Create new document"
		Me.createNewDocumentRadioButton.UseVisualStyleBackColor = True
		' 
		' pdfTitleTextBox
		' 
		Me.pdfTitleTextBox.Location = New System.Drawing.Point(58, 103)
		Me.pdfTitleTextBox.Name = "pdfTitleTextBox"
		Me.pdfTitleTextBox.Size = New System.Drawing.Size(185, 20)
		Me.pdfTitleTextBox.TabIndex = 13
		' 
		' label3
		' 
		Me.label3.AutoSize = True
		Me.label3.Location = New System.Drawing.Point(9, 106)
		Me.label3.Name = "label3"
		Me.label3.Size = New System.Drawing.Size(30, 13)
		Me.label3.TabIndex = 12
		Me.label3.Text = "Title:"
		' 
		' pdfAuthorTextBox
		' 
		Me.pdfAuthorTextBox.Location = New System.Drawing.Point(58, 77)
		Me.pdfAuthorTextBox.Name = "pdfAuthorTextBox"
		Me.pdfAuthorTextBox.Size = New System.Drawing.Size(185, 20)
		Me.pdfAuthorTextBox.TabIndex = 11
		' 
		' label2
		' 
		Me.label2.AutoSize = True
		Me.label2.Location = New System.Drawing.Point(9, 80)
		Me.label2.Name = "label2"
		Me.label2.Size = New System.Drawing.Size(41, 13)
		Me.label2.TabIndex = 10
		Me.label2.Text = "Author:"
		' 
		' groupBox3
		' 
		Me.groupBox3.Controls.Add(Me.saveAllImagesRadioButton)
		Me.groupBox3.Controls.Add(Me.saveCurrentImageRadioButton)
		Me.groupBox3.Location = New System.Drawing.Point(10, 4)
		Me.groupBox3.Name = "groupBox3"
		Me.groupBox3.Size = New System.Drawing.Size(256, 58)
		Me.groupBox3.TabIndex = 12
		Me.groupBox3.TabStop = False
		Me.groupBox3.Text = "Save settings"
		' 
		' saveAllImagesRadioButton
		' 
		Me.saveAllImagesRadioButton.AutoSize = True
		Me.saveAllImagesRadioButton.Location = New System.Drawing.Point(15, 35)
		Me.saveAllImagesRadioButton.Name = "saveAllImagesRadioButton"
		Me.saveAllImagesRadioButton.Size = New System.Drawing.Size(99, 17)
		Me.saveAllImagesRadioButton.TabIndex = 1
		Me.saveAllImagesRadioButton.Text = "Save all images"
		Me.saveAllImagesRadioButton.UseVisualStyleBackColor = True
		' 
		' saveCurrentImageRadioButton
		' 
		Me.saveCurrentImageRadioButton.AutoSize = True
		Me.saveCurrentImageRadioButton.Checked = True
		Me.saveCurrentImageRadioButton.Location = New System.Drawing.Point(15, 17)
		Me.saveCurrentImageRadioButton.Name = "saveCurrentImageRadioButton"
		Me.saveCurrentImageRadioButton.Size = New System.Drawing.Size(139, 17)
		Me.saveCurrentImageRadioButton.TabIndex = 0
		Me.saveCurrentImageRadioButton.TabStop = True
		Me.saveCurrentImageRadioButton.Text = "Save only current image"
		Me.saveCurrentImageRadioButton.UseVisualStyleBackColor = True
		' 
		' PdfSaveSettingsForm
		' 
		Me.AcceptButton = Me.okButton
		Me.AutoScaleDimensions = New System.Drawing.SizeF(6F, 13F)
		Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
		Me.CancelButton = Me.cancelButton
		Me.ClientSize = New System.Drawing.Size(276, 375)
		Me.Controls.Add(Me.groupBox3)
		Me.Controls.Add(Me.groupBox2)
		Me.Controls.Add(Me.gbJpegCompression)
		Me.Controls.Add(Me.groupBox1)
		Me.Controls.Add(Me.cancelButton)
		Me.Controls.Add(Me.okButton)
		Me.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle
		Me.MaximizeBox = False
		Me.MinimizeBox = False
		Me.Name = "PdfSaveSettingsForm"
		Me.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent
		Me.Text = "PDF save settings"
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
	Private WithEvents pdfACompatibleCheckBox As System.Windows.Forms.CheckBox
	Private WithEvents groupBox2 As System.Windows.Forms.GroupBox
	Private WithEvents pdfAuthorTextBox As System.Windows.Forms.TextBox
	Private WithEvents label2 As System.Windows.Forms.Label
	Private WithEvents pdfTitleTextBox As System.Windows.Forms.TextBox
	Private WithEvents label3 As System.Windows.Forms.Label
	Private WithEvents addToDocumentRadioButton As System.Windows.Forms.RadioButton
	Private WithEvents createNewDocumentRadioButton As System.Windows.Forms.RadioButton
	Private WithEvents groupBox3 As System.Windows.Forms.GroupBox
	Private WithEvents saveAllImagesRadioButton As System.Windows.Forms.RadioButton
	Private WithEvents saveCurrentImageRadioButton As System.Windows.Forms.RadioButton
End Class
