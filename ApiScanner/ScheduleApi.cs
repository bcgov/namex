using AsyncRequests;
using Json;
using RestSharp;
using System.Collections.Generic;
using System.Net;

namespace ApiScanner
{
    public class ScheduleApi
    {
        static public string get()
        {
            string endpoint = "/doc/api/v1/scanning/schedules";
            string resp = APIRequest.MakeKeyRequest("", endpoint, RestSharp.Method.GET);           
            return resp;
        }      
    }

    public class ScheduleModel
    {
        public int scheduleNumber;
        public int sequenceNumber;
    }

}
