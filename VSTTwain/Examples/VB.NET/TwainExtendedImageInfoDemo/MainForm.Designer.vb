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
		Me.extendedImageInfoCheckedListBox = New System.Windows.Forms.CheckedListBox()
		Me.extendedImageInfoAboutAcquiredImageTextBox = New System.Windows.Forms.TextBox()
		Me.acquireImageButton = New System.Windows.Forms.Button()
		Me.groupBox1 = New System.Windows.Forms.GroupBox()
		Me.selectAllExtendedImageInfoButton = New System.Windows.Forms.Button()
		Me.groupBox2 = New System.Windows.Forms.GroupBox()
		Me.groupBox1.SuspendLayout()
		Me.groupBox2.SuspendLayout()
		Me.SuspendLayout()
		' 
		' extendedImageInfoCheckedListBox
		' 
		Me.extendedImageInfoCheckedListBox.Anchor = CType(((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Bottom) Or System.Windows.Forms.AnchorStyles.Left), System.Windows.Forms.AnchorStyles)
		Me.extendedImageInfoCheckedListBox.FormattingEnabled = True
		Me.extendedImageInfoCheckedListBox.Location = New System.Drawing.Point(12, 49)
		Me.extendedImageInfoCheckedListBox.Name = "extendedImageInfoCheckedListBox"
		Me.extendedImageInfoCheckedListBox.Size = New System.Drawing.Size(308, 484)
		Me.extendedImageInfoCheckedListBox.TabIndex = 1
		' 
		' extendedImageInfoAboutAcquiredImageTextBox
		' 
		Me.extendedImageInfoAboutAcquiredImageTextBox.Anchor = CType((((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Bottom) Or System.Windows.Forms.AnchorStyles.Left) Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
		Me.extendedImageInfoAboutAcquiredImageTextBox.Location = New System.Drawing.Point(10, 19)
		Me.extendedImageInfoAboutAcquiredImageTextBox.Multiline = True
		Me.extendedImageInfoAboutAcquiredImageTextBox.Name = "extendedImageInfoAboutAcquiredImageTextBox"
		Me.extendedImageInfoAboutAcquiredImageTextBox.ScrollBars = System.Windows.Forms.ScrollBars.Both
		Me.extendedImageInfoAboutAcquiredImageTextBox.Size = New System.Drawing.Size(333, 514)
		Me.extendedImageInfoAboutAcquiredImageTextBox.TabIndex = 2
		' 
		' acquireImageButton
		' 
		Me.acquireImageButton.Location = New System.Drawing.Point(12, 12)
		Me.acquireImageButton.Name = "acquireImageButton"
		Me.acquireImageButton.Size = New System.Drawing.Size(187, 45)
		Me.acquireImageButton.TabIndex = 110
		Me.acquireImageButton.Text = "Acquire image"
		Me.acquireImageButton.UseVisualStyleBackColor = True
		AddHandler Me.acquireImageButton.Click, New System.EventHandler(AddressOf Me.acquireImageButton_Click)
		' 
		' groupBox1
		' 
		Me.groupBox1.Anchor = CType(((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Bottom) Or System.Windows.Forms.AnchorStyles.Left), System.Windows.Forms.AnchorStyles)
		Me.groupBox1.Controls.Add(Me.selectAllExtendedImageInfoButton)
		Me.groupBox1.Controls.Add(Me.extendedImageInfoCheckedListBox)
		Me.groupBox1.Location = New System.Drawing.Point(12, 63)
		Me.groupBox1.Name = "groupBox1"
		Me.groupBox1.Size = New System.Drawing.Size(330, 543)
		Me.groupBox1.TabIndex = 111
		Me.groupBox1.TabStop = False
		Me.groupBox1.Text = "Extended Image Info to retrieve"
		' 
		' selectAllExtendedImageInfoButton
		' 
		Me.selectAllExtendedImageInfoButton.Location = New System.Drawing.Point(12, 20)
		Me.selectAllExtendedImageInfoButton.Name = "selectAllExtendedImageInfoButton"
		Me.selectAllExtendedImageInfoButton.Size = New System.Drawing.Size(75, 23)
		Me.selectAllExtendedImageInfoButton.TabIndex = 112
		Me.selectAllExtendedImageInfoButton.Text = "Select all"
		Me.selectAllExtendedImageInfoButton.UseVisualStyleBackColor = True
		AddHandler Me.selectAllExtendedImageInfoButton.Click, New System.EventHandler(AddressOf Me.selectAllExtendedImageInfoButton_Click)
		' 
		' groupBox2
		' 
		Me.groupBox2.Anchor = CType((((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Bottom) Or System.Windows.Forms.AnchorStyles.Left) Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
		Me.groupBox2.Controls.Add(Me.extendedImageInfoAboutAcquiredImageTextBox)
		Me.groupBox2.Location = New System.Drawing.Point(348, 63)
		Me.groupBox2.Name = "groupBox2"
		Me.groupBox2.Size = New System.Drawing.Size(353, 543)
		Me.groupBox2.TabIndex = 112
		Me.groupBox2.TabStop = False
		Me.groupBox2.Text = "Extended Image Info about acquired image(s)"
		' 
		' MainForm
		' 
		Me.AutoScaleDimensions = New System.Drawing.SizeF(6F, 13F)
		Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
		Me.ClientSize = New System.Drawing.Size(713, 618)
		Me.Controls.Add(Me.groupBox2)
		Me.Controls.Add(Me.groupBox1)
		Me.Controls.Add(Me.acquireImageButton)
		Me.Name = "MainForm"
		Me.Text = "VintaSoft TWAIN Extended Image Info Demo"
		AddHandler Me.Shown, New System.EventHandler(AddressOf Me.MainForm_Shown)
		AddHandler Me.FormClosing, New System.Windows.Forms.FormClosingEventHandler(AddressOf Me.MainForm_FormClosing)
		Me.groupBox1.ResumeLayout(False)
		Me.groupBox2.ResumeLayout(False)
		Me.groupBox2.PerformLayout()
		Me.ResumeLayout(False)

	End Sub

	#End Region

	Private WithEvents extendedImageInfoCheckedListBox As System.Windows.Forms.CheckedListBox
	Private WithEvents extendedImageInfoAboutAcquiredImageTextBox As System.Windows.Forms.TextBox
	Private WithEvents acquireImageButton As System.Windows.Forms.Button
	Private WithEvents groupBox1 As System.Windows.Forms.GroupBox
	Private WithEvents selectAllExtendedImageInfoButton As System.Windows.Forms.Button
	Private WithEvents groupBox2 As System.Windows.Forms.GroupBox
End Class

