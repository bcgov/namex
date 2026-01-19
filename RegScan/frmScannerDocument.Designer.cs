namespace RegScan
{
    partial class frmScannerDocument
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
            this.useDuplexCheckBox = new System.Windows.Forms.CheckBox();
            this.useAdfCheckBox = new System.Windows.Forms.CheckBox();
            this.txtOwner = new System.Windows.Forms.TextBox();
            this.label11 = new System.Windows.Forms.Label();
            this.txtLegalEntityKey = new System.Windows.Forms.TextBox();
            this.label10 = new System.Windows.Forms.Label();
            this.txtDocumentId = new System.Windows.Forms.TextBox();
            this.label2 = new System.Windows.Forms.Label();
            this.txtPagesInBox = new System.Windows.Forms.TextBox();
            this.label9 = new System.Windows.Forms.Label();
            this.txtAccessionNumber = new System.Windows.Forms.TextBox();
            this.label8 = new System.Windows.Forms.Label();
            this.txtBatchNumber = new System.Windows.Forms.TextBox();
            this.label7 = new System.Windows.Forms.Label();
            this.txtPagesInDocument = new System.Windows.Forms.TextBox();
            this.label6 = new System.Windows.Forms.Label();
            this.txtVersionNumber = new System.Windows.Forms.TextBox();
            this.label5 = new System.Windows.Forms.Label();
            this.txtDocumentType = new System.Windows.Forms.TextBox();
            this.label4 = new System.Windows.Forms.Label();
            this.txtDocumentDescription = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.txtBarCode = new System.Windows.Forms.TextBox();
            this.showProgressIndicatorUICheckBox = new System.Windows.Forms.CheckBox();
            this.useUICheckBox = new System.Windows.Forms.CheckBox();
            this.ckBoxLowResolution = new System.Windows.Forms.CheckBox();
            this.panel2 = new System.Windows.Forms.Panel();
            this.label12 = new System.Windows.Forms.Label();
            this.cBoxPageSize = new System.Windows.Forms.ComboBox();
            this.cBoxOrientation = new System.Windows.Forms.ComboBox();
            this.heightLabel = new System.Windows.Forms.Label();
            this.pnlNextPreviosImage = new System.Windows.Forms.Panel();
            this.btnDeleteImage = new System.Windows.Forms.Button();
            this.lbImageDisplay = new System.Windows.Forms.Label();
            this.btnPreviousImage = new System.Windows.Forms.Button();
            this.btnNextImage = new System.Windows.Forms.Button();
            this.lbPagesScanned = new System.Windows.Forms.Label();
            this.lbDisplayImage = new System.Windows.Forms.Label();
            this.widthLabel = new System.Windows.Forms.Label();
            this.progressBar = new System.Windows.Forms.ProgressBar();
            this.btnCancelScan = new System.Windows.Forms.Button();
            this.upSharpen = new System.Windows.Forms.NumericUpDown();
            this.btnViewAsPDF = new System.Windows.Forms.Button();
            this.btnSharpen = new System.Windows.Forms.Button();
            this.btnSave = new System.Windows.Forms.Button();
            this.txtMessage = new System.Windows.Forms.TextBox();
            this.splitContainer1 = new System.Windows.Forms.SplitContainer();
            this.statusStrip1 = new System.Windows.Forms.StatusStrip();
            this.positionToolStripStatusLabel = new System.Windows.Forms.ToolStripStatusLabel();
            this.imageSizeToolStripStatusLabel = new System.Windows.Forms.ToolStripStatusLabel();
            this.zoomToolStripStatusLabel = new System.Windows.Forms.ToolStripStatusLabel();
            this.btnPrintBatchLabel = new System.Windows.Forms.Button();
            this.btnNewBox = new System.Windows.Forms.Button();
            this.panel1 = new System.Windows.Forms.Panel();
            this.btnScanPage = new System.Windows.Forms.Button();
            this.label1 = new System.Windows.Forms.Label();
            this.imageBox = new RegScan.ImageBox();
            this.panel2.SuspendLayout();
            this.pnlNextPreviosImage.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.upSharpen)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer1)).BeginInit();
            this.splitContainer1.Panel1.SuspendLayout();
            this.splitContainer1.Panel2.SuspendLayout();
            this.splitContainer1.SuspendLayout();
            this.statusStrip1.SuspendLayout();
            this.panel1.SuspendLayout();
            this.SuspendLayout();
            // 
            // useDuplexCheckBox
            // 
            this.useDuplexCheckBox.AutoSize = true;
            this.useDuplexCheckBox.Location = new System.Drawing.Point(234, 6);
            this.useDuplexCheckBox.Name = "useDuplexCheckBox";
            this.useDuplexCheckBox.Size = new System.Drawing.Size(105, 17);
            this.useDuplexCheckBox.TabIndex = 34;
            this.useDuplexCheckBox.Text = "Scan Both Sides";
            this.useDuplexCheckBox.UseVisualStyleBackColor = true;
            // 
            // useAdfCheckBox
            // 
            this.useAdfCheckBox.AutoSize = true;
            this.useAdfCheckBox.Location = new System.Drawing.Point(3, 6);
            this.useAdfCheckBox.Name = "useAdfCheckBox";
            this.useAdfCheckBox.Size = new System.Drawing.Size(183, 17);
            this.useAdfCheckBox.TabIndex = 29;
            this.useAdfCheckBox.Text = "Use Automatic Document Feeder";
            this.useAdfCheckBox.UseVisualStyleBackColor = true;
            this.useAdfCheckBox.CheckedChanged += new System.EventHandler(this.useAdfCheckBox_CheckedChanged);
            // 
            // txtOwner
            // 
            this.txtOwner.BackColor = System.Drawing.SystemColors.Info;
            this.txtOwner.Location = new System.Drawing.Point(183, 187);
            this.txtOwner.Name = "txtOwner";
            this.txtOwner.ReadOnly = true;
            this.txtOwner.Size = new System.Drawing.Size(141, 20);
            this.txtOwner.TabIndex = 86;
            // 
            // label11
            // 
            this.label11.AutoSize = true;
            this.label11.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label11.Location = new System.Drawing.Point(9, 187);
            this.label11.Name = "label11";
            this.label11.Size = new System.Drawing.Size(59, 17);
            this.label11.TabIndex = 85;
            this.label11.Text = "Owner:";
            // 
            // txtLegalEntityKey
            // 
            this.txtLegalEntityKey.BackColor = System.Drawing.SystemColors.Info;
            this.txtLegalEntityKey.Location = new System.Drawing.Point(183, 160);
            this.txtLegalEntityKey.Name = "txtLegalEntityKey";
            this.txtLegalEntityKey.ReadOnly = true;
            this.txtLegalEntityKey.Size = new System.Drawing.Size(141, 20);
            this.txtLegalEntityKey.TabIndex = 84;
            // 
            // label10
            // 
            this.label10.AutoSize = true;
            this.label10.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label10.Location = new System.Drawing.Point(9, 160);
            this.label10.Name = "label10";
            this.label10.Size = new System.Drawing.Size(99, 17);
            this.label10.TabIndex = 83;
            this.label10.Text = "Legal Entity:";
            // 
            // txtDocumentId
            // 
            this.txtDocumentId.BackColor = System.Drawing.SystemColors.Info;
            this.txtDocumentId.Location = new System.Drawing.Point(183, 134);
            this.txtDocumentId.Name = "txtDocumentId";
            this.txtDocumentId.ReadOnly = true;
            this.txtDocumentId.Size = new System.Drawing.Size(141, 20);
            this.txtDocumentId.TabIndex = 82;
            this.txtDocumentId.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label2.Location = new System.Drawing.Point(9, 134);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(103, 17);
            this.label2.TabIndex = 81;
            this.label2.Text = "Document Id:";
            // 
            // txtPagesInBox
            // 
            this.txtPagesInBox.BackColor = System.Drawing.SystemColors.Info;
            this.txtPagesInBox.Location = new System.Drawing.Point(183, 348);
            this.txtPagesInBox.Name = "txtPagesInBox";
            this.txtPagesInBox.ReadOnly = true;
            this.txtPagesInBox.Size = new System.Drawing.Size(95, 20);
            this.txtPagesInBox.TabIndex = 80;
            this.txtPagesInBox.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            // 
            // label9
            // 
            this.label9.AutoSize = true;
            this.label9.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label9.Location = new System.Drawing.Point(9, 349);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(107, 17);
            this.label9.TabIndex = 79;
            this.label9.Text = "Pages In Box:";
            // 
            // txtAccessionNumber
            // 
            this.txtAccessionNumber.BackColor = System.Drawing.SystemColors.Info;
            this.txtAccessionNumber.Location = new System.Drawing.Point(183, 293);
            this.txtAccessionNumber.Name = "txtAccessionNumber";
            this.txtAccessionNumber.ReadOnly = true;
            this.txtAccessionNumber.Size = new System.Drawing.Size(95, 20);
            this.txtAccessionNumber.TabIndex = 78;
            this.txtAccessionNumber.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label8.Location = new System.Drawing.Point(9, 293);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(147, 17);
            this.label8.TabIndex = 77;
            this.label8.Text = "Accession Number:";
            // 
            // txtBatchNumber
            // 
            this.txtBatchNumber.BackColor = System.Drawing.SystemColors.Info;
            this.txtBatchNumber.Location = new System.Drawing.Point(183, 374);
            this.txtBatchNumber.Name = "txtBatchNumber";
            this.txtBatchNumber.ReadOnly = true;
            this.txtBatchNumber.Size = new System.Drawing.Size(95, 20);
            this.txtBatchNumber.TabIndex = 76;
            this.txtBatchNumber.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label7.Location = new System.Drawing.Point(9, 378);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(115, 17);
            this.label7.TabIndex = 75;
            this.label7.Text = "Batch Number:";
            // 
            // txtPagesInDocument
            // 
            this.txtPagesInDocument.BackColor = System.Drawing.SystemColors.Info;
            this.txtPagesInDocument.Location = new System.Drawing.Point(183, 322);
            this.txtPagesInDocument.Name = "txtPagesInDocument";
            this.txtPagesInDocument.ReadOnly = true;
            this.txtPagesInDocument.Size = new System.Drawing.Size(95, 20);
            this.txtPagesInDocument.TabIndex = 74;
            this.txtPagesInDocument.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label6.Location = new System.Drawing.Point(9, 322);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(153, 17);
            this.label6.TabIndex = 73;
            this.label6.Text = "Pages In Document:";
            // 
            // txtVersionNumber
            // 
            this.txtVersionNumber.BackColor = System.Drawing.SystemColors.Info;
            this.txtVersionNumber.Location = new System.Drawing.Point(183, 267);
            this.txtVersionNumber.Name = "txtVersionNumber";
            this.txtVersionNumber.ReadOnly = true;
            this.txtVersionNumber.Size = new System.Drawing.Size(95, 20);
            this.txtVersionNumber.TabIndex = 72;
            this.txtVersionNumber.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label5.Location = new System.Drawing.Point(9, 267);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(145, 17);
            this.label5.TabIndex = 71;
            this.label5.Text = "Document Version:";
            // 
            // txtDocumentType
            // 
            this.txtDocumentType.BackColor = System.Drawing.SystemColors.Info;
            this.txtDocumentType.Location = new System.Drawing.Point(183, 241);
            this.txtDocumentType.Name = "txtDocumentType";
            this.txtDocumentType.ReadOnly = true;
            this.txtDocumentType.Size = new System.Drawing.Size(298, 20);
            this.txtDocumentType.TabIndex = 70;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label4.Location = new System.Drawing.Point(9, 241);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(126, 17);
            this.label4.TabIndex = 69;
            this.label4.Text = "Document Type:";
            // 
            // txtDocumentDescription
            // 
            this.txtDocumentDescription.BackColor = System.Drawing.SystemColors.Info;
            this.txtDocumentDescription.Location = new System.Drawing.Point(183, 215);
            this.txtDocumentDescription.Name = "txtDocumentDescription";
            this.txtDocumentDescription.ReadOnly = true;
            this.txtDocumentDescription.Size = new System.Drawing.Size(298, 20);
            this.txtDocumentDescription.TabIndex = 65;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label3.Location = new System.Drawing.Point(9, 215);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(172, 17);
            this.label3.TabIndex = 68;
            this.label3.Text = "Document Description:";
            // 
            // txtBarCode
            // 
            this.txtBarCode.BackColor = System.Drawing.SystemColors.Info;
            this.txtBarCode.Location = new System.Drawing.Point(183, 108);
            this.txtBarCode.Name = "txtBarCode";
            this.txtBarCode.ReadOnly = true;
            this.txtBarCode.Size = new System.Drawing.Size(141, 20);
            this.txtBarCode.TabIndex = 67;
            this.txtBarCode.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            // 
            // showProgressIndicatorUICheckBox
            // 
            this.showProgressIndicatorUICheckBox.AutoSize = true;
            this.showProgressIndicatorUICheckBox.Checked = true;
            this.showProgressIndicatorUICheckBox.CheckState = System.Windows.Forms.CheckState.Checked;
            this.showProgressIndicatorUICheckBox.Location = new System.Drawing.Point(234, 28);
            this.showProgressIndicatorUICheckBox.Name = "showProgressIndicatorUICheckBox";
            this.showProgressIndicatorUICheckBox.Size = new System.Drawing.Size(97, 17);
            this.showProgressIndicatorUICheckBox.TabIndex = 33;
            this.showProgressIndicatorUICheckBox.Text = "Show Progress";
            this.showProgressIndicatorUICheckBox.UseVisualStyleBackColor = true;
            // 
            // useUICheckBox
            // 
            this.useUICheckBox.AutoSize = true;
            this.useUICheckBox.Checked = true;
            this.useUICheckBox.CheckState = System.Windows.Forms.CheckState.Checked;
            this.useUICheckBox.Location = new System.Drawing.Point(3, 28);
            this.useUICheckBox.Name = "useUICheckBox";
            this.useUICheckBox.Size = new System.Drawing.Size(141, 17);
            this.useUICheckBox.TabIndex = 30;
            this.useUICheckBox.Text = "Show Advanced Setting";
            this.useUICheckBox.UseVisualStyleBackColor = true;
            // 
            // ckBoxLowResolution
            // 
            this.ckBoxLowResolution.AutoSize = true;
            this.ckBoxLowResolution.Checked = true;
            this.ckBoxLowResolution.CheckState = System.Windows.Forms.CheckState.Checked;
            this.ckBoxLowResolution.Location = new System.Drawing.Point(3, 49);
            this.ckBoxLowResolution.Name = "ckBoxLowResolution";
            this.ckBoxLowResolution.Size = new System.Drawing.Size(99, 17);
            this.ckBoxLowResolution.TabIndex = 31;
            this.ckBoxLowResolution.Text = "Low Resolution";
            this.ckBoxLowResolution.UseVisualStyleBackColor = true;
            // 
            // panel2
            // 
            this.panel2.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.panel2.Controls.Add(this.label12);
            this.panel2.Controls.Add(this.cBoxPageSize);
            this.panel2.Controls.Add(this.cBoxOrientation);
            this.panel2.Controls.Add(this.heightLabel);
            this.panel2.Controls.Add(this.pnlNextPreviosImage);
            this.panel2.Controls.Add(this.widthLabel);
            this.panel2.Controls.Add(this.progressBar);
            this.panel2.Controls.Add(this.btnCancelScan);
            this.panel2.Controls.Add(this.upSharpen);
            this.panel2.Controls.Add(this.btnViewAsPDF);
            this.panel2.Controls.Add(this.btnSharpen);
            this.panel2.Controls.Add(this.btnSave);
            this.panel2.Controls.Add(this.txtMessage);
            this.panel2.Location = new System.Drawing.Point(-1, 419);
            this.panel2.Name = "panel2";
            this.panel2.Size = new System.Drawing.Size(521, 156);
            this.panel2.TabIndex = 91;
            // 
            // label12
            // 
            this.label12.AutoSize = true;
            this.label12.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label12.Location = new System.Drawing.Point(419, 3);
            this.label12.Name = "label12";
            this.label12.Size = new System.Drawing.Size(80, 13);
            this.label12.TabIndex = 66;
            this.label12.Text = "Page Setting";
            // 
            // cBoxPageSize
            // 
            this.cBoxPageSize.Enabled = false;
            this.cBoxPageSize.FormattingEnabled = true;
            this.cBoxPageSize.Location = new System.Drawing.Point(421, 55);
            this.cBoxPageSize.Name = "cBoxPageSize";
            this.cBoxPageSize.Size = new System.Drawing.Size(75, 21);
            this.cBoxPageSize.TabIndex = 65;
            this.cBoxPageSize.SelectedIndexChanged += new System.EventHandler(this.cBoxPageSize_SelectedIndexChanged);
            // 
            // cBoxOrientation
            // 
            this.cBoxOrientation.Enabled = false;
            this.cBoxOrientation.FormattingEnabled = true;
            this.cBoxOrientation.Location = new System.Drawing.Point(421, 28);
            this.cBoxOrientation.Name = "cBoxOrientation";
            this.cBoxOrientation.Size = new System.Drawing.Size(75, 21);
            this.cBoxOrientation.TabIndex = 64;
            this.cBoxOrientation.SelectedIndexChanged += new System.EventHandler(this.cBoxOrientation_SelectedIndexChanged);
            // 
            // heightLabel
            // 
            this.heightLabel.AutoSize = true;
            this.heightLabel.Location = new System.Drawing.Point(426, 186);
            this.heightLabel.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.heightLabel.Name = "heightLabel";
            this.heightLabel.Size = new System.Drawing.Size(38, 13);
            this.heightLabel.TabIndex = 62;
            this.heightLabel.Text = "Height";
            // 
            // pnlNextPreviosImage
            // 
            this.pnlNextPreviosImage.BackColor = System.Drawing.SystemColors.ActiveCaption;
            this.pnlNextPreviosImage.Controls.Add(this.btnDeleteImage);
            this.pnlNextPreviosImage.Controls.Add(this.lbImageDisplay);
            this.pnlNextPreviosImage.Controls.Add(this.btnPreviousImage);
            this.pnlNextPreviosImage.Controls.Add(this.btnNextImage);
            this.pnlNextPreviosImage.Controls.Add(this.lbPagesScanned);
            this.pnlNextPreviosImage.Controls.Add(this.lbDisplayImage);
            this.pnlNextPreviosImage.Location = new System.Drawing.Point(16, 125);
            this.pnlNextPreviosImage.Name = "pnlNextPreviosImage";
            this.pnlNextPreviosImage.Size = new System.Drawing.Size(492, 26);
            this.pnlNextPreviosImage.TabIndex = 60;
            // 
            // btnDeleteImage
            // 
            this.btnDeleteImage.ForeColor = System.Drawing.Color.Red;
            this.btnDeleteImage.Location = new System.Drawing.Point(425, 2);
            this.btnDeleteImage.Name = "btnDeleteImage";
            this.btnDeleteImage.Size = new System.Drawing.Size(55, 21);
            this.btnDeleteImage.TabIndex = 50;
            this.btnDeleteImage.Text = "Delete";
            this.btnDeleteImage.UseVisualStyleBackColor = true;
            this.btnDeleteImage.Visible = false;
            this.btnDeleteImage.Click += new System.EventHandler(this.btnDeleteImage_Click);
            // 
            // lbImageDisplay
            // 
            this.lbImageDisplay.AutoSize = true;
            this.lbImageDisplay.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lbImageDisplay.Location = new System.Drawing.Point(154, 4);
            this.lbImageDisplay.Name = "lbImageDisplay";
            this.lbImageDisplay.Size = new System.Drawing.Size(88, 17);
            this.lbImageDisplay.TabIndex = 17;
            this.lbImageDisplay.Text = "Displaying:";
            // 
            // btnPreviousImage
            // 
            this.btnPreviousImage.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnPreviousImage.ForeColor = System.Drawing.Color.Blue;
            this.btnPreviousImage.Location = new System.Drawing.Point(244, 4);
            this.btnPreviousImage.Name = "btnPreviousImage";
            this.btnPreviousImage.Size = new System.Drawing.Size(34, 21);
            this.btnPreviousImage.TabIndex = 16;
            this.btnPreviousImage.Text = "<";
            this.btnPreviousImage.UseVisualStyleBackColor = true;
            this.btnPreviousImage.Click += new System.EventHandler(this.btnPreviousImage_Click);
            // 
            // btnNextImage
            // 
            this.btnNextImage.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnNextImage.ForeColor = System.Drawing.Color.Blue;
            this.btnNextImage.Location = new System.Drawing.Point(372, 4);
            this.btnNextImage.Name = "btnNextImage";
            this.btnNextImage.Size = new System.Drawing.Size(34, 21);
            this.btnNextImage.TabIndex = 15;
            this.btnNextImage.Text = ">";
            this.btnNextImage.UseVisualStyleBackColor = true;
            this.btnNextImage.Click += new System.EventHandler(this.btnNextImage_Click);
            // 
            // lbPagesScanned
            // 
            this.lbPagesScanned.AutoSize = true;
            this.lbPagesScanned.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lbPagesScanned.Location = new System.Drawing.Point(3, 4);
            this.lbPagesScanned.Name = "lbPagesScanned";
            this.lbPagesScanned.Size = new System.Drawing.Size(140, 17);
            this.lbPagesScanned.TabIndex = 45;
            this.lbPagesScanned.Text = "Pages Scanned: 0";
            // 
            // lbDisplayImage
            // 
            this.lbDisplayImage.AutoSize = true;
            this.lbDisplayImage.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lbDisplayImage.Location = new System.Drawing.Point(295, 4);
            this.lbDisplayImage.Name = "lbDisplayImage";
            this.lbDisplayImage.Size = new System.Drawing.Size(55, 20);
            this.lbDisplayImage.TabIndex = 14;
            this.lbDisplayImage.Text = "0 of 0";
            // 
            // widthLabel
            // 
            this.widthLabel.AutoSize = true;
            this.widthLabel.Location = new System.Drawing.Point(426, 160);
            this.widthLabel.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.widthLabel.Name = "widthLabel";
            this.widthLabel.Size = new System.Drawing.Size(35, 13);
            this.widthLabel.TabIndex = 61;
            this.widthLabel.Text = "Width";
            // 
            // progressBar
            // 
            this.progressBar.Location = new System.Drawing.Point(16, 55);
            this.progressBar.Name = "progressBar";
            this.progressBar.Size = new System.Drawing.Size(278, 23);
            this.progressBar.TabIndex = 59;
            this.progressBar.Visible = false;
            // 
            // btnCancelScan
            // 
            this.btnCancelScan.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnCancelScan.Location = new System.Drawing.Point(155, 12);
            this.btnCancelScan.Name = "btnCancelScan";
            this.btnCancelScan.Size = new System.Drawing.Size(136, 37);
            this.btnCancelScan.TabIndex = 4;
            this.btnCancelScan.Text = "Reject Scan";
            this.btnCancelScan.UseVisualStyleBackColor = true;
            this.btnCancelScan.Click += new System.EventHandler(this.btnCancelScan_Click);
            // 
            // upSharpen
            // 
            this.upSharpen.DecimalPlaces = 2;
            this.upSharpen.Increment = new decimal(new int[] {
            5,
            0,
            0,
            131072});
            this.upSharpen.Location = new System.Drawing.Point(429, 95);
            this.upSharpen.Maximum = new decimal(new int[] {
            1,
            0,
            0,
            0});
            this.upSharpen.Name = "upSharpen";
            this.upSharpen.Size = new System.Drawing.Size(70, 20);
            this.upSharpen.TabIndex = 57;
            this.upSharpen.Value = new decimal(new int[] {
            5,
            0,
            0,
            131072});
            this.upSharpen.Visible = false;
            // 
            // btnViewAsPDF
            // 
            this.btnViewAsPDF.Enabled = false;
            this.btnViewAsPDF.Location = new System.Drawing.Point(315, 55);
            this.btnViewAsPDF.Name = "btnViewAsPDF";
            this.btnViewAsPDF.Size = new System.Drawing.Size(80, 23);
            this.btnViewAsPDF.TabIndex = 56;
            this.btnViewAsPDF.Text = "View PDF";
            this.btnViewAsPDF.UseVisualStyleBackColor = true;
            this.btnViewAsPDF.Click += new System.EventHandler(this.btnViewAsPDF_Click);
            // 
            // btnSharpen
            // 
            this.btnSharpen.Enabled = false;
            this.btnSharpen.Location = new System.Drawing.Point(315, 28);
            this.btnSharpen.Name = "btnSharpen";
            this.btnSharpen.Size = new System.Drawing.Size(80, 23);
            this.btnSharpen.TabIndex = 55;
            this.btnSharpen.Text = "Rotate";
            this.btnSharpen.UseVisualStyleBackColor = true;
            this.btnSharpen.Click += new System.EventHandler(this.btnRotate_Click);
            // 
            // btnSave
            // 
            this.btnSave.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnSave.ForeColor = System.Drawing.Color.Green;
            this.btnSave.Location = new System.Drawing.Point(13, 12);
            this.btnSave.Name = "btnSave";
            this.btnSave.Size = new System.Drawing.Size(136, 37);
            this.btnSave.TabIndex = 3;
            this.btnSave.Text = "Save Scan";
            this.btnSave.UseVisualStyleBackColor = true;
            this.btnSave.Click += new System.EventHandler(this.btnSave_Click);
            // 
            // txtMessage
            // 
            this.txtMessage.Location = new System.Drawing.Point(16, 84);
            this.txtMessage.Multiline = true;
            this.txtMessage.Name = "txtMessage";
            this.txtMessage.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.txtMessage.Size = new System.Drawing.Size(394, 31);
            this.txtMessage.TabIndex = 63;
            this.txtMessage.Visible = false;
            // 
            // splitContainer1
            // 
            this.splitContainer1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.splitContainer1.FixedPanel = System.Windows.Forms.FixedPanel.Panel1;
            this.splitContainer1.Location = new System.Drawing.Point(0, 0);
            this.splitContainer1.Name = "splitContainer1";
            // 
            // splitContainer1.Panel1
            // 
            this.splitContainer1.Panel1.Controls.Add(this.statusStrip1);
            this.splitContainer1.Panel1.Controls.Add(this.panel2);
            this.splitContainer1.Panel1.Controls.Add(this.btnPrintBatchLabel);
            this.splitContainer1.Panel1.Controls.Add(this.btnNewBox);
            this.splitContainer1.Panel1.Controls.Add(this.panel1);
            this.splitContainer1.Panel1.Controls.Add(this.txtOwner);
            this.splitContainer1.Panel1.Controls.Add(this.label11);
            this.splitContainer1.Panel1.Controls.Add(this.txtLegalEntityKey);
            this.splitContainer1.Panel1.Controls.Add(this.label10);
            this.splitContainer1.Panel1.Controls.Add(this.txtDocumentId);
            this.splitContainer1.Panel1.Controls.Add(this.label2);
            this.splitContainer1.Panel1.Controls.Add(this.txtPagesInBox);
            this.splitContainer1.Panel1.Controls.Add(this.label9);
            this.splitContainer1.Panel1.Controls.Add(this.txtAccessionNumber);
            this.splitContainer1.Panel1.Controls.Add(this.label8);
            this.splitContainer1.Panel1.Controls.Add(this.txtBatchNumber);
            this.splitContainer1.Panel1.Controls.Add(this.label7);
            this.splitContainer1.Panel1.Controls.Add(this.txtPagesInDocument);
            this.splitContainer1.Panel1.Controls.Add(this.label6);
            this.splitContainer1.Panel1.Controls.Add(this.txtVersionNumber);
            this.splitContainer1.Panel1.Controls.Add(this.label5);
            this.splitContainer1.Panel1.Controls.Add(this.txtDocumentType);
            this.splitContainer1.Panel1.Controls.Add(this.label4);
            this.splitContainer1.Panel1.Controls.Add(this.txtDocumentDescription);
            this.splitContainer1.Panel1.Controls.Add(this.label3);
            this.splitContainer1.Panel1.Controls.Add(this.txtBarCode);
            this.splitContainer1.Panel1.Controls.Add(this.label1);
            // 
            // splitContainer1.Panel2
            // 
            this.splitContainer1.Panel2.Controls.Add(this.imageBox);
            this.splitContainer1.Size = new System.Drawing.Size(1034, 602);
            this.splitContainer1.SplitterDistance = 514;
            this.splitContainer1.TabIndex = 67;
            // 
            // statusStrip1
            // 
            this.statusStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.positionToolStripStatusLabel,
            this.imageSizeToolStripStatusLabel,
            this.zoomToolStripStatusLabel});
            this.statusStrip1.Location = new System.Drawing.Point(0, 580);
            this.statusStrip1.Name = "statusStrip1";
            this.statusStrip1.Size = new System.Drawing.Size(514, 22);
            this.statusStrip1.TabIndex = 92;
            // 
            // positionToolStripStatusLabel
            // 
            this.positionToolStripStatusLabel.BorderSides = ((System.Windows.Forms.ToolStripStatusLabelBorderSides)((((System.Windows.Forms.ToolStripStatusLabelBorderSides.Left | System.Windows.Forms.ToolStripStatusLabelBorderSides.Top) 
            | System.Windows.Forms.ToolStripStatusLabelBorderSides.Right) 
            | System.Windows.Forms.ToolStripStatusLabelBorderSides.Bottom)));
            this.positionToolStripStatusLabel.BorderStyle = System.Windows.Forms.Border3DStyle.SunkenInner;
            this.positionToolStripStatusLabel.Name = "positionToolStripStatusLabel";
            this.positionToolStripStatusLabel.Size = new System.Drawing.Size(4, 17);
            // 
            // imageSizeToolStripStatusLabel
            // 
            this.imageSizeToolStripStatusLabel.BorderSides = ((System.Windows.Forms.ToolStripStatusLabelBorderSides)((((System.Windows.Forms.ToolStripStatusLabelBorderSides.Left | System.Windows.Forms.ToolStripStatusLabelBorderSides.Top) 
            | System.Windows.Forms.ToolStripStatusLabelBorderSides.Right) 
            | System.Windows.Forms.ToolStripStatusLabelBorderSides.Bottom)));
            this.imageSizeToolStripStatusLabel.BorderStyle = System.Windows.Forms.Border3DStyle.SunkenInner;
            this.imageSizeToolStripStatusLabel.Name = "imageSizeToolStripStatusLabel";
            this.imageSizeToolStripStatusLabel.Size = new System.Drawing.Size(4, 17);
            // 
            // zoomToolStripStatusLabel
            // 
            this.zoomToolStripStatusLabel.BorderSides = ((System.Windows.Forms.ToolStripStatusLabelBorderSides)((((System.Windows.Forms.ToolStripStatusLabelBorderSides.Left | System.Windows.Forms.ToolStripStatusLabelBorderSides.Top) 
            | System.Windows.Forms.ToolStripStatusLabelBorderSides.Right) 
            | System.Windows.Forms.ToolStripStatusLabelBorderSides.Bottom)));
            this.zoomToolStripStatusLabel.BorderStyle = System.Windows.Forms.Border3DStyle.SunkenInner;
            this.zoomToolStripStatusLabel.Name = "zoomToolStripStatusLabel";
            this.zoomToolStripStatusLabel.Size = new System.Drawing.Size(4, 17);
            // 
            // btnPrintBatchLabel
            // 
            this.btnPrintBatchLabel.Enabled = false;
            this.btnPrintBatchLabel.Font = new System.Drawing.Font("Microsoft Sans Serif", 8F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnPrintBatchLabel.ForeColor = System.Drawing.Color.Blue;
            this.btnPrintBatchLabel.Location = new System.Drawing.Point(284, 370);
            this.btnPrintBatchLabel.Name = "btnPrintBatchLabel";
            this.btnPrintBatchLabel.Size = new System.Drawing.Size(144, 25);
            this.btnPrintBatchLabel.TabIndex = 90;
            this.btnPrintBatchLabel.Text = "Print/Select Batch ";
            this.btnPrintBatchLabel.UseVisualStyleBackColor = true;
            this.btnPrintBatchLabel.Click += new System.EventHandler(this.btnPrintBatchLabel_Click);
            // 
            // btnNewBox
            // 
            this.btnNewBox.Enabled = false;
            this.btnNewBox.Font = new System.Drawing.Font("Microsoft Sans Serif", 8F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnNewBox.ForeColor = System.Drawing.Color.Blue;
            this.btnNewBox.Location = new System.Drawing.Point(284, 344);
            this.btnNewBox.Name = "btnNewBox";
            this.btnNewBox.Size = new System.Drawing.Size(144, 24);
            this.btnNewBox.TabIndex = 89;
            this.btnNewBox.Text = "Create/Change Box";
            this.btnNewBox.UseVisualStyleBackColor = true;
            this.btnNewBox.Click += new System.EventHandler(this.btnNewBox_Click);
            // 
            // panel1
            // 
            this.panel1.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.panel1.Controls.Add(this.useDuplexCheckBox);
            this.panel1.Controls.Add(this.useAdfCheckBox);
            this.panel1.Controls.Add(this.showProgressIndicatorUICheckBox);
            this.panel1.Controls.Add(this.useUICheckBox);
            this.panel1.Controls.Add(this.ckBoxLowResolution);
            this.panel1.Controls.Add(this.btnScanPage);
            this.panel1.Location = new System.Drawing.Point(12, 12);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(422, 82);
            this.panel1.TabIndex = 88;
            // 
            // btnScanPage
            // 
            this.btnScanPage.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnScanPage.ForeColor = System.Drawing.Color.Blue;
            this.btnScanPage.Location = new System.Drawing.Point(234, 49);
            this.btnScanPage.Name = "btnScanPage";
            this.btnScanPage.Size = new System.Drawing.Size(175, 26);
            this.btnScanPage.TabIndex = 1;
            this.btnScanPage.Text = "Scan";
            this.btnScanPage.UseVisualStyleBackColor = true;
            this.btnScanPage.Click += new System.EventHandler(this.btnScanPage_Click);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.Location = new System.Drawing.Point(9, 108);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(73, 17);
            this.label1.TabIndex = 66;
            this.label1.Text = "Barcode:";
            // 
            // imageBox
            // 
            this.imageBox.AutoScroll = true;
            this.imageBox.AutoSize = false;
            this.imageBox.Dock = System.Windows.Forms.DockStyle.Fill;
            this.imageBox.Location = new System.Drawing.Point(0, 0);
            this.imageBox.Name = "imageBox";
            this.imageBox.Size = new System.Drawing.Size(516, 602);
            this.imageBox.TabIndex = 0;
            this.imageBox.ZoomChanged += new System.EventHandler(this.imageBox_ZoomChanged);
            this.imageBox.Scroll += new System.Windows.Forms.ScrollEventHandler(this.imageBox_Scroll);
            this.imageBox.Resize += new System.EventHandler(this.imageBox_Resize);
            // 
            // frmScannerDocument
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1034, 602);
            this.ControlBox = false;
            this.Controls.Add(this.splitContainer1);
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "frmScannerDocument";
            this.Text = "Document Scanner";
            this.Activated += new System.EventHandler(this.frmScanDocument_Activated);
            this.panel2.ResumeLayout(false);
            this.panel2.PerformLayout();
            this.pnlNextPreviosImage.ResumeLayout(false);
            this.pnlNextPreviosImage.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.upSharpen)).EndInit();
            this.splitContainer1.Panel1.ResumeLayout(false);
            this.splitContainer1.Panel1.PerformLayout();
            this.splitContainer1.Panel2.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer1)).EndInit();
            this.splitContainer1.ResumeLayout(false);
            this.statusStrip1.ResumeLayout(false);
            this.statusStrip1.PerformLayout();
            this.panel1.ResumeLayout(false);
            this.panel1.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.CheckBox useDuplexCheckBox;
        private System.Windows.Forms.CheckBox useAdfCheckBox;
        private System.Windows.Forms.TextBox txtOwner;
        private System.Windows.Forms.Label label11;
        private System.Windows.Forms.TextBox txtLegalEntityKey;
        private System.Windows.Forms.Label label10;
        private System.Windows.Forms.TextBox txtDocumentId;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox txtPagesInBox;
        private System.Windows.Forms.Label label9;
        private System.Windows.Forms.TextBox txtAccessionNumber;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.TextBox txtBatchNumber;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.TextBox txtPagesInDocument;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.TextBox txtVersionNumber;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.TextBox txtDocumentType;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.TextBox txtDocumentDescription;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox txtBarCode;
        private System.Windows.Forms.CheckBox showProgressIndicatorUICheckBox;
        private ImageBox imageBox;
        private System.Windows.Forms.CheckBox useUICheckBox;
        private System.Windows.Forms.CheckBox ckBoxLowResolution;
        private System.Windows.Forms.Panel panel2;
        private System.Windows.Forms.TextBox txtMessage;
        private System.Windows.Forms.Label heightLabel;
        private System.Windows.Forms.Panel pnlNextPreviosImage;
        private System.Windows.Forms.Button btnDeleteImage;
        private System.Windows.Forms.Label lbImageDisplay;
        private System.Windows.Forms.Button btnPreviousImage;
        private System.Windows.Forms.Button btnNextImage;
        private System.Windows.Forms.Label lbPagesScanned;
        private System.Windows.Forms.Label lbDisplayImage;
        private System.Windows.Forms.Label widthLabel;
        private System.Windows.Forms.ProgressBar progressBar;
        private System.Windows.Forms.Button btnCancelScan;
        private System.Windows.Forms.NumericUpDown upSharpen;
        private System.Windows.Forms.Button btnViewAsPDF;
        private System.Windows.Forms.Button btnSharpen;
        private System.Windows.Forms.Button btnSave;
        private System.Windows.Forms.SplitContainer splitContainer1;
        private System.Windows.Forms.Button btnPrintBatchLabel;
        private System.Windows.Forms.Button btnNewBox;
        private System.Windows.Forms.Panel panel1;
        private System.Windows.Forms.Button btnScanPage;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.StatusStrip statusStrip1;
        private System.Windows.Forms.ToolStripStatusLabel positionToolStripStatusLabel;
        private System.Windows.Forms.ToolStripStatusLabel imageSizeToolStripStatusLabel;
        private System.Windows.Forms.ToolStripStatusLabel zoomToolStripStatusLabel;
        private System.Windows.Forms.ComboBox cBoxOrientation;
        private System.Windows.Forms.ComboBox cBoxPageSize;
        private System.Windows.Forms.Label label12;
    }
}