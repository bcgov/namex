using ApiScanner;
using Newtonsoft.Json;
using PdfSharp.Pdf.Filters;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Reflection;

namespace RegScan
{
    public static class UtilityObj
    {
        static public int NOID = -1;
        static public DateTime DATENOTFOUND = DateTime.Parse("01-Jan-1900");
        static public long NOACCESSIONNUMBER = 9999999999;

        // Converts a string that contains either Y or N to a bool value.
        static public bool ConvertYN(string _YN)
        {
            bool value = false;
            if (_YN.ToUpper() == "Y")
                value = true;

            return value;
        }

        // Converts a bool to a string containing 'Y' or 'N'
        static public string ConvertBool(bool _Value)
        {
            return _Value ? "Y" : "N";
        }

        // Converts a bool to a string containing 'Y' or 'N'
        static public bool ConvertToBool(string _Value)
        {
            if (_Value == "true")
            {
                return true;
            }
            return false;                  
        }

        // Converts a date to a format for inserting updating into an oracle database.
        static public string To_Date(DateTime _Date)
        {
            return "TO_DATE('" + _Date.ToString("dd-MMM-yyyy") + "','DD-MON-YYYY')";
        }

        // Converts a date/time to a format for inserting updating into an oracle database.
        static public string To_DateTime(DateTime _DateTime)
        {
            return "TO_DATE('" + _DateTime.ToString("dd-MMM-yyyy HH:mm:ss") + "','DD-MON-YYYY hh24:mi:ss')";
        }

        // Write message string to log file.
        static public void writeLog(string msg)
        {
            msg = (DateTime.Now).ToString() + ": " + msg + System.Environment.NewLine;
            //System.IO.File.WriteAllText(@"log.txt", msg);
            System.IO.File.AppendAllText(@"log.txt", msg);
        }

        // Save image as file.
        static public void saveImageAsFile(string fileName, Bitmap img)
        {
            System.IO.File.WriteAllBytes(fileName, imageToByte(img));
        }     

        // Convert bitmap to byte array. 
        static public byte[] imageToByte(Image img)
        {
            ImageConverter converter = new ImageConverter();
            return (byte[])converter.ConvertTo(img, typeof(byte[]));
        }

        // Read file into image.
        static public Bitmap readFileAsImage(string fileName)
        {
            byte[] imageData = System.IO.File.ReadAllBytes(fileName);

            Bitmap bmp;
            using (var ms = new MemoryStream(imageData))
            {
                bmp = new Bitmap(ms);
            }
            return bmp;
        }

        // Read file into image.
        static public Bitmap readImageFile(string fileName)
        {
            byte[] imageData = System.IO.File.ReadAllBytes(fileName);

            return (Bitmap)((new ImageConverter()).ConvertFrom(imageData));

        }

        // Create the images folder. 
        static public void createFolder(string folder)
        {
            if (!Directory.Exists(folder))
            {
                Directory.CreateDirectory(folder);
            }
        }

        // Remove the images folder. 
        static public void deleteFolder(string folder)
        {
            if (Directory.Exists(folder))
            {
                Directory.Delete(folder,true);
            }
        }

        // Remove the images folder.
        static public List<string> readFolder(string folder)
        {
            folder = Directory.GetCurrentDirectory() + "\\" + folder;
            if (Directory.Exists(folder))
            {
                return Directory.GetFiles(folder).ToList();
            }
            return null;
        }

        static public DataTable makeDataTable(string json)
        {
            DataTable dataTable = new DataTable();
            if (string.IsNullOrWhiteSpace(json))
            {
                return dataTable;
            }

            dataTable = JsonConvert.DeserializeObject<DataTable>(json);

            return dataTable;
        }

        // Set API values into database objects        
        /*static public void copyValues( object apiParams, object dbSettings)
        {
            //apiParmas.
            Type myType = apiParams.GetType();
            IList<PropertyInfo> props = new List<PropertyInfo>(myType.GetProperties());

            foreach (PropertyInfo prop in props)
            {
                object propValue = prop.GetValue(apiParams, null);
                // Do something with propValue
                dbSettings.prop = propValue;
            }
        }
        */

        static public bool copyShallow(Object api, Object srcObj)
        {
            
            var srcT = srcObj.GetType();
            var dstT = api.GetType();
            
            foreach (var f in srcT.GetFields())
            {
                var dstF = dstT.GetField(f.Name);
                if (dstF == null || dstF.IsLiteral)
                    continue;
                dstF.SetValue(dstT, f.GetValue(srcT));
            }

            foreach (var f in srcT.GetProperties())
            {
                var dstF = dstT.GetProperty(f.Name);
                if (dstF == null)
                    continue;

                dstF.SetValue(dstT, f.GetValue(srcT, null), null);
            }
            return true;
        }
                
    }
}
