namespace TwainCustomUIDemo
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
            this.components = new System.ComponentModel.Container();
            this.devicesComboBox = new System.Windows.Forms.ComboBox();
            this.label1 = new System.Windows.Forms.Label();
            this.pageGroupBox = new System.Windows.Forms.GroupBox();
            this.pageOrientationComboBox = new System.Windows.Forms.ComboBox();
            this.pageOrientationLabel = new System.Windows.Forms.Label();
            this.pageSizeComboBox = new System.Windows.Forms.ComboBox();
            this.pageSizeLabel = new System.Windows.Forms.Label();
            this.imageGroupBox = new System.Windows.Forms.GroupBox();
            this.thresholdComboBox = new System.Windows.Forms.ComboBox();
            this.contrastComboBox = new System.Windows.Forms.ComboBox();
            this.brightnessComboBox = new System.Windows.Forms.ComboBox();
            this.contrastLabel = new System.Windows.Forms.Label();
            this.bitDepthComboBox = new System.Windows.Forms.ComboBox();
            this.bitDepthLabel = new System.Windows.Forms.Label();
            this.pixelTypeComboBox = new System.Windows.Forms.ComboBox();
            this.pixelTypeLabel = new System.Windows.Forms.Label();
            this.brightnessLabel = new System.Windows.Forms.Label();
            this.thresholdLabel = new System.Windows.Forms.Label();
            this.contrastTrackBar = new System.Windows.Forms.TrackBar();
            this.thresholdTrackBar = new System.Windows.Forms.TrackBar();
            this.brightnessTrackBar = new System.Windows.Forms.TrackBar();
            this.imageProcessingGroupBox = new System.Windows.Forms.GroupBox();
            this.autoBorderDetectionCheckBox = new System.Windows.Forms.CheckBox();
            this.autoRotateCheckBox = new System.Windows.Forms.CheckBox();
            this.noiseFilterComboBox = new System.Windows.Forms.ComboBox();
            this.noiseFilterLabel = new System.Windows.Forms.Label();
            this.imageFilterComboBox = new System.Windows.Forms.ComboBox();
            this.imageFilterLabel = new System.Windows.Forms.Label();
            this.resolutionGroupBox = new System.Windows.Forms.GroupBox();
            this.unitOfMeasureComboBox = new System.Windows.Forms.ComboBox();
            this.unitOfMeasureLabel = new System.Windows.Forms.Label();
            this.yResComboBox = new System.Windows.Forms.ComboBox();
            this.yResLabel = new System.Windows.Forms.Label();
            this.xResLabel = new System.Windows.Forms.Label();
            this.xResComboBox = new System.Windows.Forms.ComboBox();
            this.yResTrackBar = new System.Windows.Forms.TrackBar();
            this.xResTrackBar = new System.Windows.Forms.TrackBar();
            this.twain2CompatibleCheckBox = new System.Windows.Forms.CheckBox();
            this.imageLayoutGroupBox = new System.Windows.Forms.GroupBox();
            this.resetImageLayoutButton = new System.Windows.Forms.Button();
            this.bottomTextBox = new System.Windows.Forms.TextBox();
            this.rightTextBox = new System.Windows.Forms.TextBox();
            this.topTextBox = new System.Windows.Forms.TextBox();
            this.leftTextBox = new System.Windows.Forms.TextBox();
            this.label13 = new System.Windows.Forms.Label();
            this.label14 = new System.Windows.Forms.Label();
            this.label7 = new System.Windows.Forms.Label();
            this.label12 = new System.Windows.Forms.Label();
            this.acquireImageButton = new System.Windows.Forms.Button();
            this.imageAcquisitionProgressBar = new System.Windows.Forms.ProgressBar();
            this.acquiredImagesTabControl = new System.Windows.Forms.TabControl();
            this.label15 = new System.Windows.Forms.Label();
            this.pagesToAcquireNumericUpDown = new System.Windows.Forms.NumericUpDown();
            this.comboBox1 = new System.Windows.Forms.ComboBox();
            this.label16 = new System.Windows.Forms.Label();
            this.comboBox2 = new System.Windows.Forms.ComboBox();
            this.label17 = new System.Windows.Forms.Label();
            this.imagesToAcquireGroupBox = new System.Windows.Forms.GroupBox();
            this.transferModeGroupBox = new System.Windows.Forms.GroupBox();
            this.memoryTransferRadioButton = new System.Windows.Forms.RadioButton();
            this.nativeTransferRadioButton = new System.Windows.Forms.RadioButton();
            this.clearImagesButton = new System.Windows.Forms.Button();
            this.toolTip1 = new System.Windows.Forms.ToolTip(this.components);
            this.pageGroupBox.SuspendLayout();
            this.imageGroupBox.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.contrastTrackBar)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.thresholdTrackBar)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.brightnessTrackBar)).BeginInit();
            this.imageProcessingGroupBox.SuspendLayout();
            this.resolutionGroupBox.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.yResTrackBar)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.xResTrackBar)).BeginInit();
            this.imageLayoutGroupBox.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pagesToAcquireNumericUpDown)).BeginInit();
            this.imagesToAcquireGroupBox.SuspendLayout();
            this.transferModeGroupBox.SuspendLayout();
            this.SuspendLayout();
            // 
            // devicesComboBox
            // 
            this.devicesComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.devicesComboBox.Location = new System.Drawing.Point(56, 29);
            this.devicesComboBox.Name = "devicesComboBox";
            this.devicesComboBox.Size = new System.Drawing.Size(286, 21);
            this.devicesComboBox.TabIndex = 89;
            this.devicesComboBox.SelectedIndexChanged += new System.EventHandler(this.devicesComboBox_SelectedIndexChanged);
            // 
            // label1
            // 
            this.label1.Location = new System.Drawing.Point(6, 31);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(56, 16);
            this.label1.TabIndex = 99;
            this.label1.Text = "Device:";
            // 
            // pageGroupBox
            // 
            this.pageGroupBox.Controls.Add(this.pageOrientationComboBox);
            this.pageGroupBox.Controls.Add(this.pageOrientationLabel);
            this.pageGroupBox.Controls.Add(this.pageSizeComboBox);
            this.pageGroupBox.Controls.Add(this.pageSizeLabel);
            this.pageGroupBox.Location = new System.Drawing.Point(9, 100);
            this.pageGroupBox.Name = "pageGroupBox";
            this.pageGroupBox.Size = new System.Drawing.Size(262, 67);
            this.pageGroupBox.TabIndex = 100;
            this.pageGroupBox.TabStop = false;
            this.pageGroupBox.Text = "Page";
            // 
            // pageOrientationComboBox
            // 
            this.pageOrientationComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.pageOrientationComboBox.FormattingEnabled = true;
            this.pageOrientationComboBox.Location = new System.Drawing.Point(75, 40);
            this.pageOrientationComboBox.Name = "pageOrientationComboBox";
            this.pageOrientationComboBox.Size = new System.Drawing.Size(177, 21);
            this.pageOrientationComboBox.TabIndex = 3;
            // 
            // pageOrientationLabel
            // 
            this.pageOrientationLabel.AutoSize = true;
            this.pageOrientationLabel.Location = new System.Drawing.Point(8, 43);
            this.pageOrientationLabel.Name = "pageOrientationLabel";
            this.pageOrientationLabel.Size = new System.Drawing.Size(61, 13);
            this.pageOrientationLabel.TabIndex = 2;
            this.pageOrientationLabel.Text = "Orientation:";
            // 
            // pageSizeComboBox
            // 
            this.pageSizeComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.pageSizeComboBox.FormattingEnabled = true;
            this.pageSizeComboBox.Location = new System.Drawing.Point(75, 15);
            this.pageSizeComboBox.Name = "pageSizeComboBox";
            this.pageSizeComboBox.Size = new System.Drawing.Size(177, 21);
            this.pageSizeComboBox.TabIndex = 1;
            // 
            // pageSizeLabel
            // 
            this.pageSizeLabel.AutoSize = true;
            this.pageSizeLabel.Location = new System.Drawing.Point(8, 18);
            this.pageSizeLabel.Name = "pageSizeLabel";
            this.pageSizeLabel.Size = new System.Drawing.Size(30, 13);
            this.pageSizeLabel.TabIndex = 0;
            this.pageSizeLabel.Text = "Size:";
            // 
            // imageGroupBox
            // 
            this.imageGroupBox.Controls.Add(this.thresholdComboBox);
            this.imageGroupBox.Controls.Add(this.contrastComboBox);
            this.imageGroupBox.Controls.Add(this.brightnessComboBox);
            this.imageGroupBox.Controls.Add(this.contrastLabel);
            this.imageGroupBox.Controls.Add(this.bitDepthComboBox);
            this.imageGroupBox.Controls.Add(this.bitDepthLabel);
            this.imageGroupBox.Controls.Add(this.pixelTypeComboBox);
            this.imageGroupBox.Controls.Add(this.pixelTypeLabel);
            this.imageGroupBox.Controls.Add(this.brightnessLabel);
            this.imageGroupBox.Controls.Add(this.thresholdLabel);
            this.imageGroupBox.Controls.Add(this.contrastTrackBar);
            this.imageGroupBox.Controls.Add(this.thresholdTrackBar);
            this.imageGroupBox.Controls.Add(this.brightnessTrackBar);
            this.imageGroupBox.Location = new System.Drawing.Point(277, 101);
            this.imageGroupBox.Name = "imageGroupBox";
            this.imageGroupBox.Size = new System.Drawing.Size(262, 124);
            this.imageGroupBox.TabIndex = 101;
            this.imageGroupBox.TabStop = false;
            this.imageGroupBox.Text = "Image";
            // 
            // thresholdComboBox
            // 
            this.thresholdComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.thresholdComboBox.FormattingEnabled = true;
            this.thresholdComboBox.Location = new System.Drawing.Point(75, 70);
            this.thresholdComboBox.Name = "thresholdComboBox";
            this.thresholdComboBox.Size = new System.Drawing.Size(171, 21);
            this.thresholdComboBox.TabIndex = 119;
            // 
            // contrastComboBox
            // 
            this.contrastComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.contrastComboBox.FormattingEnabled = true;
            this.contrastComboBox.Location = new System.Drawing.Point(75, 97);
            this.contrastComboBox.Name = "contrastComboBox";
            this.contrastComboBox.Size = new System.Drawing.Size(171, 21);
            this.contrastComboBox.TabIndex = 118;
            // 
            // brightnessComboBox
            // 
            this.brightnessComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.brightnessComboBox.FormattingEnabled = true;
            this.brightnessComboBox.Location = new System.Drawing.Point(75, 70);
            this.brightnessComboBox.Name = "brightnessComboBox";
            this.brightnessComboBox.Size = new System.Drawing.Size(171, 21);
            this.brightnessComboBox.TabIndex = 117;
            // 
            // contrastLabel
            // 
            this.contrastLabel.AutoSize = true;
            this.contrastLabel.Location = new System.Drawing.Point(9, 100);
            this.contrastLabel.Name = "contrastLabel";
            this.contrastLabel.Size = new System.Drawing.Size(49, 13);
            this.contrastLabel.TabIndex = 6;
            this.contrastLabel.Text = "Contrast:";
            // 
            // bitDepthComboBox
            // 
            this.bitDepthComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.bitDepthComboBox.FormattingEnabled = true;
            this.bitDepthComboBox.Location = new System.Drawing.Point(74, 43);
            this.bitDepthComboBox.Name = "bitDepthComboBox";
            this.bitDepthComboBox.Size = new System.Drawing.Size(171, 21);
            this.bitDepthComboBox.TabIndex = 3;
            // 
            // bitDepthLabel
            // 
            this.bitDepthLabel.AutoSize = true;
            this.bitDepthLabel.Location = new System.Drawing.Point(8, 46);
            this.bitDepthLabel.Name = "bitDepthLabel";
            this.bitDepthLabel.Size = new System.Drawing.Size(52, 13);
            this.bitDepthLabel.TabIndex = 2;
            this.bitDepthLabel.Text = "Bit depth:";
            // 
            // pixelTypeComboBox
            // 
            this.pixelTypeComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.pixelTypeComboBox.FormattingEnabled = true;
            this.pixelTypeComboBox.Location = new System.Drawing.Point(74, 16);
            this.pixelTypeComboBox.Name = "pixelTypeComboBox";
            this.pixelTypeComboBox.Size = new System.Drawing.Size(171, 21);
            this.pixelTypeComboBox.TabIndex = 1;
            this.pixelTypeComboBox.SelectedIndexChanged += new System.EventHandler(this.pixelTypeComboBox_SelectedIndexChanged);
            // 
            // pixelTypeLabel
            // 
            this.pixelTypeLabel.AutoSize = true;
            this.pixelTypeLabel.Location = new System.Drawing.Point(8, 18);
            this.pixelTypeLabel.Name = "pixelTypeLabel";
            this.pixelTypeLabel.Size = new System.Drawing.Size(55, 13);
            this.pixelTypeLabel.TabIndex = 0;
            this.pixelTypeLabel.Text = "Pixel type:";
            // 
            // brightnessLabel
            // 
            this.brightnessLabel.AutoSize = true;
            this.brightnessLabel.Location = new System.Drawing.Point(9, 73);
            this.brightnessLabel.Name = "brightnessLabel";
            this.brightnessLabel.Size = new System.Drawing.Size(59, 13);
            this.brightnessLabel.TabIndex = 4;
            this.brightnessLabel.Text = "Brightness:";
            // 
            // thresholdLabel
            // 
            this.thresholdLabel.AutoSize = true;
            this.thresholdLabel.Location = new System.Drawing.Point(8, 73);
            this.thresholdLabel.Name = "thresholdLabel";
            this.thresholdLabel.Size = new System.Drawing.Size(57, 13);
            this.thresholdLabel.TabIndex = 8;
            this.thresholdLabel.Text = "Threshold:";
            // 
            // contrastTrackBar
            // 
            this.contrastTrackBar.AutoSize = false;
            this.contrastTrackBar.Location = new System.Drawing.Point(71, 97);
            this.contrastTrackBar.Name = "contrastTrackBar";
            this.contrastTrackBar.Size = new System.Drawing.Size(181, 21);
            this.contrastTrackBar.TabIndex = 115;
            this.contrastTrackBar.Scroll += new System.EventHandler(this.trackBar_Scroll);
            this.contrastTrackBar.MouseHover += new System.EventHandler(this.trackBar_MouseHover);
            // 
            // thresholdTrackBar
            // 
            this.thresholdTrackBar.AutoSize = false;
            this.thresholdTrackBar.Location = new System.Drawing.Point(71, 70);
            this.thresholdTrackBar.Name = "thresholdTrackBar";
            this.thresholdTrackBar.Size = new System.Drawing.Size(181, 21);
            this.thresholdTrackBar.TabIndex = 116;
            this.thresholdTrackBar.Scroll += new System.EventHandler(this.trackBar_Scroll);
            this.thresholdTrackBar.MouseHover += new System.EventHandler(this.trackBar_MouseHover);
            // 
            // brightnessTrackBar
            // 
            this.brightnessTrackBar.AutoSize = false;
            this.brightnessTrackBar.Location = new System.Drawing.Point(71, 70);
            this.brightnessTrackBar.Name = "brightnessTrackBar";
            this.brightnessTrackBar.Size = new System.Drawing.Size(181, 21);
            this.brightnessTrackBar.TabIndex = 114;
            this.brightnessTrackBar.Scroll += new System.EventHandler(this.trackBar_Scroll);
            this.brightnessTrackBar.MouseHover += new System.EventHandler(this.trackBar_MouseHover);
            // 
            // imageProcessingGroupBox
            // 
            this.imageProcessingGroupBox.Controls.Add(this.autoBorderDetectionCheckBox);
            this.imageProcessingGroupBox.Controls.Add(this.autoRotateCheckBox);
            this.imageProcessingGroupBox.Controls.Add(this.noiseFilterComboBox);
            this.imageProcessingGroupBox.Controls.Add(this.noiseFilterLabel);
            this.imageProcessingGroupBox.Controls.Add(this.imageFilterComboBox);
            this.imageProcessingGroupBox.Controls.Add(this.imageFilterLabel);
            this.imageProcessingGroupBox.Location = new System.Drawing.Point(277, 228);
            this.imageProcessingGroupBox.Name = "imageProcessingGroupBox";
            this.imageProcessingGroupBox.Size = new System.Drawing.Size(262, 108);
            this.imageProcessingGroupBox.TabIndex = 102;
            this.imageProcessingGroupBox.TabStop = false;
            this.imageProcessingGroupBox.Text = "Image processing";
            // 
            // autoBorderDetectionCheckBox
            // 
            this.autoBorderDetectionCheckBox.AutoSize = true;
            this.autoBorderDetectionCheckBox.Location = new System.Drawing.Point(11, 85);
            this.autoBorderDetectionCheckBox.Name = "autoBorderDetectionCheckBox";
            this.autoBorderDetectionCheckBox.Size = new System.Drawing.Size(153, 17);
            this.autoBorderDetectionCheckBox.TabIndex = 6;
            this.autoBorderDetectionCheckBox.Text = "Automatic border detection";
            this.autoBorderDetectionCheckBox.UseVisualStyleBackColor = true;
            // 
            // autoRotateCheckBox
            // 
            this.autoRotateCheckBox.AutoSize = true;
            this.autoRotateCheckBox.Location = new System.Drawing.Point(11, 68);
            this.autoRotateCheckBox.Name = "autoRotateCheckBox";
            this.autoRotateCheckBox.Size = new System.Drawing.Size(103, 17);
            this.autoRotateCheckBox.TabIndex = 4;
            this.autoRotateCheckBox.Text = "Automatic rotate";
            this.autoRotateCheckBox.UseVisualStyleBackColor = true;
            // 
            // noiseFilterComboBox
            // 
            this.noiseFilterComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.noiseFilterComboBox.FormattingEnabled = true;
            this.noiseFilterComboBox.Location = new System.Drawing.Point(75, 42);
            this.noiseFilterComboBox.Name = "noiseFilterComboBox";
            this.noiseFilterComboBox.Size = new System.Drawing.Size(177, 21);
            this.noiseFilterComboBox.TabIndex = 3;
            // 
            // noiseFilterLabel
            // 
            this.noiseFilterLabel.AutoSize = true;
            this.noiseFilterLabel.Location = new System.Drawing.Point(8, 45);
            this.noiseFilterLabel.Name = "noiseFilterLabel";
            this.noiseFilterLabel.Size = new System.Drawing.Size(59, 13);
            this.noiseFilterLabel.TabIndex = 2;
            this.noiseFilterLabel.Text = "Noise filter:";
            // 
            // imageFilterComboBox
            // 
            this.imageFilterComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.imageFilterComboBox.FormattingEnabled = true;
            this.imageFilterComboBox.Location = new System.Drawing.Point(75, 16);
            this.imageFilterComboBox.Name = "imageFilterComboBox";
            this.imageFilterComboBox.Size = new System.Drawing.Size(177, 21);
            this.imageFilterComboBox.TabIndex = 1;
            // 
            // imageFilterLabel
            // 
            this.imageFilterLabel.AutoSize = true;
            this.imageFilterLabel.Location = new System.Drawing.Point(8, 19);
            this.imageFilterLabel.Name = "imageFilterLabel";
            this.imageFilterLabel.Size = new System.Drawing.Size(61, 13);
            this.imageFilterLabel.TabIndex = 0;
            this.imageFilterLabel.Text = "Image filter:";
            // 
            // resolutionGroupBox
            // 
            this.resolutionGroupBox.Controls.Add(this.unitOfMeasureComboBox);
            this.resolutionGroupBox.Controls.Add(this.unitOfMeasureLabel);
            this.resolutionGroupBox.Controls.Add(this.yResComboBox);
            this.resolutionGroupBox.Controls.Add(this.yResLabel);
            this.resolutionGroupBox.Controls.Add(this.xResLabel);
            this.resolutionGroupBox.Controls.Add(this.xResComboBox);
            this.resolutionGroupBox.Controls.Add(this.yResTrackBar);
            this.resolutionGroupBox.Controls.Add(this.xResTrackBar);
            this.resolutionGroupBox.Location = new System.Drawing.Point(9, 169);
            this.resolutionGroupBox.Name = "resolutionGroupBox";
            this.resolutionGroupBox.Size = new System.Drawing.Size(262, 93);
            this.resolutionGroupBox.TabIndex = 103;
            this.resolutionGroupBox.TabStop = false;
            this.resolutionGroupBox.Text = "Resolution";
            // 
            // unitOfMeasureComboBox
            // 
            this.unitOfMeasureComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.unitOfMeasureComboBox.FormattingEnabled = true;
            this.unitOfMeasureComboBox.Location = new System.Drawing.Point(96, 15);
            this.unitOfMeasureComboBox.Name = "unitOfMeasureComboBox";
            this.unitOfMeasureComboBox.Size = new System.Drawing.Size(156, 21);
            this.unitOfMeasureComboBox.TabIndex = 5;
            this.unitOfMeasureComboBox.SelectedIndexChanged += new System.EventHandler(this.unitOfMeasureComboBox_SelectedIndexChanged);
            // 
            // unitOfMeasureLabel
            // 
            this.unitOfMeasureLabel.AutoSize = true;
            this.unitOfMeasureLabel.Location = new System.Drawing.Point(6, 18);
            this.unitOfMeasureLabel.Name = "unitOfMeasureLabel";
            this.unitOfMeasureLabel.Size = new System.Drawing.Size(84, 13);
            this.unitOfMeasureLabel.TabIndex = 4;
            this.unitOfMeasureLabel.Text = "Unit of measure:";
            // 
            // yResComboBox
            // 
            this.yResComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.yResComboBox.FormattingEnabled = true;
            this.yResComboBox.Location = new System.Drawing.Point(96, 65);
            this.yResComboBox.Name = "yResComboBox";
            this.yResComboBox.Size = new System.Drawing.Size(156, 21);
            this.yResComboBox.TabIndex = 3;
            // 
            // yResLabel
            // 
            this.yResLabel.AutoSize = true;
            this.yResLabel.Location = new System.Drawing.Point(7, 68);
            this.yResLabel.Name = "yResLabel";
            this.yResLabel.Size = new System.Drawing.Size(45, 13);
            this.yResLabel.TabIndex = 2;
            this.yResLabel.Text = "Vertical:";
            // 
            // xResLabel
            // 
            this.xResLabel.AutoSize = true;
            this.xResLabel.Location = new System.Drawing.Point(7, 43);
            this.xResLabel.Name = "xResLabel";
            this.xResLabel.Size = new System.Drawing.Size(57, 13);
            this.xResLabel.TabIndex = 0;
            this.xResLabel.Text = "Horizontal:";
            // 
            // xResComboBox
            // 
            this.xResComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.xResComboBox.FormattingEnabled = true;
            this.xResComboBox.Location = new System.Drawing.Point(96, 40);
            this.xResComboBox.Name = "xResComboBox";
            this.xResComboBox.Size = new System.Drawing.Size(156, 21);
            this.xResComboBox.TabIndex = 1;
            // 
            // yResTrackBar
            // 
            this.yResTrackBar.AutoSize = false;
            this.yResTrackBar.Location = new System.Drawing.Point(91, 65);
            this.yResTrackBar.Name = "yResTrackBar";
            this.yResTrackBar.Size = new System.Drawing.Size(168, 21);
            this.yResTrackBar.TabIndex = 118;
            this.yResTrackBar.Scroll += new System.EventHandler(this.trackBar_Scroll);
            this.yResTrackBar.MouseHover += new System.EventHandler(this.trackBar_MouseHover);
            // 
            // xResTrackBar
            // 
            this.xResTrackBar.AutoSize = false;
            this.xResTrackBar.Location = new System.Drawing.Point(91, 40);
            this.xResTrackBar.Name = "xResTrackBar";
            this.xResTrackBar.Size = new System.Drawing.Size(168, 21);
            this.xResTrackBar.TabIndex = 117;
            this.xResTrackBar.Scroll += new System.EventHandler(this.trackBar_Scroll);
            this.xResTrackBar.MouseHover += new System.EventHandler(this.trackBar_MouseHover);
            // 
            // twain2CompatibleCheckBox
            // 
            this.twain2CompatibleCheckBox.Checked = true;
            this.twain2CompatibleCheckBox.CheckState = System.Windows.Forms.CheckState.Checked;
            this.twain2CompatibleCheckBox.Location = new System.Drawing.Point(9, 6);
            this.twain2CompatibleCheckBox.Name = "twain2CompatibleCheckBox";
            this.twain2CompatibleCheckBox.Size = new System.Drawing.Size(136, 17);
            this.twain2CompatibleCheckBox.TabIndex = 104;
            this.twain2CompatibleCheckBox.Text = "TWAIN 2.0 compatible";
            this.twain2CompatibleCheckBox.UseVisualStyleBackColor = true;
            this.twain2CompatibleCheckBox.CheckedChanged += new System.EventHandler(this.twain2CompatibleCheckBox_CheckedChanged);
            // 
            // imageLayoutGroupBox
            // 
            this.imageLayoutGroupBox.Controls.Add(this.resetImageLayoutButton);
            this.imageLayoutGroupBox.Controls.Add(this.bottomTextBox);
            this.imageLayoutGroupBox.Controls.Add(this.rightTextBox);
            this.imageLayoutGroupBox.Controls.Add(this.topTextBox);
            this.imageLayoutGroupBox.Controls.Add(this.leftTextBox);
            this.imageLayoutGroupBox.Controls.Add(this.label13);
            this.imageLayoutGroupBox.Controls.Add(this.label14);
            this.imageLayoutGroupBox.Controls.Add(this.label7);
            this.imageLayoutGroupBox.Controls.Add(this.label12);
            this.imageLayoutGroupBox.Location = new System.Drawing.Point(9, 265);
            this.imageLayoutGroupBox.Name = "imageLayoutGroupBox";
            this.imageLayoutGroupBox.Size = new System.Drawing.Size(262, 94);
            this.imageLayoutGroupBox.TabIndex = 105;
            this.imageLayoutGroupBox.TabStop = false;
            this.imageLayoutGroupBox.Text = "Image layout:";
            // 
            // resetImageLayoutButton
            // 
            this.resetImageLayoutButton.Location = new System.Drawing.Point(177, 64);
            this.resetImageLayoutButton.Name = "resetImageLayoutButton";
            this.resetImageLayoutButton.Size = new System.Drawing.Size(75, 23);
            this.resetImageLayoutButton.TabIndex = 14;
            this.resetImageLayoutButton.Text = "Reset";
            this.resetImageLayoutButton.UseVisualStyleBackColor = true;
            this.resetImageLayoutButton.Click += new System.EventHandler(this.resetImageLayoutButton_Click);
            // 
            // bottomTextBox
            // 
            this.bottomTextBox.Location = new System.Drawing.Point(177, 40);
            this.bottomTextBox.Name = "bottomTextBox";
            this.bottomTextBox.Size = new System.Drawing.Size(75, 20);
            this.bottomTextBox.TabIndex = 13;
            // 
            // rightTextBox
            // 
            this.rightTextBox.Location = new System.Drawing.Point(45, 40);
            this.rightTextBox.Name = "rightTextBox";
            this.rightTextBox.Size = new System.Drawing.Size(75, 20);
            this.rightTextBox.TabIndex = 12;
            // 
            // topTextBox
            // 
            this.topTextBox.Location = new System.Drawing.Point(177, 16);
            this.topTextBox.Name = "topTextBox";
            this.topTextBox.Size = new System.Drawing.Size(75, 20);
            this.topTextBox.TabIndex = 11;
            // 
            // leftTextBox
            // 
            this.leftTextBox.Location = new System.Drawing.Point(45, 17);
            this.leftTextBox.Name = "leftTextBox";
            this.leftTextBox.Size = new System.Drawing.Size(75, 20);
            this.leftTextBox.TabIndex = 10;
            // 
            // label13
            // 
            this.label13.AutoSize = true;
            this.label13.Location = new System.Drawing.Point(129, 43);
            this.label13.Name = "label13";
            this.label13.Size = new System.Drawing.Size(43, 13);
            this.label13.TabIndex = 7;
            this.label13.Text = "Bottom:";
            // 
            // label14
            // 
            this.label14.AutoSize = true;
            this.label14.Location = new System.Drawing.Point(8, 43);
            this.label14.Name = "label14";
            this.label14.Size = new System.Drawing.Size(35, 13);
            this.label14.TabIndex = 6;
            this.label14.Text = "Right:";
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Location = new System.Drawing.Point(129, 19);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(29, 13);
            this.label7.TabIndex = 2;
            this.label7.Text = "Top:";
            // 
            // label12
            // 
            this.label12.AutoSize = true;
            this.label12.Location = new System.Drawing.Point(8, 19);
            this.label12.Name = "label12";
            this.label12.Size = new System.Drawing.Size(28, 13);
            this.label12.TabIndex = 0;
            this.label12.Text = "Left:";
            // 
            // acquireImageButton
            // 
            this.acquireImageButton.Location = new System.Drawing.Point(352, 6);
            this.acquireImageButton.Name = "acquireImageButton";
            this.acquireImageButton.Size = new System.Drawing.Size(187, 45);
            this.acquireImageButton.TabIndex = 106;
            this.acquireImageButton.Text = "Acquire image(s)";
            this.acquireImageButton.UseVisualStyleBackColor = true;
            this.acquireImageButton.Click += new System.EventHandler(this.acquireImageButton_Click);
            // 
            // imageAcquisitionProgressBar
            // 
            this.imageAcquisitionProgressBar.Location = new System.Drawing.Point(9, 676);
            this.imageAcquisitionProgressBar.Name = "imageAcquisitionProgressBar";
            this.imageAcquisitionProgressBar.Size = new System.Drawing.Size(530, 23);
            this.imageAcquisitionProgressBar.TabIndex = 107;
            // 
            // acquiredImagesTabControl
            // 
            this.acquiredImagesTabControl.Location = new System.Drawing.Point(9, 364);
            this.acquiredImagesTabControl.Name = "acquiredImagesTabControl";
            this.acquiredImagesTabControl.SelectedIndex = 0;
            this.acquiredImagesTabControl.Size = new System.Drawing.Size(530, 306);
            this.acquiredImagesTabControl.TabIndex = 108;
            // 
            // label15
            // 
            this.label15.AutoSize = true;
            this.label15.Location = new System.Drawing.Point(8, 16);
            this.label15.Name = "label15";
            this.label15.Size = new System.Drawing.Size(95, 13);
            this.label15.TabIndex = 109;
            this.label15.Text = "Number of images:";
            // 
            // pagesToAcquireNumericUpDown
            // 
            this.pagesToAcquireNumericUpDown.Location = new System.Drawing.Point(112, 15);
            this.pagesToAcquireNumericUpDown.Maximum = new decimal(new int[] {
            255,
            0,
            0,
            0});
            this.pagesToAcquireNumericUpDown.Minimum = new decimal(new int[] {
            1,
            0,
            0,
            -2147483648});
            this.pagesToAcquireNumericUpDown.Name = "pagesToAcquireNumericUpDown";
            this.pagesToAcquireNumericUpDown.Size = new System.Drawing.Size(93, 20);
            this.pagesToAcquireNumericUpDown.TabIndex = 110;
            this.pagesToAcquireNumericUpDown.Value = new decimal(new int[] {
            1,
            0,
            0,
            -2147483648});
            // 
            // comboBox1
            // 
            this.comboBox1.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBox1.FormattingEnabled = true;
            this.comboBox1.Location = new System.Drawing.Point(75, 47);
            this.comboBox1.Name = "comboBox1";
            this.comboBox1.Size = new System.Drawing.Size(177, 21);
            this.comboBox1.TabIndex = 3;
            // 
            // label16
            // 
            this.label16.AutoSize = true;
            this.label16.Location = new System.Drawing.Point(8, 50);
            this.label16.Name = "label16";
            this.label16.Size = new System.Drawing.Size(61, 13);
            this.label16.TabIndex = 2;
            this.label16.Text = "Orientation:";
            // 
            // comboBox2
            // 
            this.comboBox2.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBox2.FormattingEnabled = true;
            this.comboBox2.Location = new System.Drawing.Point(75, 20);
            this.comboBox2.Name = "comboBox2";
            this.comboBox2.Size = new System.Drawing.Size(177, 21);
            this.comboBox2.TabIndex = 1;
            // 
            // label17
            // 
            this.label17.AutoSize = true;
            this.label17.Location = new System.Drawing.Point(8, 23);
            this.label17.Name = "label17";
            this.label17.Size = new System.Drawing.Size(30, 13);
            this.label17.TabIndex = 0;
            this.label17.Text = "Size:";
            // 
            // imagesToAcquireGroupBox
            // 
            this.imagesToAcquireGroupBox.Controls.Add(this.pagesToAcquireNumericUpDown);
            this.imagesToAcquireGroupBox.Controls.Add(this.label15);
            this.imagesToAcquireGroupBox.Location = new System.Drawing.Point(277, 57);
            this.imagesToAcquireGroupBox.Name = "imagesToAcquireGroupBox";
            this.imagesToAcquireGroupBox.Size = new System.Drawing.Size(262, 41);
            this.imagesToAcquireGroupBox.TabIndex = 111;
            this.imagesToAcquireGroupBox.TabStop = false;
            this.imagesToAcquireGroupBox.Text = "Images to acquire";
            // 
            // transferModeGroupBox
            // 
            this.transferModeGroupBox.Controls.Add(this.memoryTransferRadioButton);
            this.transferModeGroupBox.Controls.Add(this.nativeTransferRadioButton);
            this.transferModeGroupBox.Location = new System.Drawing.Point(9, 57);
            this.transferModeGroupBox.Name = "transferModeGroupBox";
            this.transferModeGroupBox.Size = new System.Drawing.Size(262, 41);
            this.transferModeGroupBox.TabIndex = 112;
            this.transferModeGroupBox.TabStop = false;
            this.transferModeGroupBox.Text = "Transfer mode";
            // 
            // memoryTransferRadioButton
            // 
            this.memoryTransferRadioButton.AutoSize = true;
            this.memoryTransferRadioButton.Checked = true;
            this.memoryTransferRadioButton.Location = new System.Drawing.Point(132, 16);
            this.memoryTransferRadioButton.Name = "memoryTransferRadioButton";
            this.memoryTransferRadioButton.Size = new System.Drawing.Size(62, 17);
            this.memoryTransferRadioButton.TabIndex = 1;
            this.memoryTransferRadioButton.TabStop = true;
            this.memoryTransferRadioButton.Text = "Memory";
            this.memoryTransferRadioButton.UseVisualStyleBackColor = true;
            this.memoryTransferRadioButton.CheckedChanged += new System.EventHandler(this.memoryTransferRadioButton_CheckedChanged);
            // 
            // nativeTransferRadioButton
            // 
            this.nativeTransferRadioButton.AutoSize = true;
            this.nativeTransferRadioButton.Location = new System.Drawing.Point(14, 16);
            this.nativeTransferRadioButton.Name = "nativeTransferRadioButton";
            this.nativeTransferRadioButton.Size = new System.Drawing.Size(56, 17);
            this.nativeTransferRadioButton.TabIndex = 0;
            this.nativeTransferRadioButton.Text = "Native";
            this.nativeTransferRadioButton.UseVisualStyleBackColor = true;
            this.nativeTransferRadioButton.CheckedChanged += new System.EventHandler(this.nativeTransferRadioButton_CheckedChanged);
            // 
            // clearImagesButton
            // 
            this.clearImagesButton.Location = new System.Drawing.Point(432, 342);
            this.clearImagesButton.Name = "clearImagesButton";
            this.clearImagesButton.Size = new System.Drawing.Size(107, 23);
            this.clearImagesButton.TabIndex = 113;
            this.clearImagesButton.Text = "Clear images";
            this.clearImagesButton.UseVisualStyleBackColor = true;
            this.clearImagesButton.Click += new System.EventHandler(this.clearImagesButton_Click);
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(547, 704);
            this.Controls.Add(this.clearImagesButton);
            this.Controls.Add(this.transferModeGroupBox);
            this.Controls.Add(this.imagesToAcquireGroupBox);
            this.Controls.Add(this.acquiredImagesTabControl);
            this.Controls.Add(this.imageAcquisitionProgressBar);
            this.Controls.Add(this.acquireImageButton);
            this.Controls.Add(this.imageLayoutGroupBox);
            this.Controls.Add(this.twain2CompatibleCheckBox);
            this.Controls.Add(this.resolutionGroupBox);
            this.Controls.Add(this.imageProcessingGroupBox);
            this.Controls.Add(this.imageGroupBox);
            this.Controls.Add(this.pageGroupBox);
            this.Controls.Add(this.devicesComboBox);
            this.Controls.Add(this.label1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "MainForm";
            this.Text = "VintaSoft TWAIN Custom UI Demo";
            this.Shown += new System.EventHandler(this.MainForm_Shown);
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.MainForm_FormClosing);
            this.pageGroupBox.ResumeLayout(false);
            this.pageGroupBox.PerformLayout();
            this.imageGroupBox.ResumeLayout(false);
            this.imageGroupBox.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.contrastTrackBar)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.thresholdTrackBar)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.brightnessTrackBar)).EndInit();
            this.imageProcessingGroupBox.ResumeLayout(false);
            this.imageProcessingGroupBox.PerformLayout();
            this.resolutionGroupBox.ResumeLayout(false);
            this.resolutionGroupBox.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.yResTrackBar)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.xResTrackBar)).EndInit();
            this.imageLayoutGroupBox.ResumeLayout(false);
            this.imageLayoutGroupBox.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pagesToAcquireNumericUpDown)).EndInit();
            this.imagesToAcquireGroupBox.ResumeLayout(false);
            this.imagesToAcquireGroupBox.PerformLayout();
            this.transferModeGroupBox.ResumeLayout(false);
            this.transferModeGroupBox.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.ComboBox devicesComboBox;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.GroupBox pageGroupBox;
        private System.Windows.Forms.ComboBox pageOrientationComboBox;
        private System.Windows.Forms.Label pageOrientationLabel;
        private System.Windows.Forms.ComboBox pageSizeComboBox;
        private System.Windows.Forms.Label pageSizeLabel;
        private System.Windows.Forms.GroupBox imageGroupBox;
        private System.Windows.Forms.ComboBox bitDepthComboBox;
        private System.Windows.Forms.Label bitDepthLabel;
        private System.Windows.Forms.ComboBox pixelTypeComboBox;
        private System.Windows.Forms.Label pixelTypeLabel;
        private System.Windows.Forms.Label brightnessLabel;
        private System.Windows.Forms.GroupBox imageProcessingGroupBox;
        private System.Windows.Forms.ComboBox noiseFilterComboBox;
        private System.Windows.Forms.Label noiseFilterLabel;
        private System.Windows.Forms.ComboBox imageFilterComboBox;
        private System.Windows.Forms.Label imageFilterLabel;
        private System.Windows.Forms.Label thresholdLabel;
        private System.Windows.Forms.Label contrastLabel;
        private System.Windows.Forms.GroupBox resolutionGroupBox;
        private System.Windows.Forms.ComboBox unitOfMeasureComboBox;
        private System.Windows.Forms.Label unitOfMeasureLabel;
        private System.Windows.Forms.ComboBox yResComboBox;
        private System.Windows.Forms.Label yResLabel;
        private System.Windows.Forms.ComboBox xResComboBox;
        private System.Windows.Forms.Label xResLabel;
        private System.Windows.Forms.CheckBox twain2CompatibleCheckBox;
        private System.Windows.Forms.GroupBox imageLayoutGroupBox;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.Label label12;
        private System.Windows.Forms.Label label13;
        private System.Windows.Forms.Label label14;
        private System.Windows.Forms.TextBox bottomTextBox;
        private System.Windows.Forms.TextBox rightTextBox;
        private System.Windows.Forms.TextBox topTextBox;
        private System.Windows.Forms.TextBox leftTextBox;
        private System.Windows.Forms.Button resetImageLayoutButton;
        private System.Windows.Forms.CheckBox autoBorderDetectionCheckBox;
        private System.Windows.Forms.CheckBox autoRotateCheckBox;
        private System.Windows.Forms.Button acquireImageButton;
        private System.Windows.Forms.ProgressBar imageAcquisitionProgressBar;
        private System.Windows.Forms.TabControl acquiredImagesTabControl;
        private System.Windows.Forms.Label label15;
        private System.Windows.Forms.NumericUpDown pagesToAcquireNumericUpDown;
        private System.Windows.Forms.ComboBox comboBox1;
        private System.Windows.Forms.Label label16;
        private System.Windows.Forms.ComboBox comboBox2;
        private System.Windows.Forms.Label label17;
        private System.Windows.Forms.GroupBox imagesToAcquireGroupBox;
        private System.Windows.Forms.GroupBox transferModeGroupBox;
        private System.Windows.Forms.RadioButton memoryTransferRadioButton;
        private System.Windows.Forms.RadioButton nativeTransferRadioButton;
        private System.Windows.Forms.Button clearImagesButton;
        private System.Windows.Forms.TrackBar brightnessTrackBar;
        private System.Windows.Forms.TrackBar contrastTrackBar;
        private System.Windows.Forms.TrackBar thresholdTrackBar;
        private System.Windows.Forms.ToolTip toolTip1;
        private System.Windows.Forms.TrackBar xResTrackBar;
        private System.Windows.Forms.TrackBar yResTrackBar;
        private System.Windows.Forms.ComboBox brightnessComboBox;
        private System.Windows.Forms.ComboBox thresholdComboBox;
        private System.Windows.Forms.ComboBox contrastComboBox;
    }
}

