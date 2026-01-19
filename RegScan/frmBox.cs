using System;
using System.Drawing;
using System.Drawing.Printing;
using System.Windows.Forms;

namespace RegScan
{
    public partial class frmBox : Form
    {
        private BoxObj _boxObj = null;                  // Is set if called from the scanning form.

        public frmBox()
        {
            InitializeComponent();
            cBoxScheduleId.DataSource = ScheduleObj.List(true);
            _boxObj = new BoxObj();
        }

        private void btnClose_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void btnNew_Click(object sender, EventArgs e)
        {

            if (cBoxScheduleId.SelectedIndex < 1)
                return;

            // Confirm box creation.
            if (MessageBox.Show("Confirm closing of existing open box and creating a new box?", "Confirm Box Creation", MessageBoxButtons.YesNo, MessageBoxIcon.Question, MessageBoxDefaultButton.Button1) == System.Windows.Forms.DialogResult.Yes)
            {
                // Close Exising Box.
                var schedule = ScheduleObj.Find((int)cBoxScheduleId.SelectedValue);
                var box = BoxObj.Find(schedule.SequenceNumber, schedule.ScheduleNumber);
                if (box == null)
                    // No box found, so create a new one.
                    BoxObj.CopyBox(BoxObj.OpenBox(schedule.SequenceNumber, schedule.ScheduleNumber, 1), _boxObj);
                else
                    // Close existing box and open new one.
                    BoxObj.CopyBox(BoxObj.CloseOpen(box), _boxObj);

                cBoxScheduleId_SelectedIndexChanged(sender, e);
                cBoxBoxId.SelectedIndex = cBoxBoxId.Items.Count - 1;

            }

        }

        // Find an existing box.
        private void btnFind_Click(object sender, EventArgs e)
        {

            if (cBoxScheduleId.SelectedIndex < 1)
            {
                Clear();
                return;
            }

            if (cBoxBoxId.SelectedIndex < 1)
            {
                Clear();
                return;
            }

            var schedule = ScheduleObj.Find((int)cBoxScheduleId.SelectedValue);
            var boxObj = BoxObj.Find(schedule.SequenceNumber, schedule.ScheduleNumber, int.Parse(cBoxBoxId.Text));
            if (boxObj == null)
                MessageBox.Show("Box not found");
            else
            {
                txtBoxId.Text = boxObj.BoxId.ToString();
                txtDateBoxOpened.Text = boxObj.OpendedDate.ToString("dd-MMM-yyyy");
                txtDateBoxClosed.Text = boxObj.ClosedDate == BoxObj.BOXSTILLOPEN ? "" : boxObj.ClosedDate.ToString("dd-MMM-yyyy");
                txtPagesInBox.Text = boxObj.PageCount.ToString();
                btnPrint.Visible = true;
                btnPrintBatchLabel.Visible = true;
            }
        }

        // Schedule combo box clicked, so load the box numbers associated with it.
        private void cBoxScheduleId_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (cBoxScheduleId.SelectedIndex < 1)
            {
                cBoxBoxId.DataSource = null;
                btnNew.Visible = false;
                btnPrint.Visible = false;
                btnPrintBatchLabel.Visible = false;
                return;
            }

            btnNew.Visible = true;
            cBoxBoxId.DisplayMember = "BoxNumberText";
            cBoxBoxId.ValueMember = "BoxId";
            var schedule = ScheduleObj.Find((int)cBoxScheduleId.SelectedValue);
            cBoxBoxId.DataSource = BoxObj.List(schedule.SequenceNumber, schedule.ScheduleNumber, true);
            Clear();
        }

        private void Clear()
        {
            txtDateBoxClosed.Text = "";
            txtDateBoxOpened.Text = "";
            txtPagesInBox.Text = "";
        }

        private void PrintPage(object sender, System.Drawing.Printing.PrintPageEventArgs e)
        {
            //This part sets up the data to be printed
            Graphics g = e.Graphics;
            SolidBrush Brush = new SolidBrush(Color.Black);

            // Accession Number
            string printText = "\n     " + ((ScheduleObj)cBoxScheduleId.SelectedItem).Description.Replace(" ", "") + "-" +
                                cBoxBoxId.Text.PadLeft(4, '0');
            g.DrawString(printText, new Font("arial", 40), Brush, 10, 10);

            // Date Box Started.
            printText = "\n\n\n\n\n\n\n\n\r  " +
                                "Date Started: " + DateTime.Parse(txtDateBoxOpened.Text).ToLongDateString();

            //Makes the file to print and sets the look of it
            g.DrawString(printText, new Font("arial", 18), Brush, 10, 10);
        }

        private void btnPrint_Click(object sender, EventArgs e)
        {
            if (cBoxScheduleId.SelectedIndex < 1)
            {
                Clear();
                return;
            }

            if (cBoxBoxId.SelectedIndex < 1)
            {
                Clear();
                return;
            }

            var printDoc = new PrintDocument();
            printDoc.DocumentName = "Box Label: " + ((ScheduleObj)cBoxScheduleId.SelectedItem).Description + " - " +
                                cBoxBoxId.Text.PadLeft(4, '0');
            printDoc.PrintPage += new PrintPageEventHandler(PrintPage);
            printDoc.DefaultPageSettings.PaperSize = new PaperSize("Box Label", 600, 400);
            printDoc.Print();
        }

        /// <summary>
        /// Sets the box information based on the Accession number
        /// </summary>
        /// <param name="_AccessionNumber"></param>
        /// <returns>An error message or blank.</returns>
        public string SetBoxNumber(BoxObj _BoxObj)
        {
            _boxObj = _BoxObj;
            var accessionNumber = _boxObj.AccessionNumber.Replace("-", "");
            if (accessionNumber.Length != BoxObj.ACCESSION_NUMBER_LENGTH)
                return "Accession Number is incorrect lenght ... lenght should be " + BoxObj.ACCESSION_NUMBER_LENGTH.ToString() + " digits";

            // Get the sequence/schedule number and box number.
            var fqn = int.Parse(accessionNumber.Substring(0, 6));
            var boxNumber = int.Parse(accessionNumber.Substring(6, 4));

            // Display the sequence/schedule number.
            int index = -1;
            foreach (ScheduleObj item in cBoxScheduleId.Items)
            {
                index++;
                if (item.FQN == fqn)
                    break;
            }
            cBoxScheduleId.SelectedIndex = index;

            // Display the box number.
            index = -1;
            foreach (BoxObj item in cBoxBoxId.Items)
            {
                index++;
                if (item.BoxNumber == boxNumber)
                    break;
            }
            cBoxBoxId.SelectedIndex = index;

            // Display the box contents
            btnFind_Click(new object(), new EventArgs());

            // Select button is visable now.
            btnSelect.Visible = true;

            return "";

        }

        private void cBoxBoxId_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (cBoxBoxId.SelectedIndex < 1)
            {
                btnPrint.Visible = false;
                btnPrintBatchLabel.Visible = false;
                return;
            }

            btnFind_Click(sender, e);
            btnPrint.Visible = true;
            btnPrintBatchLabel.Visible = true;
        }

        // Button will only be activce if form was called from the frmDocument.
        private void btnSelect_Click(object sender, EventArgs e)
        {
            if (cBoxScheduleId.SelectedIndex < 1)
            {
                Clear();
                return;
            }

            if (cBoxBoxId.SelectedIndex < 1)
            {
                Clear();
                return;
            }

            var schedule = ScheduleObj.Find((int)cBoxScheduleId.SelectedValue);
            BoxObj.CopyBox(BoxObj.Find(schedule.SequenceNumber, schedule.ScheduleNumber, int.Parse(cBoxBoxId.Text)), _boxObj);

            this.Close();
        }

        private void btnPrintBatchLabel_Click(object sender, EventArgs e)
        {
            if (cBoxScheduleId.SelectedIndex < 1)
            {
                Clear();
                return;
            }

            if (cBoxBoxId.SelectedIndex < 1)
            {
                Clear();
                return;
            }

            BatchObj batch = new BatchObj();
            batch.AccessionNumber = long.Parse(((ScheduleObj)cBoxScheduleId.SelectedItem).Description.Replace(" - ", "") +
                               cBoxBoxId.Text.ToString().PadLeft(4, '0'));


            // Display the batch form.
            var frm = new frmBatchPrint(batch, false);
            frm.ShowDialog();

        }

    }
}
