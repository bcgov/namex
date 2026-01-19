using System;
using System.Drawing;
using System.Drawing.Printing;
using System.Windows.Forms;

namespace RegScan
{
    public partial class frmBatchPrint : Form
    {
        private BatchObj _batch = null;
        public frmBatchPrint(BatchObj _Batch, bool _ShowSelection)
        {
            InitializeComponent();

            // Save our batch incase it is to be modified.
            _batch = _Batch;
            txtAccessionNumber.Text = _batch.AccessionNumberFormatted;
            numericUpDownBatchNumber.Value = _batch.BatchId;
            numericUpDownBatchNumber.Focus();

            if (!_ShowSelection)
                btnUpdate.Visible = false;
        }

        private void btnClose_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void btnUpdate_Click(object sender, EventArgs e)
        {
            if ((int)numericUpDownBatchNumber.Value == 0)
            {
                MessageBox.Show("Please enter a value greater than 0", "Wrong Value");
                return;
            }

            _batch.BatchId = (int)numericUpDownBatchNumber.Value;
            this.Close();
        }

        private void btnPrintLabel_Click(object sender, EventArgs e)
        {
            _batch.BatchId = (int)numericUpDownBatchNumber.Value;
            var printDoc = new PrintDocument();
            printDoc.DocumentName = "Batch Label: " + _batch.BatchId.ToString();
            printDoc.PrintPage += new PrintPageEventHandler(PrintPage);
            printDoc.Print();
        }

        private void PrintPage(object sender, System.Drawing.Printing.PrintPageEventArgs e)
        {
            // Get list of Owner Types

            //This part sets up the data to be printed
            Graphics g = e.Graphics;
            SolidBrush Brush = new SolidBrush(Color.Black);

            //gets the text from the textbox
            string printText = "\r\n\n\n\n" +
                                "Date:                ____________\r\n\n" +
                                "Batch Number:      " + _batch.BatchId.ToString() + "\r\n\n" +
                                "Accession Number: " + _batch.AccessionNumberFormatted;

            //Makes the file to print and sets the look of it
            g.DrawString(printText, new Font("arial", 34), Brush, 10, 10);
        }

    }
}
