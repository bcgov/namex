using AsyncRequests;

namespace ApiScanner
{
    public class ScanningAuthorApi 
    {     
        //List
        static public string get()
        {
            string endpoint = "/doc/api/v1/scanning/authors";
            string resp = APIRequest.MakeKeyRequest("", endpoint, RestSharp.Method.GET);
            return resp;
        }
    }

    public class AuthorModel
    {
        public string authorId;
        public string jobTitle;
        public string firstName;
        public string lastName;
        public string phoneNumber;
        public string email;
    }

}
