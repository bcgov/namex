Imports System.Windows.Forms
Imports Vintasoft.Twain
Imports Vintasoft.Twain.ImageEncoders

Partial Public Class PdfSaveSettingsForm
    Inherits Form

#Region "Fields & properties"

    Private _saveAllImages As Boolean = False
    Public ReadOnly Property SaveAllImages() As Boolean
        Get
            Return _saveAllImages
        End Get
    End Property

    Private _multiPage As Boolean = True
    Public ReadOnly Property MultiPage() As Boolean
        Get
            Return _multiPage
        End Get
    End Property

    Private _pdfACompatible As Boolean = True
    Public ReadOnly Property PdfACompatible() As Boolean
        Get
            Return _pdfACompatible
        End Get
    End Property

    Private _pdfAuthor As String = String.Empty
    Public ReadOnly Property PdfAuthor() As String
        Get
            Return _pdfAuthor
        End Get
    End Property

    Private _pdfTitle As String = String.Empty
    Public ReadOnly Property PdfTitle() As String
        Get
            Return _pdfTitle
        End Get
    End Property

    Private _compression As PdfImageCompression = PdfImageCompression.Auto
    Public ReadOnly Property Compression() As PdfImageCompression
        Get
            Return _compression
        End Get
    End Property

    Private _jpegQuality As Integer = 90
    Public ReadOnly Property JpegQuality() As Integer
        Get
            Return _jpegQuality
        End Get
    End Property

#End Region


#Region "Constructor"

    Public Sub New(ByVal isFileExist As Boolean)
        InitializeComponent()

        If Not isFileExist Then
            createNewDocumentRadioButton.Checked = True
            addToDocumentRadioButton.Enabled = False
        End If
    End Sub

#End Region


#Region "Methods"

    Private Sub okButton_Click(ByVal sender As Object, ByVal e As EventArgs)
        _saveAllImages = saveAllImagesRadioButton.Checked

        _multiPage = addToDocumentRadioButton.Checked
        _pdfACompatible = pdfACompatibleCheckBox.Checked
        _pdfAuthor = pdfAuthorTextBox.Text
        _pdfTitle = pdfTitleTextBox.Text

        If noneCompressionRadioButton.Checked Then
            _compression = PdfImageCompression.None
        ElseIf ccittCompressionRadioButton.Checked Then
            _compression = PdfImageCompression.CcittFax
        ElseIf lzwCompressionRadioButton.Checked Then
            _compression = PdfImageCompression.LZW
        ElseIf jpegCompressionRadioButton.Checked Then
            _compression = PdfImageCompression.JPEG
            _jpegQuality = CInt(Math.Truncate(jpegQualityNumericUpDown.Value))
        ElseIf zipCompressionRadioButton.Checked Then
            _compression = PdfImageCompression.ZIP
        ElseIf autoCompressionRadioButton.Checked Then
            _compression = PdfImageCompression.Auto
        End If

        DialogResult = DialogResult.OK
    End Sub

    Private Sub EnableJpegCompressionQuality(ByVal sender As Object, ByVal e As EventArgs)
        gbJpegCompression.Enabled = True
    End Sub

    Private Sub DisableJpegCompressionQuality(ByVal sender As Object, ByVal e As EventArgs)
        gbJpegCompression.Enabled = False
    End Sub

#End Region

End Class
