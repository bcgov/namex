using AsyncRequests;

namespace ApiScanner
{
    public class ScanningDocumentApi
    {
        public string get()
        {
            string endpoint = "/doc/api/v1/scanning/document-classes";
            string resp = APIRequest.MakeKeyRequest("", endpoint, RestSharp.Method.GET);
            return resp;
        }

    }
}
