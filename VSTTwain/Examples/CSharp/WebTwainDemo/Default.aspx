<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>VintaSoft Web TWAIN Demo</title>
    <script language="JavaScript" type="text/javascript">

        var _device;
        var _acquireImageIndex = -1;
        var _acquiredImage;


        // Scan image(s) from scanner.

        function ScanImage() {
            // check that DeviceManager1 object is initialized properly
            if (DeviceManager1.IsTwainAvailable == null) {
                document.getElementById('ErrorString').innerHTML = "<a href=http://www.vintasoft.com/docs/vstwain-dotnet/Deploying_Twain_WebApp.html>Click here to see how to configure your web application correctly</a>";
                alert("Web application is configured not correctly.");
                return;
            }

            try {
                var showUI = document.getElementById('ShowUI').checked;
                var useAdf = document.getElementById('UseADF').checked;
                var useDuplex = document.getElementById('UseDuplex').checked;
                var scanPixelTypes = document.getElementsByName('ScanPixelType');
                var pixelType = 0;
                if (scanPixelTypes[1].checked)
                    pixelType = 1;
                if (scanPixelTypes[2].checked)
                    pixelType = 2;

                // enable/disable the User Interface of device
                _device.ShowUI = showUI;
                // disable the User Interface after the image is acquired
                _device.DisableAfterAcquire = 1;

                // if UI is disabled
                if (!showUI) {
                    // open the device
                    _device.Open();

                    // set pixel type
                    _device.PixelType = pixelType;

                    if (_device.FeederPresent == 1) {
                        try {
                            _device.DocumentFeeder.Enabled = useAdf;

                            if (_device.DocumentFeeder.DuplexMode != 0)
                                _device.DocumentFeeder.DuplexEnabled = useDuplex;
                        }
                        catch (ex) {
                        }
                    }
                }

                // acquire image(s) from the device
                var acquireModalState;
                var acquireStatusString = "Scan canceled";
                do {
                    acquireModalState = _device.AcquireModal();

                    // image acquired
                    if (acquireModalState == 2) {
                        // add acquired image to the image collection
                        AcquiredImages1.Add(_device.AcquiredImage);
                        // go to the last image
                        GoToLastImage();
                    }

                        // scan completed
                    else if (acquireModalState == 3)
                        acquireStatusString = "Scan completed";

                        // scan failed
                    else if (acquireModalState == 4)
                        acquireStatusString = "Scan failed";

                        // scan canceled
                    else if (acquireModalState == 5)
                        acquireStatusString = "Scan canceled";
                }
                while (acquireModalState != 0)
            }
            catch (ex) {
                alert(ex.message);
            }
            finally {
                // disable the device if device is enabled
                if (_device.State == 2)
                    _device.Disable();
                // close the device if device is opened
                if (_device.State == 1)
                    _device.Close();

                alert(acquireStatusString);

                UpdateUI();
            }
        }


        // Navigate images.

        function GoToFirstImage() {
            if (AcquiredImages1.Count > 0) {
                _acquireImageIndex = 0;
                _acquiredImage = AcquiredImages1.Item(_acquireImageIndex);
                PreviewImage();
                UpdateUI();
            }
        }

        function GoToPreviousImage() {
            if ((AcquiredImages1.Count > 0) && ((_acquireImageIndex - 1) >= 0)) {
                _acquireImageIndex = _acquireImageIndex - 1;
                _acquiredImage = AcquiredImages1.Item(_acquireImageIndex);
                PreviewImage();
                UpdateUI();
            }
        }

        function GoToNextImage() {
            if ((AcquiredImages1.Count > 0) && ((_acquireImageIndex + 1) < AcquiredImages1.Count)) {
                _acquireImageIndex = _acquireImageIndex + 1;
                _acquiredImage = AcquiredImages1.Item(_acquireImageIndex);
                PreviewImage();
                UpdateUI();
            }
        }

        function GoToLastImage() {
            if (AcquiredImages1.Count > 0) {
                _acquireImageIndex = AcquiredImages1.Count - 1;
                _acquiredImage = AcquiredImages1.Item(_acquireImageIndex);
                PreviewImage();
                UpdateUI();
            }
        }


        // Delete image(s).

        function DeleteImage() {
            if (AcquiredImages1.Count > 0) {
                AcquiredImages1.Item(_acquireImageIndex).Dispose();

                AcquiredImages1.RemoveAt(_acquireImageIndex);

                if (AcquiredImages1.Count == 0) {
                    _acquireImageIndex = -1;
                    _acquiredImage = null;
                }
                else {
                    GoToFirstImage();
                }

                PreviewImage();
                UpdateUI();
            }
        }

        function DeleteAllImages() {
            if (AcquiredImages1.Count > 0) {
                _acquireImageIndex = -1;
                _acquiredImage = null;
                AcquiredImages1.ClearAndDisposeItems();
                PreviewImage();
                UpdateUI();
            }
        }


        // Edit image.

        function IsImageBlank() {
            if (_acquiredImage.IsBlank(0.01, 0) == 0)
                alert("Image is NOT blank");
            else
                alert("Image is blank.");
        }

        function InvertImage(contrast) {
            _acquiredImage.Invert();

            PreviewImage();
        }

        function ChangeImageBrightness(brightness) {
            _acquiredImage.ChangeBrightness(brightness);

            PreviewImage();
        }

        function ChangeImageContrast(contrast) {
            _acquiredImage.ChangeContrast(contrast);

            PreviewImage();
        }

        function CropImage() {
            imageWidth = _acquiredImage.ImageInfo.Width;
            imageHeight = _acquiredImage.ImageInfo.Height;
            if (imageWidth > 20 && imageHeight > 20)
                _acquiredImage.Crop(10, 10, imageWidth - 20, imageHeight - 20);

            PreviewImage();
            UpdateImagesInfo();
        }

        function ResizeImageCanvas() {
            var canvasWidth = _acquiredImage.ImageInfo.Width + 20
            var canvasHeight = _acquiredImage.ImageInfo.Height + 20
            _acquiredImage.ResizeCanvas(canvasWidth, canvasHeight, 0, 10, 10);

            PreviewImage();
            UpdateImagesInfo();
        }

        function RotateImage(angle) {
            _acquiredImage.Rotate(angle, 0);

            PreviewImage();
            UpdateImagesInfo();
        }
        function DespeckleImage() {
            _acquiredImage.Despeckle(8, 25, 30, 400);

            PreviewImage();
        }

        function DeskewImage() {
            _acquiredImage.Deskew(0, 5, 5);

            PreviewImage();
            UpdateImagesInfo();
        }

        function DetectImageBorder() {
            _acquiredImage.DetectBorder(5);

            PreviewImage();
            UpdateImagesInfo();
        }


        // Utils.

        function GetImageFileEncoderSettings(imageFileFormatRadioName, saveAllImages) {
            var imageFileFormats = document.getElementsByName(imageFileFormatRadioName);
            var imageEncoderSettings = TwainImageEncoderSettingsFactory1.GetTwainBmpEncoderSettings();
            
            // GIF
            if (imageFileFormats[1].checked)
            {
                imageEncoderSettings = TwainImageEncoderSettingsFactory1.GetTwainGifEncoderSettings();
            }
            // JPEG
            if (imageFileFormats[2].checked)
            {
                imageEncoderSettings = TwainImageEncoderSettingsFactory1.GetTwainJpegEncoderSettings();
            }
            // PDF
            if (imageFileFormats[3].checked)
            {
                imageEncoderSettings = TwainImageEncoderSettingsFactory1.GetTwainPdfEncoderSettings();
                imageEncoderSettings.PdfMultiPage = saveAllImages;
            }
            // PNG
            if (imageFileFormats[4].checked)
            {
                imageEncoderSettings = TwainImageEncoderSettingsFactory1.GetTwainPngEncoderSettings();
            }
            // TIFF
            if (imageFileFormats[5].checked)
            {
                imageEncoderSettings = TwainImageEncoderSettingsFactory1.GetTwainTiffEncoderSettings();
                imageEncoderSettings.TiffMultiPage = saveAllImages;
            }

            return imageEncoderSettings;
        }

        function GetFileExtension(imageFileFormatRadioName) {
            var imageFileFormats = document.getElementsByName(imageFileFormatRadioName);
            
            // GIF
            if (imageFileFormats[1].checked)
            {
                return ".gif";
            }
            // JPEG
            if (imageFileFormats[2].checked)
            {
                return ".jpg";
            }
            // PDF
            if (imageFileFormats[3].checked)
            {
                return ".pdf";
            }
            // PNG
            if (imageFileFormats[4].checked)
            {
                return ".png";
            }
            // TIFF
            if (imageFileFormats[5].checked)
            {
                return ".tif";
            }

            return ".bmp";
        }

        function GetImageStream(imageEncoderSettings, saveAllImages) {
            try {
                var imageStream;
                // if all images must be saved in multipage PDF or TIFF file
                if (saveAllImages) {
                    // get the image stream with the first acquired image
                    imageStream = AcquiredImages1.Item(0).GetAsStream(imageEncoderSettings);
                    // for the second and next acquired images
                    for (var i = 1; i < AcquiredImages1.Count; i++)
                        // save (add) acquired image to the image stream
                        AcquiredImages1.Item(i).SaveToStream(imageStream, imageEncoderSettings);
                }
                // if single image must be saved
                else {
                    imageStream = _acquiredImage.GetAsStream(imageEncoderSettings);
                }
            }
            catch (ex) {
                alert(ex.message);
            }

            return imageStream;
        }


        // Save image.

        function SaveImage() {
            try {
                var filepath = String(document.getElementById('SaveImagePath').value);
                if (filepath == "") {
                    alert('Image file path is not specified.');
                    return;
                }

                var saveAllImages = document.getElementById('SaveAllImages').checked;
                var imageEncoderSettings = GetImageFileEncoderSettings('SaveImageFormat', saveAllImages);
                filepath = filepath + GetFileExtension('SaveImageFormat');

                var addToMultiPageFile = document.getElementById('AddToMultiPageFile').checked;

                
                if (saveAllImages) {
                    for (var i = 0; i < AcquiredImages1.Count; i++)
                        AcquiredImages1.Item(i).SaveToFile(filepath, imageEncoderSettings);
                }
                else if (addToMultiPageFile) {
                    _acquiredImage.SaveToFile(filepath, imageEncoderSettings);
                }
                else {
                    _acquiredImage.SaveToFile(filepath, imageEncoderSettings);
                }

                alert("Image is saved successfully.");
            }
            catch (e) {
                alert("Image is not saved: " + e.message);
            }
        }


        // Upload image to HTTP(S) server.

        function UploadToHttpServer() {
            if (_acquiredImage == null)
                return;

            var httpUrl = String(document.getElementById('HttpUrlTextBox').value);
            var httpTextField1 = String(document.getElementById('HttpTextField1TextBox').value);
            var httpTextField1Value = String(document.getElementById('HttpTextField1ValueTextBox').value);
            var httpTextField2 = String(document.getElementById('HttpTextField2TextBox').value);
            var httpTextField2Value = String(document.getElementById('HttpTextField2ValueTextBox').value);
            var httpFileField = String(document.getElementById('HttpFileFieldTextBox').value);
            var httpFileFieldValue = String(document.getElementById('HttpFileFieldValueTextBox').value);

            if (httpFileField == "") {
                alert('HTTP file name is not specified.');
                return;
            }
            if (httpFileFieldValue == "") {
                alert('HTTP file value is not specified.');
                return;
            }

            document.getElementById('HttpUploadButton').disabled = true;
            document.getElementById('HttpCancelButton').disabled = false;

            try {
                HttpUpload1.Url = httpUrl;
                HttpUpload1.UseDefaultCredentials = true;

                HttpUpload1.ClearTextFields();
                HttpUpload1.ClearFileFields();

                if (httpTextField1 != "")
                    HttpUpload1.AddTextField(httpTextField1, httpTextField1Value);
                if (httpTextField2 != "")
                    HttpUpload1.AddTextField(httpTextField2, httpTextField2Value);

                var saveAllImages = document.getElementById('UploadAllImagesToHttp').checked;
                var imageEncoderSettings = GetImageFileEncoderSettings('HttpUploadImageFileFormat', saveAllImages);
                var imageFileName = httpFileFieldValue + GetFileExtension('HttpUploadImageFileFormat');
                var imageFileStream = GetImageStream(imageEncoderSettings, saveAllImages);
                HttpUpload1.AddFileField(httpFileField, imageFileName, imageFileStream);

                if (HttpUpload1.PostData() == 0) {
                    alert(HttpUpload1.ErrorString);
                    document.getElementById('HttpUploadButton').disabled = false;
                    document.getElementById('HttpCancelButton').disabled = true;
                }
                else
                    setTimeout("HttpUploadStatus()", 10);
            }
            catch (e) {
                alert(e.message);
                document.getElementById('HttpUploadButton').disabled = false;
                document.getElementById('HttpCancelButton').disabled = true;
            }
        }

        function HttpUploadStatus() {
            var statString = HttpUpload1.statusString;
            if (HttpUpload1.statusCode == 3)
                statString = statString + " Uploaded " + String(HttpUpload1.bytesUploaded) + " bytes from " + String(HttpUpload1.BytesTotal) + " bytes.";
            window.status = statString;
            if ((HttpUpload1.statusCode == 5) || (HttpUpload1.errorCode != 0)) {
                if (HttpUpload1.errorCode == 0) {
                    if (HttpUpload1.responseCode == 200) {
                        alert("HTTP: Image is uploaded successfully!");
                        alert("Response content: " + HttpUpload1.responseContent);
                    }
                    else {
                        alert("Response code: " + HttpUpload1.responseCode);
                        alert("Response string: " + HttpUpload1.responseString);
                    }
                }
                else {
                    alert("Error: " + HttpUpload1.errorString);
                }
                window.status = "";
                document.getElementById('HttpUploadButton').disabled = false;
                document.getElementById('HttpCancelButton').disabled = true;
            }
            else
                setTimeout("HttpUploadStatus()", 10);
        }

        function CancelUploadToHttpServer() {
            HttpUpload1.Abort()
        }


        // Upload image to FTP server.

        function UploadToFtpServer() {
            document.getElementById('FtpUploadButton').disabled = true;
            document.getElementById('FtpCancelButton').disabled = false;

            var ftpHost = String(document.getElementById('FtpHostTextBox').value);
            var ftpUser = String(document.getElementById('FtpUserTextBox').value);
            var ftpPassword = String(document.getElementById('FtpPasswordTextBox').value);
            var ftpPath = String(document.getElementById('FtpPathTextBox').value);
            var ftpFileName = String(document.getElementById('FtpFileNameTextBox').value);

            try {
                FtpUpload1.Host = ftpHost;
                FtpUpload1.Port = 21;
                FtpUpload1.PassiveMode = true;
                FtpUpload1.User = ftpUser;
                FtpUpload1.Password = ftpPassword;
                FtpUpload1.Path = ftpPath;

                FtpUpload1.ClearFiles();

                var saveAllImages = document.getElementById('UploadAllImagesToFtp').checked;
                var imageEncoderSettings = GetImageFileEncoderSettings('FtpUploadImageFileFormat', saveAllImages);
                var imageFileName = ftpFileName + GetFileExtension('FtpUploadImageFileFormat');
                var imageFileStream = GetImageStream(imageEncoderSettings, saveAllImages);
                FtpUpload1.AddFile(imageFileName, imageFileStream);

                if (FtpUpload1.PostData() == 0) {
                    alert(FtpUpload1.ErrorString);
                    document.getElementById('FtpUploadButton').disabled = false;
                    document.getElementById('FtpCancelButton').disabled = true;
                }
                else setTimeout("FtpUploadStatus()", 10);
            }
            catch (e) {
                alert(e.message);
                document.getElementById('FtpUploadButton').disabled = false;
                document.getElementById('FtpCancelButton').disabled = true;
            }
        }

        function FtpUploadStatus() {
            var statString = FtpUpload1.statusString;
            if (FtpUpload1.statusCode == 9)
                statString = statString + " Uploaded " + String(FtpUpload1.bytesUploaded) + " bytes from " + String(FtpUpload1.BytesTotal) + " bytes.";
            window.status = statString;
            if ((FtpUpload1.statusCode == 12) || (FtpUpload1.errorCode != 0)) {
                if (FtpUpload1.errorCode == 0) {
                    alert("FTP: Image is uploaded successfully!");
                }
                else {
                    alert("Error: " + FtpUpload1.errorString);
                }
                window.status = "";
                document.getElementById('FtpUploadButton').disabled = false;
                document.getElementById('FtpCancelButton').disabled = true;
            }
            else
                setTimeout("FtpUploadStatus()", 10);
        }

        function CancelUploadToFtpServer() {
            FtpUpload1.Abort();
        }


        // User Interface.

        function UpdateUI() {
            var isImageAcquired = 0;
            if (_acquiredImage != null)
                isImageAcquired = 1;

            var acquiredImagesCount = AcquiredImages1.Count;

            document.getElementById('GoToFirstImageButton').disabled = (acquiredImagesCount <= 1) || (_acquireImageIndex == 0);
            document.getElementById('GoToPreviousImageButton').disabled = (acquiredImagesCount <= 1) || (_acquireImageIndex == 0);
            document.getElementById('GoToNextImageButton').disabled = (acquiredImagesCount <= 1) || (_acquireImageIndex == (acquiredImagesCount - 1));
            document.getElementById('GoToLastImageButton').disabled = (acquiredImagesCount <= 1) || (_acquireImageIndex == (acquiredImagesCount - 1));
            document.getElementById('DeleteImageButton').disabled = !isImageAcquired;
            document.getElementById('DeleteAllImagesButton').disabled = !isImageAcquired;

            document.getElementById('IsImageBlankButton').disabled = !isImageAcquired;
            document.getElementById('InvertButton').disabled = !isImageAcquired;
            document.getElementById('IncreaseBrightnessButton').disabled = !isImageAcquired;
            document.getElementById('DecreaseBrightnessButton').disabled = !isImageAcquired;
            document.getElementById('IncreaseContrastButton').disabled = !isImageAcquired;
            document.getElementById('DecreaseContrastButton').disabled = !isImageAcquired;
            document.getElementById('CropButton').disabled = !isImageAcquired;
            document.getElementById('IncreaseCanvasButton').disabled = !isImageAcquired;
            document.getElementById('Rotate90Button').disabled = !isImageAcquired;
            document.getElementById('Rotate180Button').disabled = !isImageAcquired;
            document.getElementById('Rotate270Button').disabled = !isImageAcquired;
            document.getElementById('DespeckleButton').disabled = !isImageAcquired;
            document.getElementById('DeskewButton').disabled = !isImageAcquired;
            document.getElementById('DetectImageBorderButton').disabled = !isImageAcquired;

            document.getElementById('SaveImagedButton').disabled = !isImageAcquired;

            document.getElementById('HttpUploadButton').disabled = !isImageAcquired;

            document.getElementById('FtpUploadButton').disabled = !isImageAcquired;

            UpdateImagesInfo();
        }

        function UpdateImagesInfo() {
            var imagesInfo;
            if (_acquiredImage == null)
                imagesInfo = "No image";
            else {
                imagesInfo = "Image N" + (_acquireImageIndex + 1) + " from " + AcquiredImages1.Count + " images";
                imagesInfo = imagesInfo + "<br />";
                imagesInfo = imagesInfo + _acquiredImage.ImageInfo.Width + "x" + _acquiredImage.ImageInfo.Height
                imagesInfo = imagesInfo + ", " + _acquiredImage.ImageInfo.BitCount + "bpp"
                imagesInfo = imagesInfo + ", " + _acquiredImage.ImageInfo.Resolution.Horizontal + "x" + _acquiredImage.ImageInfo.Resolution.Vertical + " dpi"
            }

            document.getElementById('ImagesInfo').innerHTML = imagesInfo;
        }

        function PreviewImage() {
            try {
                var previewImageObject = document.getElementById("PreviewImage");
                if (_acquiredImage != null) {
                    if (_acquiredImage.ImageInfo.BitCount <= 8) {
                        var encoderSetings = TwainImageEncoderSettingsFactory1.GetTwainPngEncoderSettings();
                        previewImageObject.src = "data:image/png;base64," + _acquiredImage.GetAsBase64String(encoderSetings);
                    }
                    else {
                        // restriction of evaluation version
                        var encoderSetings = TwainImageEncoderSettingsFactory1.GetTwainBmpEncoderSettings();
                        previewImageObject.src = "data:image/bmp;base64," + _acquiredImage.GetAsBase64String(encoderSetings);
                    }
                }
                else
                    previewImageObject.src = null;
            }
            catch (ex) {
                alert(ex.message);
            }
        }

        function onDevicesSelectChange() {
            //
            var objSel = document.getElementById("DevicesSelect");
            // get a reference to current device
            _device = DeviceManager1.GetDevices().GetDevice(objSel.selectedIndex);
        }

        function OnPageUnload() {
            if (DeviceManager1.IsTwainAvailable != null) {
                if (_device != null) {
                    // disable the device if device is enabled
                    if (_device.State == 2)
                        _device.Disable();
                    // close the device if device is opened
                    if (_device.State == 1)
                        _device.Close();
                }

                // close the device manager
                if (DeviceManager1.State != 0)
                    DeviceManager1.Close();
            }
        }
    </script>
</head>

<body onunload="JavaScript:OnPageUnload()">
    <center>
        <h2><a href="http://www.vintasoft.com/vstwain-dotnet-index.html" target="_blank">VintaSoft Twain .NET</a> HTML Demo for Internet Explorer</h2>
        This demo shows how to acquire image(s) from scanner, process acquired image,<br />
        save acquired image to a disk or upload to HTTP(S) or FTP server.<br />
        <a href="http://www.vintasoft.com/docs/vstwain-dotnet/Deploying_Twain_WebApp.html" target="_blank">Deployment requirements</a><br />
        <br />

        <object id="DeviceManager1" width="1" height="1"
                classid="Vintasoft.Twain.dll#Vintasoft.Twain.DeviceManager"
                codebase="Vintasoft.Twain.dll#version=10,0,0,3">
        </object>

        <object id="AcquiredImages1" width="1" height="1"
                classid="Vintasoft.Twain.dll#Vintasoft.Twain.AcquiredImageCollection"
                codebase="Vintasoft.Twain.dll#version=10,0,0,3"></object>

        <object id="TwainImageEncoderSettingsFactory1" width="1" height="1"
                classid="Vintasoft.Twain.dll#Vintasoft.Twain.ImageEncoders.TwainImageEncoderSettingsFactory"
                codebase="Vintasoft.Twain.dll#version=10,0,0,3"></object>

        <object id="FtpUpload1" width="1" height="1"
                classid="Vintasoft.Twain.dll#Vintasoft.Twain.ImageUploading.Ftp.FtpUpload"
                codebase="Vintasoft.Twain.dll#version=10,0,0,3"></object>
        <object id="HttpUpload1" width="1" height="1"
                classid="Vintasoft.Twain.dll#Vintasoft.Twain.ImageUploading.Http.HttpUpload"
                codebase="Vintasoft.Twain.dll#version=10,0,0,3"></object>


        <form id="ScanImageForm" action="">
            <label for="DevicesSelect">Devices:</label>
            <select id="DevicesSelect" onchange="JavaScript:onDevicesSelectChange()"></select>
            <br />
            <br />

            <input type="checkbox" id="ShowUI" checked="checked" />Show UI
            <input type="checkbox" id="UseADF" />Use ADF
            <input type="checkbox" id="UseDuplex" />Use Duplex
            <br />

            <label for="ScanPixelType">Pixel Type:</label>
            <input type="radio" name="ScanPixelType" value="0" />Black-White
            <input type="radio" name="ScanPixelType" value="1" checked="checked" />Gray
            <input type="radio" name="ScanPixelType" value="2" />Color
            <br />

            <br />

            <input type="button" id="ScanImageButton" value="Scan Image" onclick="JavaScript:ScanImage()" />
        </form>
        <div id="ErrorString"></div>

        <script language="JavaScript" type="text/javascript">
            if (DeviceManager1.IsTwainAvailable != null) {
                var isTwainAvailable = true;
                // specify that TWAIN 1.x Data Source Manager should be used
                DeviceManager1.IsTwain2Compatible = false;
                // if TWAIN 1.x Data Source Manager is not available
                if (DeviceManager1.IsTwainAvailable == false)
                {
                    // specify that TWAIN 2.x Data Source Manager should be used
                    DeviceManager1.IsTwain2Compatible = true;
                    
                    // if TWAIN 2.x Data Source Manager is not available
                    if (DeviceManager1.IsTwainAvailable == false)
                    {
                        alert('TWAIN Data Source Manager is not available.');
                        isTwainAvailable = false;
                    }
                }

                if (isTwainAvailable)
                {
                    // open the data source manager
                    DeviceManager1.Open();

                    if (DeviceManager1.GetDevices().Count > 0) {
                        //
                        var objSel = document.getElementById("DevicesSelect");
                        for (var i = 0; i < DeviceManager1.GetDevices().Count; i++) {
                            objSel.options.length = objSel.options.length + 1;
                            objSel.options[i].text = DeviceManager1.GetDevices().Item(i).Info.ProductName;
                            objSel.options[i].value = DeviceManager1.GetDevices().Item(i);
                        }

                        // get a reference to the default device
                        _device = DeviceManager1.GetDefaultDevice();

                        //
                        var currentDeviceProductName = _device.Info.ProductName;
                        for (var i = 0; i < objSel.options.length; i++) {
                            if (objSel.options[i].text == currentDeviceProductName) {
                                objSel.selectedIndex = i;
                                break;
                            }
                        }
                    }
                }
            }
        </script>

        <hr width="400" />

        <h3>Acquired images</h3>
        <form id="ImageNavigationForm" action="">
            <img id="PreviewImage" src="" width="350" height="270" alt="Preview of scanned image" border="1" />
            <br />

            <div id="ImagesInfo">No image<br /></div>
            <br />

            <input type="button" value="First Image" id="GoToFirstImageButton" onclick="JavaScript:GoToFirstImage()" disabled="disabled" />
            <input type="button" value="Previous Image" id="GoToPreviousImageButton" onclick="JavaScript:GoToPreviousImage()" disabled="disabled" />
            <input type="button" value="Next Image" id="GoToNextImageButton" onclick="JavaScript:GoToNextImage()" disabled="disabled" />
            <input type="button" value="Last Image" id="GoToLastImageButton" onclick="JavaScript:GoToLastImage()" disabled="disabled" />
            <br />

            <input type="button" value="Delete Image" id="DeleteImageButton" onclick="JavaScript:DeleteImage()" disabled="disabled" />
            <input type="button" value="Delete All Images" id="DeleteAllImagesButton" onclick="JavaScript:DeleteAllImages()" disabled="disabled" />
        </form>
        <hr width="400" />


        <h3>Edit acquired image</h3>
        <form id="EditImageForm" action="">
            <input type="button" value="Is Image Blank?" id="IsImageBlankButton" onclick="JavaScript:IsImageBlank()" disabled="disabled" />
            &nbsp; &nbsp;
            <input type="button" value="Invert" id="InvertButton" onclick="JavaScript:InvertImage()" disabled="disabled" />
            <br />

            <input type="button" value="Increase Brightness" id="IncreaseBrightnessButton" onclick="JavaScript:ChangeImageBrightness(5)" disabled="disabled" />
            &nbsp; &nbsp;
            <input type="button" value="Decrease Brightness" id="DecreaseBrightnessButton" onclick="JavaScript:ChangeImageBrightness(-5)" disabled="disabled" />
            <br />

            <input type="button" value="Increase Contrast" id="IncreaseContrastButton" onclick="JavaScript:ChangeImageContrast(5)" disabled="disabled" />
            &nbsp; &nbsp;
            <input type="button" value="Decrease Contrast" id="DecreaseContrastButton" onclick="JavaScript:ChangeImageContrast(-5)" disabled="disabled" />
            <br />

            <input type="button" value="Crop" id="CropButton" onclick="JavaScript:CropImage()" disabled="disabled" />
            &nbsp; &nbsp;
            <input type="button" value="Increase Canvas" id="IncreaseCanvasButton" onclick="JavaScript:ResizeImageCanvas()" disabled="disabled" />
            <br />

            <input type="button" value="Rotate 90" id="Rotate90Button" onclick="JavaScript:RotateImage(90)" disabled="disabled" />
            &nbsp; &nbsp;
            <input type="button" value="Rotate 180" id="Rotate180Button" onclick="JavaScript:RotateImage(180)" disabled="disabled" />
            &nbsp; &nbsp;
            <input type="button" value="Rotate 270" id="Rotate270Button" onclick="JavaScript:RotateImage(270)" disabled="disabled" />
            <br />

            <input type="button" value="Despeckle" id="DespeckleButton" onclick="JavaScript:DespeckleImage()" disabled="disabled" />
            &nbsp; &nbsp;
            <input type="button" value="Deskew" id="DeskewButton" onclick="JavaScript:DeskewImage()" disabled="disabled" />
            &nbsp; &nbsp;
            <input type="button" value="Detect Border" id="DetectImageBorderButton" onclick="JavaScript:DetectImageBorder()" disabled="disabled" />
        </form>
        <hr width="400" />


        <h3>Save acquired image(s) to a local disk</h3>
        <form id="SaveImageForm" action="">
            Image path without file extension:
            <input type="text" size="50" value="d:\test" id="SaveImagePath" /><br />
            <input type="radio" name="SaveImageFormat" value="0" />BMP
            <input type="radio" name="SaveImageFormat" value="1" />GIF
            <input type="radio" name="SaveImageFormat" value="2" checked="checked" />JPEG
            <input type="radio" name="SaveImageFormat" value="3" />PDF
            <input type="radio" name="SaveImageFormat" value="4" />PNG
            <input type="radio" name="SaveImageFormat" value="5" />TIFF
            <br />
            <br />
            <input type="checkbox" id="AddToMultiPageFile" />Add acquired image to multipage TIFF or PDF file<br />
            <input type="checkbox" id="SaveAllImages" />Save all acquired images as multipage TIFF or PDF file<br />
            <br />
            <input type="button" onclick="JavaScript:SaveImage()" value="Save Image" id="SaveImagedButton" disabled="disabled" />
        </form>
        <hr width="400" />


        <h3>Upload acquired image(s) to HTTP(S) server</h3>
        <form id="UploadImageToHttpForm" action="">
            <table width="500" border="0" cellpadding="0">
                <tr>
                    <td width="100">HTTP(S) Url:</td>
                    <td width="400" colspan="3"><input type="text" size="55" value="http://demos.vintasoft.com/WebTwainDemo/ImageUpload.aspx" id="HttpUrlTextBox" /></td>
                </tr>
                <tr>
                    <td>File field:</td>
                    <td><input type="text" size="20" value="file" id="HttpFileFieldTextBox" /></td>
                    <td>Value:</td>
                    <td><input type="text" size="30" value="image" id="HttpFileFieldValueTextBox" /></td>
                </tr>
                <tr>
                    <td colspan="4">
                        <input type="radio" name="HttpUploadImageFileFormat" value="0" />BMP
                        <input type="radio" name="HttpUploadImageFileFormat" value="1" />GIF
                        <input type="radio" name="HttpUploadImageFileFormat" value="2" checked="checked" />JPEG
                        <input type="radio" name="HttpUploadImageFileFormat" value="3" />PDF
                        <input type="radio" name="HttpUploadImageFileFormat" value="4" />PNG
                        <input type="radio" name="HttpUploadImageFileFormat" value="5" />TIFF
                    </td>
                </tr>
                <tr>
                    <td>Text field 1:</td>
                    <td><input type="text" size="20" value="" id="HttpTextField1TextBox" /></td>
                    <td>Value:</td>
                    <td><input type="text" size="30" value="" id="HttpTextField1ValueTextBox" /></td>
                </tr>
                <tr>
                    <td>Text field 2:</td>
                    <td><input type="text" size="20" value="" id="HttpTextField2TextBox" /></td>
                    <td>Value:</td>
                    <td><input type="text" size="30" value="" id="HttpTextField2ValueTextBox" /></td>
                </tr>
            </table>
            <br />
            <input type="checkbox" id="UploadAllImagesToHttp" />Upload all acquired images as multipage TIFF or PDF file<br />
            <br />
            <input style="LEFT: 17px; WIDTH: 241px; TOP: 363px; HEIGHT: 29px" onclick="JavaScript:UploadToHttpServer()" type="button" size="34" value="Upload image to HTTP server" id="HttpUploadButton" disabled="disabled" />&nbsp;&nbsp;
            <input style="LEFT: 17px; WIDTH: 100px; TOP: 363px; HEIGHT: 29px" onclick="JavaScript:CancelUploadToHttpServer()" type="button" size="34" value="Cancel" id="HttpCancelButton" disabled="disabled" />
        </form>
        <hr width="400" />


        <h3>Upload acquired image(s) to FTP server</h3>
        <form id="UploadImageToFtpForm" action="">
            <table width="500" border="0" cellpadding="0">
                <tr>
                    <td width="100">FTP server:</td>
                    <td width="400"><input type="text" size="50" value="ftp.test.com" id="FtpHostTextBox" /></td>
                </tr>
                <tr>
                    <td>FTP user:</td>
                    <td><input type="text" size="50" value="guest" id="FtpUserTextBox" /></td>
                </tr>
                <tr>
                    <td>FTP password:</td>
                    <td><input type="password" size="50" value="" id="FtpPasswordTextBox" /></td>
                </tr>
                <tr>
                    <td>FTP path:</td>
                    <td><input type="text" size="50" value="/imgs/" id="FtpPathTextBox" /></td>
                </tr>
                <tr>
                    <td>FTP file name:</td>
                    <td><input type="text" size="50" value="image" id="FtpFileNameTextBox" /></td>
                </tr>
                <tr>
                    <td colspan="2">
                        <input type="radio" name="FtpUploadImageFileFormat" value="0" />BMP
                        <input type="radio" name="FtpUploadImageFileFormat" value="1" />GIF
                        <input type="radio" name="FtpUploadImageFileFormat" value="2" checked="checked" />JPEG
                        <input type="radio" name="FtpUploadImageFileFormat" value="3" />PDF
                        <input type="radio" name="FtpUploadImageFileFormat" value="4" />PNG
                        <input type="radio" name="FtpUploadImageFileFormat" value="5" />TIFF
                    </td>
                </tr>
            </table>
            <br />
            <input type="checkbox" id="UploadAllImagesToFtp" />Upload all acquired images as multipage TIFF or PDF file<br />
            <br />
            <input style="LEFT: 17px; WIDTH: 241px; TOP: 363px; HEIGHT: 29px" onclick="JavaScript:UploadToFtpServer()" type="button" size="34" value="Upload image to FTP server" id="FtpUploadButton" disabled="disabled" />&nbsp;&nbsp;
            <input style="LEFT: 17px; WIDTH: 100px; TOP: 363px; HEIGHT: 29px" onclick="JavaScript:CancelUploadToFtpServer()" type="button" size="34" value="Cancel" id="FtpCancelButton" disabled="disabled" />
        </form>

        <br />
        <br />

    </center>
</body>
</html>
