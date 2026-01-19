namespace TwainAdvancedDemo
{
	partial class PdfSaveSettingsForm
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
            this.jpegQualityNumericUpDown = new System.Windows.Forms.NumericUpDown();
            this.label1 = new System.Windows.Forms.Label();
            this.okButton = new System.Windows.Forms.Button();
            this.cancelButton = new System.Windows.Forms.Button();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.zipCompressionRadioButton = new System.Windows.Forms.RadioButton();
            this.autoCompressionRadioButton = new System.Windows.Forms.RadioButton();
            this.jpegCompressionRadioButton = new System.Windows.Forms.RadioButton();
            this.lzwCompressionRadioButton = new System.Windows.Forms.RadioButton();
            this.ccittCompressionRadioButton = new System.Windows.Forms.RadioButton();
            this.noneCompressionRadioButton = new System.Windows.Forms.RadioButton();
            this.gbJpegCompression = new System.Windows.Forms.GroupBox();
            this.pdfACompatibleCheckBox = new System.Windows.Forms.CheckBox();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.addToDocumentRadioButton = new System.Windows.Forms.RadioButton();
            this.createNewDocumentRadioButton = new System.Windows.Forms.RadioButton();
            this.pdfTitleTextBox = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.pdfAuthorTextBox = new System.Windows.Forms.TextBox();
            this.label2 = new System.Windows.Forms.Label();
            this.groupBox3 = new System.Windows.Forms.GroupBox();
            this.saveAllImagesRadioButton = new System.Windows.Forms.RadioButton();
            this.saveCurrentImageRadioButton = new System.Windows.Forms.RadioButton();
            ((System.ComponentModel.ISupportInitialize)(this.jpegQualityNumericUpDown)).BeginInit();
            this.groupBox1.SuspendLayout();
            this.gbJpegCompression.SuspendLayout();
            this.groupBox2.SuspendLayout();
            this.groupBox3.SuspendLayout();
            this.SuspendLayout();
            // 
            // jpegQualityNumericUpDown
            // 
            this.jpegQualityNumericUpDown.Location = new System.Drawing.Point(108, 19);
            this.jpegQualityNumericUpDown.Minimum = new decimal(new int[] {
            5,
            0,
            0,
            0});
            this.jpegQualityNumericUpDown.Name = "jpegQualityNumericUpDown";
            this.jpegQualityNumericUpDown.Size = new System.Drawing.Size(89, 20);
            this.jpegQualityNumericUpDown.TabIndex = 1;
            this.jpegQualityNumericUpDown.Value = new decimal(new int[] {
            90,
            0,
            0,
            0});
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(60, 21);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(42, 13);
            this.label1.TabIndex = 2;
            this.label1.Text = "Quality:";
            // 
            // okButton
            // 
            this.okButton.Location = new System.Drawing.Point(57, 346);
            this.okButton.Name = "okButton";
            this.okButton.Size = new System.Drawing.Size(75, 23);
            this.okButton.TabIndex = 3;
            this.okButton.Text = "Ok";
            this.okButton.UseVisualStyleBackColor = true;
            this.okButton.Click += new System.EventHandler(this.okButton_Click);
            // 
            // cancelButton
            // 
            this.cancelButton.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.cancelButton.Location = new System.Drawing.Point(144, 346);
            this.cancelButton.Name = "cancelButton";
            this.cancelButton.Size = new System.Drawing.Size(75, 23);
            this.cancelButton.TabIndex = 4;
            this.cancelButton.Text = "Cancel";
            this.cancelButton.UseVisualStyleBackColor = true;
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.zipCompressionRadioButton);
            this.groupBox1.Controls.Add(this.autoCompressionRadioButton);
            this.groupBox1.Controls.Add(this.jpegCompressionRadioButton);
            this.groupBox1.Controls.Add(this.lzwCompressionRadioButton);
            this.groupBox1.Controls.Add(this.ccittCompressionRadioButton);
            this.groupBox1.Controls.Add(this.noneCompressionRadioButton);
            this.groupBox1.Location = new System.Drawing.Point(10, 202);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(256, 80);
            this.groupBox1.TabIndex = 5;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "Compression";
            // 
            // zipCompressionRadioButton
            // 
            this.zipCompressionRadioButton.AutoSize = true;
            this.zipCompressionRadioButton.Location = new System.Drawing.Point(157, 37);
            this.zipCompressionRadioButton.Name = "zipCompressionRadioButton";
            this.zipCompressionRadioButton.Size = new System.Drawing.Size(42, 17);
            this.zipCompressionRadioButton.TabIndex = 5;
            this.zipCompressionRadioButton.Text = "ZIP";
            this.zipCompressionRadioButton.UseVisualStyleBackColor = true;
            this.zipCompressionRadioButton.CheckedChanged += new System.EventHandler(this.DisableJpegCompressionQuality);
            // 
            // autoCompressionRadioButton
            // 
            this.autoCompressionRadioButton.AutoSize = true;
            this.autoCompressionRadioButton.Checked = true;
            this.autoCompressionRadioButton.Location = new System.Drawing.Point(12, 19);
            this.autoCompressionRadioButton.Name = "autoCompressionRadioButton";
            this.autoCompressionRadioButton.Size = new System.Drawing.Size(47, 17);
            this.autoCompressionRadioButton.TabIndex = 4;
            this.autoCompressionRadioButton.TabStop = true;
            this.autoCompressionRadioButton.Text = "Auto";
            this.autoCompressionRadioButton.UseVisualStyleBackColor = true;
            this.autoCompressionRadioButton.CheckedChanged += new System.EventHandler(this.EnableJpegCompressionQuality);
            // 
            // jpegCompressionRadioButton
            // 
            this.jpegCompressionRadioButton.AutoSize = true;
            this.jpegCompressionRadioButton.Location = new System.Drawing.Point(157, 55);
            this.jpegCompressionRadioButton.Name = "jpegCompressionRadioButton";
            this.jpegCompressionRadioButton.Size = new System.Drawing.Size(52, 17);
            this.jpegCompressionRadioButton.TabIndex = 3;
            this.jpegCompressionRadioButton.Text = "JPEG";
            this.jpegCompressionRadioButton.UseVisualStyleBackColor = true;
            this.jpegCompressionRadioButton.CheckedChanged += new System.EventHandler(this.EnableJpegCompressionQuality);
            // 
            // lzwCompressionRadioButton
            // 
            this.lzwCompressionRadioButton.AutoSize = true;
            this.lzwCompressionRadioButton.Location = new System.Drawing.Point(157, 19);
            this.lzwCompressionRadioButton.Name = "lzwCompressionRadioButton";
            this.lzwCompressionRadioButton.Size = new System.Drawing.Size(49, 17);
            this.lzwCompressionRadioButton.TabIndex = 2;
            this.lzwCompressionRadioButton.Text = "LZW";
            this.lzwCompressionRadioButton.UseVisualStyleBackColor = true;
            this.lzwCompressionRadioButton.CheckedChanged += new System.EventHandler(this.DisableJpegCompressionQuality);
            // 
            // ccittCompressionRadioButton
            // 
            this.ccittCompressionRadioButton.AutoSize = true;
            this.ccittCompressionRadioButton.Location = new System.Drawing.Point(12, 55);
            this.ccittCompressionRadioButton.Name = "ccittCompressionRadioButton";
            this.ccittCompressionRadioButton.Size = new System.Drawing.Size(117, 17);
            this.ccittCompressionRadioButton.TabIndex = 1;
            this.ccittCompressionRadioButton.Text = "CCITT Group 4 Fax";
            this.ccittCompressionRadioButton.UseVisualStyleBackColor = true;
            this.ccittCompressionRadioButton.CheckedChanged += new System.EventHandler(this.DisableJpegCompressionQuality);
            // 
            // noneCompressionRadioButton
            // 
            this.noneCompressionRadioButton.AutoSize = true;
            this.noneCompressionRadioButton.Location = new System.Drawing.Point(12, 37);
            this.noneCompressionRadioButton.Name = "noneCompressionRadioButton";
            this.noneCompressionRadioButton.Size = new System.Drawing.Size(51, 17);
            this.noneCompressionRadioButton.TabIndex = 0;
            this.noneCompressionRadioButton.Text = "None";
            this.noneCompressionRadioButton.UseVisualStyleBackColor = true;
            this.noneCompressionRadioButton.CheckedChanged += new System.EventHandler(this.DisableJpegCompressionQuality);
            // 
            // gbJpegCompression
            // 
            this.gbJpegCompression.Controls.Add(this.jpegQualityNumericUpDown);
            this.gbJpegCompression.Controls.Add(this.label1);
            this.gbJpegCompression.Enabled = false;
            this.gbJpegCompression.Location = new System.Drawing.Point(10, 286);
            this.gbJpegCompression.Name = "gbJpegCompression";
            this.gbJpegCompression.Size = new System.Drawing.Size(256, 51);
            this.gbJpegCompression.TabIndex = 6;
            this.gbJpegCompression.TabStop = false;
            this.gbJpegCompression.Text = "JPEG compression";
            // 
            // pdfACompatibleCheckBox
            // 
            this.pdfACompatibleCheckBox.AutoSize = true;
            this.pdfACompatibleCheckBox.Checked = true;
            this.pdfACompatibleCheckBox.CheckState = System.Windows.Forms.CheckState.Checked;
            this.pdfACompatibleCheckBox.Location = new System.Drawing.Point(12, 56);
            this.pdfACompatibleCheckBox.Name = "pdfACompatibleCheckBox";
            this.pdfACompatibleCheckBox.Size = new System.Drawing.Size(113, 17);
            this.pdfACompatibleCheckBox.TabIndex = 8;
            this.pdfACompatibleCheckBox.Text = "PDF/A compatible";
            this.pdfACompatibleCheckBox.UseVisualStyleBackColor = true;
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.addToDocumentRadioButton);
            this.groupBox2.Controls.Add(this.createNewDocumentRadioButton);
            this.groupBox2.Controls.Add(this.pdfTitleTextBox);
            this.groupBox2.Controls.Add(this.label3);
            this.groupBox2.Controls.Add(this.pdfAuthorTextBox);
            this.groupBox2.Controls.Add(this.label2);
            this.groupBox2.Controls.Add(this.pdfACompatibleCheckBox);
            this.groupBox2.Location = new System.Drawing.Point(10, 65);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(256, 133);
            this.groupBox2.TabIndex = 9;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "Document settings";
            // 
            // addToDocumentRadioButton
            // 
            this.addToDocumentRadioButton.AutoSize = true;
            this.addToDocumentRadioButton.Checked = true;
            this.addToDocumentRadioButton.Location = new System.Drawing.Point(12, 32);
            this.addToDocumentRadioButton.Name = "addToDocumentRadioButton";
            this.addToDocumentRadioButton.Size = new System.Drawing.Size(144, 17);
            this.addToDocumentRadioButton.TabIndex = 15;
            this.addToDocumentRadioButton.TabStop = true;
            this.addToDocumentRadioButton.Text = "Add to existing document";
            this.addToDocumentRadioButton.UseVisualStyleBackColor = true;
            // 
            // createNewDocumentRadioButton
            // 
            this.createNewDocumentRadioButton.AutoSize = true;
            this.createNewDocumentRadioButton.Location = new System.Drawing.Point(12, 15);
            this.createNewDocumentRadioButton.Name = "createNewDocumentRadioButton";
            this.createNewDocumentRadioButton.Size = new System.Drawing.Size(129, 17);
            this.createNewDocumentRadioButton.TabIndex = 14;
            this.createNewDocumentRadioButton.Text = "Create new document";
            this.createNewDocumentRadioButton.UseVisualStyleBackColor = true;
            // 
            // pdfTitleTextBox
            // 
            this.pdfTitleTextBox.Location = new System.Drawing.Point(58, 103);
            this.pdfTitleTextBox.Name = "pdfTitleTextBox";
            this.pdfTitleTextBox.Size = new System.Drawing.Size(185, 20);
            this.pdfTitleTextBox.TabIndex = 13;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(9, 106);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(30, 13);
            this.label3.TabIndex = 12;
            this.label3.Text = "Title:";
            // 
            // pdfAuthorTextBox
            // 
            this.pdfAuthorTextBox.Location = new System.Drawing.Point(58, 77);
            this.pdfAuthorTextBox.Name = "pdfAuthorTextBox";
            this.pdfAuthorTextBox.Size = new System.Drawing.Size(185, 20);
            this.pdfAuthorTextBox.TabIndex = 11;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(9, 80);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(41, 13);
            this.label2.TabIndex = 10;
            this.label2.Text = "Author:";
            // 
            // groupBox3
            // 
            this.groupBox3.Controls.Add(this.saveAllImagesRadioButton);
            this.groupBox3.Controls.Add(this.saveCurrentImageRadioButton);
            this.groupBox3.Location = new System.Drawing.Point(10, 4);
            this.groupBox3.Name = "groupBox3";
            this.groupBox3.Size = new System.Drawing.Size(256, 58);
            this.groupBox3.TabIndex = 12;
            this.groupBox3.TabStop = false;
            this.groupBox3.Text = "Save settings";
            // 
            // saveAllImagesRadioButton
            // 
            this.saveAllImagesRadioButton.AutoSize = true;
            this.saveAllImagesRadioButton.Location = new System.Drawing.Point(15, 35);
            this.saveAllImagesRadioButton.Name = "saveAllImagesRadioButton";
            this.saveAllImagesRadioButton.Size = new System.Drawing.Size(99, 17);
            this.saveAllImagesRadioButton.TabIndex = 1;
            this.saveAllImagesRadioButton.Text = "Save all images";
            this.saveAllImagesRadioButton.UseVisualStyleBackColor = true;
            // 
            // saveCurrentImageRadioButton
            // 
            this.saveCurrentImageRadioButton.AutoSize = true;
            this.saveCurrentImageRadioButton.Checked = true;
            this.saveCurrentImageRadioButton.Location = new System.Drawing.Point(15, 17);
            this.saveCurrentImageRadioButton.Name = "saveCurrentImageRadioButton";
            this.saveCurrentImageRadioButton.Size = new System.Drawing.Size(139, 17);
            this.saveCurrentImageRadioButton.TabIndex = 0;
            this.saveCurrentImageRadioButton.TabStop = true;
            this.saveCurrentImageRadioButton.Text = "Save only current image";
            this.saveCurrentImageRadioButton.UseVisualStyleBackColor = true;
            // 
            // PdfSaveSettingsForm
            // 
            this.AcceptButton = this.okButton;
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.CancelButton = this.cancelButton;
            this.ClientSize = new System.Drawing.Size(276, 375);
            this.Controls.Add(this.groupBox3);
            this.Controls.Add(this.groupBox2);
            this.Controls.Add(this.gbJpegCompression);
            this.Controls.Add(this.groupBox1);
            this.Controls.Add(this.cancelButton);
            this.Controls.Add(this.okButton);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "PdfSaveSettingsForm";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent;
            this.Text = "PDF save settings";
            ((System.ComponentModel.ISupportInitialize)(this.jpegQualityNumericUpDown)).EndInit();
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            this.gbJpegCompression.ResumeLayout(false);
            this.gbJpegCompression.PerformLayout();
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            this.groupBox3.ResumeLayout(false);
            this.groupBox3.PerformLayout();
            this.ResumeLayout(false);

		}

		#endregion

		private System.Windows.Forms.NumericUpDown jpegQualityNumericUpDown;
		private System.Windows.Forms.Label label1;
		private System.Windows.Forms.Button okButton;
		private System.Windows.Forms.Button cancelButton;
		private System.Windows.Forms.GroupBox groupBox1;
		private System.Windows.Forms.RadioButton noneCompressionRadioButton;
		private System.Windows.Forms.RadioButton jpegCompressionRadioButton;
		private System.Windows.Forms.RadioButton lzwCompressionRadioButton;
		private System.Windows.Forms.RadioButton ccittCompressionRadioButton;
		private System.Windows.Forms.GroupBox gbJpegCompression;
		private System.Windows.Forms.RadioButton autoCompressionRadioButton;
		private System.Windows.Forms.RadioButton zipCompressionRadioButton;
		private System.Windows.Forms.CheckBox pdfACompatibleCheckBox;
		private System.Windows.Forms.GroupBox groupBox2;
		private System.Windows.Forms.TextBox pdfAuthorTextBox;
		private System.Windows.Forms.Label label2;
		private System.Windows.Forms.TextBox pdfTitleTextBox;
		private System.Windows.Forms.Label label3;
		private System.Windows.Forms.RadioButton addToDocumentRadioButton;
		private System.Windows.Forms.RadioButton createNewDocumentRadioButton;
        private System.Windows.Forms.GroupBox groupBox3;
        private System.Windows.Forms.RadioButton saveAllImagesRadioButton;
        private System.Windows.Forms.RadioButton saveCurrentImageRadioButton;
	}
}