using System.Data;

namespace RegScan
{
    class OptionsObj
    {
        private int _maximumPagesInBox;

        public int MaximumPagesInBox { get { return _maximumPagesInBox; } set { _maximumPagesInBox = value; } }

        private ScannerSettingObj mySetting = new ScannerSettingObj();
        
        public OptionsObj()
        {           
            _maximumPagesInBox = mySetting.MaxPagesInBox;
        }

        public void Update()
        {
            mySetting.Update();
        }
    }
}
