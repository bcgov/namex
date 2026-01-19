using System;
using System.Windows.Forms;

namespace RegScan
{
    public partial class frmEnterBarCode : Form
    {

        private BarCodeString _barCodeString;

        public frmEnterBarCode(BarCodeString _BarCodeString)
        {
            InitializeComponent();
            _barCodeString = _BarCodeString;
        }

        private void btnOk_Click(object sender, EventArgs e)
        {
            if (txtBarCode.Text == "")
                return;

            var document = DocumentObj.Find(txtBarCode.Text);
            if (DocumentObj.ErrorMessage != "")
                MessageBox.Show(DocumentObj.ErrorMessage);
            else
            {
                _barCodeString.BarCode = txtBarCode.Text;
                this.Close();
            }

        }

        private void btnCancel_Click(object sender, EventArgs e)
        {
            _barCodeString.BarCode = "";
            this.Close();
        }
    }
}
