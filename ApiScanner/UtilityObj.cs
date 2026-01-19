using ApiScanner;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Reflection;

namespace ApiScanner
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
                Directory.Delete(folder);
            }
        }
        
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
