using ApiScanner;
using Json;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.Collections;
using System;
using System.Collections.Generic;
using System.Data;

namespace RegScan
{
    public class ScannerSettingObj
    {
        
        public int MaxPagesInBox = 300;
        public bool UseDocumentFeeder = false;
        public bool ShowTwainUI = true;
        public bool ShowProgressIndicatorUI = true;
        public bool UseDuplex = true;
        public bool BlackAndWhiteCheckBox = true;
        public bool ShouldTransferAllPages = true;
        public bool AutoRotateCheckBox = true;
        public bool AutoDetectBorderCheckBox = false;
        public bool checkBoxArea = false;

        private ScannerParametersModel ApiModel = new ScannerParametersModel();

        public ScannerSettingObj()
        {           
            load();            
        }

        public void Update()
        {
            copyToModel();
            string resp = ScanningParameterApi.patch(ApiModel);          
        }      

        public void copyToModel()
        {
            ApiModel.maxPagesInBox = MaxPagesInBox;
            ApiModel.useDocumentFeeder = UseDocumentFeeder;
            ApiModel.showTwainUi = ShowTwainUI;
            ApiModel.showTwainProgress = ShowProgressIndicatorUI;
            ApiModel.useFullDuplex = UseDuplex;
            ApiModel.useLowResolution = BlackAndWhiteCheckBox;
        }

        public void copyFromModel(string resp)
        {
            var token = JToken.Parse(resp);

            MaxPagesInBox = token.Value<int>("maxPagesInBox");
            UseDocumentFeeder = token.Value<bool>("useDocumentFeeder");
            ShowTwainUI = token.Value<bool>("showTwainUi");
            ShowProgressIndicatorUI = token.Value<bool>("showTwainProgress");
            UseDuplex = token.Value<bool>("useFullDuplex");
            BlackAndWhiteCheckBox = token.Value<bool>("useLowResolution");
        }

        private void load()
        {
            string resp = ScanningParameterApi.get();
            copyFromModel(resp);
        }                  

    }
}
