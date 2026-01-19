namespace RegScan
{
    partial class frmBox
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
            this.label1 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.txtBoxId = new System.Windows.Forms.TextBox();
            this.btnFind = new System.Windows.Forms.Button();
            this.btnNew = new System.Windows.Forms.Button();
            this.btnClose = new System.Windows.Forms.Button();
            this.txtPagesInBox = new System.Windows.Forms.TextBox();
            this.cBoxScheduleId = new System.Windows.Forms.ComboBox();
            this.label6 = new System.Windows.Forms.Label();
            this.txtDateBoxOpened = new System.Windows.Forms.TextBox();
            this.txtDateBoxClosed = new System.Windows.Forms.TextBox();
            this.label7 = new System.Windows.Forms.Label();
            this.cBoxBoxId = new System.Windows.Forms.ComboBox();
            this.printBox = new System.Windows.Forms.PrintDialog();
            this.btnPrint = new System.Windows.Forms.Button();
            this.btnSelect = new System.Windows.Forms.Button();
            this.btnPrintBatchLabel = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.Location = new System.Drawing.Point(163, 142);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(47, 13);
            this.label1.TabIndex = 0;
            this.label1.Text = "Box Id:";
            this.label1.Visible = false;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label3.Location = new System.Drawing.Point(4, 10);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(127, 13);
            this.label3.TabIndex = 2;
            this.label3.Text = "Sequence/Schedule:";
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label4.Location = new System.Drawing.Point(5, 40);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(79, 13);
            this.label4.TabIndex = 3;
            this.label4.Text = "Box Number:";
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label5.Location = new System.Drawing.Point(5, 71);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(86, 13);
            this.label5.TabIndex = 4;
            this.label5.Text = "Pages In Box:";
            // 
            // txtBoxId
            // 
            this.txtBoxId.Location = new System.Drawing.Point(166, 158);
            this.txtBoxId.Name = "txtBoxId";
            this.txtBoxId.Size = new System.Drawing.Size(63, 20);
            this.txtBoxId.TabIndex = 5;
            this.txtBoxId.TabStop = false;
            this.txtBoxId.Visible = false;
            // 
            // btnFind
            // 
            this.btnFind.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnFind.ForeColor = System.Drawing.Color.Blue;
            this.btnFind.Location = new System.Drawing.Point(272, 121);
            this.btnFind.Name = "btnFind";
            this.btnFind.Size = new System.Drawing.Size(164, 28);
            this.btnFind.TabIndex = 5;
            this.btnFind.Text = "Find...";
            this.btnFind.UseVisualStyleBackColor = true;
            this.btnFind.Visible = false;
            this.btnFind.Click += new System.EventHandler(this.btnFind_Click);
            // 
            // btnNew
            // 
            this.btnNew.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnNew.ForeColor = System.Drawing.Color.Black;
            this.btnNew.Location = new System.Drawing.Point(271, 3);
            this.btnNew.Name = "btnNew";
            this.btnNew.Size = new System.Drawing.Size(164, 26);
            this.btnNew.TabIndex = 2;
            this.btnNew.Text = "Create New Box";
            this.btnNew.UseVisualStyleBackColor = true;
            this.btnNew.Visible = false;
            this.btnNew.Click += new System.EventHandler(this.btnNew_Click);
            // 
            // btnClose
            // 
            this.btnClose.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnClose.ForeColor = System.Drawing.Color.Black;
            this.btnClose.Location = new System.Drawing.Point(272, 155);
            this.btnClose.Name = "btnClose";
            this.btnClose.Size = new System.Drawing.Size(163, 28);
            this.btnClose.TabIndex = 8;
            this.btnClose.Text = "Close";
            this.btnClose.UseVisualStyleBackColor = true;
            this.btnClose.Click += new System.EventHandler(this.btnClose_Click);
            // 
            // txtPagesInBox
            // 
            this.txtPagesInBox.Location = new System.Drawing.Point(147, 71);
            this.txtPagesInBox.Name = "txtPagesInBox";
            this.txtPagesInBox.ReadOnly = true;
            this.txtPagesInBox.Size = new System.Drawing.Size(63, 20);
            this.txtPagesInBox.TabIndex = 12;
            this.txtPagesInBox.TabStop = false;
            // 
            // cBoxScheduleId
            // 
            this.cBoxScheduleId.DisplayMember = "Description";
            this.cBoxScheduleId.FormattingEnabled = true;
            this.cBoxScheduleId.Items.AddRange(new object[] {
            "MH",
            "DS",
            "CC"});
            this.cBoxScheduleId.Location = new System.Drawing.Point(147, 6);
            this.cBoxScheduleId.Name = "cBoxScheduleId";
            this.cBoxScheduleId.RightToLeft = System.Windows.Forms.RightToLeft.No;
            this.cBoxScheduleId.Size = new System.Drawing.Size(118, 21);
            this.cBoxScheduleId.TabIndex = 0;
            this.cBoxScheduleId.ValueMember = "ScheduleNumber";
            this.cBoxScheduleId.SelectedIndexChanged += new System.EventHandler(this.cBoxScheduleId_SelectedIndexChanged);
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label6.Location = new System.Drawing.Point(5, 100);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(111, 13);
            this.label6.TabIndex = 15;
            this.label6.Text = "Date Box Opened:";
            // 
            // txtDateBoxOpened
            // 
            this.txtDateBoxOpened.Location = new System.Drawing.Point(147, 93);
            this.txtDateBoxOpened.Name = "txtDateBoxOpened";
            this.txtDateBoxOpened.ReadOnly = true;
            this.txtDateBoxOpened.Size = new System.Drawing.Size(99, 20);
            this.txtDateBoxOpened.TabIndex = 16;
            this.txtDateBoxOpened.TabStop = false;
            // 
            // txtDateBoxClosed
            // 
            this.txtDateBoxClosed.Location = new System.Drawing.Point(147, 119);
            this.txtDateBoxClosed.Name = "txtDateBoxClosed";
            this.txtDateBoxClosed.ReadOnly = true;
            this.txtDateBoxClosed.Size = new System.Drawing.Size(99, 20);
            this.txtDateBoxClosed.TabIndex = 18;
            this.txtDateBoxClosed.TabStop = false;
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label7.Location = new System.Drawing.Point(5, 126);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(105, 13);
            this.label7.TabIndex = 17;
            this.label7.Text = "Date Box Closed:";
            // 
            // cBoxBoxId
            // 
            this.cBoxBoxId.DisplayMember = "BoxNumberText";
            this.cBoxBoxId.FormattingEnabled = true;
            this.cBoxBoxId.Location = new System.Drawing.Point(147, 37);
            this.cBoxBoxId.Name = "cBoxBoxId";
            this.cBoxBoxId.RightToLeft = System.Windows.Forms.RightToLeft.No;
            this.cBoxBoxId.Size = new System.Drawing.Size(118, 21);
            this.cBoxBoxId.TabIndex = 1;
            this.cBoxBoxId.ValueMember = "BoxId";
            this.cBoxBoxId.SelectedIndexChanged += new System.EventHandler(this.cBoxBoxId_SelectedIndexChanged);
            // 
            // printBox
            // 
            this.printBox.UseEXDialog = true;
            // 
            // btnPrint
            // 
            this.btnPrint.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.5F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnPrint.ForeColor = System.Drawing.Color.Blue;
            this.btnPrint.Location = new System.Drawing.Point(271, 35);
            this.btnPrint.Name = "btnPrint";
            this.btnPrint.Size = new System.Drawing.Size(165, 23);
            this.btnPrint.TabIndex = 3;
            this.btnPrint.Text = "Print Box Label...";
            this.btnPrint.UseVisualStyleBackColor = true;
            this.btnPrint.Visible = false;
            this.btnPrint.Click += new System.EventHandler(this.btnPrint_Click);
            // 
            // btnSelect
            // 
            this.btnSelect.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnSelect.ForeColor = System.Drawing.Color.Blue;
            this.btnSelect.Location = new System.Drawing.Point(7, 155);
            this.btnSelect.Name = "btnSelect";
            this.btnSelect.Size = new System.Drawing.Size(132, 28);
            this.btnSelect.TabIndex = 7;
            this.btnSelect.Text = "Select...";
            this.btnSelect.UseVisualStyleBackColor = true;
            this.btnSelect.Visible = false;
            this.btnSelect.Click += new System.EventHandler(this.btnSelect_Click);
            // 
            // btnPrintBatchLabel
            // 
            this.btnPrintBatchLabel.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.5F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnPrintBatchLabel.ForeColor = System.Drawing.Color.Blue;
            this.btnPrintBatchLabel.Location = new System.Drawing.Point(272, 64);
            this.btnPrintBatchLabel.Name = "btnPrintBatchLabel";
            this.btnPrintBatchLabel.Size = new System.Drawing.Size(165, 23);
            this.btnPrintBatchLabel.TabIndex = 4;
            this.btnPrintBatchLabel.Text = "Print Batch Label...";
            this.btnPrintBatchLabel.UseVisualStyleBackColor = true;
            this.btnPrintBatchLabel.Visible = false;
            this.btnPrintBatchLabel.Click += new System.EventHandler(this.btnPrintBatchLabel_Click);
            // 
            // frmBox
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(449, 193);
            this.Controls.Add(this.btnPrintBatchLabel);
            this.Controls.Add(this.btnSelect);
            this.Controls.Add(this.btnPrint);
            this.Controls.Add(this.cBoxBoxId);
            this.Controls.Add(this.txtDateBoxClosed);
            this.Controls.Add(this.label7);
            this.Controls.Add(this.txtDateBoxOpened);
            this.Controls.Add(this.label6);
            this.Controls.Add(this.cBoxScheduleId);
            this.Controls.Add(this.txtPagesInBox);
            this.Controls.Add(this.btnClose);
            this.Controls.Add(this.btnNew);
            this.Controls.Add(this.btnFind);
            this.Controls.Add(this.txtBoxId);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label1);
            this.Name = "frmBox";
            this.Text = "Box Maintenance";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.TextBox txtBoxId;
        private System.Windows.Forms.Button btnFind;
        private System.Windows.Forms.Button btnNew;
        private System.Windows.Forms.Button btnClose;
        private System.Windows.Forms.TextBox txtPagesInBox;
        private System.Windows.Forms.ComboBox cBoxScheduleId;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.TextBox txtDateBoxOpened;
        private System.Windows.Forms.TextBox txtDateBoxClosed;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.ComboBox cBoxBoxId;
        private System.Windows.Forms.PrintDialog printBox;
        private System.Windows.Forms.Button btnPrint;
        private System.Windows.Forms.Button btnSelect;
        private System.Windows.Forms.Button btnPrintBatchLabel;
    }
}