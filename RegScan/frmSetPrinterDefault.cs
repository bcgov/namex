using System;
using System.Drawing.Printing;
using System.Runtime.InteropServices;
using System.Windows.Forms;

namespace RegScan
{
    public partial class frmSetPrinterDefault : Form
    {
        public frmSetPrinterDefault()
        {
            InitializeComponent();
            listAllPrinters();
        }

        private void listAllPrinters()
        {
            var printerSetting = new PrinterSettings();
            foreach (var item in PrinterSettings.InstalledPrinters)
            {
                this.lBoxPrinters.Items.Add(item.ToString());
                if (printerSetting.PrinterName == item.ToString())
                    lBoxPrinters.SelectedIndex = lBoxPrinters.Items.Count - 1;
            }
        }

        private void btnClose_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void btnSelect_Click(object sender, EventArgs e)
        {
            string pname = this.lBoxPrinters.SelectedItem.ToString();
            myPrinters.SetDefaultPrinter(pname);
            this.Close();
        }
    }

    public static class myPrinters
    {
        [DllImport("winspool.drv", CharSet = CharSet.Auto, SetLastError = true)]
        public static extern bool SetDefaultPrinter(string Name);

    }
}


