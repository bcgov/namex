using PdfSharp.Drawing;
using PdfSharp.Pdf;
using PdfSharp.Pdf.IO;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;

namespace RegScan
{
    class PDFObj
    {
        static public string ErrorMessage = "";
        static public string ConvertImagesToPdf(List<Bitmap> _Images)
        {
            string ErrorMessage = "";
            string fileName = Path.GetTempFileName().Replace(".tmp", ".pdf");

            try
            {
                // Create and Save the document, then close it.
                var pdf = ImagesToPdf(_Images);
                pdf.Save(fileName);
                pdf.Close();

                // Now let ADOBE PDF Viewer display it.
                System.Diagnostics.Process.Start(fileName);

            }
            catch (Exception _Error)
            {
                ErrorMessage = _Error.Message;
                fileName = "";
            }

            return fileName;
        }

        // Display PDF file.
        static public string DisplayPdf(PdfDocument _PDF)
        {
            string ErrorMessage = "";
            string fileName = Path.GetTempFileName().Replace(".tmp", ".pdf");
            try
            {
                // Create and Save the document, then close it.
                _PDF.Save(fileName);
                _PDF.Close();

                // Now let ADOBE PDF Viewer display it.
                System.Diagnostics.Process.Start(fileName);

            }
            catch (Exception _Error)
            {
                ErrorMessage = _Error.Message;
                fileName = "";
            }

            return fileName;
        }

        // Converts a byte array to a pdf document
        static public PdfDocument ConvertByteArrayToPDF(byte[] _PDFByteArray)
        {
            return PdfReader.Open(new MemoryStream((byte[])_PDFByteArray));
        }

        // Converts an images list to a pdf document and returns it as a byte array.
        static public byte[] ConvertImagesToPdfToByteArray(List<Bitmap> _Images)
        {
            // Convert Images to PDF.
            return ConvertPdfToByteArray(ImagesToPdf(_Images));
        }

        // Convert PDF to byte array.
        static public byte[] ConvertPdfToByteArray(PdfDocument _PDF)
        {
            // Save pdf file to memory stream.
            MemoryStream ms = new MemoryStream();
            _PDF.Save(ms, true);
            return ms.ToArray();
        }

        // Creats a PDF file and adds the images to it.
        static public PdfDocument ImagesToPdf(List<Bitmap> _Images)
        {
            // Create a PDF document.
            var pdf = new PdfDocument();

            // FOREACH image create a new page.
            foreach (var bp in _Images)
            {
                // Create a new page and add in the image.
                var pdfPage = new PdfPage();
                pdf.AddPage(pdfPage);
                var xgr = XGraphics.FromPdfPage(pdfPage);
                var img = XImage.FromGdiPlusImage(bp);
                xgr.DrawImage(img, 0, 0);

            }

            return pdf;
        }
    }
}
