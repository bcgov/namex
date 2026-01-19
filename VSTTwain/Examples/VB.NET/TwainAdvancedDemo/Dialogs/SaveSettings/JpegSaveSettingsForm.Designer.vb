Partial Class JpegSaveSettingsForm
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
		Me.qualityNumericUpDown = New System.Windows.Forms.NumericUpDown()
		Me.label1 = New System.Windows.Forms.Label()
		Me.okButton = New System.Windows.Forms.Button()
		Me.cancelButton = New System.Windows.Forms.Button()
		DirectCast(Me.qualityNumericUpDown, System.ComponentModel.ISupportInitialize).BeginInit()
		Me.SuspendLayout()
		' 
		' qualityNumericUpDown
		' 
		Me.qualityNumericUpDown.Location = New System.Drawing.Point(94, 9)
		Me.qualityNumericUpDown.Minimum = New Decimal(New Integer() {5, 0, 0, 0})
		Me.qualityNumericUpDown.Name = "qualityNumericUpDown"
		Me.qualityNumericUpDown.Size = New System.Drawing.Size(89, 20)
		Me.qualityNumericUpDown.TabIndex = 1
		Me.qualityNumericUpDown.Value = New Decimal(New Integer() {90, 0, 0, 0})
		' 
		' label1
		' 
		Me.label1.AutoSize = True
		Me.label1.Location = New System.Drawing.Point(46, 11)
		Me.label1.Name = "label1"
		Me.label1.Size = New System.Drawing.Size(42, 13)
		Me.label1.TabIndex = 2
		Me.label1.Text = "Quality:"
		' 
		' okButton
		' 
		Me.okButton.Location = New System.Drawing.Point(33, 41)
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
		Me.cancelButton.Location = New System.Drawing.Point(120, 41)
		Me.cancelButton.Name = "cancelButton"
		Me.cancelButton.Size = New System.Drawing.Size(75, 23)
		Me.cancelButton.TabIndex = 4
		Me.cancelButton.Text = "Cancel"
		Me.cancelButton.UseVisualStyleBackColor = True
		' 
		' JpegSaveSettingsForm
		' 
		Me.AcceptButton = Me.okButton
		Me.AutoScaleDimensions = New System.Drawing.SizeF(6F, 13F)
		Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
		Me.CancelButton = Me.cancelButton
		Me.ClientSize = New System.Drawing.Size(229, 74)
		Me.Controls.Add(Me.cancelButton)
		Me.Controls.Add(Me.okButton)
		Me.Controls.Add(Me.label1)
		Me.Controls.Add(Me.qualityNumericUpDown)
		Me.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle
		Me.MaximizeBox = False
		Me.MinimizeBox = False
		Me.Name = "JpegSaveSettingsForm"
		Me.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent
		Me.Text = "JPEG save settings"
		DirectCast(Me.qualityNumericUpDown, System.ComponentModel.ISupportInitialize).EndInit()
		Me.ResumeLayout(False)
		Me.PerformLayout()

	End Sub

	#End Region

	Private WithEvents qualityNumericUpDown As System.Windows.Forms.NumericUpDown
	Private WithEvents label1 As System.Windows.Forms.Label
	Private WithEvents okButton As System.Windows.Forms.Button
	Private WithEvents cancelButton As System.Windows.Forms.Button
End Class
