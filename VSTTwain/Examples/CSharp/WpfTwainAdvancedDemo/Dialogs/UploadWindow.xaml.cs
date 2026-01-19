using System;
using System.Windows;
using System.Net;
using System.IO;
using Vintasoft.WpfTwain;
using Vintasoft.WpfTwain.ImageEncoders;
using Vintasoft.WpfTwain.ImageUploading.Ftp;
using Vintasoft.WpfTwain.ImageUploading.Http;

namespace WpfTwainAdvancedDemo
{
    /// <summary>
    /// Interaction logic for UploadWindow.xaml
    /// </summary>
    public partial class UploadWindow : Window
    {

        #region Fields

        // acquired image to upload
        AcquiredImage _acquiredImageToUpload;

        // FTP uploader
        FtpUpload _ftpUpload = null;
        // HTTP uploader
        HttpUpload _httpUpload = null;

        #endregion



        #region Constructor

        public UploadWindow(Window owner, AcquiredImage acquiredImageToUpload)
        {
            InitializeComponent();

            this.Owner = owner;

            _acquiredImageToUpload = acquiredImageToUpload;
        }

        #endregion



        #region Methdos

        #region FTP upload

        /// <summary>
        /// Start image uploading process to FTP server.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void ftpUploadButton_Click(object sender, RoutedEventArgs e)
        {
            MainWindow mainWindow = Owner as MainWindow;
            ftpUploadButton.IsEnabled = false;
            ftpUploadCancelButton.IsEnabled = true;
            ftpUploadProgressBar.Value = 0;

            try
            {
                _ftpUpload = new FtpUpload(this);
                _ftpUpload.StatusChanged += new EventHandler<Vintasoft.WpfTwain.ImageUploading.Ftp.StatusChangedEventArgs>(_ftpUpload_StatusChanged);
                _ftpUpload.ProgressChanged += new EventHandler<Vintasoft.WpfTwain.ImageUploading.Ftp.ProgressChangedEventArgs>(_ftpUpload_ProgressChanged);
                _ftpUpload.Completed += new EventHandler<Vintasoft.WpfTwain.ImageUploading.Ftp.CompletedEventArgs>(_ftpUpload_Completed);

                _ftpUpload.Host = ftpServerTextBox.Text;

                int ftpServerPort = 21;
                try
                {
                    ftpServerPort = int.Parse(ftpServerPortTextBox.Text);
                }
                catch
                {
                }
                _ftpUpload.Port = ftpServerPort;

                _ftpUpload.User = ftpUserTextBox.Text;
                _ftpUpload.Password = ftpPasswTextBox.Password;
                _ftpUpload.PassiveMode = (bool)flagPassModeCheckBox.IsChecked;
                _ftpUpload.Timeout = 2000;
                _ftpUpload.Path = ftpPathTextBox.Text;
                _ftpUpload.AddFile(ftpFileNameTextBox.Text, _acquiredImageToUpload.GetAsStream(GetImageFileFormat(ftpFileNameTextBox.Text)));
                _ftpUpload.PostData();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "FTP error", MessageBoxButton.OK, MessageBoxImage.Error);
                ftpUploadButton.IsEnabled = true;
                ftpUploadCancelButton.IsEnabled = false;
            }
            finally
            {
                ftpUploadProgressBar.Maximum = _ftpUpload.BytesTotal;
            }
        }

        /// <summary>
        /// Cancel image uploading process.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void ftpUploadCancelButton_Click(object sender, RoutedEventArgs e)
        {
            _ftpUpload.Abort();
        }

        /// <summary>
        /// Status of uploading process is changed.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void _ftpUpload_StatusChanged(object sender, Vintasoft.WpfTwain.ImageUploading.Ftp.StatusChangedEventArgs e)
        {
            ftpStatusLabel.Content = e.StatusString;
        }

        /// <summary>
        /// Progress of uploading process is changed.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void _ftpUpload_ProgressChanged(object sender, Vintasoft.WpfTwain.ImageUploading.Ftp.ProgressChangedEventArgs e)
        {
            ftpUploadProgressBar.Value = e.BytesUploaded;
            if (e.StatusCode == Vintasoft.WpfTwain.ImageUploading.Ftp.StatusCode.SendingData)
                ftpStatusLabel.Content = string.Format("{0}{1} Uploaded {2} bytes from {3} bytes.", e.StatusString, Environment.NewLine, e.BytesUploaded, e.BytesTotal);
        }

        /// <summary>
        /// Uploading process is completed.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void _ftpUpload_Completed(object sender, Vintasoft.WpfTwain.ImageUploading.Ftp.CompletedEventArgs e)
        {
            ftpStatusLabel.Content = "";

            if (e.ErrorCode == Vintasoft.WpfTwain.ImageUploading.Ftp.ErrorCode.None)
                MessageBox.Show("FTP: Image is uploaded successfully!", "FTP");
            else
                MessageBox.Show(e.ErrorString, "FTP error", MessageBoxButton.OK, MessageBoxImage.Error);

            ftpUploadButton.IsEnabled = true;
            ftpUploadCancelButton.IsEnabled = false;
        }

        #endregion


        #region HTTP upload

        /// <summary>
        /// Start image uploading process to FTP server.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void httpUploadButton_Click(object sender, RoutedEventArgs e)
        {
            MainWindow mainWindow = Owner as MainWindow;
            httpUploadButton.IsEnabled = false;
            httpUploadCancelButton.IsEnabled = true;
            httpUploadProgressBar.Value = 0;

            System.Net.ServicePointManager.Expect100Continue = false;

            try
            {
                _httpUpload = new HttpUpload(this);
                _httpUpload.StatusChanged += new EventHandler<Vintasoft.WpfTwain.ImageUploading.Http.StatusChangedEventArgs>(_httpUpload_StatusChanged);
                _httpUpload.ProgressChanged += new EventHandler<Vintasoft.WpfTwain.ImageUploading.Http.ProgressChangedEventArgs>(_httpUpload_ProgressChanged);
                _httpUpload.Completed += new EventHandler<Vintasoft.WpfTwain.ImageUploading.Http.CompletedEventArgs>(_httpUpload_Completed);

                _httpUpload.Url = httpUrlTextBox.Text;
                _httpUpload.UseDefaultCredentials = true;
                _httpUpload.AddTextField(httpTextField1TextBox.Text, httpTextField1ValueTextBox.Text);
                _httpUpload.AddTextField(httpTextField2TextBox.Text, httpTextField2ValueTextBox.Text);
                _httpUpload.AddFileField(httpFileFieldTextBox.Text, httpFileFieldValueTextBox.Text, _acquiredImageToUpload.GetAsStream(GetImageFileFormat(httpFileFieldValueTextBox.Text)));

                _httpUpload.PostData();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "HTTP error", MessageBoxButton.OK, MessageBoxImage.Error);
                httpUploadButton.IsEnabled = true;
                httpUploadCancelButton.IsEnabled = false;
            }
            finally
            {
                httpUploadProgressBar.Maximum = _httpUpload.BytesTotal;
            }
        }

        /// <summary>
        /// Cancel image uploading process.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void httpUploadCancelButton_Click(object sender, RoutedEventArgs e)
        {
            _httpUpload.Abort();
        }

        /// <summary>
        /// Status of uploading process is changed.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void _httpUpload_StatusChanged(object sender, Vintasoft.WpfTwain.ImageUploading.Http.StatusChangedEventArgs e)
        {
            httpStatusLabel.Content = e.StatusString;
        }

        /// <summary>
        /// Progress of uploading process is changed.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void _httpUpload_ProgressChanged(object sender, Vintasoft.WpfTwain.ImageUploading.Http.ProgressChangedEventArgs e)
        {
            httpUploadProgressBar.Value = e.BytesUploaded;
            if (e.StatusCode == Vintasoft.WpfTwain.ImageUploading.Http.StatusCode.Sending)
                httpStatusLabel.Content = string.Format("{0}{3} Uploaded {1}  bytes from {2} bytes", e.StatusString, e.BytesUploaded, e.BytesTotal, Environment.NewLine);
        }

        /// <summary>
        /// Uploading process is completed.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void _httpUpload_Completed(object sender, Vintasoft.WpfTwain.ImageUploading.Http.CompletedEventArgs e)
        {
            httpStatusLabel.Content = "";

            if (e.ErrorCode == 0)
            {
                if (e.ResponseCode == HttpStatusCode.OK)
                {
                    MessageBox.Show("HTTP: Image is uploaded successfully!", "HTTP");
                    MessageBox.Show("Response content: " + Environment.NewLine + e.ResponseContent, "HTTP");
                }
                else
                {
                    MessageBox.Show("Response code: " + e.ResponseCode, "HTTP");
                    MessageBox.Show("Response string: " + e.ResponseString, "HTTP");
                }
            }
            else
            {
                MessageBox.Show(e.ErrorString, "HTTP error", MessageBoxButton.OK, MessageBoxImage.Error);
            }

            httpUploadButton.IsEnabled = true;
            httpUploadCancelButton.IsEnabled = false;
        }

        #endregion


        #region Form events handlers

        /// <summary>
        /// Exit the window.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void exitButton_Click(object sender, RoutedEventArgs e)
        {
            DialogResult = false;
            Close();
        }

        #endregion


        private TwainImageEncoderSettings GetImageFileFormat(string filename)
        {
            string filenameExt = Path.GetExtension(filename);
            switch (filenameExt)
            {
                case ".bmp":
                    return new TwainBmpEncoderSettings();

                case ".gif":
                    return new TwainGifEncoderSettings();

                case ".pdf":
                    return new TwainPdfEncoderSettings();

                case ".png":
                    return new TwainPngEncoderSettings();

                case ".tif":
                case ".tiff":
                    return new TwainTiffEncoderSettings();
            }

            return new TwainJpegEncoderSettings();
        }

        #endregion

    }
}
