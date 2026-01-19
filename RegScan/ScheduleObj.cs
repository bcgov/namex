using ApiScanner;
using AsyncRequests;
using Json;
using System;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Security.AccessControl;
using System.Web;

namespace RegScan
{
    class ScheduleObj
    {        
        private int _scheduleNumber;
        private int _sequenceNumber;

        public int SequenceNumber { get { return _sequenceNumber; } }
        public int ScheduleNumber { get { return _scheduleNumber; } }
        public string Description
        {
            get
            {
                if (_sequenceNumber == UtilityObj.NOID)
                    return "<Select Schedule>";
                else
                    return _sequenceNumber.ToString().PadLeft(2, '0') + " - " + _scheduleNumber.ToString().PadLeft(4, '0');
            }
        }

        public int FQN
        {
            get
            {
                if (_sequenceNumber == -1)
                    return -1;
                else
                    return int.Parse(_sequenceNumber.ToString() + _scheduleNumber.ToString());
            }
        }

        public ScheduleObj(int _ScheduleNumber, int _SequenceNumber)
        {
            _scheduleNumber = _ScheduleNumber;
            _sequenceNumber = _SequenceNumber;
        }

        // Static
        private static List<ScheduleObj> _list = new List<ScheduleObj>();

        // Find the schedule assocated with this schedule number.
        static public ScheduleObj Find(int _ScheduleNumber)
        {
            if (_list.Count == 0)
                Refresh();

            try
            {
                return _list.Where(a => a._scheduleNumber == _ScheduleNumber).First();
            }
            catch
            {
                return null;
            }
        }

        // Find the schedule associated with this owner type.
        static public ScheduleObj Find(string _OwnerTypeCode)
        {
            var ownerTypeCode = OwnerTypeObj.Find(_OwnerTypeCode);
            return Find(ownerTypeCode.ScheduleNumber);
        }               
        
        static public void Refresh()
        {
            SetListFromApi();
        }              

        static public List<ScheduleObj> List(bool _IncludeSelect)
        {
            if (_list.Count == 0)
                Refresh();

            if (_IncludeSelect)
            {
                List<ScheduleObj> list = new List<ScheduleObj>();
                list.Add(new ScheduleObj(UtilityObj.NOID, UtilityObj.NOID));
                foreach (var schedule in _list)
                    list.Add(new ScheduleObj(schedule._scheduleNumber, schedule._sequenceNumber));
                return list;
            }
            else
                return _list;
        }

        static private void SetListFromApi()
        {
            string resp = ScheduleApi.get();

            if (JsonParser.FromJson(resp).Count > 0)
            {
                _list.Clear();

                var respArray = JsonParser.FromJson(resp).ElementAt(0);
                List<object> schedules = (List<object>)respArray.Value;

                foreach (Dictionary<string, object> record in schedules)
                {
                    _list.Add(new ScheduleObj(Convert.ToInt32(record.ElementAt(0).Value), Convert.ToInt32(record.ElementAt(1).Value)));
                }
            }
        }

        public void test()
        {
            //test API endpoints            
            Refresh();
        }

    }
}
