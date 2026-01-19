using ApiScanner;
using AsyncRequests;
using Json;
using System;
using System.Collections.Generic;
using System.Windows.Forms;
using System.Windows.Forms.VisualStyles;

namespace RegScan
{
    public partial class frmScannerSetting : Form
    {
        private ScannerSettingObj _defaultSetting = null;        

        public frmScannerSetting()
        {        
            InitializeComponent();
            // DB - Settings from DB
            _defaultSetting = new ScannerSettingObj();
            useAdfCheckBox.Checked = _defaultSetting.UseDocumentFeeder;
            useDuplexCheckBox.Checked = _defaultSetting.UseDuplex;
            useUICheckBox.Checked = _defaultSetting.ShowTwainUI;
            showProgressIndicatorUICheckBox.Checked = _defaultSetting.ShowProgressIndicatorUI;
            blackAndWhiteCheckBox.Checked = _defaultSetting.BlackAndWhiteCheckBox;
            checkBoxArea.Checked = _defaultSetting.checkBoxArea;
            autoDetectBorderCheckBox.Checked = _defaultSetting.AutoDetectBorderCheckBox;
            autoRotateCheckBox.Checked = _defaultSetting.AutoRotateCheckBox;
        }

        private void btnClose_Click(object sender, EventArgs e)
        {
            
            this.Close();
        }

        private void btnUpdate4_Click(object sender, EventArgs e)
        {
            if (_defaultSetting == null)
                return;

            _defaultSetting.UseDocumentFeeder = useAdfCheckBox.Checked;
            _defaultSetting.UseDuplex = useDuplexCheckBox.Checked;
            _defaultSetting.ShowTwainUI = useUICheckBox.Checked;
            _defaultSetting.ShowProgressIndicatorUI = showProgressIndicatorUICheckBox.Checked;
            _defaultSetting.BlackAndWhiteCheckBox = blackAndWhiteCheckBox.Checked;
            _defaultSetting.checkBoxArea = checkBoxArea.Checked;
            _defaultSetting.AutoDetectBorderCheckBox = autoDetectBorderCheckBox.Checked;
            _defaultSetting.AutoRotateCheckBox = autoRotateCheckBox.Checked;
            _defaultSetting.Update();

            // FIX
            //if (DBSupport.ErrorMessage != "")
            //    MessageBox.Show(DBSupport.ErrorMessage);
            //else
            //    MessageBox.Show("Scanner Parameters Updated");
        }
    }
}
