using AsyncRequests;
using System;

namespace ApiScanner
{
    public class ScanningBoxApi
    {        
        // Refresh
        static public string get()
        {
            string endpoint = "/doc/api/v1/scanning/boxes";
            string resp = APIRequest.MakeKeyRequest("", endpoint, RestSharp.Method.GET);
            return resp;
        }

        // UpdatePageCount + CloseOpen  
        static public string patch(object data)
        {
            string endpoint = "/doc/api/v1/scanning/boxes";
            string resp = APIRequest.MakeKeyRequest(data, endpoint, RestSharp.Method.PATCH);
            return resp;
        }

        // Insert
        static public string post(object data)
        {
            string endpoint = "/doc/api/v1/scanning/boxes";
            string resp = APIRequest.MakeKeyRequest(data, endpoint, RestSharp.Method.POST);
            return resp;
        }

        // List
        static public string get(string seqNum, string schedNum)
        {
            string endpoint = "/doc/api/v1/scanning/boxes/" + seqNum + "/" + schedNum;
            string resp = APIRequest.MakeKeyRequest("", endpoint, RestSharp.Method.GET);
            return resp;
        }
    }

    public class BoxModel
    {
        public int boxId;
        public int sequenceNumber;
        public int scheduleNumber;
        public int boxNumber;
        public DateTime openedDate;
        public DateTime closedDate;
        public int pageCount;
    }

}
