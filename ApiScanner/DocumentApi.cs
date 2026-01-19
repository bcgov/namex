using AsyncRequests;
using Json;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using PdfSharp.Pdf;
using RestSharp;
using System;
using System.Collections.Generic;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Net;

namespace ApiScanner
{
    public class DocumentApi
    {
        // consumerDocumentId
        public static List<JObject> getDocObjectList(string docType, string conDocId)
        {
            string resp = get(docType, conDocId);

            List<JObject> jList = new List<JObject>();
            var token = JToken.Parse(resp);

            foreach (object token2 in token)
            {
                jList.Add((JObject)token2);
            }

            return jList;
        }

        public static Byte[] getDocBytes(string docURL)
        {
            return APIRequest.download(docURL);
        }        

        // Create pdf document
        public static string post(string fileName, byte[] pdfBytes, object data)
        {
            DocumentModel myData = (DocumentModel)data;

            Dictionary<string, object> param = new Dictionary<string, object>();
            param.Add("consumerIdentifier", (string)myData.consumerIdentifier);
            param.Add("consumerFilename", (string)myData.consumerFilename);
            param.Add("consumerFilingDate", (DateTime)myData.consumerFilingDate);
            param.Add("consumerDocumentId", (int)myData.consumerDocumentId);

            //string endpoint = "doc/api/v1/documents/" + myData.documentClass + "/" + myData.documentType;
            string endpoint = "doc/api/v1/scanning/" + myData.documentClass + "/" + myData.consumerDocumentId;

            string resp = APIRequest.MakeKeyRequest(fileName, pdfBytes, param, endpoint, RestSharp.Method.POST);

            return resp;
        }

        //Update document data
        public static string patch(object data, string docServId)
        {
            DocumentModel myData = (DocumentModel)data;

            string endpoint = "doc/api/v1/documents/" + docServId;
            string resp = APIRequest.MakeKeyRequest(data, endpoint, RestSharp.Method.PATCH);
            return resp;
        }

        // Update document image
        public static string put(string _fileName, byte[] pdfBytes, object data)
        {
            DocumentModel myData = (DocumentModel)data;

            Dictionary<string, object> param = new Dictionary<string, object>();
            if (_fileName != "")
            {                
                param.Add("consumerFilename", (string)myData.consumerFilename);
            }
            string endpoint = "/doc/api/v1/documents/" + myData.documentServiceId;
            string resp = APIRequest.MakeKeyRequest(myData.consumerFilename, pdfBytes, param, endpoint, RestSharp.Method.PUT);
            return resp;
        }

        /// In documentation, possible expansion of application. Not currently used by scanner

        ////Documents       

        // consumerDocumentId
        public static string get(string conDocId)
        {           
            string endpoint = "/doc/api/v1/documents/verify/" + conDocId;
            string resp = APIRequest.MakeKeyRequest("", endpoint, RestSharp.Method.GET);           
            return resp;
        }

        // documentServiceId
        public static string delete(string docServId)
        {
            string endpoint = "/doc/api/v1/documents/" + docServId;
            string resp = APIRequest.MakeKeyRequest("", endpoint, RestSharp.Method.DELETE);
            return resp;
        }

        // documentServiceId
        public static string patch2(object data, string docServId)
        {
            string endpoint = "/doc/api/v1/documents/" + docServId;
            string resp = APIRequest.MakeKeyRequest(data, endpoint, RestSharp.Method.PATCH);
            return resp;
        }

        // documentClass documentType
        public static string post(object data)
        {
            DocumentModel myData = (DocumentModel)data;

            string endpoint = "doc/api/v1/documents/" + myData.documentClass + "/" + myData.documentType;
            string resp = APIRequest.MakeKeyRequest(data, endpoint, RestSharp.Method.POST);
            return resp;
        }    

        ////search

        public static string getSearch()
        {
            string endpoint = "/doc/api/v1/searches";
            string resp = APIRequest.MakeKeyRequest("", endpoint, RestSharp.Method.GET);
            return resp;
        }

        //Search by docClass
        public static string getSearch(string docClass)
        {
            string endpoint = "/doc/api/v1/searches/" + docClass;
            string resp = APIRequest.MakeKeyRequest("", endpoint, RestSharp.Method.GET);
            return resp;
        }

        //Update pdf document
        public static string update(string fileName, byte[] pdfBytes, object data)
        {
            DocumentModel myData = (DocumentModel)data;

            Dictionary<string, object> param = new Dictionary<string, object>();
            param.Add("consumerIdentifier", (string)myData.consumerIdentifier);
            param.Add("consumerFilename", (string)myData.consumerFilename);
            param.Add("consumerFilingDate", (DateTime)myData.consumerFilingDate);
            param.Add("consumerDocumentId", (int)myData.consumerDocumentId);

            string endpoint = "doc/api/v1/documents/" + myData.documentClass + "/" + myData.documentType;
            string resp = APIRequest.MakeKeyRequest(fileName, pdfBytes, param, endpoint, RestSharp.Method.PATCH);

            return resp;
        }

        //Update pdf document
        public static string patch(string fileName, byte[] pdfBytes, object data)
        {
            DocumentModel myData = (DocumentModel)data;

            Dictionary<string, object> param = new Dictionary<string, object>();
            param.Add("consumerIdentifier", (string)myData.consumerIdentifier);
            param.Add("consumerFilename", (string)myData.consumerFilename);
            param.Add("consumerFilingDate", (DateTime)myData.consumerFilingDate);
            param.Add("consumerDocumentId", (int)myData.consumerDocumentId);

            //string endpoint = "doc/api/v1/documents/" + myData.documentClass + "/" + myData.consumerDocumentId;
            string endpoint = "doc/api/v1/scanning/" + myData.documentClass + "/" + myData.consumerDocumentId;

            string resp = APIRequest.MakeKeyRequest(fileName, pdfBytes, param, endpoint, RestSharp.Method.PATCH);

            return resp;
        }

        // documenttype consumerDocumentId
        public static string get(string docType, string conDocId)
        {
            string endpoint = "/doc/api/v1/business/" + docType + "?consumerDocumentId=" + conDocId;
            string resp = APIRequest.MakeKeyRequest("", endpoint, RestSharp.Method.GET);
            return resp;
        }       
    }

    public class DocumentModel
    {
        public string author;
        public int consumerDocumentId;
        public string consumerFilename;
        public DateTime consumerFilingDate;
        public string consumerIdentifier;
        public string consumerReferenceId;
        public DateTime createDateTime;
        public string documentClass;
        public string documentExists;
        public string documentServiceId;
        public string documentType;
        public string documentTypeDescription;
        public string documentURL;
        public object scanningInformation;
    }

}