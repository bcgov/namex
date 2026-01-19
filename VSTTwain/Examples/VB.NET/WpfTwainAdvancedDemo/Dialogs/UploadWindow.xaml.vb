Imports System.Windows
Imports System.Net
Imports System.IO
Imports Vintasoft.WpfTwain
Imports Vintasoft.WpfTwain.ImageEncoders
Imports Vintasoft.WpfTwain.ImageUploading.Ftp
Imports Vintasoft.WpfTwain.ImageUploading.Http

''' <summary>
''' Interaction logic for UploadWindow.xaml
''' </summary>
Partial Public Class UploadWindow
    Inherits Window

#Region "Fields"

    ' acquired image to upload
    Private _acquiredImageToUpload As AcquiredImage

    ' FTP uploader
    Private _ftpUpload As FtpUpload = Nothing
    ' HTTP uploader
    Private _httpUpload As HttpUpload = Nothing

#End Region



#Region "Constructor"

    Public Sub New(ByVal owner As Window, ByVal acquiredImageToUpload As AcquiredImage)
        InitializeComponent()

        Me.Owner = owner

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
    Private Sub ftpUploadButton_Click(ByVal sender As Object, ByVal e As RoutedEventArgs)
        Dim mainWindow As MainWindow = TryCast(Owner, MainWindow)
        ftpUploadButton.IsEnabled = False
        ftpUploadCancelButton.IsEnabled = True
        ftpUploadProgressBar.Value = 0

        Try
            _ftpUpload = New FtpUpload(Me)
            AddHandler _ftpUpload.StatusChanged, New EventHandler(Of Vintasoft.WpfTwain.ImageUploading.Ftp.StatusChangedEventArgs)(AddressOf _ftpUpload_StatusChanged)
            AddHandler _ftpUpload.ProgressChanged, New EventHandler(Of Vintasoft.WpfTwain.ImageUploading.Ftp.ProgressChangedEventArgs)(AddressOf _ftpUpload_ProgressChanged)
            AddHandler _ftpUpload.Completed, New EventHandler(Of Vintasoft.WpfTwain.ImageUploading.Ftp.CompletedEventArgs)(AddressOf _ftpUpload_Completed)

            _ftpUpload.Host = ftpServerTextBox.Text

            Dim ftpServerPort As Integer = 21
            Try
                ftpServerPort = Integer.Parse(ftpServerPortTextBox.Text)
            Catch ex As Exception
            End Try
            _ftpUpload.Port = ftpServerPort

            _ftpUpload.User = ftpUserTextBox.Text
            _ftpUpload.Password = ftpPasswTextBox.Password
            _ftpUpload.PassiveMode = CBool(flagPassModeCheckBox.IsChecked)
            _ftpUpload.Timeout = 2000
            _ftpUpload.Path = ftpPathTextBox.Text
            _ftpUpload.AddFile(ftpFileNameTextBox.Text, _acquiredImageToUpload.GetAsStream(GetImageFileFormat(ftpFileNameTextBox.Text)))
            _ftpUpload.PostData()
        Catch ex As Exception
            MessageBox.Show(ex.Message, "FTP error", MessageBoxButton.OK, MessageBoxImage.[Error])
            ftpUploadButton.IsEnabled = True
            ftpUploadCancelButton.IsEnabled = False
        Finally
            ftpUploadProgressBar.Maximum = _ftpUpload.BytesTotal
        End Try
    End Sub

    ''' <summary>
    ''' Cancel image uploading process.
    ''' </summary>
    ''' <param name="sender"></param>
    ''' <param name="e"></param>
    Private Sub ftpUploadCancelButton_Click(ByVal sender As Object, ByVal e As RoutedEventArgs)
        _ftpUpload.Abort()
    End Sub

    ''' <summary>
    ''' Status of uploading process is changed.
    ''' </summary>
    ''' <param name="sender"></param>
    ''' <param name="e"></param>
    Private Sub _ftpUpload_StatusChanged(ByVal sender As Object, ByVal e As Vintasoft.WpfTwain.ImageUploading.Ftp.StatusChangedEventArgs)
        ftpStatusLabel.Content = e.StatusString
    End Sub

    ''' <summary>
    ''' Progress of uploading process is changed.
    ''' </summary>
    ''' <param name="sender"></param>
    ''' <param name="e"></param>
    Private Sub _ftpUpload_ProgressChanged(ByVal sender As Object, ByVal e As Vintasoft.WpfTwain.ImageUploading.Ftp.ProgressChangedEventArgs)
        ftpUploadProgressBar.Value = e.BytesUploaded
        If e.StatusCode = Vintasoft.WpfTwain.ImageUploading.Ftp.StatusCode.SendingData Then
            ftpStatusLabel.Content = String.Format("{0}{1} Uploaded {2} bytes from {3} bytes.", e.StatusString, Environment.NewLine, e.BytesUploaded, e.BytesTotal)
        End If
    End Sub

    ''' <summary>
    ''' Uploading process is completed.
    ''' </summary>
    ''' <param name="sender"></param>
    ''' <param name="e"></param>
    Private Sub _ftpUpload_Completed(ByVal sender As Object, ByVal e As Vintasoft.WpfTwain.ImageUploading.Ftp.CompletedEventArgs)
        ftpStatusLabel.Content = ""

        If e.ErrorCode = Vintasoft.WpfTwain.ImageUploading.Ftp.ErrorCode.None Then
            MessageBox.Show("FTP: Image is uploaded successfully!", "FTP")
        Else
            MessageBox.Show(e.ErrorString, "FTP error", MessageBoxButton.OK, MessageBoxImage.[Error])
        End If

        ftpUploadButton.IsEnabled = True
        ftpUploadCancelButton.IsEnabled = False
    End Sub

#End Region


#Region "HTTP upload"

    ''' <summary>
    ''' Start image uploading process to FTP server.
    ''' </summary>
    ''' <param name="sender"></param>
    ''' <param name="e"></param>
    Private Sub httpUploadButton_Click(ByVal sender As Object, ByVal e As RoutedEventArgs)
        Dim mainWindow As MainWindow = TryCast(Owner, MainWindow)
        httpUploadButton.IsEnabled = False
        httpUploadCancelButton.IsEnabled = True
        httpUploadProgressBar.Value = 0

        System.Net.ServicePointManager.Expect100Continue = False

        Try
            _httpUpload = New HttpUpload(Me)
            AddHandler _httpUpload.StatusChanged, New EventHandler(Of Vintasoft.WpfTwain.ImageUploading.Http.StatusChangedEventArgs)(AddressOf _httpUpload_StatusChanged)
            AddHandler _httpUpload.ProgressChanged, New EventHandler(Of Vintasoft.WpfTwain.ImageUploading.Http.ProgressChangedEventArgs)(AddressOf _httpUpload_ProgressChanged)
            AddHandler _httpUpload.Completed, New EventHandler(Of Vintasoft.WpfTwain.ImageUploading.Http.CompletedEventArgs)(AddressOf _httpUpload_Completed)

            _httpUpload.Url = httpUrlTextBox.Text
            _httpUpload.UseDefaultCredentials = True
            _httpUpload.AddTextField(httpTextField1TextBox.Text, httpTextField1ValueTextBox.Text)
            _httpUpload.AddTextField(httpTextField2TextBox.Text, httpTextField2ValueTextBox.Text)
            _httpUpload.AddFileField(httpFileFieldTextBox.Text, httpFileFieldValueTextBox.Text, _acquiredImageToUpload.GetAsStream(GetImageFileFormat(httpFileFieldValueTextBox.Text)))

            _httpUpload.PostData()
        Catch ex As Exception
            MessageBox.Show(ex.Message, "HTTP error", MessageBoxButton.OK, MessageBoxImage.[Error])
            httpUploadButton.IsEnabled = True
            httpUploadCancelButton.IsEnabled = False
        Finally
            httpUploadProgressBar.Maximum = _httpUpload.BytesTotal
        End Try
    End Sub

    ''' <summary>
    ''' Cancel image uploading process.
    ''' </summary>
    ''' <param name="sender"></param>
    ''' <param name="e"></param>
    Private Sub httpUploadCancelButton_Click(ByVal sender As Object, ByVal e As RoutedEventArgs)
        _httpUpload.Abort()
    End Sub

    ''' <summary>
    ''' Status of uploading process is changed.
    ''' </summary>
    ''' <param name="sender"></param>
    ''' <param name="e"></param>
    Private Sub _httpUpload_StatusChanged(ByVal sender As Object, ByVal e As Vintasoft.WpfTwain.ImageUploading.Http.StatusChangedEventArgs)
        httpStatusLabel.Content = e.StatusString
    End Sub

    ''' <summary>
    ''' Progress of uploading process is changed.
    ''' </summary>
    ''' <param name="sender"></param>
    ''' <param name="e"></param>
    Private Sub _httpUpload_ProgressChanged(ByVal sender As Object, ByVal e As Vintasoft.WpfTwain.ImageUploading.Http.ProgressChangedEventArgs)
        httpUploadProgressBar.Value = e.BytesUploaded
        If e.StatusCode = Vintasoft.WpfTwain.ImageUploading.Http.StatusCode.Sending Then
            httpStatusLabel.Content = String.Format("{0}{3} Uploaded {1}  bytes from {2} bytes", e.StatusString, e.BytesUploaded, e.BytesTotal, Environment.NewLine)
        End If
    End Sub

    ''' <summary>
    ''' Uploading process is completed.
    ''' </summary>
    ''' <param name="sender"></param>
    ''' <param name="e"></param>
    Private Sub _httpUpload_Completed(ByVal sender As Object, ByVal e As Vintasoft.WpfTwain.ImageUploading.Http.CompletedEventArgs)
        httpStatusLabel.Content = ""

        If e.ErrorCode = 0 Then
            If e.ResponseCode = HttpStatusCode.OK Then
                MessageBox.Show("HTTP: Image is uploaded successfully!", "HTTP")
                MessageBox.Show("Response content: " & Environment.NewLine & Convert.ToString(e.ResponseContent), "HTTP")
            Else
                MessageBox.Show("Response code: " & Convert.ToString(e.ResponseCode), "HTTP")
                MessageBox.Show("Response string: " & Convert.ToString(e.ResponseString), "HTTP")
            End If
        Else
            MessageBox.Show(e.ErrorString, "HTTP error", MessageBoxButton.OK, MessageBoxImage.[Error])
        End If

        httpUploadButton.IsEnabled = True
        httpUploadCancelButton.IsEnabled = False
    End Sub

#End Region


#Region "Form events handlers"

    ''' <summary>
    ''' Exit the window.
    ''' </summary>
    ''' <param name="sender"></param>
    ''' <param name="e"></param>
    Private Sub exitButton_Click(ByVal sender As Object, ByVal e As RoutedEventArgs)
        DialogResult = False
        Close()
    End Sub

#End Region


    Private Function GetImageFileFormat(ByVal filename As String) As TwainImageEncoderSettings
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
