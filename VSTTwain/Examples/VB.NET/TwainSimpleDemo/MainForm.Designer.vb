Imports Vintasoft.Twain
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
		Me.pictureBox1 = New System.Windows.Forms.PictureBox()
		Me.scanImagesButton = New System.Windows.Forms.Button()
		Me.twain2CheckBox = New System.Windows.Forms.CheckBox()
		Me.showIndicatorsCheckBox = New System.Windows.Forms.CheckBox()
		Me.showUiCheckBox = New System.Windows.Forms.CheckBox()
		DirectCast(Me.pictureBox1, System.ComponentModel.ISupportInitialize).BeginInit()
		Me.SuspendLayout()
		' 
		' pictureBox1
		' 
		Me.pictureBox1.Anchor = CType((((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Bottom) Or System.Windows.Forms.AnchorStyles.Left) Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
		Me.pictureBox1.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle
		Me.pictureBox1.Location = New System.Drawing.Point(7, 75)
		Me.pictureBox1.Name = "pictureBox1"
		Me.pictureBox1.Size = New System.Drawing.Size(440, 481)
		Me.pictureBox1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage
		Me.pictureBox1.TabIndex = 6
		Me.pictureBox1.TabStop = False
		' 
		' scanImagesButton
		' 
		Me.scanImagesButton.Location = New System.Drawing.Point(133, 12)
		Me.scanImagesButton.Name = "scanImagesButton"
		Me.scanImagesButton.Size = New System.Drawing.Size(314, 57)
		Me.scanImagesButton.TabIndex = 7
		Me.scanImagesButton.Text = "Scan images"
		AddHandler Me.scanImagesButton.Click, New System.EventHandler(AddressOf Me.scanImagesButton_Click)
		' 
		' twain2CheckBox
		' 
		Me.twain2CheckBox.AutoSize = True
		Me.twain2CheckBox.Checked = True
		Me.twain2CheckBox.CheckState = System.Windows.Forms.CheckState.Checked
		Me.twain2CheckBox.Location = New System.Drawing.Point(7, 12)
		Me.twain2CheckBox.Name = "twain2CheckBox"
		Me.twain2CheckBox.Size = New System.Drawing.Size(71, 17)
		Me.twain2CheckBox.TabIndex = 8
		Me.twain2CheckBox.Text = "TWAIN 2"
		Me.twain2CheckBox.UseVisualStyleBackColor = True
		' 
		' showIndicatorsCheckBox
		' 
		Me.showIndicatorsCheckBox.AutoSize = True
		Me.showIndicatorsCheckBox.Checked = True
		Me.showIndicatorsCheckBox.CheckState = System.Windows.Forms.CheckState.Checked
		Me.showIndicatorsCheckBox.Location = New System.Drawing.Point(7, 52)
		Me.showIndicatorsCheckBox.Name = "showIndicatorsCheckBox"
		Me.showIndicatorsCheckBox.Size = New System.Drawing.Size(102, 17)
		Me.showIndicatorsCheckBox.TabIndex = 9
		Me.showIndicatorsCheckBox.Text = "Show Indicators"
		Me.showIndicatorsCheckBox.UseVisualStyleBackColor = True
		' 
		' showUiCheckBox
		' 
		Me.showUiCheckBox.AutoSize = True
		Me.showUiCheckBox.Checked = True
		Me.showUiCheckBox.CheckState = System.Windows.Forms.CheckState.Checked
		Me.showUiCheckBox.Location = New System.Drawing.Point(7, 31)
		Me.showUiCheckBox.Name = "showUiCheckBox"
		Me.showUiCheckBox.Size = New System.Drawing.Size(67, 17)
		Me.showUiCheckBox.TabIndex = 10
		Me.showUiCheckBox.Text = "Show UI"
		Me.showUiCheckBox.UseVisualStyleBackColor = True
		' 
		' MainForm
		' 
		Me.AutoScaleDimensions = New System.Drawing.SizeF(6F, 13F)
		Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
		Me.ClientSize = New System.Drawing.Size(456, 566)
		Me.Controls.Add(Me.showUiCheckBox)
		Me.Controls.Add(Me.showIndicatorsCheckBox)
		Me.Controls.Add(Me.twain2CheckBox)
		Me.Controls.Add(Me.scanImagesButton)
		Me.Controls.Add(Me.pictureBox1)
		Me.Name = "MainForm"
		Me.Text = "VintaSoft TWAIN Simple Demo"
		DirectCast(Me.pictureBox1, System.ComponentModel.ISupportInitialize).EndInit()
		Me.ResumeLayout(False)
		Me.PerformLayout()

	End Sub

	#End Region

	Private WithEvents pictureBox1 As System.Windows.Forms.PictureBox
	Private WithEvents scanImagesButton As System.Windows.Forms.Button
	Private WithEvents twain2CheckBox As System.Windows.Forms.CheckBox
	Private WithEvents showIndicatorsCheckBox As System.Windows.Forms.CheckBox
	Private WithEvents showUiCheckBox As System.Windows.Forms.CheckBox
End Class

