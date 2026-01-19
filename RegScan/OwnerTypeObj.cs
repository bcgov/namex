using ApiScanner;
using Json;
using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Windows.Forms;

namespace RegScan
{
    public class OwnerTypeObj
    {
        private string _ownerTypeCode;
        private string _description;
        private bool _isActive;
        private int _scheduleNumber;

        public string OwnerTypeCode { get { return _ownerTypeCode; } }
        public string Description { get { return _description; } }
        public bool IsActive { get { return _isActive; } }
        public int ScheduleNumber { get { return _scheduleNumber; } }

        public OwnerTypeObj(string _OwnerTypeCode, string _Description, bool _IsActive, int _ScheduleNumber)
        {
            _ownerTypeCode = _OwnerTypeCode;
            _description = _Description;
            _isActive = _IsActive;
            _scheduleNumber = _ScheduleNumber;
        }

        static List<OwnerTypeObj> _list = new List<OwnerTypeObj>();
        
        static public void Refresh()
        {
            SetListFromApi();
        }

        static private void SetListFromApi()
        {
            string resp = OwnerTypeApi.get();

            if (resp == ""){ return; }
            if (resp.Contains("errorMessage")) 
            {
                MessageBox.Show("Error: " + resp);
                Application.Exit();
            }

            if (JsonParser.FromJson(resp).Count > 0)
            {
                _list.Clear();

                var respArray = JsonParser.FromJson(resp).ElementAt(0);
                List<object> ownerTypes = (List<object>)respArray.Value;

                foreach (Dictionary<string, object> record in ownerTypes)
                {
                    _list.Add(new OwnerTypeObj(Convert.ToString(record.ElementAt(3).Value), Convert.ToString(record.ElementAt(2).Value), 
                                               Convert.ToBoolean(record.ElementAt(0).Value), Convert.ToInt32(record.ElementAt(4).Value)));
                }
            }
        }

        static public OwnerTypeObj Find(string _OwnerTypeCode)
        {
            // Load list if first time through.
            if (_list.Count == 0)
                Refresh();

            try
            {
                return _list.Where(a => a.OwnerTypeCode == _OwnerTypeCode).First();
            }
            catch
            {
                return new OwnerTypeObj("NT", "Not Found", false, UtilityObj.NOID);
            }
        }

        // Returns a list based on the schedule.
        static public List<OwnerTypeObj> FindList(int _Schedule)
        {
            // Load master list if first time through
            if (_list.Count == 0)
                Refresh();

            try
            {
                return _list.Where(a => a.ScheduleNumber == _Schedule).ToList();
            }
            catch
            {
                return new List<OwnerTypeObj>();
            }
        }

        static public List<OwnerTypeObj> List()
        {
            // Load list if first time through.
            if (_list.Count == 0)
                Refresh();

            return _list;

        }
    }
}
