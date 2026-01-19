namespace TwainAdvancedDemo
{
    partial class DevCapsForm
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
            this.supportedCapabilitiesListBox = new System.Windows.Forms.ListBox();
            this.label1 = new System.Windows.Forms.Label();
            this.closeButton = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            this.currentValueTextBox = new System.Windows.Forms.TextBox();
            this.defaultValueTextBox = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.supportedValuesListBox = new System.Windows.Forms.ListBox();
            this.usageModeTextBox = new System.Windows.Forms.TextBox();
            this.label5 = new System.Windows.Forms.Label();
            this.copyToClipboardButton = new System.Windows.Forms.Button();
            this.deviceManufacturerLabel = new System.Windows.Forms.Label();
            this.deviceProductFamilyLabel = new System.Windows.Forms.Label();
            this.deviceProductNameLabel = new System.Windows.Forms.Label();
            this.driverTwainVersionLabel = new System.Windows.Forms.Label();
            this.driverTwain2CompatibleLabel = new System.Windows.Forms.Label();
            this.feederPresentLabel = new System.Windows.Forms.Label();
            this.flatbedPresentLabel = new System.Windows.Forms.Label();
            this.maxValueTextBox = new System.Windows.Forms.TextBox();
            this.label6 = new System.Windows.Forms.Label();
            this.minValueTextBox = new System.Windows.Forms.TextBox();
            this.label7 = new System.Windows.Forms.Label();
            this.containerTypeTextBox = new System.Windows.Forms.TextBox();
            this.label8 = new System.Windows.Forms.Label();
            this.getMethodComboBox = new System.Windows.Forms.ComboBox();
            this.label9 = new System.Windows.Forms.Label();
            this.stepSizeTextBox = new System.Windows.Forms.TextBox();
            this.label10 = new System.Windows.Forms.Label();
            this.valueTypeTextBox = new System.Windows.Forms.TextBox();
            this.label11 = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // supportedCapabilitiesListBox
            // 
            this.supportedCapabilitiesListBox.FormattingEnabled = true;
            this.supportedCapabilitiesListBox.Location = new System.Drawing.Point(12, 124);
            this.supportedCapabilitiesListBox.Name = "supportedCapabilitiesListBox";
            this.supportedCapabilitiesListBox.Size = new System.Drawing.Size(231, 511);
            this.supportedCapabilitiesListBox.TabIndex = 0;
            this.supportedCapabilitiesListBox.SelectedIndexChanged += new System.EventHandler(this.supportedCapabilitiesListBox_SelectedIndexChanged);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(9, 108);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(114, 13);
            this.label1.TabIndex = 1;
            this.label1.Text = "Supported capabilities:";
            // 
            // closeButton
            // 
            this.closeButton.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.closeButton.Location = new System.Drawing.Point(342, 643);
            this.closeButton.Name = "closeButton";
            this.closeButton.Size = new System.Drawing.Size(156, 30);
            this.closeButton.TabIndex = 2;
            this.closeButton.Text = "Close";
            this.closeButton.UseVisualStyleBackColor = true;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(257, 188);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(73, 13);
            this.label2.TabIndex = 3;
            this.label2.Text = "Current value:";
            // 
            // currentValueTextBox
            // 
            this.currentValueTextBox.Location = new System.Drawing.Point(260, 204);
            this.currentValueTextBox.Name = "currentValueTextBox";
            this.currentValueTextBox.ReadOnly = true;
            this.currentValueTextBox.Size = new System.Drawing.Size(401, 20);
            this.currentValueTextBox.TabIndex = 4;
            // 
            // defaultValueTextBox
            // 
            this.defaultValueTextBox.Location = new System.Drawing.Point(260, 285);
            this.defaultValueTextBox.Name = "defaultValueTextBox";
            this.defaultValueTextBox.ReadOnly = true;
            this.defaultValueTextBox.Size = new System.Drawing.Size(172, 20);
            this.defaultValueTextBox.TabIndex = 6;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(257, 269);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(73, 13);
            this.label3.TabIndex = 5;
            this.label3.Text = "Default value:";
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(257, 314);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(93, 13);
            this.label4.TabIndex = 7;
            this.label4.Text = "Supported values:";
            // 
            // supportedValuesListBox
            // 
            this.supportedValuesListBox.Location = new System.Drawing.Point(260, 332);
            this.supportedValuesListBox.Name = "supportedValuesListBox";
            this.supportedValuesListBox.Size = new System.Drawing.Size(401, 303);
            this.supportedValuesListBox.TabIndex = 8;
            // 
            // usageModeTextBox
            // 
            this.usageModeTextBox.Location = new System.Drawing.Point(260, 125);
            this.usageModeTextBox.Name = "usageModeTextBox";
            this.usageModeTextBox.ReadOnly = true;
            this.usageModeTextBox.Size = new System.Drawing.Size(401, 20);
            this.usageModeTextBox.TabIndex = 10;
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(257, 108);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(70, 13);
            this.label5.TabIndex = 9;
            this.label5.Text = "Usage mode:";
            // 
            // copyToClipboardButton
            // 
            this.copyToClipboardButton.Location = new System.Drawing.Point(174, 643);
            this.copyToClipboardButton.Name = "copyToClipboardButton";
            this.copyToClipboardButton.Size = new System.Drawing.Size(156, 30);
            this.copyToClipboardButton.TabIndex = 11;
            this.copyToClipboardButton.Text = "Copy to clipboard";
            this.copyToClipboardButton.UseVisualStyleBackColor = true;
            this.copyToClipboardButton.Click += new System.EventHandler(this.copyToClipboardButton_Click);
            // 
            // deviceManufacturerLabel
            // 
            this.deviceManufacturerLabel.AutoSize = true;
            this.deviceManufacturerLabel.Location = new System.Drawing.Point(9, 9);
            this.deviceManufacturerLabel.Name = "deviceManufacturerLabel";
            this.deviceManufacturerLabel.Size = new System.Drawing.Size(73, 13);
            this.deviceManufacturerLabel.TabIndex = 12;
            this.deviceManufacturerLabel.Text = "Manufacturer:";
            // 
            // deviceProductFamilyLabel
            // 
            this.deviceProductFamilyLabel.AutoSize = true;
            this.deviceProductFamilyLabel.Location = new System.Drawing.Point(9, 27);
            this.deviceProductFamilyLabel.Name = "deviceProductFamilyLabel";
            this.deviceProductFamilyLabel.Size = new System.Drawing.Size(76, 13);
            this.deviceProductFamilyLabel.TabIndex = 13;
            this.deviceProductFamilyLabel.Text = "Product family:";
            // 
            // deviceProductNameLabel
            // 
            this.deviceProductNameLabel.AutoSize = true;
            this.deviceProductNameLabel.Location = new System.Drawing.Point(9, 45);
            this.deviceProductNameLabel.Name = "deviceProductNameLabel";
            this.deviceProductNameLabel.Size = new System.Drawing.Size(76, 13);
            this.deviceProductNameLabel.TabIndex = 14;
            this.deviceProductNameLabel.Text = "Product name:";
            // 
            // driverTwainVersionLabel
            // 
            this.driverTwainVersionLabel.AutoSize = true;
            this.driverTwainVersionLabel.Location = new System.Drawing.Point(9, 63);
            this.driverTwainVersionLabel.Name = "driverTwainVersionLabel";
            this.driverTwainVersionLabel.Size = new System.Drawing.Size(83, 13);
            this.driverTwainVersionLabel.TabIndex = 15;
            this.driverTwainVersionLabel.Text = "TWAIN version:";
            // 
            // driverTwain2CompatibleLabel
            // 
            this.driverTwain2CompatibleLabel.AutoSize = true;
            this.driverTwain2CompatibleLabel.Location = new System.Drawing.Point(254, 63);
            this.driverTwain2CompatibleLabel.Name = "driverTwain2CompatibleLabel";
            this.driverTwain2CompatibleLabel.Size = new System.Drawing.Size(118, 13);
            this.driverTwain2CompatibleLabel.TabIndex = 16;
            this.driverTwain2CompatibleLabel.Text = "TWAIN 2.0 compatible:";
            // 
            // feederPresentLabel
            // 
            this.feederPresentLabel.AutoSize = true;
            this.feederPresentLabel.Location = new System.Drawing.Point(254, 82);
            this.feederPresentLabel.Name = "feederPresentLabel";
            this.feederPresentLabel.Size = new System.Drawing.Size(81, 13);
            this.feederPresentLabel.TabIndex = 18;
            this.feederPresentLabel.Text = "Feeder present:";
            // 
            // flatbedPresentLabel
            // 
            this.flatbedPresentLabel.AutoSize = true;
            this.flatbedPresentLabel.Location = new System.Drawing.Point(9, 82);
            this.flatbedPresentLabel.Name = "flatbedPresentLabel";
            this.flatbedPresentLabel.Size = new System.Drawing.Size(83, 13);
            this.flatbedPresentLabel.TabIndex = 17;
            this.flatbedPresentLabel.Text = "Flatbed present:";
            // 
            // maxValueTextBox
            // 
            this.maxValueTextBox.Location = new System.Drawing.Point(489, 245);
            this.maxValueTextBox.Name = "maxValueTextBox";
            this.maxValueTextBox.ReadOnly = true;
            this.maxValueTextBox.Size = new System.Drawing.Size(172, 20);
            this.maxValueTextBox.TabIndex = 22;
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(486, 229);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(59, 13);
            this.label6.TabIndex = 21;
            this.label6.Text = "Max value:";
            // 
            // minValueTextBox
            // 
            this.minValueTextBox.Location = new System.Drawing.Point(260, 245);
            this.minValueTextBox.Name = "minValueTextBox";
            this.minValueTextBox.ReadOnly = true;
            this.minValueTextBox.Size = new System.Drawing.Size(172, 20);
            this.minValueTextBox.TabIndex = 20;
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Location = new System.Drawing.Point(257, 229);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(56, 13);
            this.label7.TabIndex = 19;
            this.label7.Text = "Min value:";
            // 
            // containerTypeTextBox
            // 
            this.containerTypeTextBox.Location = new System.Drawing.Point(454, 163);
            this.containerTypeTextBox.Name = "containerTypeTextBox";
            this.containerTypeTextBox.ReadOnly = true;
            this.containerTypeTextBox.Size = new System.Drawing.Size(92, 20);
            this.containerTypeTextBox.TabIndex = 24;
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Location = new System.Drawing.Point(451, 147);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(78, 13);
            this.label8.TabIndex = 23;
            this.label8.Text = "Container type:";
            // 
            // getMethodComboBox
            // 
            this.getMethodComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.getMethodComboBox.FormattingEnabled = true;
            this.getMethodComboBox.Location = new System.Drawing.Point(260, 162);
            this.getMethodComboBox.Name = "getMethodComboBox";
            this.getMethodComboBox.Size = new System.Drawing.Size(172, 21);
            this.getMethodComboBox.TabIndex = 25;
            this.getMethodComboBox.SelectedIndexChanged += new System.EventHandler(this.getMethodComboBox_SelectedIndexChanged);
            // 
            // label9
            // 
            this.label9.AutoSize = true;
            this.label9.Location = new System.Drawing.Point(257, 148);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(56, 13);
            this.label9.TabIndex = 26;
            this.label9.Text = "Operation:";
            // 
            // stepSizeTextBox
            // 
            this.stepSizeTextBox.Location = new System.Drawing.Point(489, 285);
            this.stepSizeTextBox.Name = "stepSizeTextBox";
            this.stepSizeTextBox.ReadOnly = true;
            this.stepSizeTextBox.Size = new System.Drawing.Size(172, 20);
            this.stepSizeTextBox.TabIndex = 28;
            // 
            // label10
            // 
            this.label10.AutoSize = true;
            this.label10.Location = new System.Drawing.Point(486, 269);
            this.label10.Name = "label10";
            this.label10.Size = new System.Drawing.Size(53, 13);
            this.label10.TabIndex = 27;
            this.label10.Text = "Step size:";
            // 
            // valueTypeTextBox
            // 
            this.valueTypeTextBox.Location = new System.Drawing.Point(569, 163);
            this.valueTypeTextBox.Name = "valueTypeTextBox";
            this.valueTypeTextBox.ReadOnly = true;
            this.valueTypeTextBox.Size = new System.Drawing.Size(92, 20);
            this.valueTypeTextBox.TabIndex = 30;
            // 
            // label11
            // 
            this.label11.AutoSize = true;
            this.label11.Location = new System.Drawing.Point(566, 147);
            this.label11.Name = "label11";
            this.label11.Size = new System.Drawing.Size(60, 13);
            this.label11.TabIndex = 29;
            this.label11.Text = "Value type:";
            // 
            // DevCapsForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.CancelButton = this.closeButton;
            this.ClientSize = new System.Drawing.Size(673, 681);
            this.Controls.Add(this.valueTypeTextBox);
            this.Controls.Add(this.label11);
            this.Controls.Add(this.stepSizeTextBox);
            this.Controls.Add(this.label10);
            this.Controls.Add(this.label9);
            this.Controls.Add(this.getMethodComboBox);
            this.Controls.Add(this.containerTypeTextBox);
            this.Controls.Add(this.label8);
            this.Controls.Add(this.maxValueTextBox);
            this.Controls.Add(this.label6);
            this.Controls.Add(this.minValueTextBox);
            this.Controls.Add(this.label7);
            this.Controls.Add(this.feederPresentLabel);
            this.Controls.Add(this.flatbedPresentLabel);
            this.Controls.Add(this.driverTwain2CompatibleLabel);
            this.Controls.Add(this.driverTwainVersionLabel);
            this.Controls.Add(this.deviceProductNameLabel);
            this.Controls.Add(this.deviceProductFamilyLabel);
            this.Controls.Add(this.deviceManufacturerLabel);
            this.Controls.Add(this.copyToClipboardButton);
            this.Controls.Add(this.usageModeTextBox);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.supportedValuesListBox);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.defaultValueTextBox);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.currentValueTextBox);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.closeButton);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.supportedCapabilitiesListBox);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "DevCapsForm";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent;
            this.Text = "Device capabilities";
            this.Load += new System.EventHandler(this.DevCapsForm_Load);
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.DevCapsForm_FormClosing);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.ListBox supportedCapabilitiesListBox;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button closeButton;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox currentValueTextBox;
        private System.Windows.Forms.TextBox defaultValueTextBox;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.ListBox supportedValuesListBox;
        private System.Windows.Forms.TextBox usageModeTextBox;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Button copyToClipboardButton;
        private System.Windows.Forms.Label deviceManufacturerLabel;
        private System.Windows.Forms.Label deviceProductFamilyLabel;
        private System.Windows.Forms.Label deviceProductNameLabel;
        private System.Windows.Forms.Label driverTwainVersionLabel;
        private System.Windows.Forms.Label driverTwain2CompatibleLabel;
        private System.Windows.Forms.Label feederPresentLabel;
        private System.Windows.Forms.Label flatbedPresentLabel;
        private System.Windows.Forms.TextBox maxValueTextBox;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.TextBox minValueTextBox;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.TextBox containerTypeTextBox;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.ComboBox getMethodComboBox;
        private System.Windows.Forms.Label label9;
        private System.Windows.Forms.TextBox stepSizeTextBox;
        private System.Windows.Forms.Label label10;
        private System.Windows.Forms.TextBox valueTypeTextBox;
        private System.Windows.Forms.Label label11;
    }
}