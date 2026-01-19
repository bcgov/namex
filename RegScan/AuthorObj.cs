using ApiScanner;
using Json;
using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Windows.Forms;

namespace RegScan
{
    public class AuthorObj
    {
        private string _authorId;
        private string _jobTitle;
        private string _firstName;
        private string _lastName;
        private string _phoneNumber;
        private string _email;

        public string AuthorId { get { return _authorId; } }
        public string JobTitle { get { return _jobTitle; } }
        public string FirstName { get { return _firstName; } }
        public string LastName { get { return _lastName; } }
        public string PhoneNumber { get { return _phoneNumber; } }
        public string Email { get { return _email; } }

        public string FQName { get { return _firstName.Trim() + ", " + _lastName.Trim(); } }

        public AuthorObj(string _AuthorId, string _JobTitle, string _FirstName, string _LastName, string _PhoneNumber, string _Email)
        {
            _authorId = _AuthorId;
            _jobTitle = _JobTitle;
            _firstName = _FirstName;
            _lastName = _LastName;
            _phoneNumber = _PhoneNumber;
            _email = _Email;
        }

        public AuthorObj()
        { }

        //static private List<AuthorObj> _list = new List<AuthorObj>();
        static public List<AuthorObj> _list = new List<AuthorObj>();

        static public void Refresh()
        {
            SetListFromApi();
        }

        static public AuthorObj Find(string _AuthorId)
        {
            // Load list if first time through.
            if (_list.Count == 0)
                Refresh();

            try
            {
                return _list.Where(a => a.AuthorId == _AuthorId).First();
            }
            catch
            {
                return new AuthorObj("-1", "Not Found", "Not", "Found", "", "");
            }
        }

        static private void SetListFromApi()
        {
            string resp = ScanningAuthorApi.get();

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
                List<object> authors = (List<object>)respArray.Value;

                foreach (Dictionary<string, object> record in authors)
                {
                    _list.Add(new AuthorObj("", Convert.ToString(record.ElementAt(2).Value), Convert.ToString(record.ElementAt(1).Value), Convert.ToString(record.ElementAt(3).Value),
                                            Convert.ToString(record.ElementAt(4).Value), Convert.ToString(record.ElementAt(0).Value)));
                }
            }
        }
    }
}
