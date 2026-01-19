Imports System.Windows.Forms
Imports System.Net
Imports System.IO
Imports Vintasoft.Twain
Imports Vintasoft.Twain.ImageEncoders
Imports Vintasoft.Twain.ImageUploading.Ftp
Imports Vintasoft.Twain.ImageUploading.Http

Public Partial Class UploadForm
	Inherits Form

	#Region "Fields"

	' acquired image to upload
	Private _acquiredImageToUpload As AcquiredImage

	' FTP uploader
	Private _ftpUpload As FtpUpload = Nothing
	' HTTP uploader
	Private _httpUpload As HttpUpload = Nothing

	#End Region



	#Region "Constructor"

	Public Sub New(acquiredImageToUpload As AcquiredImage)
		InitializeComponent()

		_acquiredImageToUpload = acquiredImageToUpload
	End Sub

	#End Region



	#Region "Methdos"

	#Region "FTP upload"

	''' <summary>
	''' Start image uploading process to FTP server.
	''' </summary>
	''' <param name="sender"></param>
	''' <param name="e"></param>
	Private Sub ftpUploadButton_Click(sender As Object, e As EventArgs)
		Dim mainForm As MainForm
		mainForm = TryCast(Owner, MainForm)
		ftpUploadButton.Enabled = False
		ftpUploadCancelButton.Enabled = True
		ftpUploadProgressBar.Value = 0

		Try
			_ftpUpload = New FtpUpload(Me)
            AddHandler _ftpUpload.StatusChanged, New EventHandler(Of Vintasoft.Twain.ImageUploading.Ftp.StatusChangedEventArgs)(AddressOf _ftpUpload_StatusChanged)
            AddHandler _ftpUpload.ProgressChanged, New EventHandler(Of Vintasoft.Twain.ImageUploading.Ftp.ProgressChangedEventArgs)(AddressOf _ftpUpload_ProgressChanged)
            AddHandler _ftpUpload.Completed, New EventHandler(Of Vintasoft.Twain.ImageUploading.Ftp.CompletedEventArgs)(AddressOf _ftpUpload_Completed)

			_ftpUpload.Host = ftpServerTextBox.Text

			Dim ftpServerPort As Integer = 21
			Try
				ftpServerPort = Integer.Parse(ftpServerPortTextBox.Text)
			Catch
			End Try
			_ftpUpload.Port = ftpServerPort

			_ftpUpload.User = ftpUserTextBox.Text
			_ftpUpload.Password = ftpPasswordTextBox.Text
			_ftpUpload.PassiveMode = flagPassMode.Checked
			_ftpUpload.Timeout = 2000
			_ftpUpload.Path = ftpPathTextBox.Text
			_ftpUpload.AddFile(ftpFileNameTextBox.Text, _acquiredImageToUpload.GetAsStream(GetImageFileFormat(ftpFileNameTextBox.Text)))
			_ftpUpload.PostData()
		Catch ex As Exception
			MessageBox.Show(ex.Message, "FTP error", MessageBoxButtons.OK, MessageBoxIcon.[Error])
			ftpUploadButton.Enabled = True
			ftpUploadCancelButton.Enabled = False
		Finally
			ftpUploadProgressBar.Maximum = _ftpUpload.BytesTotal
		End Try
	End Sub

	''' <summary>
	''' Cancel image uploading process.
	''' </summary>
	''' <param name="sender"></param>
	''' <param name="e"></param>
	Private Sub ftpUploadCancelButton_Click(sender As Object, e As EventArgs)
		_ftpUpload.Abort()
	End Sub

	''' <summary>
	''' Status of uploading process is changed.
	''' </summary>
	''' <param name="sender"></param>
	''' <param name="e"></param>
	Private Sub _ftpUpload_StatusChanged(sender As Object, e As Vintasoft.Twain.ImageUploading.Ftp.StatusChangedEventArgs)
		ftpStatusLabel.Text = e.StatusString
	End Sub

	''' <summary>
	''' Progress of uploading process is changed.
	''' </summary>
	''' <param name="sender"></param>
	''' <param name="e"></param>
	Private Sub _ftpUpload_ProgressChanged(sender As Object, e As Vintasoft.Twain.ImageUploading.Ftp.ProgressChangedEventArgs)
		ftpUploadProgressBar.Value = e.BytesUploaded
		If e.StatusCode = Vintasoft.Twain.ImageUploading.Ftp.StatusCode.SendingData Then
			ftpStatusLabel.Text = String.Format("{0}{1} Uploaded {2} bytes from {3} bytes.", e.StatusString, Environment.NewLine, e.BytesUploaded, e.BytesTotal)
		End If
	End Sub

	''' <summary>
	''' Uploading process is completed.
	''' </summary>
	''' <param name="sender"></param>
	''' <param name="e"></param>
	Private Sub _ftpUpload_Completed(sender As Object, e As Vintasoft.Twain.ImageUploading.Ftp.CompletedEventArgs)
		If e.ErrorCode = Vintasoft.Twain.ImageUploading.Ftp.ErrorCode.None Then
			MessageBox.Show("FTP: Image is uploaded successfully!", "FTP")
		Else
			MessageBox.Show(e.ErrorString, "FTP error", MessageBoxButtons.OK, MessageBoxIcon.[Error])
		End If

		ftpUploadButton.Enabled = True
		ftpUploadCancelButton.Enabled = False
	End Sub

	#End Region


	#Region "HTTP upload"

	''' <summary>
	''' Start image uploading process to FTP server.
	''' </summary>
	''' <param name="sender"></param>
	''' <param name="e"></param>
	Private Sub httpUploadButton_Click(sender As Object, e As EventArgs)
		Dim mainForm As MainForm
		mainForm = TryCast(Owner, MainForm)
		httpUploadButton.Enabled = False
		httpUploadCancelButton.Enabled = True
		httpUploadProgressBar.Value = 0

		System.Net.ServicePointManager.Expect100Continue = False

		Try
			_httpUpload = New HttpUpload(Me)
            AddHandler _httpUpload.StatusChanged, New EventHandler(Of Vintasoft.Twain.ImageUploading.Http.StatusChangedEventArgs)(AddressOf _httpUpload_StatusChanged)
            AddHandler _httpUpload.ProgressChanged, New EventHandler(Of Vintasoft.Twain.ImageUploading.Http.ProgressChangedEventArgs)(AddressOf _httpUpload_ProgressChanged)
            AddHandler _httpUpload.Completed, New EventHandler(Of Vintasoft.Twain.ImageUploading.Http.CompletedEventArgs)(AddressOf _httpUpload_Completed)

			_httpUpload.Url = httpUrlTextBox.Text
			_httpUpload.UseDefaultCredentials = True
			_httpUpload.AddTextField(httpTextField1TextBox.Text, httpTextField1ValueTextBox.Text)
			_httpUpload.AddTextField(httpTextField2TextBox.Text, httpTextField2ValueTextBox.Text)
			_httpUpload.AddFileField(httpFileFieldTextBox.Text, httpFileFieldValueTextBox.Text, _acquiredImageToUpload.GetAsStream(GetImageFileFormat(httpFileFieldValueTextBox.Text)))
			_httpUpload.PostData()
		Catch ex As Exception
			MessageBox.Show(ex.Message, "HTTP error", MessageBoxButtons.OK, MessageBoxIcon.[Error])
			httpUploadButton.Enabled = True
			httpUploadCancelButton.Enabled = False
		Finally
			httpUploadProgressBar.Maximum = _httpUpload.BytesTotal
		End Try
	End Sub

	''' <summary>
	''' Cancel image uploading process.
	''' </summary>
	''' <param name="sender"></param>
	''' <param name="e"></param>
	Private Sub httpUploadCancelButton_Click(sender As Object, e As EventArgs)
		_httpUpload.Abort()
	End Sub

	''' <summary>
	''' Status of uploading process is changed.
	''' </summary>
	''' <param name="sender"></param>
	''' <param name="e"></param>
	Private Sub _httpUpload_StatusChanged(sender As Object, e As Vintasoft.Twain.ImageUploading.Http.StatusChangedEventArgs)
		httpStatusLabel.Text = e.StatusString
	End Sub

	''' <summary>
	''' Progress of uploading process is changed.
	''' </summary>
	''' <param name="sender"></param>
	''' <param name="e"></param>
	Private Sub _httpUpload_ProgressChanged(sender As Object, e As Vintasoft.Twain.ImageUploading.Http.ProgressChangedEventArgs)
		httpUploadProgressBar.Value = e.BytesUploaded
		If e.StatusCode = Vintasoft.Twain.ImageUploading.Http.StatusCode.Sending Then
			httpStatusLabel.Text = String.Format("{0}{3} Uploaded {1}  bytes from {2} bytes", e.StatusString, e.BytesUploaded, e.BytesTotal, Environment.NewLine)
		End If
	End Sub

	''' <summary>
	''' Uploading process is completed.
	''' </summary>
	''' <param name="sender"></param>
	''' <param name="e"></param>
	Private Sub _httpUpload_Completed(sender As Object, e As Vintasoft.Twain.ImageUploading.Http.CompletedEventArgs)
		If e.ErrorCode = 0 Then
			If e.ResponseCode = HttpStatusCode.OK Then
				MessageBox.Show("HTTP: Image is uploaded successfully!", "HTTP")
				MessageBox.Show("Response content: " & Convert.ToString(e.ResponseContent), "HTTP")
			Else
				MessageBox.Show("Response code: " & Convert.ToString(e.ResponseCode), "HTTP")
				MessageBox.Show("Response string: " & Convert.ToString(e.ResponseString), "HTTP")
			End If
		Else
			MessageBox.Show(e.ErrorString, "HTTP error", MessageBoxButtons.OK, MessageBoxIcon.[Error])
		End If
		httpUploadButton.Enabled = True
		httpUploadCancelButton.Enabled = False
	End Sub

	#End Region


	Private Function GetImageFileFormat(filename As String) As TwainImageEncoderSettings
		Dim filenameExt As String = Path.GetExtension(filename)
		Select Case filenameExt
			Case ".bmp"
				Return New TwainBmpEncoderSettings()

			Case ".gif"
				Return New TwainGifEncoderSettings()

			Case ".pdf"
				Return New TwainPdfEncoderSettings()

			Case ".png"
				Return New TwainPngEncoderSettings()

			Case ".tif", ".tiff"
				Return New TwainTiffEncoderSettings()
		End Select

		Return New TwainJpegEncoderSettings()
	End Function

	#End Region

End Class
