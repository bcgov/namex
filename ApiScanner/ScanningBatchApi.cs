using AsyncRequests;

namespace ApiScanner
{
    public class ScanningBatchApi
    {   
        static public string get(long accessionNumber)
        {
            string endpoint = "/doc/api/v1/scanning/batchid/" + accessionNumber.ToString() + "/";
            string resp = APIRequest.MakeKeyRequest("", endpoint, RestSharp.Method.GET);
            return resp;
        }
    }

    public class BatchModel
    {
        public int batchId;        
    }
}
