using System;
using System.Windows.Forms;

namespace TwainAdvancedDemo
{
	public partial class JpegSaveSettingsForm : Form
	{
		int _quality = 90;
		public int Quality
		{
			get { return _quality; }
		}

		public JpegSaveSettingsForm()
		{
			InitializeComponent();
		}

		private void okButton_Click(object sender, EventArgs e)
		{
			_quality = (int)qualityNumericUpDown.Value;
			DialogResult = DialogResult.OK;
		}
	}
}