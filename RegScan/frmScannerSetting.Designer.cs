namespace RegScan
{
    partial class frmScannerSetting
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
            this.autoRotateCheckBox = new System.Windows.Forms.CheckBox();
            this.autoDetectBorderCheckBox = new System.Windows.Forms.CheckBox();
            this.useDuplexCheckBox = new System.Windows.Forms.CheckBox();
            this.useAdfCheckBox = new System.Windows.Forms.CheckBox();
            this.showProgressIndicatorUICheckBox = new System.Windows.Forms.CheckBox();
            this.useUICheckBox = new System.Windows.Forms.CheckBox();
            this.checkBoxArea = new System.Windows.Forms.CheckBox();
            this.blackAndWhiteCheckBox = new System.Windows.Forms.CheckBox();
            this.btnClose = new System.Windows.Forms.Button();
            this.btnUpdate4 = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // autoRotateCheckBox
            // 
            this.autoRotateCheckBox.AutoSize = true;
            this.autoRotateCheckBox.Location = new System.Drawing.Point(149, 67);
            this.autoRotateCheckBox.Name = "autoRotateCheckBox";
            this.autoRotateCheckBox.Size = new System.Drawing.Size(83, 17);
            this.autoRotateCheckBox.TabIndex = 8;
            this.autoRotateCheckBox.Text = "Auto Rotate";
            this.autoRotateCheckBox.UseVisualStyleBackColor = true;
            this.autoRotateCheckBox.Visible = false;
            // 
            // autoDetectBorderCheckBox
            // 
            this.autoDetectBorderCheckBox.AutoSize = true;
            this.autoDetectBorderCheckBox.Location = new System.Drawing.Point(149, 44);
            this.autoDetectBorderCheckBox.Name = "autoDetectBorderCheckBox";
            this.autoDetectBorderCheckBox.Size = new System.Drawing.Size(117, 17);
            this.autoDetectBorderCheckBox.TabIndex = 7;
            this.autoDetectBorderCheckBox.Text = "Auto Detect Border";
            this.autoDetectBorderCheckBox.UseVisualStyleBackColor = true;
            this.autoDetectBorderCheckBox.Visible = false;
            // 
            // useDuplexCheckBox
            // 
            this.useDuplexCheckBox.AutoSize = true;
            this.useDuplexCheckBox.Location = new System.Drawing.Point(12, 35);
            this.useDuplexCheckBox.Name = "useDuplexCheckBox";
            this.useDuplexCheckBox.Size = new System.Drawing.Size(105, 17);
            this.useDuplexCheckBox.TabIndex = 2;
            this.useDuplexCheckBox.Text = "Scan Both Sides";
            this.useDuplexCheckBox.UseVisualStyleBackColor = true;
            // 
            // useAdfCheckBox
            // 
            this.useAdfCheckBox.AutoSize = true;
            this.useAdfCheckBox.Location = new System.Drawing.Point(12, 12);
            this.useAdfCheckBox.Name = "useAdfCheckBox";
            this.useAdfCheckBox.Size = new System.Drawing.Size(183, 17);
            this.useAdfCheckBox.TabIndex = 1;
            this.useAdfCheckBox.Text = "Use Automatic Document Feeder";
            this.useAdfCheckBox.UseVisualStyleBackColor = true;
            // 
            // showProgressIndicatorUICheckBox
            // 
            this.showProgressIndicatorUICheckBox.AutoSize = true;
            this.showProgressIndicatorUICheckBox.Checked = true;
            this.showProgressIndicatorUICheckBox.CheckState = System.Windows.Forms.CheckState.Checked;
            this.showProgressIndicatorUICheckBox.Location = new System.Drawing.Point(12, 83);
            this.showProgressIndicatorUICheckBox.Name = "showProgressIndicatorUICheckBox";
            this.showProgressIndicatorUICheckBox.Size = new System.Drawing.Size(97, 17);
            this.showProgressIndicatorUICheckBox.TabIndex = 4;
            this.showProgressIndicatorUICheckBox.Text = "Show Progress";
            this.showProgressIndicatorUICheckBox.UseVisualStyleBackColor = true;
            // 
            // useUICheckBox
            // 
            this.useUICheckBox.AutoSize = true;
            this.useUICheckBox.Checked = true;
            this.useUICheckBox.CheckState = System.Windows.Forms.CheckState.Checked;
            this.useUICheckBox.Location = new System.Drawing.Point(12, 60);
            this.useUICheckBox.Name = "useUICheckBox";
            this.useUICheckBox.Size = new System.Drawing.Size(141, 17);
            this.useUICheckBox.TabIndex = 3;
            this.useUICheckBox.Text = "Show Advanced Setting";
            this.useUICheckBox.UseVisualStyleBackColor = true;
            // 
            // checkBoxArea
            // 
            this.checkBoxArea.AutoSize = true;
            this.checkBoxArea.Location = new System.Drawing.Point(149, 21);
            this.checkBoxArea.Name = "checkBoxArea";
            this.checkBoxArea.Size = new System.Drawing.Size(73, 17);
            this.checkBoxArea.TabIndex = 6;
            this.checkBoxArea.Text = "Grab area";
            this.checkBoxArea.UseVisualStyleBackColor = true;
            this.checkBoxArea.Visible = false;
            // 
            // blackAndWhiteCheckBox
            // 
            this.blackAndWhiteCheckBox.AutoSize = true;
            this.blackAndWhiteCheckBox.Checked = true;
            this.blackAndWhiteCheckBox.CheckState = System.Windows.Forms.CheckState.Checked;
            this.blackAndWhiteCheckBox.Location = new System.Drawing.Point(12, 108);
            this.blackAndWhiteCheckBox.Name = "blackAndWhiteCheckBox";
            this.blackAndWhiteCheckBox.Size = new System.Drawing.Size(99, 17);
            this.blackAndWhiteCheckBox.TabIndex = 5;
            this.blackAndWhiteCheckBox.Text = "Low Resolution";
            this.blackAndWhiteCheckBox.UseVisualStyleBackColor = true;
            // 
            // btnClose
            // 
            this.btnClose.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnClose.ForeColor = System.Drawing.Color.Black;
            this.btnClose.Location = new System.Drawing.Point(149, 148);
            this.btnClose.Name = "btnClose";
            this.btnClose.Size = new System.Drawing.Size(98, 28);
            this.btnClose.TabIndex = 10;
            this.btnClose.Text = "Close";
            this.btnClose.UseVisualStyleBackColor = true;
            this.btnClose.Click += new System.EventHandler(this.btnClose_Click);
            // 
            // btnUpdate4
            // 
            this.btnUpdate4.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnUpdate4.ForeColor = System.Drawing.Color.Blue;
            this.btnUpdate4.Location = new System.Drawing.Point(14, 148);
            this.btnUpdate4.Name = "btnUpdate4";
            this.btnUpdate4.Size = new System.Drawing.Size(99, 28);
            this.btnUpdate4.TabIndex = 9;
            this.btnUpdate4.Text = "Update";
            this.btnUpdate4.UseVisualStyleBackColor = true;
            this.btnUpdate4.Click += new System.EventHandler(this.btnUpdate4_Click);
            // 
            // frmScannerSetting
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(273, 198);
            this.Controls.Add(this.btnClose);
            this.Controls.Add(this.btnUpdate4);
            this.Controls.Add(this.autoRotateCheckBox);
            this.Controls.Add(this.autoDetectBorderCheckBox);
            this.Controls.Add(this.useDuplexCheckBox);
            this.Controls.Add(this.useAdfCheckBox);
            this.Controls.Add(this.showProgressIndicatorUICheckBox);
            this.Controls.Add(this.useUICheckBox);
            this.Controls.Add(this.checkBoxArea);
            this.Controls.Add(this.blackAndWhiteCheckBox);
            this.Name = "frmScannerSetting";
            this.Text = "Scanner Default Setting";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.CheckBox autoRotateCheckBox;
        private System.Windows.Forms.CheckBox autoDetectBorderCheckBox;
        private System.Windows.Forms.CheckBox useDuplexCheckBox;
        private System.Windows.Forms.CheckBox useAdfCheckBox;
        private System.Windows.Forms.CheckBox showProgressIndicatorUICheckBox;
        private System.Windows.Forms.CheckBox useUICheckBox;
        private System.Windows.Forms.CheckBox checkBoxArea;
        private System.Windows.Forms.CheckBox blackAndWhiteCheckBox;
        private System.Windows.Forms.Button btnClose;
        private System.Windows.Forms.Button btnUpdate4;
    }
}