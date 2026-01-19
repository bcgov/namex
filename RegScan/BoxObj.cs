using ApiScanner;
using Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;

namespace RegScan
{
    public class BoxObj
    {

        #region Properties and Constructors       

        public static int ACCESSION_NUMBER_LENGTH = 10;
        public static DateTime BOXSTILLOPEN = DateTime.Parse("01-Jan-1900");
        private static int SELECTBOX = -9999;
        
        private int _boxId;
        private int _sequenceNumber;
        private int _scheduleNumber;
        private int _boxNumber;
        private DateTime _openedDate;
        private DateTime _closedDate;
        private int _pageCount;

        public int BoxId { get { return _boxId; } set { _boxId = value; } }
        public int PageCount { get { return _pageCount; } set { _pageCount = value; } }
        public int SequenceNumber { get { return _sequenceNumber; } set { _sequenceNumber = value; } }
        public int ScheduleNumber { get { return _scheduleNumber; } set { _scheduleNumber = value; } }
        public int BoxNumber { get { return _boxNumber; } set { _boxNumber = value; } }
        public DateTime OpendedDate { get { return _openedDate; } set { _openedDate = value; } }
        public DateTime ClosedDate { get { return _closedDate; } set { _closedDate = value; } }

        public string ErrorMessage;

        public string SequenceScheduleNumber { get { return _sequenceNumber.ToString().PadLeft(2, '0') + "-" + _scheduleNumber.ToString().PadLeft(4, '0'); } }

        public string AccessionNumber
        {
            get
            {
                if (_sequenceNumber == -1)
                    return (0).ToString().PadLeft(BoxObj.ACCESSION_NUMBER_LENGTH, '0');
                else
                    return BoxObj.FormatAccessionNumber(long.Parse(_sequenceNumber.ToString().PadLeft(2, '0') +
                                                                _scheduleNumber.ToString().PadLeft(4, '0') +
                                                                _boxNumber.ToString().PadLeft(4, '0')));
            }
        }

        public string BoxNumberText
        {
            get
            {
                if (_scheduleNumber == SELECTBOX)
                    return "<Select Box>";
                else
                    return _boxNumber.ToString();
            }
        }

        public BoxObj()
        {
            _boxId = UtilityObj.NOID;
            _pageCount = 0;
            _sequenceNumber = UtilityObj.NOID;
            _scheduleNumber = UtilityObj.NOID;
            _boxNumber = 0;
            _openedDate = System.DateTime.Today;
            _closedDate = BOXSTILLOPEN;
            ErrorMessage = "";
        }

        public BoxObj(int _BoxId, int _SequenceNumber, int _ScheduledNumber, int _BoxNumber, DateTime _OpenedDate, DateTime _ClosedDate, int _PageCount)
        {
            _boxId = _BoxId;
            _pageCount = _PageCount;
            _sequenceNumber = _SequenceNumber;
            _scheduleNumber = _ScheduledNumber;
            _boxNumber = _BoxNumber;
            _openedDate = _OpenedDate;
            _closedDate = _ClosedDate;
            ErrorMessage = "";
        }

        #endregion

        #region API Calls

        // Insert new box information to API.
        public void Insert()
        {
            BoxModel boxModel = new BoxModel();

            copyToModel(boxModel);            
            string resp = ScanningBoxApi.post(boxModel);

            var box = Find(_sequenceNumber, _scheduleNumber, _boxNumber);
            if (box != null)
                _boxId = box.BoxId;

        }

        // Update existing box information
        public void UpdatePageCount()
        {
            BoxModel boxModel = new BoxModel();

            copyToModel(boxModel);
            string resp = ScanningBoxApi.patch(boxModel);
        }


        static List<BoxObj> _list = new List<BoxObj>();
        static public string ERROR_MESSAGE = "";
        static public void Refresh()
        {
            ERROR_MESSAGE = "";
            _list.Clear();
            try
            {
                string resp = ScanningBoxApi.get();
                _list = SetListFromApi(resp);            
            }
            catch (Exception e)
            {
                ERROR_MESSAGE = e.Message;
            }
            
        }

        #endregion
      
        #region Static Find/Select

        public BoxObj Find(int _BoxId)
        {
            // Load list.
            Refresh();

            try
            {
                return _list.Where(a => a.BoxId == _BoxId).OrderByDescending(a => a.BoxNumber).First();
            }
            catch
            {
                ERROR_MESSAGE += "No box found for Id " + _BoxId.ToString();
                return null;
            }
        }


        /// <summary>
        /// //// MIGHT NEED TO REWRITE
        /// </summary>
        /// <param name="_SequenceNumber"></param>
        /// <param name="_ScheduleNumber"></param>
        /// <returns></returns>
        static public BoxObj Find(int _SequenceNumber, int _ScheduleNumber)
        {
            // Load list.
            Refresh();

            try
            {
                return _list.Where(a => a.SequenceNumber == _SequenceNumber && a.ScheduleNumber == _ScheduleNumber).OrderByDescending(a => a.BoxNumber).First();
            }
            catch
            {
                ERROR_MESSAGE += "No box found for sequence " + _SequenceNumber.ToString() + " and chedule " + _ScheduleNumber.ToString();
                return null;
            }
        }

        static public BoxObj Find(int _SequenceNumber, int _ScheduleNumber, int _BoxNumber)
        {
            // Load list
            Refresh();

            try
            {
                BoxObj xBox = _list.Where(a => a.SequenceNumber == _SequenceNumber &&
                                    a.ScheduleNumber == _ScheduleNumber &&
                                    a.BoxNumber == _BoxNumber).First();

                return xBox; 
            }
            catch
            {
                ERROR_MESSAGE += "No box found for sequence " + _SequenceNumber.ToString() + " and schedule " + _ScheduleNumber.ToString() + " and box number " + _BoxNumber.ToString();
                return null;
            }
        }

        // Find the box assocated with this owner type code ... if not found, then create a box.
        static public BoxObj Find(string _OwnerTypeCode)
        {
            ERROR_MESSAGE = "";

            ScheduleObj schedule = ScheduleObj.Find(_OwnerTypeCode);
            if (schedule == null)
            {
                ERROR_MESSAGE = "No sequence/schedule found for owner type code " + _OwnerTypeCode + " in the schedule database table";
                return null;
            }
            else
            {
                var box = Find(schedule.SequenceNumber, schedule.ScheduleNumber);
                if (box == null)
                    // If not box found ... create one.
                    box = OpenBox(schedule.SequenceNumber, schedule.ScheduleNumber, 1);
                return box;
            }

        }

        static public List<BoxObj> List(int _SequencyNumber, int _ScheduleNumber, bool _IncludeNoBoxesFound)
        {
            ERROR_MESSAGE = "";
            List<BoxObj> list = new List<BoxObj>();

            try
            {
                string resp = ScanningBoxApi.get();
                list = SetListFromApi(resp);              
            }
            catch (Exception e)
            {
                ERROR_MESSAGE = e.Message;
            }

            return list;
        }

        static public BoxObj CloseOpen(BoxObj _Box)
        {
            ERROR_MESSAGE = "";
            BoxModel boxModel = new BoxModel();

            try
            {
                _Box.copyToModel(_Box, boxModel);
                string resp = ScanningBoxApi.patch(boxModel);
                
                if (resp == null)
                {
                    var box = new BoxObj();
                    box.ErrorMessage = "Box not found.";
                    return box;
                }
                else
                {
                    return OpenBox(_Box.SequenceNumber, _Box.ScheduleNumber, _Box.BoxNumber + 1);
                }
            }
            catch (Exception e)
            {
                ERROR_MESSAGE = e.Message;
            }
            return null;
        }                        

       /// <summary>
       /// Open new box.
       /// </summary>
       /// <param name="_SequencyNumber"></param>
       /// <param name="_ScheduleNumber"></param>
       /// <param name="_BoxNumber"></param>
       /// <returns>BoxObj</returns>
       static public BoxObj OpenBox(int _SequenceNumber, int _ScheduleNumber, int _BoxNumber)
        {
            BoxObj box = new BoxObj();
            box.SequenceNumber = _SequenceNumber;
            box.ScheduleNumber = _ScheduleNumber;
            box.PageCount = 0;
            box.OpendedDate = DateTime.Now;
            box.BoxNumber = _BoxNumber;

            // Insert Box 
            box.Insert();
            ERROR_MESSAGE = box.ErrorMessage;
            return box;

        }

        // Format an accession number for display
        public static string FormatAccessionNumber(long _AccessionNumber)
        {
            string str = _AccessionNumber.ToString().PadLeft(BoxObj.ACCESSION_NUMBER_LENGTH, '0');
            return str.Substring(0, 2) + "-" + str.Substring(2, 4) + "-" + str.Substring(6, 4);
        }


        /// <summary>
        /// Copy box 
        /// </summary>
        /// <param name="_Source"></param>
        /// <param name="_Destination"></param>
        static public void CopyBox(BoxObj _Source, BoxObj _Destination)
        {
            _Destination.BoxId = _Source.BoxId;
            _Destination.BoxNumber = _Source.BoxNumber;
            _Destination.ClosedDate = _Source.ClosedDate;
            _Destination.OpendedDate = _Source.OpendedDate;
            _Destination.PageCount = _Source.PageCount;
            _Destination.ScheduleNumber = _Source.ScheduleNumber;
            _Destination.SequenceNumber = _Source.SequenceNumber;
        }

        public void copyToModel(BoxModel boxModel)
        {
            boxModel.boxId = _boxId;
            boxModel.sequenceNumber = _sequenceNumber;
            boxModel.scheduleNumber = _scheduleNumber;
            boxModel.boxNumber = _boxNumber;
            boxModel.openedDate = _openedDate;
            boxModel.closedDate = _closedDate;
            boxModel.pageCount = _pageCount;
                     
        }

        public void copyToModel(BoxObj box, BoxModel boxModel)
        {
            boxModel.boxId = box.BoxId;
            boxModel.sequenceNumber = box.SequenceNumber;
            boxModel.scheduleNumber = box.ScheduleNumber;
            boxModel.boxNumber = box.BoxNumber;
            boxModel.openedDate = box.OpendedDate;
            boxModel.closedDate = box.ClosedDate;
            boxModel.pageCount = box.PageCount;

        }
       
        public void copyFromModel(string resp)
        {
            var token = JToken.Parse(resp);

            _boxId = token.Value<int>("boxId");
            _sequenceNumber = token.Value<int>("_sequenceNumber");
            _scheduleNumber = token.Value<int>("_scheduleNumber");
            _boxNumber = token.Value<int>("_boxNumber");
            _openedDate = token.Value<DateTime>("useFullDuplex");
            _closedDate = token.Value<DateTime>("useLowResolution");
            _pageCount = token.Value<int>("useLowResolution");

        }
       

        static private List<BoxObj> SetListFromApi(string resp)
        {           
            if (JsonParser.FromJson(resp).Count > 0)
            {
                _list.Clear();

                var respArray = JsonParser.FromJson(resp).ElementAt(0);
                List<object> boxList = (List<object>)respArray.Value;               

                foreach (Dictionary<string, object> record in boxList)
                {                                      
                    _list.Add(new BoxObj(Convert.ToInt32(record.ElementAt(0).Value), Convert.ToInt32(record.ElementAt(6).Value), Convert.ToInt32(record.ElementAt(5).Value),
                                         Convert.ToInt32(record.ElementAt(1).Value), Convert.ToDateTime(record.ElementAt(3).Value), Convert.ToDateTime(record.ElementAt(2).Value),
                                         Convert.ToInt32(record.ElementAt(4).Value)));                   
                        
                }
            }
            return _list;
        }    

        #endregion
    }
}
