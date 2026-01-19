using System;
using System.Windows.Forms;
using System.Drawing;
using Vintasoft.Twain;
using Vintasoft.Twain.ImageProcessing;

namespace TwainAdvancedDemo
{
    public partial class ImageProcessingForm : Form
    {

        #region Fields

        AcquiredImage _image;

        #endregion



        #region Constructors

        public ImageProcessingForm()
        {
            InitializeComponent();
        }

        public ImageProcessingForm(AcquiredImage image)
            : this()
        {
            _image = image;

            UpdateImage();
        }

        #endregion



        #region Methods

        /// <summary>
        /// Update the image on a form.
        /// </summary>
        private void UpdateImage()
        {
            lock (_image)
            {
                if (pictureBox1.Image != null)
                {
                    pictureBox1.Image.Dispose();
                    pictureBox1.Image = null;
                }

                pictureBox1.Image = _image.GetAsBitmap();

                this.Text = string.Format("Image Processing - {0} bpp, {1}x{2}, {3}x{4} dpi", _image.ImageInfo.BitCount, _image.ImageInfo.Width, _image.ImageInfo.Height, _image.ImageInfo.Resolution.Horizontal, _image.ImageInfo.Resolution.Vertical);
            }
        }

        /// <summary>
        /// Value of stretch check box is changed.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void stretchImageCheckBox_CheckedChanged(object sender, EventArgs e)
        {
            if (stretchImageCheckBox.Checked)
            {
                pictureBox1.Size = new Size(pictureBoxPanel.Size.Width - 2, pictureBoxPanel.Size.Height - 2);
                pictureBox1.SizeMode = PictureBoxSizeMode.StretchImage;
            }
            else
                pictureBox1.SizeMode = PictureBoxSizeMode.AutoSize;
        }

        /// <summary>
        /// Form is resized.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void ImageProcessingForm_Resize(object sender, EventArgs e)
        {
            if (stretchImageCheckBox.Checked)
                pictureBox1.Size = new Size(pictureBoxPanel.Size.Width - 2, pictureBoxPanel.Size.Height - 2);
        }

        /// <summary>
        /// Processing command is changed.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void commandsComboBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            param1Label.Visible = false;
            param1NumericUpDown.Visible = false;

            param2Label.Visible = false;
            param2NumericUpDown.Visible = false;

            param3Label.Visible = false;
            param3NumericUpDown.Visible = false;

            param4Label.Visible = false;
            param4NumericUpDown.Visible = false;

            switch (commandsComboBox.Text)
            {
                case "Is Image Blank?":
                    param1Label.Text = "Max Noise Level (%):";
                    param1Label.Visible = true;
                    param1NumericUpDown.Minimum = 0;
                    param1NumericUpDown.Maximum = 100;
                    param1NumericUpDown.Value = 1;
                    param1NumericUpDown.Visible = true;
                    break;
                
                case "Change Brightness":
                    param1Label.Text = "Brightness:";
                    param1Label.Visible = true;
                    param1NumericUpDown.Minimum = -100;
                    param1NumericUpDown.Maximum = 100;
                    param1NumericUpDown.Value = 0;
                    param1NumericUpDown.Visible = true;
                    break;

                case "Change Contrast":
                    param1Label.Text = "Contrast:";
                    param1Label.Visible = true;
                    param1NumericUpDown.Minimum = -100;
                    param1NumericUpDown.Maximum = 100;
                    param1NumericUpDown.Value = 0;
                    param1NumericUpDown.Visible = true;
                    break;

                case "Crop":
                    param1Label.Text = "Left:";
                    param1Label.Visible = true;
                    param1NumericUpDown.Minimum = 0;
                    param1NumericUpDown.Maximum = _image.ImageInfo.Width - 1;
                    param1NumericUpDown.Value = 0;
                    param1NumericUpDown.Visible = true;

                    param2Label.Text = "Top:";
                    param2Label.Visible = true;
                    param2NumericUpDown.Minimum = 0;
                    param2NumericUpDown.Maximum = _image.ImageInfo.Height - 1;
                    param2NumericUpDown.Value = 0;
                    param2NumericUpDown.Visible = true;

                    param3Label.Text = "Width:";
                    param3Label.Visible = true;
                    param3NumericUpDown.Minimum = 0;
                    param3NumericUpDown.Maximum = _image.ImageInfo.Width;
                    param3NumericUpDown.Value = _image.ImageInfo.Width;
                    param3NumericUpDown.Visible = true;

                    param4Label.Text = "Height:";
                    param4Label.Visible = true;
                    param4NumericUpDown.Minimum = 0;
                    param4NumericUpDown.Maximum = _image.ImageInfo.Height;
                    param4NumericUpDown.Value = _image.ImageInfo.Height;
                    param4NumericUpDown.Visible = true;
                    break;

                case "Resize Canvas":
                    param1Label.Text = "Canvas Width:";
                    param1Label.Visible = true;
                    param1NumericUpDown.Minimum = _image.ImageInfo.Width;
                    param1NumericUpDown.Maximum = 2 * _image.ImageInfo.Width;
                    param1NumericUpDown.Value = _image.ImageInfo.Width;
                    param1NumericUpDown.Visible = true;

                    param2Label.Text = "Canvas Height:";
                    param2Label.Visible = true;
                    param2NumericUpDown.Minimum = _image.ImageInfo.Height;
                    param2NumericUpDown.Maximum = 2 * _image.ImageInfo.Height;
                    param2NumericUpDown.Value = _image.ImageInfo.Height;
                    param2NumericUpDown.Visible = true;

                    param3Label.Text = "Image X Pos:";
                    param3Label.Visible = true;
                    param3NumericUpDown.Minimum = 0;
                    param3NumericUpDown.Maximum = _image.ImageInfo.Width;
                    param3NumericUpDown.Value = 0;
                    param3NumericUpDown.Visible = true;

                    param4Label.Text = "Image Y Pos:";
                    param4Label.Visible = true;
                    param4NumericUpDown.Minimum = 0;
                    param4NumericUpDown.Maximum = _image.ImageInfo.Height;
                    param4NumericUpDown.Value = 0;
                    param4NumericUpDown.Visible = true;
                    break;
                
                case "Rotate":
                    param1Label.Text = "Angle:";
                    param1Label.Visible = true;
                    param1NumericUpDown.Minimum = 0;
                    param1NumericUpDown.Maximum = 360;
                    param1NumericUpDown.Value = 90;
                    param1NumericUpDown.Visible = true;
                    break;

                case "Despeckle":
                    param1Label.Text = "Level1:";
                    param1Label.Visible = true;
                    param1NumericUpDown.Minimum = 0;
                    param1NumericUpDown.Maximum = 100;
                    param1NumericUpDown.Value = 8;
                    param1NumericUpDown.Visible = true;

                    param2Label.Text = "Level2:";
                    param2Label.Visible = true;
                    param2NumericUpDown.Minimum = 0;
                    param2NumericUpDown.Maximum = 100;
                    param2NumericUpDown.Value = 25;
                    param2NumericUpDown.Visible = true;

                    param3Label.Text = "Radius:";
                    param3Label.Visible = true;
                    param3NumericUpDown.Minimum = 0;
                    param3NumericUpDown.Maximum = 100;
                    param3NumericUpDown.Value = 30;
                    param3NumericUpDown.Visible = true;

                    param4Label.Text = "Level3:";
                    param4Label.Visible = true;
                    param4NumericUpDown.Minimum = 0;
                    param4NumericUpDown.Maximum = 3000;
                    param4NumericUpDown.Value = 400;
                    param4NumericUpDown.Visible = true;
                    break;

                case "Deskew":
                    param1Label.Text = "Scan Interval X:";
                    param1Label.Visible = true;
                    param1NumericUpDown.Minimum = 1;
                    param1NumericUpDown.Maximum = 31;
                    param1NumericUpDown.Value = 5;
                    param1NumericUpDown.Visible = true;

                    param2Label.Text = "Scan Interval Y:";
                    param2Label.Visible = true;
                    param2NumericUpDown.Minimum = 1;
                    param2NumericUpDown.Maximum = 31;
                    param2NumericUpDown.Value = 5;
                    param2NumericUpDown.Visible = true;
                    break;

                case "Remove Border":
                    param1Label.Text = "Border Size:";
                    param1Label.Visible = true;
                    param1NumericUpDown.Minimum = 0;
                    param1NumericUpDown.Maximum = 100;
                    param1NumericUpDown.Value = 5;
                    param1NumericUpDown.Visible = true;
                    break;
            }
        }

        /// <summary>
        /// Run the processing command.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void runCommandButton_Click(object sender, EventArgs e)
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
