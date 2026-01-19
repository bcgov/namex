Partial Class UploadForm
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
		Me.httpUrlTextBox = New System.Windows.Forms.TextBox()
		Me.label7 = New System.Windows.Forms.Label()
		Me.label15 = New System.Windows.Forms.Label()
		Me.httpStatusLabel = New System.Windows.Forms.Label()
		Me.httpFileFieldValueTextBox = New System.Windows.Forms.TextBox()
		Me.label13 = New System.Windows.Forms.Label()
		Me.label12 = New System.Windows.Forms.Label()
		Me.label11 = New System.Windows.Forms.Label()
		Me.httpTextField2TextBox = New System.Windows.Forms.TextBox()
		Me.httpFileFieldTextBox = New System.Windows.Forms.TextBox()
		Me.label14 = New System.Windows.Forms.Label()
		Me.label10 = New System.Windows.Forms.Label()
		Me.httpUploadCancelButton = New System.Windows.Forms.Button()
		Me.httpTextField1TextBox = New System.Windows.Forms.TextBox()
		Me.ftpFileNameTextBox = New System.Windows.Forms.TextBox()
		Me.ftpServerTextBox = New System.Windows.Forms.TextBox()
		Me.label4 = New System.Windows.Forms.Label()
		Me.label3 = New System.Windows.Forms.Label()
		Me.httpUploadButton = New System.Windows.Forms.Button()
		Me.label2 = New System.Windows.Forms.Label()
		Me.ftpPathTextBox = New System.Windows.Forms.TextBox()
		Me.ftpPasswordTextBox = New System.Windows.Forms.TextBox()
		Me.label9 = New System.Windows.Forms.Label()
		Me.label8 = New System.Windows.Forms.Label()
		Me.ftpUserTextBox = New System.Windows.Forms.TextBox()
		Me.httpTextField2ValueTextBox = New System.Windows.Forms.TextBox()
		Me.label1 = New System.Windows.Forms.Label()
		Me.ftpUploadProgressBar = New System.Windows.Forms.ProgressBar()
		Me.flagPassMode = New System.Windows.Forms.CheckBox()
		Me.label5 = New System.Windows.Forms.Label()
		Me.ftpServerPortTextBox = New System.Windows.Forms.TextBox()
		Me.ftpUploadButton = New System.Windows.Forms.Button()
		Me.ftpUploadCancelButton = New System.Windows.Forms.Button()
		Me.label6 = New System.Windows.Forms.Label()
		Me.httpUploadProgressBar = New System.Windows.Forms.ProgressBar()
		Me.groupBox3 = New System.Windows.Forms.GroupBox()
		Me.httpTextField1ValueTextBox = New System.Windows.Forms.TextBox()
		Me.groupBox2 = New System.Windows.Forms.GroupBox()
		Me.ftpStatusLabel = New System.Windows.Forms.Label()
		Me.groupBox1 = New System.Windows.Forms.GroupBox()
		Me.exitButton = New System.Windows.Forms.Button()
		Me.groupBox3.SuspendLayout()
		Me.groupBox2.SuspendLayout()
		Me.groupBox1.SuspendLayout()
		Me.SuspendLayout()
		' 
		' httpUrlTextBox
		' 
		Me.httpUrlTextBox.Location = New System.Drawing.Point(48, 24)
		Me.httpUrlTextBox.Name = "httpUrlTextBox"
		Me.httpUrlTextBox.Size = New System.Drawing.Size(248, 20)
		Me.httpUrlTextBox.TabIndex = 0
		Me.httpUrlTextBox.Text = "http://demos.vintasoft.com/WebTwainDemo/ImageUpload.aspx"
		' 
		' label7
		' 
		Me.label7.Location = New System.Drawing.Point(8, 24)
		Me.label7.Name = "label7"
		Me.label7.Size = New System.Drawing.Size(32, 16)
		Me.label7.TabIndex = 0
		Me.label7.Text = "URL:"
		' 
		' label15
		' 
		Me.label15.Location = New System.Drawing.Point(8, 184)
		Me.label15.Name = "label15"
		Me.label15.Size = New System.Drawing.Size(40, 16)
		Me.label15.TabIndex = 16
		Me.label15.Text = "Status:"
		' 
		' httpStatusLabel
		' 
		Me.httpStatusLabel.Location = New System.Drawing.Point(56, 184)
		Me.httpStatusLabel.Name = "httpStatusLabel"
		Me.httpStatusLabel.Size = New System.Drawing.Size(240, 24)
		Me.httpStatusLabel.TabIndex = 17
		' 
		' httpFileFieldValueTextBox
		' 
		Me.httpFileFieldValueTextBox.Location = New System.Drawing.Point(200, 16)
		Me.httpFileFieldValueTextBox.Name = "httpFileFieldValueTextBox"
		Me.httpFileFieldValueTextBox.Size = New System.Drawing.Size(80, 20)
		Me.httpFileFieldValueTextBox.TabIndex = 1
		Me.httpFileFieldValueTextBox.Text = "demo.jpg"
		' 
		' label13
		' 
		Me.label13.Location = New System.Drawing.Point(160, 64)
		Me.label13.Name = "label13"
		Me.label13.Size = New System.Drawing.Size(40, 16)
		Me.label13.TabIndex = 8
		Me.label13.Text = "Value:"
		' 
		' label12
		' 
		Me.label12.Location = New System.Drawing.Point(160, 40)
		Me.label12.Name = "label12"
		Me.label12.Size = New System.Drawing.Size(40, 16)
		Me.label12.TabIndex = 7
		Me.label12.Text = "Value:"
		' 
		' label11
		' 
		Me.label11.Location = New System.Drawing.Point(160, 16)
		Me.label11.Name = "label11"
		Me.label11.Size = New System.Drawing.Size(40, 16)
		Me.label11.TabIndex = 6
		Me.label11.Text = "Value:"
		' 
		' httpTextField2TextBox
		' 
		Me.httpTextField2TextBox.Location = New System.Drawing.Point(72, 64)
		Me.httpTextField2TextBox.Name = "httpTextField2TextBox"
		Me.httpTextField2TextBox.Size = New System.Drawing.Size(80, 20)
		Me.httpTextField2TextBox.TabIndex = 4
		' 
		' httpFileFieldTextBox
		' 
		Me.httpFileFieldTextBox.Location = New System.Drawing.Point(72, 16)
		Me.httpFileFieldTextBox.Name = "httpFileFieldTextBox"
		Me.httpFileFieldTextBox.Size = New System.Drawing.Size(80, 20)
		Me.httpFileFieldTextBox.TabIndex = 0
		Me.httpFileFieldTextBox.Text = "file"
		' 
		' label14
		' 
		Me.label14.Location = New System.Drawing.Point(8, 120)
		Me.label14.Name = "label14"
		Me.label14.Size = New System.Drawing.Size(64, 16)
		Me.label14.TabIndex = 16
		Me.label14.Text = "File name:"
		' 
		' label10
		' 
		Me.label10.Location = New System.Drawing.Point(8, 40)
		Me.label10.Name = "label10"
		Me.label10.Size = New System.Drawing.Size(64, 16)
		Me.label10.TabIndex = 2
		Me.label10.Text = "Text field 1:"
		' 
		' httpUploadCancelButton
		' 
		Me.httpUploadCancelButton.Enabled = False
		Me.httpUploadCancelButton.Location = New System.Drawing.Point(160, 216)
		Me.httpUploadCancelButton.Name = "httpUploadCancelButton"
		Me.httpUploadCancelButton.Size = New System.Drawing.Size(75, 23)
		Me.httpUploadCancelButton.TabIndex = 17
		Me.httpUploadCancelButton.Text = "Cancel"
		AddHandler Me.httpUploadCancelButton.Click, New System.EventHandler(AddressOf Me.httpUploadCancelButton_Click)
		' 
		' httpTextField1TextBox
		' 
		Me.httpTextField1TextBox.Location = New System.Drawing.Point(72, 40)
		Me.httpTextField1TextBox.Name = "httpTextField1TextBox"
		Me.httpTextField1TextBox.Size = New System.Drawing.Size(80, 20)
		Me.httpTextField1TextBox.TabIndex = 2
		' 
		' ftpFileNameTextBox
		' 
		Me.ftpFileNameTextBox.Location = New System.Drawing.Point(72, 120)
		Me.ftpFileNameTextBox.Name = "ftpFileNameTextBox"
		Me.ftpFileNameTextBox.Size = New System.Drawing.Size(184, 20)
		Me.ftpFileNameTextBox.TabIndex = 17
		Me.ftpFileNameTextBox.Text = "demo.jpg"
		' 
		' ftpServerTextBox
		' 
		Me.ftpServerTextBox.Location = New System.Drawing.Point(72, 24)
		Me.ftpServerTextBox.Name = "ftpServerTextBox"
		Me.ftpServerTextBox.Size = New System.Drawing.Size(184, 20)
		Me.ftpServerTextBox.TabIndex = 0
		Me.ftpServerTextBox.Text = "ftp.test.com"
		' 
		' label4
		' 
		Me.label4.Location = New System.Drawing.Point(8, 96)
		Me.label4.Name = "label4"
		Me.label4.Size = New System.Drawing.Size(64, 16)
		Me.label4.TabIndex = 3
		Me.label4.Text = "Path:"
		' 
		' label3
		' 
		Me.label3.Location = New System.Drawing.Point(144, 72)
		Me.label3.Name = "label3"
		Me.label3.Size = New System.Drawing.Size(64, 16)
		Me.label3.TabIndex = 2
		Me.label3.Text = "Password:"
		' 
		' httpUploadButton
		' 
		Me.httpUploadButton.Location = New System.Drawing.Point(72, 216)
		Me.httpUploadButton.Name = "httpUploadButton"
		Me.httpUploadButton.Size = New System.Drawing.Size(75, 23)
		Me.httpUploadButton.TabIndex = 5
		Me.httpUploadButton.Text = "Upload"
		AddHandler Me.httpUploadButton.Click, New System.EventHandler(AddressOf Me.httpUploadButton_Click)
		' 
		' label2
		' 
		Me.label2.Location = New System.Drawing.Point(8, 72)
		Me.label2.Name = "label2"
		Me.label2.Size = New System.Drawing.Size(64, 16)
		Me.label2.TabIndex = 1
		Me.label2.Text = "User:"
		' 
		' ftpPathTextBox
		' 
		Me.ftpPathTextBox.Location = New System.Drawing.Point(72, 96)
		Me.ftpPathTextBox.Name = "ftpPathTextBox"
		Me.ftpPathTextBox.Size = New System.Drawing.Size(184, 20)
		Me.ftpPathTextBox.TabIndex = 5
		Me.ftpPathTextBox.Text = "/imgs/"
		' 
		' ftpPasswordTextBox
		' 
		Me.ftpPasswordTextBox.Location = New System.Drawing.Point(200, 72)
		Me.ftpPasswordTextBox.Name = "ftpPasswordTextBox"
		Me.ftpPasswordTextBox.PasswordChar = "*"C
		Me.ftpPasswordTextBox.Size = New System.Drawing.Size(56, 20)
		Me.ftpPasswordTextBox.TabIndex = 4
		Me.ftpPasswordTextBox.Text = "guest"
		' 
		' label9
		' 
		Me.label9.Location = New System.Drawing.Point(8, 64)
		Me.label9.Name = "label9"
		Me.label9.Size = New System.Drawing.Size(64, 16)
		Me.label9.TabIndex = 1
		Me.label9.Text = "Text field 2:"
		' 
		' label8
		' 
		Me.label8.Location = New System.Drawing.Point(8, 16)
		Me.label8.Name = "label8"
		Me.label8.Size = New System.Drawing.Size(56, 16)
		Me.label8.TabIndex = 0
		Me.label8.Text = "File field:"
		' 
		' ftpUserTextBox
		' 
		Me.ftpUserTextBox.Location = New System.Drawing.Point(72, 72)
		Me.ftpUserTextBox.Name = "ftpUserTextBox"
		Me.ftpUserTextBox.Size = New System.Drawing.Size(64, 20)
		Me.ftpUserTextBox.TabIndex = 3
		Me.ftpUserTextBox.Text = "guest"
		' 
		' httpTextField2ValueTextBox
		' 
		Me.httpTextField2ValueTextBox.Location = New System.Drawing.Point(200, 64)
		Me.httpTextField2ValueTextBox.Name = "httpTextField2ValueTextBox"
		Me.httpTextField2ValueTextBox.Size = New System.Drawing.Size(80, 20)
		Me.httpTextField2ValueTextBox.TabIndex = 5
		' 
		' label1
		' 
		Me.label1.Location = New System.Drawing.Point(8, 24)
		Me.label1.Name = "label1"
		Me.label1.Size = New System.Drawing.Size(64, 16)
		Me.label1.TabIndex = 0
		Me.label1.Text = "Server:"
		' 
		' ftpUploadProgressBar
		' 
		Me.ftpUploadProgressBar.Location = New System.Drawing.Point(8, 152)
		Me.ftpUploadProgressBar.Name = "ftpUploadProgressBar"
		Me.ftpUploadProgressBar.Size = New System.Drawing.Size(248, 23)
		Me.ftpUploadProgressBar.TabIndex = 13
		' 
		' flagPassMode
		' 
		Me.flagPassMode.Location = New System.Drawing.Point(152, 48)
		Me.flagPassMode.Name = "flagPassMode"
		Me.flagPassMode.Size = New System.Drawing.Size(104, 16)
		Me.flagPassMode.TabIndex = 2
		Me.flagPassMode.Text = "Passive mode"
		' 
		' label5
		' 
		Me.label5.Location = New System.Drawing.Point(8, 48)
		Me.label5.Name = "label5"
		Me.label5.Size = New System.Drawing.Size(64, 16)
		Me.label5.TabIndex = 10
		Me.label5.Text = "Port:"
		' 
		' ftpServerPortTextBox
		' 
		Me.ftpServerPortTextBox.Location = New System.Drawing.Point(72, 48)
		Me.ftpServerPortTextBox.Name = "ftpServerPortTextBox"
		Me.ftpServerPortTextBox.Size = New System.Drawing.Size(48, 20)
		Me.ftpServerPortTextBox.TabIndex = 1
		Me.ftpServerPortTextBox.Text = "21"
		Me.ftpServerPortTextBox.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
		' 
		' ftpUploadButton
		' 
		Me.ftpUploadButton.Location = New System.Drawing.Point(48, 216)
		Me.ftpUploadButton.Name = "ftpUploadButton"
		Me.ftpUploadButton.Size = New System.Drawing.Size(75, 23)
		Me.ftpUploadButton.TabIndex = 6
		Me.ftpUploadButton.Text = "Upload"
		AddHandler Me.ftpUploadButton.Click, New System.EventHandler(AddressOf Me.ftpUploadButton_Click)
		' 
		' ftpUploadCancelButton
		' 
		Me.ftpUploadCancelButton.Enabled = False
		Me.ftpUploadCancelButton.Location = New System.Drawing.Point(139, 216)
		Me.ftpUploadCancelButton.Name = "ftpUploadCancelButton"
		Me.ftpUploadCancelButton.Size = New System.Drawing.Size(75, 23)
		Me.ftpUploadCancelButton.TabIndex = 9
		Me.ftpUploadCancelButton.Text = "Cancel"
		AddHandler Me.ftpUploadCancelButton.Click, New System.EventHandler(AddressOf Me.ftpUploadCancelButton_Click)
		' 
		' label6
		' 
		Me.label6.Location = New System.Drawing.Point(8, 184)
		Me.label6.Name = "label6"
		Me.label6.Size = New System.Drawing.Size(40, 16)
		Me.label6.TabIndex = 14
		Me.label6.Text = "Status:"
		' 
		' httpUploadProgressBar
		' 
		Me.httpUploadProgressBar.Location = New System.Drawing.Point(8, 152)
		Me.httpUploadProgressBar.Name = "httpUploadProgressBar"
		Me.httpUploadProgressBar.Size = New System.Drawing.Size(288, 23)
		Me.httpUploadProgressBar.TabIndex = 1
		' 
		' groupBox3
		' 
		Me.groupBox3.Controls.Add(Me.httpTextField2ValueTextBox)
		Me.groupBox3.Controls.Add(Me.httpTextField1ValueTextBox)
		Me.groupBox3.Controls.Add(Me.httpFileFieldValueTextBox)
		Me.groupBox3.Controls.Add(Me.label13)
		Me.groupBox3.Controls.Add(Me.label12)
		Me.groupBox3.Controls.Add(Me.label11)
		Me.groupBox3.Controls.Add(Me.httpTextField2TextBox)
		Me.groupBox3.Controls.Add(Me.httpTextField1TextBox)
		Me.groupBox3.Controls.Add(Me.httpFileFieldTextBox)
		Me.groupBox3.Controls.Add(Me.label10)
		Me.groupBox3.Controls.Add(Me.label9)
		Me.groupBox3.Controls.Add(Me.label8)
		Me.groupBox3.Location = New System.Drawing.Point(8, 48)
		Me.groupBox3.Name = "groupBox3"
		Me.groupBox3.Size = New System.Drawing.Size(288, 96)
		Me.groupBox3.TabIndex = 2
		Me.groupBox3.TabStop = False
		Me.groupBox3.Text = "Web form parameters"
		' 
		' httpTextField1ValueTextBox
		' 
		Me.httpTextField1ValueTextBox.Location = New System.Drawing.Point(200, 40)
		Me.httpTextField1ValueTextBox.Name = "httpTextField1ValueTextBox"
		Me.httpTextField1ValueTextBox.Size = New System.Drawing.Size(80, 20)
		Me.httpTextField1ValueTextBox.TabIndex = 3
		' 
		' groupBox2
		' 
		Me.groupBox2.Controls.Add(Me.httpUploadProgressBar)
		Me.groupBox2.Controls.Add(Me.groupBox3)
		Me.groupBox2.Controls.Add(Me.httpUrlTextBox)
		Me.groupBox2.Controls.Add(Me.label7)
		Me.groupBox2.Controls.Add(Me.label15)
		Me.groupBox2.Controls.Add(Me.httpStatusLabel)
		Me.groupBox2.Controls.Add(Me.httpUploadCancelButton)
		Me.groupBox2.Controls.Add(Me.httpUploadButton)
		Me.groupBox2.Location = New System.Drawing.Point(278, 5)
		Me.groupBox2.Name = "groupBox2"
		Me.groupBox2.Size = New System.Drawing.Size(304, 248)
		Me.groupBox2.TabIndex = 21
		Me.groupBox2.TabStop = False
		Me.groupBox2.Text = "HTTP"
		' 
		' ftpStatusLabel
		' 
		Me.ftpStatusLabel.Location = New System.Drawing.Point(56, 184)
		Me.ftpStatusLabel.Name = "ftpStatusLabel"
		Me.ftpStatusLabel.Size = New System.Drawing.Size(200, 24)
		Me.ftpStatusLabel.TabIndex = 15
		' 
		' groupBox1
		' 
		Me.groupBox1.Controls.Add(Me.ftpFileNameTextBox)
		Me.groupBox1.Controls.Add(Me.label14)
		Me.groupBox1.Controls.Add(Me.ftpPathTextBox)
		Me.groupBox1.Controls.Add(Me.ftpPasswordTextBox)
		Me.groupBox1.Controls.Add(Me.ftpUserTextBox)
		Me.groupBox1.Controls.Add(Me.ftpServerTextBox)
		Me.groupBox1.Controls.Add(Me.label4)
		Me.groupBox1.Controls.Add(Me.label3)
		Me.groupBox1.Controls.Add(Me.label2)
		Me.groupBox1.Controls.Add(Me.label1)
		Me.groupBox1.Controls.Add(Me.ftpStatusLabel)
		Me.groupBox1.Controls.Add(Me.label6)
		Me.groupBox1.Controls.Add(Me.ftpUploadProgressBar)
		Me.groupBox1.Controls.Add(Me.flagPassMode)
		Me.groupBox1.Controls.Add(Me.label5)
		Me.groupBox1.Controls.Add(Me.ftpServerPortTextBox)
		Me.groupBox1.Controls.Add(Me.ftpUploadButton)
		Me.groupBox1.Controls.Add(Me.ftpUploadCancelButton)
		Me.groupBox1.Location = New System.Drawing.Point(6, 5)
		Me.groupBox1.Name = "groupBox1"
		Me.groupBox1.Size = New System.Drawing.Size(264, 248)
		Me.groupBox1.TabIndex = 20
		Me.groupBox1.TabStop = False
		Me.groupBox1.Text = "FTP"
		' 
		' exitButton
		' 
		Me.exitButton.DialogResult = System.Windows.Forms.DialogResult.Cancel
		Me.exitButton.Location = New System.Drawing.Point(238, 261)
		Me.exitButton.Name = "exitButton"
		Me.exitButton.Size = New System.Drawing.Size(75, 23)
		Me.exitButton.TabIndex = 19
		Me.exitButton.Text = "Exit"
		' 
		' UploadForm
		' 
		Me.AutoScaleDimensions = New System.Drawing.SizeF(6F, 13F)
		Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
		Me.CancelButton = Me.exitButton
		Me.ClientSize = New System.Drawing.Size(591, 293)
		Me.Controls.Add(Me.groupBox2)
		Me.Controls.Add(Me.groupBox1)
		Me.Controls.Add(Me.exitButton)
		Me.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle
		Me.MaximizeBox = False
		Me.MinimizeBox = False
		Me.Name = "UploadForm"
		Me.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent
		Me.Text = "Upload image onto FTP or HTTP server"
		Me.groupBox3.ResumeLayout(False)
		Me.groupBox3.PerformLayout()
		Me.groupBox2.ResumeLayout(False)
		Me.groupBox2.PerformLayout()
		Me.groupBox1.ResumeLayout(False)
		Me.groupBox1.PerformLayout()
		Me.ResumeLayout(False)

	End Sub

	#End Region

	Private WithEvents httpUrlTextBox As System.Windows.Forms.TextBox
	Private WithEvents label7 As System.Windows.Forms.Label
	Private WithEvents label15 As System.Windows.Forms.Label
	Private WithEvents httpStatusLabel As System.Windows.Forms.Label
	Private WithEvents httpFileFieldValueTextBox As System.Windows.Forms.TextBox
	Private WithEvents label13 As System.Windows.Forms.Label
	Private WithEvents label12 As System.Windows.Forms.Label
	Private WithEvents label11 As System.Windows.Forms.Label
	Private WithEvents httpTextField2TextBox As System.Windows.Forms.TextBox
	Private WithEvents httpFileFieldTextBox As System.Windows.Forms.TextBox
	Private WithEvents label14 As System.Windows.Forms.Label
	Private WithEvents label10 As System.Windows.Forms.Label
	Private WithEvents httpUploadCancelButton As System.Windows.Forms.Button
	Private WithEvents httpTextField1TextBox As System.Windows.Forms.TextBox
	Private WithEvents ftpFileNameTextBox As System.Windows.Forms.TextBox
	Private WithEvents ftpServerTextBox As System.Windows.Forms.TextBox
	Private WithEvents label4 As System.Windows.Forms.Label
	Private WithEvents label3 As System.Windows.Forms.Label
	Private WithEvents httpUploadButton As System.Windows.Forms.Button
	Private WithEvents label2 As System.Windows.Forms.Label
	Private WithEvents ftpPathTextBox As System.Windows.Forms.TextBox
	Private WithEvents ftpPasswordTextBox As System.Windows.Forms.TextBox
	Private WithEvents label9 As System.Windows.Forms.Label
	Private WithEvents label8 As System.Windows.Forms.Label
	Private WithEvents ftpUserTextBox As System.Windows.Forms.TextBox
	Private WithEvents httpTextField2ValueTextBox As System.Windows.Forms.TextBox
	Private WithEvents label1 As System.Windows.Forms.Label
	Private WithEvents ftpUploadProgressBar As System.Windows.Forms.ProgressBar
	Private WithEvents flagPassMode As System.Windows.Forms.CheckBox
	Private WithEvents label5 As System.Windows.Forms.Label
	Private WithEvents ftpServerPortTextBox As System.Windows.Forms.TextBox
	Private WithEvents ftpUploadButton As System.Windows.Forms.Button
	Private WithEvents ftpUploadCancelButton As System.Windows.Forms.Button
	Private WithEvents label6 As System.Windows.Forms.Label
	Private WithEvents httpUploadProgressBar As System.Windows.Forms.ProgressBar
	Private WithEvents groupBox3 As System.Windows.Forms.GroupBox
	Private WithEvents httpTextField1ValueTextBox As System.Windows.Forms.TextBox
	Private WithEvents groupBox2 As System.Windows.Forms.GroupBox
	Private WithEvents ftpStatusLabel As System.Windows.Forms.Label
	Private WithEvents groupBox1 As System.Windows.Forms.GroupBox
	Private WithEvents exitButton As System.Windows.Forms.Button
End Class
