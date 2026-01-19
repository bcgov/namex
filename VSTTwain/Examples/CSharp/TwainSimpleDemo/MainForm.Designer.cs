using Vintasoft.Twain;
namespace TwainSimpleDemo
{
    partial class MainForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            this.scanImagesButton = new System.Windows.Forms.Button();
            this.twain2CheckBox = new System.Windows.Forms.CheckBox();
            this.showIndicatorsCheckBox = new System.Windows.Forms.CheckBox();
            this.showUiCheckBox = new System.Windows.Forms.CheckBox();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            this.SuspendLayout();
            // 
            // pictureBox1
            // 
            this.pictureBox1.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
                        | System.Windows.Forms.AnchorStyles.Left)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.pictureBox1.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.pictureBox1.Location = new System.Drawing.Point(7, 75);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(440, 481);
            this.pictureBox1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pictureBox1.TabIndex = 6;
            this.pictureBox1.TabStop = false;
            // 
            // scanImagesButton
            // 
            this.scanImagesButton.Location = new System.Drawing.Point(133, 12);
            this.scanImagesButton.Name = "scanImagesButton";
            this.scanImagesButton.Size = new System.Drawing.Size(314, 57);
            this.scanImagesButton.TabIndex = 7;
            this.scanImagesButton.Text = "Scan images";
            this.scanImagesButton.Click += new System.EventHandler(this.scanImagesButton_Click);
            // 
            // twain2CheckBox
            // 
            this.twain2CheckBox.AutoSize = true;
            this.twain2CheckBox.Checked = true;
            this.twain2CheckBox.CheckState = System.Windows.Forms.CheckState.Checked;
            this.twain2CheckBox.Location = new System.Drawing.Point(7, 12);
            this.twain2CheckBox.Name = "twain2CheckBox";
            this.twain2CheckBox.Size = new System.Drawing.Size(71, 17);
            this.twain2CheckBox.TabIndex = 8;
            this.twain2CheckBox.Text = "TWAIN 2";
            this.twain2CheckBox.UseVisualStyleBackColor = true;
            // 
            // showIndicatorsCheckBox
            // 
            this.showIndicatorsCheckBox.AutoSize = true;
            this.showIndicatorsCheckBox.Checked = true;
            this.showIndicatorsCheckBox.CheckState = System.Windows.Forms.CheckState.Checked;
            this.showIndicatorsCheckBox.Location = new System.Drawing.Point(7, 52);
            this.showIndicatorsCheckBox.Name = "showIndicatorsCheckBox";
            this.showIndicatorsCheckBox.Size = new System.Drawing.Size(102, 17);
            this.showIndicatorsCheckBox.TabIndex = 9;
            this.showIndicatorsCheckBox.Text = "Show Indicators";
            this.showIndicatorsCheckBox.UseVisualStyleBackColor = true;
            // 
            // showUiCheckBox
            // 
            this.showUiCheckBox.AutoSize = true;
            this.showUiCheckBox.Checked = true;
            this.showUiCheckBox.CheckState = System.Windows.Forms.CheckState.Checked;
            this.showUiCheckBox.Location = new System.Drawing.Point(7, 31);
            this.showUiCheckBox.Name = "showUiCheckBox";
            this.showUiCheckBox.Size = new System.Drawing.Size(67, 17);
            this.showUiCheckBox.TabIndex = 10;
            this.showUiCheckBox.Text = "Show UI";
            this.showUiCheckBox.UseVisualStyleBackColor = true;
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(456, 566);
            this.Controls.Add(this.showUiCheckBox);
            this.Controls.Add(this.showIndicatorsCheckBox);
            this.Controls.Add(this.twain2CheckBox);
            this.Controls.Add(this.scanImagesButton);
            this.Controls.Add(this.pictureBox1);
            this.Name = "MainForm";
            this.Text = "VintaSoft TWAIN Simple Demo";
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.PictureBox pictureBox1;
        private System.Windows.Forms.Button scanImagesButton;
        private System.Windows.Forms.CheckBox twain2CheckBox;
        private System.Windows.Forms.CheckBox showIndicatorsCheckBox;
        private System.Windows.Forms.CheckBox showUiCheckBox;
    }
}

