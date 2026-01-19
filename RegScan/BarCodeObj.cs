using BarCodeScanner;
using System.Drawing;

namespace RegScan
{
    class BarCodeObj
    {
        /// <summary>
        /// Used to specify what barcode type(s) to detect.
        /// </summary>
        public enum BarcodeType
        {
            /// <summary>Not specified</summary>
            None = 0,
            /// <summary>Code39</summary>
            Code39 = 1,
            /// <summary>EAN/UPC</summary>
            EAN = 2,
            /// <summary>Code128</summary>
            Code128 = 4,
            /// <summary>Use BarcodeType.All for all supported types</summary>
            All = Code39 | EAN | Code128

            // Note: Extend this enum with new types numbered as 8, 16, 32 ... ,
            //       so that we can use bitwise logic: All = Code39 | EAN | <your favorite type here> | ...
        }

        /// <summary>
        /// Used to specify whether to scan a page in vertical direction,
        /// horizontally, or both.
        /// </summary>
        public enum ScanDirection
        {
            /// <summary>Scan top-to-bottom</summary>
            Vertical = 1,
            /// <summary>Scan left-to-right</summary>
            Horizontal = 2
        }

        /// <summary>
        /// Scan the image for barcode type 39
        /// </summary>
        /// <param name="_BMP">Image to scan.</param>
        /// <returns>Collecation of bar code</returns>
        static public System.Collections.ArrayList Scan(Bitmap _BMP)
        {
            return Scan1(_BMP);

            //return Scan2(_BMP);
        }

        static private System.Collections.ArrayList Scan1(Bitmap _BMP)
        {
            var barcodes = new System.Collections.ArrayList();
            BarCodeScanner.BarCodeImageScanner.ScanPage(ref barcodes, _BMP, 100, BarCodeScanner.BarCodeImageScanner.ScanDirection.Vertical,
                                                        BarCodeImageScanner.BarcodeType.Code39);
            return barcodes;
        }

        static private System.Collections.ArrayList Scan2(Bitmap _BMP)
        {
            System.Collections.ArrayList barcodes = new System.Collections.ArrayList();
            return barcodes;
        }
    }
}
