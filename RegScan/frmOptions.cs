using System;
using System.Windows.Forms;

namespace RegScan
{
    public partial class frmOptions : Form
    {
        private OptionsObj _options;

        public frmOptions()
        {
            InitializeComponent();
            _options = new OptionsObj();
            txtMaximumPagesInBox.Text = _options.MaximumPagesInBox.ToString();
        }

        private void btnClose_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void btnUpdate4_Click(object sender, EventArgs e)
        {
            if (txtMaximumPagesInBox.Text == "")
            {
                MessageBox.Show("Please enter a value for Maximum Pages In a Box");
                return;
            }

            int pages = 0;
            if (!int.TryParse(txtMaximumPagesInBox.Text, out pages))
            {
                MessageBox.Show("Please enter a numeric value for Maxium Pages In a Box");
                return;
            }

            _options.MaximumPagesInBox = pages;
            _options.Update();
            
            // FIX
            //if (DBSupport.ErrorMessage != "")
            //    MessageBox.Show(DBSupport.ErrorMessage);
            //else
            //    MessageBox.Show("Option(s) Updated");
        }
    }
}
