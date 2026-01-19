using ApiScanner;
using Newtonsoft.Json.Linq;

namespace RegScan
{
    public class BatchObj
    {
        private static BatchModel batchModel = new BatchModel();

        static private int _batchId;
        private long _accessionNumber;

        public int BatchId { get { return _batchId; } set { _batchId = value; } }
        public long AccessionNumber { get { return _accessionNumber; } set { _accessionNumber = value; } }
        public string AccessionNumberFormatted
        {
            get
            {
                return BoxObj.FormatAccessionNumber(_accessionNumber);

            }
        }              

        static public BatchObj GetNextBatchId(long _Accession_Num)
        {
            var batchObj = new BatchObj();

            string resp = ScanningBatchApi.get(_Accession_Num);

            if (resp == null)
            {
                batchObj.BatchId = 1;
            }
            else
            {
                copyFromModel(resp);
                batchObj.BatchId = int.Parse(batchObj.BatchId.ToString()) + 1;
            }          
                
            return batchObj;     
        }


        static public void copyToModel()
        {
            batchModel.batchId = _batchId;
        }

        static public void copyFromModel(string resp)
        {
            var token = JToken.Parse(resp);

            _batchId = token.Value<int>("batchId");
        }
    }
}
