using Json;
using Microsoft.Extensions.Configuration;
using RestSharp;
using System;
using System.Collections.Generic;
using System.Configuration;
using System.IO;
using System.Net;
using System.Text;
using System.Threading.Tasks;


namespace AsyncRequests
{
    class APIRequest
    {
        // security        
        private Method requestType;
        private string authToken;
        private string apikey;
        private string account_id;
        private string token_url;
        private string timeout;
        private string client_id;
        private string client_secret;

        // response
        private string myResponse;

        public APIRequest()
        {
            // Get configuration
            SetEnvironment();

            // Set security protocols
            ServicePointManager.Expect100Continue = true;
            ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12;

        }

        public string MakeRequest(string data, string endPoint, Method requestType)
        {
            authToken = _GetAuthToken();

            var client = new RestClient(endPoint);
            var request = new RestRequest(requestType);

            request.AddHeader("Authorization", "Bearer " + authToken);
            request.AddHeader("cache-control", "no-cache");

            if (requestType == Method.POST || requestType == Method.PUT || requestType == Method.PATCH)
            {
                request.AddJsonBody(data);
                string answer = client.Execute(request).Content;
                return answer;
            }

            if (requestType == Method.GET)
            {
                string answer = client.Execute(request).Content;
                return answer;
            }

            if (requestType == Method.DELETE)
            {
                string answer = client.Execute(request).Content;
                return answer;
            }

            return "";
        }

        public string MakeKeyRequest(string data, string endPoint, Method requestType)
        {
            var client = new RestClient(endPoint);
            var request = new RestRequest(requestType);

            request.AddHeader("Account-Id", account_id);
            request.AddHeader("x-apikey", apikey);

            if (requestType == Method.POST || requestType == Method.PUT || requestType == Method.PATCH)
            {
                request.AddJsonBody(data);
                string answer = client.Execute(request).Content;
                return answer;
            }

            if (requestType == Method.GET)
            {
                string answer = client.Execute(request).Content;
                return answer;
            }

            if (requestType == Method.DELETE)
            {
                string answer = client.Execute(request).Content;
                return answer;
            }

            return "";
        }

        private string _GetAuthToken()
        {
            var client = new RestClient(token_url);
            var request = new RestRequest(Method.POST);

            request.AddHeader("cache-control", "no-cache");
            request.AddHeader("content-type", "application/x-www-form-urlencoded");
            string credentials = "grant_type=client_credentials&client_id=" + client_id + "&client_secret=" + client_secret;
            request.AddParameter("application/x-www-form-urlencoded", credentials, ParameterType.RequestBody);

            IRestResponse response = client.Execute(request);
            IDictionary<string, object> json = Json.JsonParser.FromJson(response.Content);

            return Json.JsonParser.ToJson(json);
        }

        private void SetEnvironment()
        {
            // Initialize environment
            string enviroment = ConfigurationManager.AppSettings["ENV"];

            if (enviroment == "prod")
            {
                apikey = Base64Decode(ConfigurationManager.AppSettings["PROD_X-APIKEY"]);
                account_id = ConfigurationManager.AppSettings["PROD_ACCOUNT_ID"];

                token_url = ConfigurationManager.AppSettings["TEST_AUTH_SVC_URL"];
                timeout = ConfigurationManager.AppSettings["AUTH_TIMEOUT"];
                client_id = ConfigurationManager.AppSettings["TEST_CLIENT_ID"];
                client_secret = ConfigurationManager.AppSettings["TEST_CLIENT_ACCOUNT"];

            }
            else if (enviroment == "test")
            {
                apikey = Base64Decode(ConfigurationManager.AppSettings["TEST_X-APIKEY"]);
                account_id = ConfigurationManager.AppSettings["TEST_ACCOUNT_ID"];

                token_url = ConfigurationManager.AppSettings["TEST_AUTH_SVC_URL"];
                timeout = ConfigurationManager.AppSettings["AUTH_TIMEOUT"];
                client_id = ConfigurationManager.AppSettings["TEST_CLIENT_ID"];
                client_secret = ConfigurationManager.AppSettings["TEST_CLIENT_ACCOUNT"];
            }
            else
            {
                apikey = Base64Decode(ConfigurationManager.AppSettings["TEST_X-APIKEY"]);
                account_id = ConfigurationManager.AppSettings["TEST_ACCOUNT_ID"];

                token_url = ConfigurationManager.AppSettings["TEST_AUTH_SVC_URL"];
                timeout = ConfigurationManager.AppSettings["AUTH_TIMEOUT"];
                client_id = ConfigurationManager.AppSettings["TEST_CLIENT_ID"];
                client_secret = ConfigurationManager.AppSettings["TEST_CLIENT_ACCOUNT"];
            }
        }

        private static string Base64Decode(string base64)
        {
            var base64Bytes = System.Convert.FromBase64String(base64);
            return System.Text.Encoding.UTF8.GetString(base64Bytes);
        }

    }  //end class
}
