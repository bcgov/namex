using AsyncRequests;
using Newtonsoft.Json.Linq;

namespace ApiScanner
{
    // In documentation, possible expansion of application. Not currently used by scanner
    public class documentTypeApi 
    {
        static public string get()
        {
            string endpoint = "/doc/api/v1/scanning/document-types";
            string resp = APIRequest.MakeKeyRequest("", endpoint, RestSharp.Method.GET);
            return resp;
        }        
    }

    public class DocumentTypeModel
    {
        /* FIX - Currently Unused 
        private bool active;
        private string applicationId;
        private string documentType;
        private string documentTypeDescription;
        */
    }
}
