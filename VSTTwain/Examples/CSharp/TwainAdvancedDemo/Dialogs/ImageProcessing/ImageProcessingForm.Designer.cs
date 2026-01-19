namespace TwainAdvancedDemo
{
    partial class ImageProcessingForm
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
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.processingCommandProgressBar = new System.Windows.Forms.ProgressBar();
            this.runCommandButton = new System.Windows.Forms.Button();
            this.param4NumericUpDown = new System.Windows.Forms.NumericUpDown();
            this.param4Label = new System.Windows.Forms.Label();
            this.param3NumericUpDown = new System.Windows.Forms.NumericUpDown();
            this.param3Label = new System.Windows.Forms.Label();
            this.param2NumericUpDown = new System.Windows.Forms.NumericUpDown();
            this.param2Label = new System.Windows.Forms.Label();
            this.param1NumericUpDown = new System.Windows.Forms.NumericUpDown();
            this.param1Label = new System.Windows.Forms.Label();
            this.commandsComboBox = new System.Windows.Forms.ComboBox();
            this.pictureBoxPanel = new System.Windows.Forms.Panel();
            this.stretchImageCheckBox = new System.Windows.Forms.CheckBox();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            this.groupBox1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.param4NumericUpDown)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.param3NumericUpDown)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.param2NumericUpDown)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.param1NumericUpDown)).BeginInit();
            this.pictureBoxPanel.SuspendLayout();
            this.SuspendLayout();
            // 
            // pictureBox1
            // 
            this.pictureBox1.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.pictureBox1.Location = new System.Drawing.Point(0, 0);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(501, 511);
            this.pictureBox1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pictureBox1.TabIndex = 0;
            this.pictureBox1.TabStop = false;
            // 
            // groupBox1
            // 
            this.groupBox1.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.groupBox1.Controls.Add(this.processingCommandProgressBar);
            this.groupBox1.Controls.Add(this.runCommandButton);
            this.groupBox1.Controls.Add(this.param4NumericUpDown);
            this.groupBox1.Controls.Add(this.param4Label);
            this.groupBox1.Controls.Add(this.param3NumericUpDown);
            this.groupBox1.Controls.Add(this.param3Label);
            this.groupBox1.Controls.Add(this.param2NumericUpDown);
            this.groupBox1.Controls.Add(this.param2Label);
            this.groupBox1.Controls.Add(this.param1NumericUpDown);
            this.groupBox1.Controls.Add(this.param1Label);
            this.groupBox1.Controls.Add(this.commandsComboBox);
            this.groupBox1.Location = new System.Drawing.Point(521, 32);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(200, 490);
            this.groupBox1.TabIndex = 1;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "Processing Command";
            // 
            // processingCommandProgressBar
            // 
            this.processingCommandProgressBar.Location = new System.Drawing.Point(11, 223);
            this.processingCommandProgressBar.Name = "processingCommandProgressBar";
            this.processingCommandProgressBar.Size = new System.Drawing.Size(175, 23);
            this.processingCommandProgressBar.TabIndex = 12;
            // 
            // runCommandButton
            // 
            this.runCommandButton.Location = new System.Drawing.Point(11, 182);
            this.runCommandButton.Name = "runCommandButton";
            this.runCommandButton.Size = new System.Drawing.Size(175, 35);
            this.runCommandButton.TabIndex = 11;
            this.runCommandButton.Text = "Run command";
            this.runCommandButton.UseVisualStyleBackColor = true;
            this.runCommandButton.Click += new System.EventHandler(this.runCommandButton_Click);
            // 
            // param4NumericUpDown
            // 
            this.param4NumericUpDown.Location = new System.Drawing.Point(125, 132);
            this.param4NumericUpDown.Name = "param4NumericUpDown";
            this.param4NumericUpDown.Size = new System.Drawing.Size(61, 20);
            this.param4NumericUpDown.TabIndex = 10;
            this.param4NumericUpDown.Visible = false;
            // 
            // param4Label
            // 
            this.param4Label.AutoSize = true;
            this.param4Label.Location = new System.Drawing.Point(8, 134);
            this.param4Label.Name = "param4Label";
            this.param4Label.Size = new System.Drawing.Size(46, 13);
            this.param4Label.TabIndex = 9;
            this.param4Label.Text = "Param4:";
            this.param4Label.Visible = false;
            // 
            // param3NumericUpDown
            // 
            this.param3NumericUpDown.Location = new System.Drawing.Point(125, 106);
            this.param3NumericUpDown.Name = "param3NumericUpDown";
            this.param3NumericUpDown.Size = new System.Drawing.Size(61, 20);
            this.param3NumericUpDown.TabIndex = 8;
            this.param3NumericUpDown.Visible = false;
            // 
            // param3Label
            // 
            this.param3Label.AutoSize = true;
            this.param3Label.Location = new System.Drawing.Point(8, 108);
            this.param3Label.Name = "param3Label";
            this.param3Label.Size = new System.Drawing.Size(46, 13);
            this.param3Label.TabIndex = 7;
            this.param3Label.Text = "Param3:";
            this.param3Label.Visible = false;
            // 
            // param2NumericUpDown
            // 
            this.param2NumericUpDown.Location = new System.Drawing.Point(125, 80);
            this.param2NumericUpDown.Name = "param2NumericUpDown";
            this.param2NumericUpDown.Size = new System.Drawing.Size(61, 20);
            this.param2NumericUpDown.TabIndex = 6;
            this.param2NumericUpDown.Visible = false;
            // 
            // param2Label
            // 
            this.param2Label.AutoSize = true;
            this.param2Label.Location = new System.Drawing.Point(8, 82);
            this.param2Label.Name = "param2Label";
            this.param2Label.Size = new System.Drawing.Size(46, 13);
            this.param2Label.TabIndex = 5;
            this.param2Label.Text = "Param2:";
            this.param2Label.Visible = false;
            // 
            // param1NumericUpDown
            // 
            this.param1NumericUpDown.Location = new System.Drawing.Point(125, 54);
            this.param1NumericUpDown.Name = "param1NumericUpDown";
            this.param1NumericUpDown.Size = new System.Drawing.Size(61, 20);
            this.param1NumericUpDown.TabIndex = 4;
            this.param1NumericUpDown.Visible = false;
            // 
            // param1Label
            // 
            this.param1Label.AutoSize = true;
            this.param1Label.Location = new System.Drawing.Point(8, 56);
            this.param1Label.Name = "param1Label";
            this.param1Label.Size = new System.Drawing.Size(46, 13);
            this.param1Label.TabIndex = 2;
            this.param1Label.Text = "Param1:";
            this.param1Label.Visible = false;
            // 
            // commandsComboBox
            // 
            this.commandsComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.commandsComboBox.FormattingEnabled = true;
            this.commandsComboBox.Items.AddRange(new object[] {
            "Is Image Blank?",
            "Invert",
            "Change Brightness",
            "Change Contrast",
            "Crop",
            "Resize Canvas",
            "Rotate",
            "Despeckle",
            "Deskew",
            "Remove Border"});
            this.commandsComboBox.Location = new System.Drawing.Point(11, 23);
            this.commandsComboBox.Name = "commandsComboBox";
            this.commandsComboBox.Size = new System.Drawing.Size(175, 21);
            this.commandsComboBox.TabIndex = 1;
            this.commandsComboBox.SelectedIndexChanged += new System.EventHandler(this.commandsComboBox_SelectedIndexChanged);
            // 
            // pictureBoxPanel
            // 
            this.pictureBoxPanel.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
                        | System.Windows.Forms.AnchorStyles.Left)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.pictureBoxPanel.AutoScroll = true;
            this.pictureBoxPanel.Controls.Add(this.pictureBox1);
            this.pictureBoxPanel.Location = new System.Drawing.Point(12, 9);
            this.pictureBoxPanel.Name = "pictureBoxPanel";
            this.pictureBoxPanel.Size = new System.Drawing.Size(503, 513);
            this.pictureBoxPanel.TabIndex = 2;
            // 
            // stretchImageCheckBox
            // 
            this.stretchImageCheckBox.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.stretchImageCheckBox.AutoSize = true;
            this.stretchImageCheckBox.Checked = true;
            this.stretchImageCheckBox.CheckState = System.Windows.Forms.CheckState.Checked;
            this.stretchImageCheckBox.Location = new System.Drawing.Point(521, 9);
            this.stretchImageCheckBox.Name = "stretchImageCheckBox";
            this.stretchImageCheckBox.Size = new System.Drawing.Size(92, 17);
            this.stretchImageCheckBox.TabIndex = 3;
            this.stretchImageCheckBox.Text = "Stretch Image";
            this.stretchImageCheckBox.UseVisualStyleBackColor = true;
            this.stretchImageCheckBox.CheckedChanged += new System.EventHandler(this.stretchImageCheckBox_CheckedChanged);
            // 
            // ImageProcessingForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(733, 534);
            this.Controls.Add(this.stretchImageCheckBox);
            this.Controls.Add(this.pictureBoxPanel);
            this.Controls.Add(this.groupBox1);
            this.Name = "ImageProcessingForm";
            this.Text = "Image Processing";
            this.Resize += new System.EventHandler(this.ImageProcessingForm_Resize);
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.param4NumericUpDown)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.param3NumericUpDown)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.param2NumericUpDown)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.param1NumericUpDown)).EndInit();
            this.pictureBoxPanel.ResumeLayout(false);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.PictureBox pictureBox1;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.Panel pictureBoxPanel;
        private System.Windows.Forms.ComboBox commandsComboBox;
        private System.Windows.Forms.NumericUpDown param4NumericUpDown;
        private System.Windows.Forms.Label param4Label;
        private System.Windows.Forms.NumericUpDown param3NumericUpDown;
        private System.Windows.Forms.Label param3Label;
        private System.Windows.Forms.NumericUpDown param2NumericUpDown;
        private System.Windows.Forms.Label param2Label;
        private System.Windows.Forms.NumericUpDown param1NumericUpDown;
        private System.Windows.Forms.Label param1Label;
        private System.Windows.Forms.Button runCommandButton;
        private System.Windows.Forms.CheckBox stretchImageCheckBox;
        private System.Windows.Forms.ProgressBar processingCommandProgressBar;
    }
}