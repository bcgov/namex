namespace RegScan
{
    partial class frmOptions
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
            this.txtMaximumPagesInBox = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.btnClose = new System.Windows.Forms.Button();
            this.btnUpdate4 = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // txtMaximumPagesInBox
            // 
            this.txtMaximumPagesInBox.Location = new System.Drawing.Point(164, 10);
            this.txtMaximumPagesInBox.Name = "txtMaximumPagesInBox";
            this.txtMaximumPagesInBox.Size = new System.Drawing.Size(59, 20);
            this.txtMaximumPagesInBox.TabIndex = 0;
            this.txtMaximumPagesInBox.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.Location = new System.Drawing.Point(3, 13);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(155, 13);
            this.label1.TabIndex = 1;
            this.label1.Text = "Maximum Pages in a Box: ";
            // 
            // btnClose
            // 
            this.btnClose.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnClose.ForeColor = System.Drawing.Color.Black;
            this.btnClose.Location = new System.Drawing.Point(159, 60);
            this.btnClose.Name = "btnClose";
            this.btnClose.Size = new System.Drawing.Size(75, 28);
            this.btnClose.TabIndex = 52;
            this.btnClose.Text = "Close";
            this.btnClose.UseVisualStyleBackColor = true;
            this.btnClose.Click += new System.EventHandler(this.btnClose_Click);
            // 
            // btnUpdate4
            // 
            this.btnUpdate4.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnUpdate4.ForeColor = System.Drawing.Color.Blue;
            this.btnUpdate4.Location = new System.Drawing.Point(5, 60);
            this.btnUpdate4.Name = "btnUpdate4";
            this.btnUpdate4.Size = new System.Drawing.Size(76, 28);
            this.btnUpdate4.TabIndex = 51;
            this.btnUpdate4.Text = "Update";
            this.btnUpdate4.UseVisualStyleBackColor = true;
            this.btnUpdate4.Click += new System.EventHandler(this.btnUpdate4_Click);
            // 
            // frmOptions
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(247, 94);
            this.Controls.Add(this.btnClose);
            this.Controls.Add(this.btnUpdate4);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.txtMaximumPagesInBox);
            this.Name = "frmOptions";
            this.Text = "Options";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox txtMaximumPagesInBox;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button btnClose;
        private System.Windows.Forms.Button btnUpdate4;
    }
}