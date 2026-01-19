namespace TwainAdvancedDemo
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
            this.stretchImageCheckBox = new System.Windows.Forms.CheckBox();
            this.saveFileDialog1 = new System.Windows.Forms.SaveFileDialog();
            this.pictureBoxPanel = new System.Windows.Forms.Panel();
            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            this.devicesLabel = new System.Windows.Forms.Label();
            this.selectDefaultDeviceButton = new System.Windows.Forms.Button();
            this.acquireImageButton = new System.Windows.Forms.Button();
            this.openDeviceManagerButton = new System.Windows.Forms.Button();
            this.showIndicatorsCheckBox = new System.Windows.Forms.CheckBox();
            this.imagesToAcquireNumericUpDown = new System.Windows.Forms.NumericUpDown();
            this.adfGroupBox = new System.Windows.Forms.GroupBox();
            this.label1 = new System.Windows.Forms.Label();
            this.imagesToAcquireRadioButton = new System.Windows.Forms.RadioButton();
            this.acquireAllImagesRadioButton = new System.Windows.Forms.RadioButton();
            this.useAdfCheckBox = new System.Windows.Forms.CheckBox();
            this.useDuplexCheckBox = new System.Windows.Forms.CheckBox();
            this.userInterfaceGroupBox = new System.Windows.Forms.GroupBox();
            this.showUICheckBox = new System.Windows.Forms.CheckBox();
            this.modalUICheckBox = new System.Windows.Forms.CheckBox();
            this.disableAfterScanCheckBox = new System.Windows.Forms.CheckBox();
            this.devicesComboBox = new System.Windows.Forms.ComboBox();
            this.twain2CompatibleCheckBox = new System.Windows.Forms.CheckBox();
            this.deleteImageButton = new System.Windows.Forms.Button();
            this.panel1 = new System.Windows.Forms.Panel();
            this.uploadImageButton = new System.Windows.Forms.Button();
            this.saveImageButton = new System.Windows.Forms.Button();
            this.getDeviceInfoButton = new System.Windows.Forms.Button();
            this.imageInfoLabel = new System.Windows.Forms.Label();
            this.nextImageButton = new System.Windows.Forms.Button();
            this.previousImageButton = new System.Windows.Forms.Button();
            this.processImageButton = new System.Windows.Forms.Button();
            this.imageAcquisitionProgressBar = new System.Windows.Forms.ProgressBar();
            this.imageGroupBox = new System.Windows.Forms.GroupBox();
            this.transferModeLabel = new System.Windows.Forms.Label();
            this.transferModeComboBox = new System.Windows.Forms.ComboBox();
            this.resolutionLabel = new System.Windows.Forms.Label();
            this.resolutionComboBox = new System.Windows.Forms.ComboBox();
            this.pixelTypeLabel = new System.Windows.Forms.Label();
            this.pixelTypeComboBox = new System.Windows.Forms.ComboBox();
            this.clearImagesButton = new System.Windows.Forms.Button();
            this.pictureBoxPanel.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.imagesToAcquireNumericUpDown)).BeginInit();
            this.adfGroupBox.SuspendLayout();
            this.userInterfaceGroupBox.SuspendLayout();
            this.imageGroupBox.SuspendLayout();
            this.SuspendLayout();
            // 
            // stretchImageCheckBox
            // 
            this.stretchImageCheckBox.Checked = true;
            this.stretchImageCheckBox.CheckState = System.Windows.Forms.CheckState.Checked;
            this.stretchImageCheckBox.Location = new System.Drawing.Point(588, 167);
            this.stretchImageCheckBox.Name = "stretchImageCheckBox";
            this.stretchImageCheckBox.Size = new System.Drawing.Size(93, 17);
            this.stretchImageCheckBox.TabIndex = 26;
            this.stretchImageCheckBox.Text = "Stretch image";
            this.stretchImageCheckBox.UseVisualStyleBackColor = true;
            this.stretchImageCheckBox.CheckedChanged += new System.EventHandler(this.stretchImageCheckBox_CheckedChanged);
            // 
            // saveFileDialog1
            // 
            this.saveFileDialog1.FileName = "doc1";
            this.saveFileDialog1.Filter = "BMP image|*.bmp|GIF image|*.gif|JPEG image|*.jpg|PNG image|*.png|TIFF image|*.tif" +
                "|PDF document|*.pdf";
            this.saveFileDialog1.FilterIndex = 3;
            // 
            // pictureBoxPanel
            // 
            this.pictureBoxPanel.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
                        | System.Windows.Forms.AnchorStyles.Left)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.pictureBoxPanel.AutoScroll = true;
            this.pictureBoxPanel.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.pictureBoxPanel.Controls.Add(this.pictureBox1);
            this.pictureBoxPanel.Location = new System.Drawing.Point(9, 188);
            this.pictureBoxPanel.Name = "pictureBoxPanel";
            this.pictureBoxPanel.Size = new System.Drawing.Size(671, 382);
            this.pictureBoxPanel.TabIndex = 81;
            // 
            // pictureBox1
            // 
            this.pictureBox1.Location = new System.Drawing.Point(-1, -1);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(669, 380);
            this.pictureBox1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pictureBox1.TabIndex = 0;
            this.pictureBox1.TabStop = false;
            // 
            // devicesLabel
            // 
            this.devicesLabel.Location = new System.Drawing.Point(169, 13);
            this.devicesLabel.Name = "devicesLabel";
            this.devicesLabel.Size = new System.Drawing.Size(56, 16);
            this.devicesLabel.TabIndex = 76;
            this.devicesLabel.Text = "Devices:";
            // 
            // selectDefaultDeviceButton
            // 
            this.selectDefaultDeviceButton.Location = new System.Drawing.Point(9, 67);
            this.selectDefaultDeviceButton.Name = "selectDefaultDeviceButton";
            this.selectDefaultDeviceButton.Size = new System.Drawing.Size(144, 26);
            this.selectDefaultDeviceButton.TabIndex = 3;
            this.selectDefaultDeviceButton.Text = "Select default device";
            this.selectDefaultDeviceButton.Click += new System.EventHandler(this.selectDefaultDeviceButton_Click);
            // 
            // acquireImageButton
            // 
            this.acquireImageButton.Location = new System.Drawing.Point(9, 99);
            this.acquireImageButton.Name = "acquireImageButton";
            this.acquireImageButton.Size = new System.Drawing.Size(144, 26);
            this.acquireImageButton.TabIndex = 4;
            this.acquireImageButton.Text = "Acquire image(s)";
            this.acquireImageButton.Click += new System.EventHandler(this.acquireImageButton_Click);
            // 
            // openDeviceManagerButton
            // 
            this.openDeviceManagerButton.Location = new System.Drawing.Point(9, 34);
            this.openDeviceManagerButton.Name = "openDeviceManagerButton";
            this.openDeviceManagerButton.Size = new System.Drawing.Size(144, 26);
            this.openDeviceManagerButton.TabIndex = 2;
            this.openDeviceManagerButton.Text = "Open device manager";
            this.openDeviceManagerButton.Click += new System.EventHandler(this.openDeviceManagerButton_Click);
            // 
            // showIndicatorsCheckBox
            // 
            this.showIndicatorsCheckBox.Checked = true;
            this.showIndicatorsCheckBox.CheckState = System.Windows.Forms.CheckState.Checked;
            this.showIndicatorsCheckBox.Location = new System.Drawing.Point(8, 51);
            this.showIndicatorsCheckBox.Name = "showIndicatorsCheckBox";
            this.showIndicatorsCheckBox.Size = new System.Drawing.Size(104, 16);
            this.showIndicatorsCheckBox.TabIndex = 9;
            this.showIndicatorsCheckBox.Text = "Show Indicators";
            // 
            // imagesToAcquireNumericUpDown
            // 
            this.imagesToAcquireNumericUpDown.Location = new System.Drawing.Point(71, 63);
            this.imagesToAcquireNumericUpDown.Maximum = new decimal(new int[] {
            1000,
            0,
            0,
            0});
            this.imagesToAcquireNumericUpDown.Minimum = new decimal(new int[] {
            1,
            0,
            0,
            0});
            this.imagesToAcquireNumericUpDown.Name = "imagesToAcquireNumericUpDown";
            this.imagesToAcquireNumericUpDown.Size = new System.Drawing.Size(64, 20);
            this.imagesToAcquireNumericUpDown.TabIndex = 18;
            this.imagesToAcquireNumericUpDown.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            this.imagesToAcquireNumericUpDown.Value = new decimal(new int[] {
            1,
            0,
            0,
            0});
            // 
            // adfGroupBox
            // 
            this.adfGroupBox.Controls.Add(this.label1);
            this.adfGroupBox.Controls.Add(this.imagesToAcquireRadioButton);
            this.adfGroupBox.Controls.Add(this.acquireAllImagesRadioButton);
            this.adfGroupBox.Controls.Add(this.imagesToAcquireNumericUpDown);
            this.adfGroupBox.Controls.Add(this.useAdfCheckBox);
            this.adfGroupBox.Controls.Add(this.useDuplexCheckBox);
            this.adfGroupBox.ForeColor = System.Drawing.SystemColors.ControlText;
            this.adfGroupBox.Location = new System.Drawing.Point(500, 37);
            this.adfGroupBox.Name = "adfGroupBox";
            this.adfGroupBox.Size = new System.Drawing.Size(182, 88);
            this.adfGroupBox.TabIndex = 14;
            this.adfGroupBox.TabStop = false;
            this.adfGroupBox.Text = "Automatic Document Feeder";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(136, 66);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(40, 13);
            this.label1.TabIndex = 0;
            this.label1.Text = "images";
            // 
            // imagesToAcquireRadioButton
            // 
            this.imagesToAcquireRadioButton.AutoSize = true;
            this.imagesToAcquireRadioButton.Location = new System.Drawing.Point(10, 64);
            this.imagesToAcquireRadioButton.Name = "imagesToAcquireRadioButton";
            this.imagesToAcquireRadioButton.Size = new System.Drawing.Size(61, 17);
            this.imagesToAcquireRadioButton.TabIndex = 17;
            this.imagesToAcquireRadioButton.TabStop = true;
            this.imagesToAcquireRadioButton.Text = "Acquire";
            this.imagesToAcquireRadioButton.UseVisualStyleBackColor = true;
            // 
            // acquireAllImagesRadioButton
            // 
            this.acquireAllImagesRadioButton.AutoSize = true;
            this.acquireAllImagesRadioButton.Checked = true;
            this.acquireAllImagesRadioButton.Location = new System.Drawing.Point(10, 43);
            this.acquireAllImagesRadioButton.Name = "acquireAllImagesRadioButton";
            this.acquireAllImagesRadioButton.Size = new System.Drawing.Size(112, 17);
            this.acquireAllImagesRadioButton.TabIndex = 16;
            this.acquireAllImagesRadioButton.TabStop = true;
            this.acquireAllImagesRadioButton.Text = "Acquire All Images";
            this.acquireAllImagesRadioButton.UseVisualStyleBackColor = true;
            // 
            // useAdfCheckBox
            // 
            this.useAdfCheckBox.Checked = true;
            this.useAdfCheckBox.CheckState = System.Windows.Forms.CheckState.Checked;
            this.useAdfCheckBox.Location = new System.Drawing.Point(10, 17);
            this.useAdfCheckBox.Name = "useAdfCheckBox";
            this.useAdfCheckBox.Size = new System.Drawing.Size(72, 16);
            this.useAdfCheckBox.TabIndex = 14;
            this.useAdfCheckBox.Text = "Use ADF";
            this.useAdfCheckBox.CheckedChanged += new System.EventHandler(this.useAdfCheckBox_CheckedChanged);
            // 
            // useDuplexCheckBox
            // 
            this.useDuplexCheckBox.Location = new System.Drawing.Point(84, 17);
            this.useDuplexCheckBox.Name = "useDuplexCheckBox";
            this.useDuplexCheckBox.Size = new System.Drawing.Size(82, 16);
            this.useDuplexCheckBox.TabIndex = 15;
            this.useDuplexCheckBox.Text = "Use Duplex";
            // 
            // userInterfaceGroupBox
            // 
            this.userInterfaceGroupBox.Controls.Add(this.showUICheckBox);
            this.userInterfaceGroupBox.Controls.Add(this.modalUICheckBox);
            this.userInterfaceGroupBox.Controls.Add(this.showIndicatorsCheckBox);
            this.userInterfaceGroupBox.Controls.Add(this.disableAfterScanCheckBox);
            this.userInterfaceGroupBox.Location = new System.Drawing.Point(162, 38);
            this.userInterfaceGroupBox.Name = "userInterfaceGroupBox";
            this.userInterfaceGroupBox.Size = new System.Drawing.Size(139, 88);
            this.userInterfaceGroupBox.TabIndex = 7;
            this.userInterfaceGroupBox.TabStop = false;
            this.userInterfaceGroupBox.Text = "User Interface";
            // 
            // showUICheckBox
            // 
            this.showUICheckBox.Checked = true;
            this.showUICheckBox.CheckState = System.Windows.Forms.CheckState.Checked;
            this.showUICheckBox.ForeColor = System.Drawing.SystemColors.ControlText;
            this.showUICheckBox.Location = new System.Drawing.Point(8, 17);
            this.showUICheckBox.Name = "showUICheckBox";
            this.showUICheckBox.Size = new System.Drawing.Size(72, 16);
            this.showUICheckBox.TabIndex = 7;
            this.showUICheckBox.Text = "Show UI";
            this.showUICheckBox.CheckedChanged += new System.EventHandler(this.showUICheckBox_CheckedChanged);
            // 
            // modalUICheckBox
            // 
            this.modalUICheckBox.Location = new System.Drawing.Point(8, 34);
            this.modalUICheckBox.Name = "modalUICheckBox";
            this.modalUICheckBox.Size = new System.Drawing.Size(72, 16);
            this.modalUICheckBox.TabIndex = 8;
            this.modalUICheckBox.Text = "Modal UI";
            // 
            // disableAfterScanCheckBox
            // 
            this.disableAfterScanCheckBox.Location = new System.Drawing.Point(8, 68);
            this.disableAfterScanCheckBox.Name = "disableAfterScanCheckBox";
            this.disableAfterScanCheckBox.Size = new System.Drawing.Size(128, 17);
            this.disableAfterScanCheckBox.TabIndex = 10;
            this.disableAfterScanCheckBox.Text = "Disable after Scan";
            // 
            // devicesComboBox
            // 
            this.devicesComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.devicesComboBox.Location = new System.Drawing.Point(217, 11);
            this.devicesComboBox.Name = "devicesComboBox";
            this.devicesComboBox.Size = new System.Drawing.Size(339, 21);
            this.devicesComboBox.TabIndex = 5;
            // 
            // twain2CompatibleCheckBox
            // 
            this.twain2CompatibleCheckBox.Checked = true;
            this.twain2CompatibleCheckBox.CheckState = System.Windows.Forms.CheckState.Checked;
            this.twain2CompatibleCheckBox.Location = new System.Drawing.Point(17, 12);
            this.twain2CompatibleCheckBox.Name = "twain2CompatibleCheckBox";
            this.twain2CompatibleCheckBox.Size = new System.Drawing.Size(146, 17);
            this.twain2CompatibleCheckBox.TabIndex = 1;
            this.twain2CompatibleCheckBox.Text = "TWAIN 2 compatible";
            this.twain2CompatibleCheckBox.UseVisualStyleBackColor = true;
            // 
            // deleteImageButton
            // 
            this.deleteImageButton.Location = new System.Drawing.Point(500, 139);
            this.deleteImageButton.Name = "deleteImageButton";
            this.deleteImageButton.Size = new System.Drawing.Size(90, 23);
            this.deleteImageButton.TabIndex = 24;
            this.deleteImageButton.Text = "Delete image";
            this.deleteImageButton.Click += new System.EventHandler(this.deleteImageButton_Click);
            // 
            // panel1
            // 
            this.panel1.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.panel1.Location = new System.Drawing.Point(9, 131);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(671, 1);
            this.panel1.TabIndex = 78;
            // 
            // uploadImageButton
            // 
            this.uploadImageButton.Location = new System.Drawing.Point(398, 139);
            this.uploadImageButton.Name = "uploadImageButton";
            this.uploadImageButton.Size = new System.Drawing.Size(90, 23);
            this.uploadImageButton.TabIndex = 23;
            this.uploadImageButton.Text = "Upload image";
            this.uploadImageButton.Click += new System.EventHandler(this.uploadImageButton_Click);
            // 
            // saveImageButton
            // 
            this.saveImageButton.Location = new System.Drawing.Point(305, 139);
            this.saveImageButton.Name = "saveImageButton";
            this.saveImageButton.Size = new System.Drawing.Size(90, 23);
            this.saveImageButton.TabIndex = 22;
            this.saveImageButton.Text = "Save image";
            this.saveImageButton.Click += new System.EventHandler(this.saveImageButton_Click);
            // 
            // getDeviceInfoButton
            // 
            this.getDeviceInfoButton.Location = new System.Drawing.Point(562, 9);
            this.getDeviceInfoButton.Name = "getDeviceInfoButton";
            this.getDeviceInfoButton.Size = new System.Drawing.Size(120, 23);
            this.getDeviceInfoButton.TabIndex = 6;
            this.getDeviceInfoButton.Text = "Get source info";
            this.getDeviceInfoButton.Click += new System.EventHandler(this.getDeviceInfoButton_Click);
            // 
            // imageInfoLabel
            // 
            this.imageInfoLabel.Location = new System.Drawing.Point(162, 168);
            this.imageInfoLabel.Name = "imageInfoLabel";
            this.imageInfoLabel.Size = new System.Drawing.Size(367, 16);
            this.imageInfoLabel.TabIndex = 77;
            this.imageInfoLabel.Text = "No images";
            this.imageInfoLabel.TextAlign = System.Drawing.ContentAlignment.TopCenter;
            // 
            // nextImageButton
            // 
            this.nextImageButton.Location = new System.Drawing.Point(102, 139);
            this.nextImageButton.Name = "nextImageButton";
            this.nextImageButton.Size = new System.Drawing.Size(90, 23);
            this.nextImageButton.TabIndex = 20;
            this.nextImageButton.Text = "Next image";
            this.nextImageButton.Click += new System.EventHandler(this.nextImageButton_Click);
            // 
            // previousImageButton
            // 
            this.previousImageButton.Location = new System.Drawing.Point(9, 139);
            this.previousImageButton.Name = "previousImageButton";
            this.previousImageButton.Size = new System.Drawing.Size(90, 23);
            this.previousImageButton.TabIndex = 19;
            this.previousImageButton.Text = "Previous image";
            this.previousImageButton.Click += new System.EventHandler(this.previousImageButton_Click);
            // 
            // processImageButton
            // 
            this.processImageButton.Location = new System.Drawing.Point(205, 139);
            this.processImageButton.Name = "processImageButton";
            this.processImageButton.Size = new System.Drawing.Size(90, 23);
            this.processImageButton.TabIndex = 21;
            this.processImageButton.Text = "Process image";
            this.processImageButton.Click += new System.EventHandler(this.rotateImageButton_Click);
            // 
            // imageAcquisitionProgressBar
            // 
            this.imageAcquisitionProgressBar.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.imageAcquisitionProgressBar.Location = new System.Drawing.Point(9, 576);
            this.imageAcquisitionProgressBar.Name = "imageAcquisitionProgressBar";
            this.imageAcquisitionProgressBar.Size = new System.Drawing.Size(672, 23);
            this.imageAcquisitionProgressBar.TabIndex = 87;
            // 
            // imageGroupBox
            // 
            this.imageGroupBox.Controls.Add(this.transferModeLabel);
            this.imageGroupBox.Controls.Add(this.transferModeComboBox);
            this.imageGroupBox.Controls.Add(this.resolutionLabel);
            this.imageGroupBox.Controls.Add(this.resolutionComboBox);
            this.imageGroupBox.Controls.Add(this.pixelTypeLabel);
            this.imageGroupBox.Controls.Add(this.pixelTypeComboBox);
            this.imageGroupBox.Location = new System.Drawing.Point(307, 37);
            this.imageGroupBox.Name = "imageGroupBox";
            this.imageGroupBox.Size = new System.Drawing.Size(187, 88);
            this.imageGroupBox.TabIndex = 11;
            this.imageGroupBox.TabStop = false;
            this.imageGroupBox.Text = "Image:";
            // 
            // transferModeLabel
            // 
            this.transferModeLabel.AutoSize = true;
            this.transferModeLabel.Location = new System.Drawing.Point(6, 18);
            this.transferModeLabel.Name = "transferModeLabel";
            this.transferModeLabel.Size = new System.Drawing.Size(76, 13);
            this.transferModeLabel.TabIndex = 5;
            this.transferModeLabel.Text = "Transfer Mode";
            // 
            // transferModeComboBox
            // 
            this.transferModeComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.transferModeComboBox.FormattingEnabled = true;
            this.transferModeComboBox.Items.AddRange(new object[] {
            "Native",
            "Memory"});
            this.transferModeComboBox.Location = new System.Drawing.Point(88, 13);
            this.transferModeComboBox.Name = "transferModeComboBox";
            this.transferModeComboBox.Size = new System.Drawing.Size(89, 21);
            this.transferModeComboBox.TabIndex = 11;
            this.transferModeComboBox.SelectedIndexChanged += new System.EventHandler(this.transferModeComboBox_SelectedIndexChanged);
            // 
            // resolutionLabel
            // 
            this.resolutionLabel.AutoSize = true;
            this.resolutionLabel.Location = new System.Drawing.Point(6, 66);
            this.resolutionLabel.Name = "resolutionLabel";
            this.resolutionLabel.Size = new System.Drawing.Size(57, 13);
            this.resolutionLabel.TabIndex = 3;
            this.resolutionLabel.Text = "Resolution";
            // 
            // resolutionComboBox
            // 
            this.resolutionComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.resolutionComboBox.FormattingEnabled = true;
            this.resolutionComboBox.Items.AddRange(new object[] {
            "100",
            "150",
            "200",
            "300",
            "600"});
            this.resolutionComboBox.Location = new System.Drawing.Point(88, 63);
            this.resolutionComboBox.Name = "resolutionComboBox";
            this.resolutionComboBox.Size = new System.Drawing.Size(89, 21);
            this.resolutionComboBox.TabIndex = 13;
            // 
            // pixelTypeLabel
            // 
            this.pixelTypeLabel.AutoSize = true;
            this.pixelTypeLabel.Location = new System.Drawing.Point(6, 41);
            this.pixelTypeLabel.Name = "pixelTypeLabel";
            this.pixelTypeLabel.Size = new System.Drawing.Size(56, 13);
            this.pixelTypeLabel.TabIndex = 1;
            this.pixelTypeLabel.Text = "Pixel Type";
            // 
            // pixelTypeComboBox
            // 
            this.pixelTypeComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.pixelTypeComboBox.FormattingEnabled = true;
            this.pixelTypeComboBox.Items.AddRange(new object[] {
            "BW",
            "Gray",
            "Color"});
            this.pixelTypeComboBox.Location = new System.Drawing.Point(88, 38);
            this.pixelTypeComboBox.Name = "pixelTypeComboBox";
            this.pixelTypeComboBox.Size = new System.Drawing.Size(89, 21);
            this.pixelTypeComboBox.TabIndex = 12;
            // 
            // clearImagesButton
            // 
            this.clearImagesButton.Location = new System.Drawing.Point(592, 139);
            this.clearImagesButton.Name = "clearImagesButton";
            this.clearImagesButton.Size = new System.Drawing.Size(90, 23);
            this.clearImagesButton.TabIndex = 25;
            this.clearImagesButton.Text = "Clear images";
            this.clearImagesButton.Click += new System.EventHandler(this.clearImagesButton_Click);
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(691, 608);
            this.Controls.Add(this.clearImagesButton);
            this.Controls.Add(this.imageGroupBox);
            this.Controls.Add(this.processImageButton);
            this.Controls.Add(this.imageAcquisitionProgressBar);
            this.Controls.Add(this.stretchImageCheckBox);
            this.Controls.Add(this.pictureBoxPanel);
            this.Controls.Add(this.selectDefaultDeviceButton);
            this.Controls.Add(this.acquireImageButton);
            this.Controls.Add(this.openDeviceManagerButton);
            this.Controls.Add(this.adfGroupBox);
            this.Controls.Add(this.userInterfaceGroupBox);
            this.Controls.Add(this.devicesComboBox);
            this.Controls.Add(this.twain2CompatibleCheckBox);
            this.Controls.Add(this.deleteImageButton);
            this.Controls.Add(this.panel1);
            this.Controls.Add(this.uploadImageButton);
            this.Controls.Add(this.saveImageButton);
            this.Controls.Add(this.getDeviceInfoButton);
            this.Controls.Add(this.imageInfoLabel);
            this.Controls.Add(this.nextImageButton);
            this.Controls.Add(this.previousImageButton);
            this.Controls.Add(this.devicesLabel);
            this.Name = "MainForm";
            this.Text = "VintaSoft TWAIN Advanced Demo";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.MainForm_FormClosing);
            this.Resize += new System.EventHandler(this.MainForm_Resize);
            this.pictureBoxPanel.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.imagesToAcquireNumericUpDown)).EndInit();
            this.adfGroupBox.ResumeLayout(false);
            this.adfGroupBox.PerformLayout();
            this.userInterfaceGroupBox.ResumeLayout(false);
            this.imageGroupBox.ResumeLayout(false);
            this.imageGroupBox.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.CheckBox stretchImageCheckBox;
        private System.Windows.Forms.SaveFileDialog saveFileDialog1;
        private System.Windows.Forms.Panel pictureBoxPanel;
        private System.Windows.Forms.PictureBox pictureBox1;
        private System.Windows.Forms.Label devicesLabel;
        private System.Windows.Forms.Button selectDefaultDeviceButton;
        private System.Windows.Forms.Button acquireImageButton;
        private System.Windows.Forms.Button openDeviceManagerButton;
        private System.Windows.Forms.CheckBox showIndicatorsCheckBox;
        private System.Windows.Forms.NumericUpDown imagesToAcquireNumericUpDown;
        private System.Windows.Forms.GroupBox adfGroupBox;
        private System.Windows.Forms.CheckBox useAdfCheckBox;
        private System.Windows.Forms.CheckBox useDuplexCheckBox;
        private System.Windows.Forms.GroupBox userInterfaceGroupBox;
        private System.Windows.Forms.CheckBox showUICheckBox;
        private System.Windows.Forms.CheckBox modalUICheckBox;
        private System.Windows.Forms.CheckBox disableAfterScanCheckBox;
        private System.Windows.Forms.ComboBox devicesComboBox;
        private System.Windows.Forms.CheckBox twain2CompatibleCheckBox;
        private System.Windows.Forms.Button deleteImageButton;
        private System.Windows.Forms.Panel panel1;
        private System.Windows.Forms.Button uploadImageButton;
        private System.Windows.Forms.Button saveImageButton;
        private System.Windows.Forms.Button getDeviceInfoButton;
        private System.Windows.Forms.Label imageInfoLabel;
        private System.Windows.Forms.Button nextImageButton;
        private System.Windows.Forms.Button previousImageButton;
        private System.Windows.Forms.Button processImageButton;
        private System.Windows.Forms.ProgressBar imageAcquisitionProgressBar;
        private System.Windows.Forms.GroupBox imageGroupBox;
        private System.Windows.Forms.RadioButton acquireAllImagesRadioButton;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.RadioButton imagesToAcquireRadioButton;
        private System.Windows.Forms.ComboBox pixelTypeComboBox;
        private System.Windows.Forms.Label resolutionLabel;
        private System.Windows.Forms.ComboBox resolutionComboBox;
        private System.Windows.Forms.Label pixelTypeLabel;
        private System.Windows.Forms.Label transferModeLabel;
        private System.Windows.Forms.ComboBox transferModeComboBox;
        private System.Windows.Forms.Button clearImagesButton;


    }
}

