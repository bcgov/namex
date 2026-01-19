namespace RegScan
{
    partial class frmFind
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
            this.txtBarCodeToFind = new System.Windows.Forms.TextBox();
            this.btnFind = new System.Windows.Forms.Button();
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
            this.label1 = new System.Windows.Forms.Label();
            this.label12 = new System.Windows.Forms.Label();
            this.pbMainImageViewer = new System.Windows.Forms.PictureBox();
            this.pnlNextPreviosImage = new System.Windows.Forms.Panel();
            this.btnPreviousImage = new System.Windows.Forms.Button();
            this.lbImageDisplay = new System.Windows.Forms.Label();
            this.lbDisplayImage = new System.Windows.Forms.Label();
            this.btnNextImage = new System.Windows.Forms.Button();
            this.pnlVersionDisplay = new System.Windows.Forms.Panel();
            this.label13 = new System.Windows.Forms.Label();
            this.btnPrevious = new System.Windows.Forms.Button();
            this.btnNext = new System.Windows.Forms.Button();
            this.lbDisplayVersion = new System.Windows.Forms.Label();
            this.btnClose = new System.Windows.Forms.Button();
            this.btnViewAsPDF = new System.Windows.Forms.Button();
            this.panel1 = new System.Windows.Forms.Panel();
            this.panel2 = new System.Windows.Forms.Panel();
            ((System.ComponentModel.ISupportInitialize)(this.pbMainImageViewer)).BeginInit();
            this.pnlNextPreviosImage.SuspendLayout();
            this.pnlVersionDisplay.SuspendLayout();
            this.panel1.SuspendLayout();
            this.panel2.SuspendLayout();
            this.SuspendLayout();
            // 
            // txtBarCodeToFind
            // 
            this.txtBarCodeToFind.Location = new System.Drawing.Point(181, 10);
            this.txtBarCodeToFind.Name = "txtBarCodeToFind";
            this.txtBarCodeToFind.Size = new System.Drawing.Size(65, 20);
            this.txtBarCodeToFind.TabIndex = 1;
            // 
            // btnFind
            // 
            this.btnFind.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnFind.ForeColor = System.Drawing.Color.Blue;
            this.btnFind.Location = new System.Drawing.Point(252, 5);
            this.btnFind.Name = "btnFind";
            this.btnFind.Size = new System.Drawing.Size(70, 28);
            this.btnFind.TabIndex = 2;
            this.btnFind.Text = "Find...";
            this.btnFind.UseVisualStyleBackColor = true;
            this.btnFind.Click += new System.EventHandler(this.btnFind_Click);
            // 
            // txtOwner
            // 
            this.txtOwner.BackColor = System.Drawing.SystemColors.Info;
            this.txtOwner.Location = new System.Drawing.Point(182, 138);
            this.txtOwner.Name = "txtOwner";
            this.txtOwner.ReadOnly = true;
            this.txtOwner.Size = new System.Drawing.Size(141, 20);
            this.txtOwner.TabIndex = 47;
            this.txtOwner.TabStop = false;
            // 
            // label11
            // 
            this.label11.AutoSize = true;
            this.label11.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label11.Location = new System.Drawing.Point(8, 138);
            this.label11.Name = "label11";
            this.label11.Size = new System.Drawing.Size(59, 17);
            this.label11.TabIndex = 46;
            this.label11.Text = "Owner:";
            // 
            // txtLegalEntityKey
            // 
            this.txtLegalEntityKey.BackColor = System.Drawing.SystemColors.Info;
            this.txtLegalEntityKey.Location = new System.Drawing.Point(182, 111);
            this.txtLegalEntityKey.Name = "txtLegalEntityKey";
            this.txtLegalEntityKey.ReadOnly = true;
            this.txtLegalEntityKey.Size = new System.Drawing.Size(141, 20);
            this.txtLegalEntityKey.TabIndex = 45;
            this.txtLegalEntityKey.TabStop = false;
            // 
            // label10
            // 
            this.label10.AutoSize = true;
            this.label10.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label10.Location = new System.Drawing.Point(8, 111);
            this.label10.Name = "label10";
            this.label10.Size = new System.Drawing.Size(99, 17);
            this.label10.TabIndex = 44;
            this.label10.Text = "Legal Entity:";
            // 
            // txtDocumentId
            // 
            this.txtDocumentId.BackColor = System.Drawing.SystemColors.Info;
            this.txtDocumentId.Location = new System.Drawing.Point(182, 85);
            this.txtDocumentId.Name = "txtDocumentId";
            this.txtDocumentId.ReadOnly = true;
            this.txtDocumentId.Size = new System.Drawing.Size(141, 20);
            this.txtDocumentId.TabIndex = 43;
            this.txtDocumentId.TabStop = false;
            this.txtDocumentId.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label2.Location = new System.Drawing.Point(8, 85);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(103, 17);
            this.label2.TabIndex = 42;
            this.label2.Text = "Document Id:";
            // 
            // txtPagesInBox
            // 
            this.txtPagesInBox.BackColor = System.Drawing.SystemColors.Info;
            this.txtPagesInBox.Location = new System.Drawing.Point(182, 299);
            this.txtPagesInBox.Name = "txtPagesInBox";
            this.txtPagesInBox.ReadOnly = true;
            this.txtPagesInBox.Size = new System.Drawing.Size(95, 20);
            this.txtPagesInBox.TabIndex = 41;
            this.txtPagesInBox.TabStop = false;
            this.txtPagesInBox.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            // 
            // label9
            // 
            this.label9.AutoSize = true;
            this.label9.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label9.Location = new System.Drawing.Point(8, 300);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(107, 17);
            this.label9.TabIndex = 40;
            this.label9.Text = "Pages In Box:";
            // 
            // txtAccessionNumber
            // 
            this.txtAccessionNumber.BackColor = System.Drawing.SystemColors.Info;
            this.txtAccessionNumber.Location = new System.Drawing.Point(182, 244);
            this.txtAccessionNumber.Name = "txtAccessionNumber";
            this.txtAccessionNumber.ReadOnly = true;
            this.txtAccessionNumber.Size = new System.Drawing.Size(95, 20);
            this.txtAccessionNumber.TabIndex = 39;
            this.txtAccessionNumber.TabStop = false;
            this.txtAccessionNumber.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label8.Location = new System.Drawing.Point(8, 244);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(147, 17);
            this.label8.TabIndex = 38;
            this.label8.Text = "Accession Number:";
            // 
            // txtBatchNumber
            // 
            this.txtBatchNumber.BackColor = System.Drawing.SystemColors.Info;
            this.txtBatchNumber.Location = new System.Drawing.Point(182, 325);
            this.txtBatchNumber.Name = "txtBatchNumber";
            this.txtBatchNumber.ReadOnly = true;
            this.txtBatchNumber.Size = new System.Drawing.Size(95, 20);
            this.txtBatchNumber.TabIndex = 37;
            this.txtBatchNumber.TabStop = false;
            this.txtBatchNumber.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label7.Location = new System.Drawing.Point(8, 329);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(115, 17);
            this.label7.TabIndex = 36;
            this.label7.Text = "Batch Number:";
            // 
            // txtPagesInDocument
            // 
            this.txtPagesInDocument.BackColor = System.Drawing.SystemColors.Info;
            this.txtPagesInDocument.Location = new System.Drawing.Point(182, 273);
            this.txtPagesInDocument.Name = "txtPagesInDocument";
            this.txtPagesInDocument.ReadOnly = true;
            this.txtPagesInDocument.Size = new System.Drawing.Size(95, 20);
            this.txtPagesInDocument.TabIndex = 35;
            this.txtPagesInDocument.TabStop = false;
            this.txtPagesInDocument.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label6.Location = new System.Drawing.Point(8, 273);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(153, 17);
            this.label6.TabIndex = 34;
            this.label6.Text = "Pages In Document:";
            // 
            // txtVersionNumber
            // 
            this.txtVersionNumber.BackColor = System.Drawing.SystemColors.Info;
            this.txtVersionNumber.Location = new System.Drawing.Point(182, 218);
            this.txtVersionNumber.Name = "txtVersionNumber";
            this.txtVersionNumber.ReadOnly = true;
            this.txtVersionNumber.Size = new System.Drawing.Size(95, 20);
            this.txtVersionNumber.TabIndex = 33;
            this.txtVersionNumber.TabStop = false;
            this.txtVersionNumber.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label5.Location = new System.Drawing.Point(8, 218);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(145, 17);
            this.label5.TabIndex = 32;
            this.label5.Text = "Document Version:";
            // 
            // txtDocumentType
            // 
            this.txtDocumentType.BackColor = System.Drawing.SystemColors.Info;
            this.txtDocumentType.Location = new System.Drawing.Point(182, 192);
            this.txtDocumentType.Name = "txtDocumentType";
            this.txtDocumentType.ReadOnly = true;
            this.txtDocumentType.Size = new System.Drawing.Size(298, 20);
            this.txtDocumentType.TabIndex = 31;
            this.txtDocumentType.TabStop = false;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label4.Location = new System.Drawing.Point(8, 192);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(126, 17);
            this.label4.TabIndex = 30;
            this.label4.Text = "Document Type:";
            // 
            // txtDocumentDescription
            // 
            this.txtDocumentDescription.BackColor = System.Drawing.SystemColors.Info;
            this.txtDocumentDescription.Location = new System.Drawing.Point(182, 166);
            this.txtDocumentDescription.Name = "txtDocumentDescription";
            this.txtDocumentDescription.ReadOnly = true;
            this.txtDocumentDescription.Size = new System.Drawing.Size(298, 20);
            this.txtDocumentDescription.TabIndex = 29;
            this.txtDocumentDescription.TabStop = false;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label3.Location = new System.Drawing.Point(8, 166);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(172, 17);
            this.label3.TabIndex = 28;
            this.label3.Text = "Document Description:";
            // 
            // txtBarCode
            // 
            this.txtBarCode.BackColor = System.Drawing.SystemColors.Info;
            this.txtBarCode.Location = new System.Drawing.Point(182, 59);
            this.txtBarCode.Name = "txtBarCode";
            this.txtBarCode.ReadOnly = true;
            this.txtBarCode.Size = new System.Drawing.Size(141, 20);
            this.txtBarCode.TabIndex = 2;
            this.txtBarCode.TabStop = false;
            this.txtBarCode.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.Location = new System.Drawing.Point(8, 59);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(73, 17);
            this.label1.TabIndex = 26;
            this.label1.Text = "Barcode:";
            // 
            // label12
            // 
            this.label12.AutoSize = true;
            this.label12.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label12.Location = new System.Drawing.Point(11, 15);
            this.label12.Name = "label12";
            this.label12.Size = new System.Drawing.Size(145, 17);
            this.label12.TabIndex = 48;
            this.label12.Text = "Enter the Barcode:";
            // 
            // pbMainImageViewer
            // 
            this.pbMainImageViewer.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.pbMainImageViewer.Location = new System.Drawing.Point(534, 3);
            this.pbMainImageViewer.Name = "pbMainImageViewer";
            this.pbMainImageViewer.Size = new System.Drawing.Size(492, 565);
            this.pbMainImageViewer.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pbMainImageViewer.TabIndex = 50;
            this.pbMainImageViewer.TabStop = false;
            // 
            // pnlNextPreviosImage
            // 
            this.pnlNextPreviosImage.BackColor = System.Drawing.SystemColors.ActiveCaption;
            this.pnlNextPreviosImage.Controls.Add(this.btnPreviousImage);
            this.pnlNextPreviosImage.Controls.Add(this.lbImageDisplay);
            this.pnlNextPreviosImage.Controls.Add(this.lbDisplayImage);
            this.pnlNextPreviosImage.Controls.Add(this.btnNextImage);
            this.pnlNextPreviosImage.Location = new System.Drawing.Point(534, 574);
            this.pnlNextPreviosImage.Name = "pnlNextPreviosImage";
            this.pnlNextPreviosImage.Size = new System.Drawing.Size(492, 26);
            this.pnlNextPreviosImage.TabIndex = 51;
            // 
            // btnPreviousImage
            // 
            this.btnPreviousImage.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnPreviousImage.ForeColor = System.Drawing.Color.Blue;
            this.btnPreviousImage.Location = new System.Drawing.Point(156, 3);
            this.btnPreviousImage.Name = "btnPreviousImage";
            this.btnPreviousImage.Size = new System.Drawing.Size(34, 21);
            this.btnPreviousImage.TabIndex = 16;
            this.btnPreviousImage.Text = "<";
            this.btnPreviousImage.UseVisualStyleBackColor = true;
            this.btnPreviousImage.Click += new System.EventHandler(this.btnPreviousImage_Click);
            // 
            // lbImageDisplay
            // 
            this.lbImageDisplay.AutoSize = true;
            this.lbImageDisplay.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lbImageDisplay.Location = new System.Drawing.Point(11, 2);
            this.lbImageDisplay.Name = "lbImageDisplay";
            this.lbImageDisplay.Size = new System.Drawing.Size(130, 17);
            this.lbImageDisplay.TabIndex = 17;
            this.lbImageDisplay.Text = "Displaying Page:";
            // 
            // lbDisplayImage
            // 
            this.lbDisplayImage.AutoSize = true;
            this.lbDisplayImage.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lbDisplayImage.Location = new System.Drawing.Point(196, 2);
            this.lbDisplayImage.Name = "lbDisplayImage";
            this.lbDisplayImage.Size = new System.Drawing.Size(55, 20);
            this.lbDisplayImage.TabIndex = 14;
            this.lbDisplayImage.Text = "0 of 0";
            // 
            // btnNextImage
            // 
            this.btnNextImage.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnNextImage.ForeColor = System.Drawing.Color.Blue;
            this.btnNextImage.Location = new System.Drawing.Point(257, 3);
            this.btnNextImage.Name = "btnNextImage";
            this.btnNextImage.Size = new System.Drawing.Size(34, 21);
            this.btnNextImage.TabIndex = 15;
            this.btnNextImage.Text = ">";
            this.btnNextImage.UseVisualStyleBackColor = true;
            this.btnNextImage.Click += new System.EventHandler(this.btnNextImage_Click);
            // 
            // pnlVersionDisplay
            // 
            this.pnlVersionDisplay.BackColor = System.Drawing.SystemColors.ActiveCaption;
            this.pnlVersionDisplay.Controls.Add(this.label13);
            this.pnlVersionDisplay.Controls.Add(this.btnPrevious);
            this.pnlVersionDisplay.Controls.Add(this.btnNext);
            this.pnlVersionDisplay.Controls.Add(this.lbDisplayVersion);
            this.pnlVersionDisplay.Location = new System.Drawing.Point(12, 20);
            this.pnlVersionDisplay.Name = "pnlVersionDisplay";
            this.pnlVersionDisplay.Size = new System.Drawing.Size(401, 34);
            this.pnlVersionDisplay.TabIndex = 52;
            this.pnlVersionDisplay.Visible = false;
            // 
            // label13
            // 
            this.label13.AutoSize = true;
            this.label13.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label13.Location = new System.Drawing.Point(8, 10);
            this.label13.Name = "label13";
            this.label13.Size = new System.Drawing.Size(148, 17);
            this.label13.TabIndex = 42;
            this.label13.Text = "Displaying Version:";
            // 
            // btnPrevious
            // 
            this.btnPrevious.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnPrevious.ForeColor = System.Drawing.Color.Blue;
            this.btnPrevious.Location = new System.Drawing.Point(171, 7);
            this.btnPrevious.Name = "btnPrevious";
            this.btnPrevious.Size = new System.Drawing.Size(34, 23);
            this.btnPrevious.TabIndex = 13;
            this.btnPrevious.Text = "<";
            this.btnPrevious.UseVisualStyleBackColor = true;
            this.btnPrevious.Click += new System.EventHandler(this.btnPrevious_Click);
            // 
            // btnNext
            // 
            this.btnNext.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnNext.ForeColor = System.Drawing.Color.Blue;
            this.btnNext.Location = new System.Drawing.Point(272, 7);
            this.btnNext.Name = "btnNext";
            this.btnNext.Size = new System.Drawing.Size(34, 23);
            this.btnNext.TabIndex = 12;
            this.btnNext.Text = ">";
            this.btnNext.UseVisualStyleBackColor = true;
            this.btnNext.Click += new System.EventHandler(this.btnNext_Click);
            // 
            // lbDisplayVersion
            // 
            this.lbDisplayVersion.AutoSize = true;
            this.lbDisplayVersion.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lbDisplayVersion.Location = new System.Drawing.Point(211, 7);
            this.lbDisplayVersion.Name = "lbDisplayVersion";
            this.lbDisplayVersion.Size = new System.Drawing.Size(55, 20);
            this.lbDisplayVersion.TabIndex = 11;
            this.lbDisplayVersion.Text = "0 of 0";
            // 
            // btnClose
            // 
            this.btnClose.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnClose.ForeColor = System.Drawing.Color.Black;
            this.btnClose.Location = new System.Drawing.Point(12, 576);
            this.btnClose.Name = "btnClose";
            this.btnClose.Size = new System.Drawing.Size(75, 28);
            this.btnClose.TabIndex = 53;
            this.btnClose.Text = "Close";
            this.btnClose.UseVisualStyleBackColor = true;
            this.btnClose.Click += new System.EventHandler(this.btnClose_Click);
            // 
            // btnViewAsPDF
            // 
            this.btnViewAsPDF.Location = new System.Drawing.Point(433, 371);
            this.btnViewAsPDF.Name = "btnViewAsPDF";
            this.btnViewAsPDF.Size = new System.Drawing.Size(80, 23);
            this.btnViewAsPDF.TabIndex = 3;
            this.btnViewAsPDF.Text = "View PDF";
            this.btnViewAsPDF.UseVisualStyleBackColor = true;
            this.btnViewAsPDF.Click += new System.EventHandler(this.btnViewAsPDF_Click);
            // 
            // panel1
            // 
            this.panel1.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.panel1.Controls.Add(this.pnlVersionDisplay);
            this.panel1.Location = new System.Drawing.Point(3, 351);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(525, 79);
            this.panel1.TabIndex = 58;
            // 
            // panel2
            // 
            this.panel2.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.panel2.Controls.Add(this.btnFind);
            this.panel2.Controls.Add(this.txtBarCodeToFind);
            this.panel2.Controls.Add(this.label12);
            this.panel2.Location = new System.Drawing.Point(0, 7);
            this.panel2.Name = "panel2";
            this.panel2.Size = new System.Drawing.Size(528, 46);
            this.panel2.TabIndex = 59;
            // 
            // frmFind
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1035, 608);
            this.Controls.Add(this.btnViewAsPDF);
            this.Controls.Add(this.btnClose);
            this.Controls.Add(this.pnlNextPreviosImage);
            this.Controls.Add(this.pbMainImageViewer);
            this.Controls.Add(this.txtOwner);
            this.Controls.Add(this.label11);
            this.Controls.Add(this.txtLegalEntityKey);
            this.Controls.Add(this.label10);
            this.Controls.Add(this.txtDocumentId);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.txtPagesInBox);
            this.Controls.Add(this.label9);
            this.Controls.Add(this.txtAccessionNumber);
            this.Controls.Add(this.label8);
            this.Controls.Add(this.txtBatchNumber);
            this.Controls.Add(this.label7);
            this.Controls.Add(this.txtPagesInDocument);
            this.Controls.Add(this.label6);
            this.Controls.Add(this.txtVersionNumber);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.txtDocumentType);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.txtDocumentDescription);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.txtBarCode);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.panel1);
            this.Controls.Add(this.panel2);
            this.Name = "frmFind";
            this.Text = "Find Document";
            this.Activated += new System.EventHandler(this.frmFind_Activated);
            this.Load += new System.EventHandler(this.frmFind_Load);
            ((System.ComponentModel.ISupportInitialize)(this.pbMainImageViewer)).EndInit();
            this.pnlNextPreviosImage.ResumeLayout(false);
            this.pnlNextPreviosImage.PerformLayout();
            this.pnlVersionDisplay.ResumeLayout(false);
            this.pnlVersionDisplay.PerformLayout();
            this.panel1.ResumeLayout(false);
            this.panel2.ResumeLayout(false);
            this.panel2.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox txtBarCodeToFind;
        private System.Windows.Forms.Button btnFind;
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
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label12;
        private System.Windows.Forms.PictureBox pbMainImageViewer;
        private System.Windows.Forms.Panel pnlNextPreviosImage;
        private System.Windows.Forms.Button btnPreviousImage;
        private System.Windows.Forms.Label lbImageDisplay;
        private System.Windows.Forms.Label lbDisplayImage;
        private System.Windows.Forms.Button btnNextImage;
        private System.Windows.Forms.Panel pnlVersionDisplay;
        private System.Windows.Forms.Label label13;
        private System.Windows.Forms.Button btnPrevious;
        private System.Windows.Forms.Button btnNext;
        private System.Windows.Forms.Label lbDisplayVersion;
        private System.Windows.Forms.Button btnClose;
        private System.Windows.Forms.Button btnViewAsPDF;
        private System.Windows.Forms.Panel panel1;
        private System.Windows.Forms.Panel panel2;
    }
}