using System;
using System.Windows;
using System.Windows.Media;
using Vintasoft.WpfTwain;
using Vintasoft.WpfTwain.ImageProcessing;

namespace WpfTwainAdvancedDemo
{
    /// <summary>
    /// Interaction logic for ImageProcessingWindow.xaml
    /// </summary>
    public partial class ImageProcessingWindow : Window
    {

        #region Fields

        AcquiredImage _image;

        #endregion



        #region Constructors

        public ImageProcessingWindow()
        {
            InitializeComponent();
        }

        public ImageProcessingWindow(AcquiredImage image)
            : this()
        {
            _image = image;
        }

        #endregion



        #region Methods

        /// <summary>
        /// Windows is loaded.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            commandsComboBox.Items.Add("Is Image Blank?");
            commandsComboBox.Items.Add("Invert");
            commandsComboBox.Items.Add("Change Brightness");
            commandsComboBox.Items.Add("Change Contrast");
            commandsComboBox.Items.Add("Crop");
            commandsComboBox.Items.Add("Resize Canvas");
            commandsComboBox.Items.Add("Rotate");
            commandsComboBox.Items.Add("Despeckle");
            commandsComboBox.Items.Add("Deskew");
            commandsComboBox.Items.Add("Remove Border");

            UpdateImage();
        }

        /// <summary>
        /// Update the image on a window.
        /// </summary>
        private void UpdateImage()
        {
            lock (_image)
            {
                // dispose previous image if necessary
                if (pictureBox1.Source != null)
                {
                    //pictureBox1.Source.Dispose();
                    pictureBox1.Source = null;
                }

                //
                pictureBox1.Source = _image.GetAsBitmapSource();
                //
                UpdateImageScrolls();

                //
                this.Title = string.Format("Image Processing - {0} bpp, {1}x{2}, {3}x{4} dpi", _image.ImageInfo.BitCount, _image.ImageInfo.Width, _image.ImageInfo.Height, _image.ImageInfo.Resolution.Horizontal, _image.ImageInfo.Resolution.Vertical);
            }
        }

        /// <summary>
        /// Update the scrolls of image.
        /// </summary>
        private void UpdateImageScrolls()
        {
            if (pictureBox1 != null && pictureBox1.Source != null)
            {
                if (chkStretchImage.IsChecked == true)
                {
                    pictureBox1.Width = imageScrollViewer.ViewportWidth;
                    pictureBox1.Height = imageScrollViewer.ViewportHeight;
                    pictureBox1.Stretch = Stretch.Fill;
                }
                else
                {
                    pictureBox1.Width = pictureBox1.Source.Width;
                    pictureBox1.Height = pictureBox1.Source.Height;
                    pictureBox1.Stretch = Stretch.None;
                }
            }
        }

        /// <summary>
        /// Value of stretch check box is changed.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void chkStretchImage_Checked(object sender, RoutedEventArgs e)
        {
            UpdateImageScrolls();
        }

        /// <summary>
        /// Scrolls of the image scroll viewer is changed.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void imageScrollViewer_ScrollChanged(object sender, System.Windows.Controls.ScrollChangedEventArgs e)
        {
            UpdateImageScrolls();
        }

        /// <summary>
        /// Processing command is changed.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void commandsComboBox_SelectionChanged(object sender, System.Windows.Controls.SelectionChangedEventArgs e)
        {
            param1Label.Visibility = Visibility.Hidden;
            param1NumericUpDown.Visibility = Visibility.Hidden;

            param2Label.Visibility = Visibility.Hidden;
            param2NumericUpDown.Visibility = Visibility.Hidden;

            param3Label.Visibility = Visibility.Hidden;
            param3NumericUpDown.Visibility = Visibility.Hidden;

            param4Label.Visibility = Visibility.Hidden;
            param4NumericUpDown.Visibility = Visibility.Hidden;

            switch ((string)commandsComboBox.SelectedValue)
            {
                case "Is Image Blank?":
                    param1Label.Content = "Max Noise Level (%):";
                    param1Label.Visibility = Visibility.Visible;
                    param1NumericUpDown.Minimum = 0;
                    param1NumericUpDown.Maximum = 100;
                    param1NumericUpDown.Value = 1;
                    param1NumericUpDown.Visibility = Visibility.Visible;
                    break;

                case "Change Brightness":
                    param1Label.Content = "Brightness:";
                    param1Label.Visibility = Visibility.Visible;
                    param1NumericUpDown.Minimum = -100;
                    param1NumericUpDown.Maximum = 100;
                    param1NumericUpDown.Value = 0;
                    param1NumericUpDown.Visibility = Visibility.Visible;
                    break;

                case "Change Contrast":
                    param1Label.Content = "Contrast:";
                    param1Label.Visibility = Visibility.Visible;
                    param1NumericUpDown.Minimum = -100;
                    param1NumericUpDown.Maximum = 100;
                    param1NumericUpDown.Value = 0;
                    param1NumericUpDown.Visibility = Visibility.Visible;
                    break;

                case "Crop":
                    param1Label.Content = "Left:";
                    param1Label.Visibility = Visibility.Visible;
                    param1NumericUpDown.Minimum = 0;
                    param1NumericUpDown.Maximum = _image.ImageInfo.Width - 1;
                    param1NumericUpDown.Value = 0;
                    param1NumericUpDown.Visibility = Visibility.Visible;

                    param2Label.Content = "Top:";
                    param2Label.Visibility = Visibility.Visible;
                    param2NumericUpDown.Minimum = 0;
                    param2NumericUpDown.Maximum = _image.ImageInfo.Height - 1;
                    param2NumericUpDown.Value = 0;
                    param2NumericUpDown.Visibility = Visibility.Visible;

                    param3Label.Content = "Width:";
                    param3Label.Visibility = Visibility.Visible;
                    param3NumericUpDown.Minimum = 0;
                    param3NumericUpDown.Maximum = _image.ImageInfo.Width;
                    param3NumericUpDown.Value = _image.ImageInfo.Width;
                    param3NumericUpDown.Visibility = Visibility.Visible;

                    param4Label.Content = "Height:";
                    param4Label.Visibility = Visibility.Visible;
                    param4NumericUpDown.Minimum = 0;
                    param4NumericUpDown.Maximum = _image.ImageInfo.Height;
                    param4NumericUpDown.Value = _image.ImageInfo.Height;
                    param4NumericUpDown.Visibility = Visibility.Visible;
                    break;

                case "Resize Canvas":
                    param1Label.Content = "Canvas Width:";
                    param1Label.Visibility = Visibility.Visible;
                    param1NumericUpDown.Minimum = _image.ImageInfo.Width;
                    param1NumericUpDown.Maximum = 2 * _image.ImageInfo.Width;
                    param1NumericUpDown.Value = _image.ImageInfo.Width;
                    param1NumericUpDown.Visibility = Visibility.Visible;

                    param2Label.Content = "Canvas Height:";
                    param2Label.Visibility = Visibility.Visible;
                    param2NumericUpDown.Minimum = _image.ImageInfo.Height;
                    param2NumericUpDown.Maximum = 2 * _image.ImageInfo.Height;
                    param2NumericUpDown.Value = _image.ImageInfo.Height;
                    param2NumericUpDown.Visibility = Visibility.Visible;

                    param3Label.Content = "Image X Pos:";
                    param3Label.Visibility = Visibility.Visible;
                    param3NumericUpDown.Minimum = 0;
                    param3NumericUpDown.Maximum = _image.ImageInfo.Width;
                    param3NumericUpDown.Value = 0;
                    param3NumericUpDown.Visibility = Visibility.Visible;

                    param4Label.Content = "Image Y Pos:";
                    param4Label.Visibility = Visibility.Visible;
                    param4NumericUpDown.Minimum = 0;
                    param4NumericUpDown.Maximum = _image.ImageInfo.Height;
                    param4NumericUpDown.Value = 0;
                    param4NumericUpDown.Visibility = Visibility.Visible;
                    break;
                
                case "Rotate":
                    param1Label.Content = "Angle:";
                    param1Label.Visibility = Visibility.Visible;
                    param1NumericUpDown.Minimum = 0;
                    param1NumericUpDown.Maximum = 360;
                    param1NumericUpDown.Value = 90;
                    param1NumericUpDown.Visibility = Visibility.Visible;
                    break;

                case "Despeckle":
                    param1Label.Content = "Level1:";
                    param1Label.Visibility = Visibility.Visible;
                    param1NumericUpDown.Minimum = 0;
                    param1NumericUpDown.Maximum = 100;
                    param1NumericUpDown.Value = 8;
                    param1NumericUpDown.Visibility = Visibility.Visible;

                    param2Label.Content = "Level2:";
                    param2Label.Visibility = Visibility.Visible;
                    param2NumericUpDown.Minimum = 0;
                    param2NumericUpDown.Maximum = 100;
                    param2NumericUpDown.Value = 25;
                    param2NumericUpDown.Visibility = Visibility.Visible;

                    param3Label.Content = "Radius:";
                    param3Label.Visibility = Visibility.Visible;
                    param3NumericUpDown.Minimum = 0;
                    param3NumericUpDown.Maximum = 100;
                    param3NumericUpDown.Value = 30;
                    param3NumericUpDown.Visibility = Visibility.Visible;

                    param4Label.Content = "Level3:";
                    param4Label.Visibility = Visibility.Visible;
                    param4NumericUpDown.Minimum = 0;
                    param4NumericUpDown.Maximum = 3000;
                    param4NumericUpDown.Value = 400;
                    param4NumericUpDown.Visibility = Visibility.Visible;
                    break;

                case "Deskew":
                    param1Label.Content = "Scan Interval X:";
                    param1Label.Visibility = Visibility.Visible;
                    param1NumericUpDown.Minimum = 1;
                    param1NumericUpDown.Maximum = 31;
                    param1NumericUpDown.Value = 5;
                    param1NumericUpDown.Visibility = Visibility.Visible;

                    param2Label.Content = "Scan Interval Y:";
                    param2Label.Visibility = Visibility.Visible;
                    param2NumericUpDown.Minimum = 1;
                    param2NumericUpDown.Maximum = 31;
                    param2NumericUpDown.Value = 5;
                    param2NumericUpDown.Visibility = Visibility.Visible;
                    break;

                case "Remove Border":
                    param1Label.Content = "Border Size:";
                    param1Label.Visibility = Visibility.Visible;
                    param1NumericUpDown.Minimum = 0;
                    param1NumericUpDown.Maximum = 100;
                    param1NumericUpDown.Value = 5;
                    param1NumericUpDown.Visibility = Visibility.Visible;
                    break;
            }
        }

        /// <summary>
        /// Run the processing command.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void runCommandButton_Click(object sender, RoutedEventArgs e)
        {
            lock (_image)
            {
                _image.Progress += new EventHandler<AcquiredImageProcessingProgressEventArgs>(ImageProcessingProgress);

                try
                {
                    switch (commandsComboBox.Text)
                    {
                        case "Is Image Blank?":
                            int maxNoiseLevel = (int)param1NumericUpDown.Value;
                            float currentNoiseLevel = 0;
                            if (_image.IsBlank(maxNoiseLevel, ref currentNoiseLevel))
                                MessageBox.Show(string.Format("Image is blank. Current noise level = {0}%", currentNoiseLevel));
                            else
                                MessageBox.Show(string.Format("Image is NOT blank. Current noise level = {0}%", currentNoiseLevel));
                            break;

                        case "Invert":
                            _image.Invert();
                            break;

                        case "Change Brightness":
                            int brightness = (int)param1NumericUpDown.Value;
                            _image.ChangeBrightness(brightness);
                            break;

                        case "Change Contrast":
                            int contrast = (int)param1NumericUpDown.Value;
                            _image.ChangeContrast(contrast);
                            break;

                        case "Crop":
                            int left = (int)param1NumericUpDown.Value;
                            int top = (int)param2NumericUpDown.Value;
                            int width = (int)param3NumericUpDown.Value;
                            int height = (int)param4NumericUpDown.Value;
                            try
                            {
                                _image.Crop(left, top, width, height);
                            }
                            catch (ArgumentOutOfRangeException ex)
                            {
                                MessageBox.Show(ex.Message);
                            }
                            break;

                        case "Resize Canvas":
                            int canvasWidth = (int)param1NumericUpDown.Value;
                            int canvasHeight = (int)param2NumericUpDown.Value;
                            int imageXPosition = (int)param3NumericUpDown.Value;
                            int imageYPosition = (int)param4NumericUpDown.Value;
                            try
                            {
                                _image.ResizeCanvas(canvasWidth, canvasHeight, BorderColor.AutoDetect, imageXPosition, imageYPosition);
                            }
                            catch (ArgumentOutOfRangeException ex)
                            {
                                MessageBox.Show(ex.Message);
                            }
                            break;

                        case "Rotate":
                            int angle = (int)param1NumericUpDown.Value;
                            _image.Rotate(angle, BorderColor.AutoDetect);
                            break;

                        case "Despeckle":
                            int level1 = (int)param1NumericUpDown.Value;
                            int level2 = (int)param2NumericUpDown.Value;
                            int radius = (int)param3NumericUpDown.Value;
                            int level3 = (int)param4NumericUpDown.Value;
                            _image.Despeckle(level1, level2, radius, level3);
                            break;

                        case "Deskew":
                            int scanIntervalX = (int)param1NumericUpDown.Value;
                            int scanIntervalY = (int)param2NumericUpDown.Value;
                            _image.Deskew(BorderColor.AutoDetect, scanIntervalX, scanIntervalY);
                            break;

                        case "Remove Border":
                            int borderSize = (int)param1NumericUpDown.Value;
                            _image.DetectBorder(borderSize);
                            break;
                    }
                }
                catch (ImagingException ex)
                {
                    MessageBox.Show(ex.Message);
                }

                _image.Progress -= new EventHandler<AcquiredImageProcessingProgressEventArgs>(ImageProcessingProgress);

                UpdateImage();
            }
        }

        /// <summary>
        /// Progress of processing command is changed.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void ImageProcessingProgress(object sender, AcquiredImageProcessingProgressEventArgs e)
        {
            processingCommandProgressBar.Value = e.Progress;
        }

        #endregion

    }
}
