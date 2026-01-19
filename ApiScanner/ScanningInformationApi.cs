using AsyncRequests;
using System;

namespace ApiScanner
{
    public class ScanningInformationApi
    {
        public string get(string consummerDocId)
        {
            string endpoint = "/doc/api/v1/documents/verify/" + consummerDocId;
            string resp = APIRequest.MakeKeyRequest("", endpoint, RestSharp.Method.GET);
            return resp;
        }

        public string patch(object data, string docServiceId)
        {
            string endpoint = "/doc/api/v1/documents/" + docServiceId;
            string resp = APIRequest.MakeKeyRequest(data, endpoint, RestSharp.Method.PATCH);
            return resp;
        }

        public string post(object data, string docType)
        {
            string endpoint = "/doc/api/v1/documents/" + docType;
            string resp = APIRequest.MakeKeyRequest(data, endpoint, RestSharp.Method.POST);
            return resp;
        }

        public string delete(string docServiceId)
        {
            string endpoint = "/doc/api/v1/documents/" + docServiceId;
            string resp = APIRequest.MakeKeyRequest("", endpoint, RestSharp.Method.DELETE);
            return resp;
        }

        public string put(object data, string docServiceId)
        {
            string endpoint = "/doc/api/v1/documents/" + docServiceId;
            string resp = APIRequest.MakeKeyRequest(data, endpoint, RestSharp.Method.PUT);
            return resp;
        }
    }

    public class ScanningInfoModel
    {
        public long accessionNumber;
        public string author;
        public int batchId;
        public DateTime createDateTime;
        public int pagecount;
        public DateTime scannedDate;
    }

}
