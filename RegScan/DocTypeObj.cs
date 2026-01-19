using ApiScanner;
using Json;
using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Windows.Forms;

namespace RegScan
{
    public class DocTypeObj
    {
        private string _code;
        private string _description;
        private bool _isActive;
        private string _applicationId;

        public string Code { get { return _code; } }
        public string Description { get { return _description; } }
        public bool IsActive { get { return _isActive; } }
        public string ApplicationId { get { return _applicationId; } }

        public string FQDescription { get { return Code + " -> " + Description; } }

        public DocTypeObj(string _Code, string _Description, bool _IsActvie, string _ApplicationId)
        {
            _code = _Code;
            _description = _Description;
            _isActive = _IsActvie;
            _applicationId = _ApplicationId;
        }

        public DocTypeObj()
        { }

        static private List<DocTypeObj> _list = new List<DocTypeObj>();
        static public DocTypeObj Find(string _Code)
        {
            if (_list.Count == 0)
                Refresh();

            try
            {
                return _list.Where(c => c.Code == _Code).First();
            }
            catch
            {
                return new DocTypeObj(_Code, "Description Not Found!", false, "NA");
            }
        }       

        static public void Refresh()
        {
            SetListFromApi();
        }

        static private void SetListFromApi()
        {
            string resp = documentTypeApi.get();

            if (resp == "") { return; }
            if (resp.Contains("errorMessage"))
            {
                MessageBox.Show("Error: " + resp);
                Application.Exit();
            }

            if (JsonParser.FromJson(resp).Count > 0)
            {
                _list.Clear();

                var respArray = JsonParser.FromJson(resp).ElementAt(0);
                List<object> docTypes = (List<object>)respArray.Value;

                foreach (Dictionary<string, object> record in docTypes)
                {
                    _list.Add(new DocTypeObj(Convert.ToString(record.ElementAt(2).Value), Convert.ToString(record.ElementAt(3).Value), Convert.ToBoolean(record.ElementAt(0).Value),
                                            Convert.ToString(record.ElementAt(1).Value)));
                }
            }
        }
    }
}
