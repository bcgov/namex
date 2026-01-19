namespace TwainExtendedImageInfoDemo
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
            this.extendedImageInfoCheckedListBox = new System.Windows.Forms.CheckedListBox();
            this.extendedImageInfoAboutAcquiredImageTextBox = new System.Windows.Forms.TextBox();
            this.acquireImageButton = new System.Windows.Forms.Button();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.selectAllExtendedImageInfoButton = new System.Windows.Forms.Button();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.groupBox1.SuspendLayout();
            this.groupBox2.SuspendLayout();
            this.SuspendLayout();
            // 
            // extendedImageInfoCheckedListBox
            // 
            this.extendedImageInfoCheckedListBox.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
                        | System.Windows.Forms.AnchorStyles.Left)));
            this.extendedImageInfoCheckedListBox.FormattingEnabled = true;
            this.extendedImageInfoCheckedListBox.Location = new System.Drawing.Point(12, 49);
            this.extendedImageInfoCheckedListBox.Name = "extendedImageInfoCheckedListBox";
            this.extendedImageInfoCheckedListBox.Size = new System.Drawing.Size(308, 484);
            this.extendedImageInfoCheckedListBox.TabIndex = 1;
            // 
            // extendedImageInfoAboutAcquiredImageTextBox
            // 
            this.extendedImageInfoAboutAcquiredImageTextBox.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
                        | System.Windows.Forms.AnchorStyles.Left)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.extendedImageInfoAboutAcquiredImageTextBox.Location = new System.Drawing.Point(10, 19);
            this.extendedImageInfoAboutAcquiredImageTextBox.Multiline = true;
            this.extendedImageInfoAboutAcquiredImageTextBox.Name = "extendedImageInfoAboutAcquiredImageTextBox";
            this.extendedImageInfoAboutAcquiredImageTextBox.ScrollBars = System.Windows.Forms.ScrollBars.Both;
            this.extendedImageInfoAboutAcquiredImageTextBox.Size = new System.Drawing.Size(333, 514);
            this.extendedImageInfoAboutAcquiredImageTextBox.TabIndex = 2;
            // 
            // acquireImageButton
            // 
            this.acquireImageButton.Location = new System.Drawing.Point(12, 12);
            this.acquireImageButton.Name = "acquireImageButton";
            this.acquireImageButton.Size = new System.Drawing.Size(187, 45);
            this.acquireImageButton.TabIndex = 110;
            this.acquireImageButton.Text = "Acquire image";
            this.acquireImageButton.UseVisualStyleBackColor = true;
            this.acquireImageButton.Click += new System.EventHandler(this.acquireImageButton_Click);
            // 
            // groupBox1
            // 
            this.groupBox1.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
                        | System.Windows.Forms.AnchorStyles.Left)));
            this.groupBox1.Controls.Add(this.selectAllExtendedImageInfoButton);
            this.groupBox1.Controls.Add(this.extendedImageInfoCheckedListBox);
            this.groupBox1.Location = new System.Drawing.Point(12, 63);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(330, 543);
            this.groupBox1.TabIndex = 111;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "Extended Image Info to retrieve";
            // 
            // selectAllExtendedImageInfoButton
            // 
            this.selectAllExtendedImageInfoButton.Location = new System.Drawing.Point(12, 20);
            this.selectAllExtendedImageInfoButton.Name = "selectAllExtendedImageInfoButton";
            this.selectAllExtendedImageInfoButton.Size = new System.Drawing.Size(75, 23);
            this.selectAllExtendedImageInfoButton.TabIndex = 112;
            this.selectAllExtendedImageInfoButton.Text = "Select all";
            this.selectAllExtendedImageInfoButton.UseVisualStyleBackColor = true;
            this.selectAllExtendedImageInfoButton.Click += new System.EventHandler(this.selectAllExtendedImageInfoButton_Click);
            // 
            // groupBox2
            // 
            this.groupBox2.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
                        | System.Windows.Forms.AnchorStyles.Left)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.groupBox2.Controls.Add(this.extendedImageInfoAboutAcquiredImageTextBox);
            this.groupBox2.Location = new System.Drawing.Point(348, 63);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(353, 543);
            this.groupBox2.TabIndex = 112;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "Extended Image Info about acquired image(s)";
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(713, 618);
            this.Controls.Add(this.groupBox2);
            this.Controls.Add(this.groupBox1);
            this.Controls.Add(this.acquireImageButton);
            this.Name = "MainForm";
            this.Text = "VintaSoft TWAIN Extended Image Info Demo";
            this.Shown += new System.EventHandler(this.MainForm_Shown);
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.MainForm_FormClosing);
            this.groupBox1.ResumeLayout(false);
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.CheckedListBox extendedImageInfoCheckedListBox;
        private System.Windows.Forms.TextBox extendedImageInfoAboutAcquiredImageTextBox;
        private System.Windows.Forms.Button acquireImageButton;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.Button selectAllExtendedImageInfoButton;
        private System.Windows.Forms.GroupBox groupBox2;
    }
}

