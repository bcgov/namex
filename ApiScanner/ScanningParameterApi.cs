using AsyncRequests;
using RestSharp;

namespace ApiScanner
{
    public class ScanningParameterApi
    {      
        static public string get()
        {
            string endpoint = "/doc/api/v1/scanning/parameters";
            string resp = APIRequest.MakeKeyRequest("", endpoint, Method.GET);
            return resp;
        }

        static public string patch(object data)
        {            
            string endpoint = "/doc/api/v1/scanning/parameters";
            string resp = APIRequest.MakeKeyRequest(data, endpoint, Method.PATCH);
            return resp;
        }   
                
    }

    public class ScannerParametersModel
    {
        public int maxPagesInBox;
        public bool useDocumentFeeder;
        public bool showTwainUi;
        public bool showTwainProgress;
        public bool useFullDuplex;
        public bool useLowResolution;
    }

}
