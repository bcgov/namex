using AsyncRequests;
using RestSharp;
using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ApiScanner
{
    public class OwnerTypeApi
    {
        static public string get()
        {
            string endpoint = "/doc/api/v1/scanning/document-classes";
            string resp = APIRequest.MakeKeyRequest("", endpoint, Method.GET);
            return resp;
        }


    }

    public class OwnerTypeModel
    {
        public string documentClassDescription;
        public string active;
        public string ownerType;
        public string sequenceNumber;
    }
}
