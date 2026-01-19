using AsyncRequests;

namespace ApiScanner
{
    // In documentation, possible expansion of application. Not currently used by scanner
    public class documentTypeSummary
    {        
        public string get()
        {
            string endpoint = "/doc/api/v1/documents/document-types";
            string resp = APIRequest.MakeKeyRequest("", endpoint, RestSharp.Method.GET);
            return resp;
        }
    }
}
