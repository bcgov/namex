using System;
using System.Drawing;

namespace RegScan
{
    public class ImageObj
    {

        public const double LETTER_ASPECT_RATIO = 1.3;
        public const double LEGAL_ASPECT_RATIO = 1.6;

        private Bitmap _image;
        private PdfSharp.PageOrientation _orientation;
        private PdfSharp.PageSize _pageSize;

        public Bitmap Image { get { return _image; } set { _image = value; } }
        public PdfSharp.PageOrientation Orientation { get { return _orientation; } set { _orientation = value; } }
        public PdfSharp.PageSize PageSize { get { return _pageSize; } set { _pageSize = value; } }


        public ImageObj(Bitmap _Image, PdfSharp.PageOrientation _Orientation, PdfSharp.PageSize _PageSize)
        {
            _image = _Image;
            _orientation = _Orientation;
            _pageSize = _PageSize;
        }

        public void SetImage(Bitmap _Image)
        {
            _image = _Image;
        }

        public void Rotate()
        {
            _image.RotateFlip(RotateFlipType.Rotate90FlipX);
        }

        public static PdfSharp.PageSize GetPageSize(double _Width, double _Height)
        {
            double asceptRatio = (double)Math.Round(((decimal)(_Height / _Width)), 1);
            if (asceptRatio >= LEGAL_ASPECT_RATIO)
                return PdfSharp.PageSize.Legal;
            else
                return PdfSharp.PageSize.Letter;

        }
    }
}
