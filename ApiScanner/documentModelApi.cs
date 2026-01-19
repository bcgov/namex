using AsyncRequests;
using Json;
using System;
using System.CodeDom;
using System.Collections.Generic;

namespace ApiScanner
{
    // In documentation, possible expansion of application. Not currently used by scanner
    public class documentModelApi
    {
        public DocumentApi _doc;
        public int consumerDocumentId;
        public string[] consumerFilenames;
        public string consumerIdentifier;
        public DateTime createDateTime;
        public string description;
        public string documentClass;
        public Boolean documentExists;
        public string documentServiceId;
        public string documentType;
        public string documentTypeDescription;


        public void setDocument(DocumentApi doc)
        {
            _doc = doc;
        }

        public List<object> getSearches()
        {
            string endpoint = "/doc/api/v1/searches";
            string resp = APIRequest.MakeKeyRequest("", endpoint, RestSharp.Method.GET);
            
            dynamic _params = JsonParser.FromJson(resp);
            List<object> resultArray = (List<object>)_params["results"];                   

            return resultArray;
        }
        /*
             foreach (var jsonitem in resultArray)
            {
                dynamic _json = (object)jsonitem;
                consumerDocumentId = _json["consumerDocumentId"];
                consumerDocumentId = _json["consumerDocumentId"];
                createDateTime = _json["createDateTime"];
                description = _json["description"];
                documentClass = _json["documentClass"];
                documentExists = _json["documentExists"];
                documentServiceId = _json["documentServiceId"];
                documentType = _json["documentType"];
                documentTypeDescription = _json["documentTypeDescription"];

                string[] consumerFilenames = _json["consumerFilenames"]; 
                
            }
            // bool result = UtilityObj.copyShallow(_doc, this);
        */

        public Dictionary<string,object> searchByDocId(string documentId)
        {
            string docId = "documentServiceId=" + documentId;
            string endpoint = "/doc/api/v1/business/CORP?" + docId;
            string resp = APIRequest.MakeKeyRequest("", endpoint, RestSharp.Method.GET);
            return (Dictionary<string, object>)JsonParser.FromJson(resp);            
        }

        public object searchByServiceId(string docServiceId)
        {
            string docId = "documentServiceId=" + docServiceId;
            string endpoint = "/doc/api/v1/searches/CORP?" + docId;
            string resp = APIRequest.MakeKeyRequest("", endpoint, RestSharp.Method.GET);
            dynamic _param = JsonParser.FromJson(resp);
            return (object)_param;
        }

        public object searchByEntityId(string entityId)
        {
            string conId = "consumerIdentifier=" + entityId;
            string endpoint = "/doc/api/v1/searches/CORP?" + conId;
            string resp = APIRequest.MakeKeyRequest("", endpoint, RestSharp.Method.GET);
            dynamic _param = JsonParser.FromJson(resp);
            return (object)_param;
        }        

        public object searchByDateRange(string startDate,string endDate)
        {
            string dateRange = "queryStartDate=" + startDate + "&queryEndDate=" + endDate;
            string endpoint = "/doc/api/v1/searches/CORP?" + dateRange;
            string resp = APIRequest.MakeKeyRequest("", endpoint, RestSharp.Method.GET);
            dynamic _param = JsonParser.FromJson(resp);
            return (object)_param;
        }

        public object searchByDateRangeDocType(string startDate, string endDate, string docType)
        {
            string dateRange = "queryStartDate=" + startDate + "&queryEndDate=" + endDate;
            string dType = "&documentType=" + docType;
            string endpoint = "/doc/api/v1/searches/CORP?" + dateRange + dType;
            string resp = APIRequest.MakeKeyRequest("", endpoint, RestSharp.Method.GET);
            dynamic _param = JsonParser.FromJson(resp);
            return (object)_param;
        }

        public object searchByDateRangeDocClass(string startDate, string endDate, string docClass)
        {   
            string dClass = "documentClass=" + docClass;
            string dateRange = "&queryStartDate=" + startDate + "&queryEndDate=" + endDate;           
            string endpoint = "/doc/api/v1/searches?" + dClass + dateRange;
            string resp = APIRequest.MakeKeyRequest("", endpoint, RestSharp.Method.GET);
            dynamic _param = JsonParser.FromJson(resp);
            return (object)_param;
        }

        public object searchByDocClass(string docClass)
        {
            string dClass = "documentClass=" + docClass;
            string endpoint = "/doc/api/v1/searches?" + dClass;
            string resp = APIRequest.MakeKeyRequest("", endpoint, RestSharp.Method.GET);
            dynamic _param = JsonParser.FromJson(resp);
            return (object)_param;
        }

        public object searchByDocClassEntityId(string docClass, string entityId)
        {
            string conId = "&consumerIdentifier=" + entityId;
            string dClass = "documentClass=" + docClass;
            string endpoint = "/doc/api/v1/searches?" + dClass + conId;
            string resp = APIRequest.MakeKeyRequest("", endpoint, RestSharp.Method.GET);
            dynamic _param = JsonParser.FromJson(resp);
            return (object)_param;
        }

        public object searchByDateRangeDocClassDocType(string startDate, string endDate, string docClass, string docType)
        {
            string dClass = "documentClass=" + docClass;
            string dateRange = "&queryStartDate=" + startDate + "&queryEndDate=" + endDate;
            string dType = "&documentType=" + docType;
            string endpoint = "/doc/api/v1/searches?" + dClass + dateRange + dType;
            string resp = APIRequest.MakeKeyRequest("", endpoint, RestSharp.Method.GET);
            dynamic _param = JsonParser.FromJson(resp);
            return (object)_param;
        }

    }   
                  
}
