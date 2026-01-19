namespace TwainFileTransferDemo
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
            this.acquireImageWithUIButton = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            this.directoryForImagesTextBox = new System.Windows.Forms.TextBox();
            this.selectDirectoryForImagesButton = new System.Windows.Forms.Button();
            this.deviceSettingsGroupBox = new System.Windows.Forms.GroupBox();
            this.supportedCompressionsComboBox = new System.Windows.Forms.ComboBox();
            this.label4 = new System.Windows.Forms.Label();
            this.supportedFileFormatsComboBox = new System.Windows.Forms.ComboBox();
            this.label3 = new System.Windows.Forms.Label();
            this.devicesComboBox = new System.Windows.Forms.ComboBox();
            this.label1 = new System.Windows.Forms.Label();
            this.statusTextBox = new System.Windows.Forms.TextBox();
            this.folderBrowserDialog1 = new System.Windows.Forms.FolderBrowserDialog();
            this.acquireImageWithoutUIButton = new System.Windows.Forms.Button();
            this.deviceSettingsGroupBox.SuspendLayout();
            this.SuspendLayout();
            // 
            // acquireImageWithUIButton
            // 
            this.acquireImageWithUIButton.Location = new System.Drawing.Point(194, 143);
            this.acquireImageWithUIButton.Name = "acquireImageWithUIButton";
            this.acquireImageWithUIButton.Size = new System.Drawing.Size(175, 36);
            this.acquireImageWithUIButton.TabIndex = 87;
            this.acquireImageWithUIButton.Text = "Acquire image with UI";
            this.acquireImageWithUIButton.Click += new System.EventHandler(this.acquireImageWithUIButton_Click);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(12, 11);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(103, 13);
            this.label2.TabIndex = 103;
            this.label2.Text = "Directory for images:";
            // 
            // directoryForImagesTextBox
            // 
            this.directoryForImagesTextBox.Location = new System.Drawing.Point(121, 9);
            this.directoryForImagesTextBox.Name = "directoryForImagesTextBox";
            this.directoryForImagesTextBox.ReadOnly = true;
            this.directoryForImagesTextBox.Size = new System.Drawing.Size(584, 20);
            this.directoryForImagesTextBox.TabIndex = 104;
            // 
            // selectDirectoryForImagesButton
            // 
            this.selectDirectoryForImagesButton.Location = new System.Drawing.Point(711, 9);
            this.selectDirectoryForImagesButton.Name = "selectDirectoryForImagesButton";
            this.selectDirectoryForImagesButton.Size = new System.Drawing.Size(26, 23);
            this.selectDirectoryForImagesButton.TabIndex = 105;
            this.selectDirectoryForImagesButton.Text = "...";
            this.selectDirectoryForImagesButton.UseVisualStyleBackColor = true;
            this.selectDirectoryForImagesButton.Click += new System.EventHandler(this.selectDirectoryForImagesButton_Click);
            // 
            // deviceSettingsGroupBox
            // 
            this.deviceSettingsGroupBox.Controls.Add(this.supportedCompressionsComboBox);
            this.deviceSettingsGroupBox.Controls.Add(this.label4);
            this.deviceSettingsGroupBox.Controls.Add(this.supportedFileFormatsComboBox);
            this.deviceSettingsGroupBox.Controls.Add(this.label3);
            this.deviceSettingsGroupBox.Location = new System.Drawing.Point(121, 62);
            this.deviceSettingsGroupBox.Name = "deviceSettingsGroupBox";
            this.deviceSettingsGroupBox.Size = new System.Drawing.Size(616, 71);
            this.deviceSettingsGroupBox.TabIndex = 114;
            this.deviceSettingsGroupBox.TabStop = false;
            this.deviceSettingsGroupBox.Text = "Device settings";
            // 
            // supportedCompressionsComboBox
            // 
            this.supportedCompressionsComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.supportedCompressionsComboBox.FormattingEnabled = true;
            this.supportedCompressionsComboBox.Location = new System.Drawing.Point(149, 41);
            this.supportedCompressionsComboBox.Name = "supportedCompressionsComboBox";
            this.supportedCompressionsComboBox.Size = new System.Drawing.Size(449, 21);
            this.supportedCompressionsComboBox.TabIndex = 22;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(10, 44);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(126, 13);
            this.label4.TabIndex = 21;
            this.label4.Text = "Supported compressions:";
            // 
            // supportedFileFormatsComboBox
            // 
            this.supportedFileFormatsComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.supportedFileFormatsComboBox.FormattingEnabled = true;
            this.supportedFileFormatsComboBox.Location = new System.Drawing.Point(149, 15);
            this.supportedFileFormatsComboBox.Name = "supportedFileFormatsComboBox";
            this.supportedFileFormatsComboBox.Size = new System.Drawing.Size(449, 21);
            this.supportedFileFormatsComboBox.TabIndex = 1;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(10, 18);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(112, 13);
            this.label3.TabIndex = 0;
            this.label3.Text = "Supported file formats:";
            // 
            // devicesComboBox
            // 
            this.devicesComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.devicesComboBox.Location = new System.Drawing.Point(121, 35);
            this.devicesComboBox.Name = "devicesComboBox";
            this.devicesComboBox.Size = new System.Drawing.Size(616, 21);
            this.devicesComboBox.TabIndex = 110;
            this.devicesComboBox.SelectedIndexChanged += new System.EventHandler(this.devicesComboBox_SelectedIndexChanged);
            // 
            // label1
            // 
            this.label1.Location = new System.Drawing.Point(59, 36);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(56, 16);
            this.label1.TabIndex = 112;
            this.label1.Text = "Devices:";
            // 
            // statusTextBox
            // 
            this.statusTextBox.Location = new System.Drawing.Point(12, 185);
            this.statusTextBox.Multiline = true;
            this.statusTextBox.Name = "statusTextBox";
            this.statusTextBox.Size = new System.Drawing.Size(725, 425);
            this.statusTextBox.TabIndex = 117;
            // 
            // acquireImageWithoutUIButton
            // 
            this.acquireImageWithoutUIButton.Location = new System.Drawing.Point(379, 143);
            this.acquireImageWithoutUIButton.Name = "acquireImageWithoutUIButton";
            this.acquireImageWithoutUIButton.Size = new System.Drawing.Size(175, 36);
            this.acquireImageWithoutUIButton.TabIndex = 118;
            this.acquireImageWithoutUIButton.Text = "Acquire image without UI";
            this.acquireImageWithoutUIButton.Click += new System.EventHandler(this.acquireImageWithoutUIButton_Click);
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(748, 622);
            this.Controls.Add(this.acquireImageWithoutUIButton);
            this.Controls.Add(this.statusTextBox);
            this.Controls.Add(this.deviceSettingsGroupBox);
            this.Controls.Add(this.devicesComboBox);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.selectDirectoryForImagesButton);
            this.Controls.Add(this.directoryForImagesTextBox);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.acquireImageWithUIButton);
            this.MaximizeBox = false;
            this.Name = "MainForm";
            this.Text = "VintaSoft TWAIN File Transfer Demo";
            this.Shown += new System.EventHandler(this.MainForm_Shown);
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.MainForm_FormClosing);
            this.deviceSettingsGroupBox.ResumeLayout(false);
            this.deviceSettingsGroupBox.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button acquireImageWithUIButton;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox directoryForImagesTextBox;
        private System.Windows.Forms.Button selectDirectoryForImagesButton;
        private System.Windows.Forms.GroupBox deviceSettingsGroupBox;
        private System.Windows.Forms.ComboBox devicesComboBox;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.ComboBox supportedFileFormatsComboBox;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox statusTextBox;
        private System.Windows.Forms.FolderBrowserDialog folderBrowserDialog1;
        private System.Windows.Forms.ComboBox supportedCompressionsComboBox;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Button acquireImageWithoutUIButton;
    }
}

