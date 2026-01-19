Imports System.Windows.Forms
Imports Vintasoft.Twain
Imports Vintasoft.Twain.ImageEncoders

Partial Public Class TiffSaveSettingsForm
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

    Private _compression As TiffCompression = TiffCompression.Auto
    Public ReadOnly Property Compression() As TiffCompression
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
            createNewDocumentaddToDocumentRadioButton.Checked = True
            addToDocumentRadioButton.Enabled = False
        End If
    End Sub

#End Region


#Region "Methods"

    Private Sub okButton_Click(ByVal sender As Object, ByVal e As EventArgs)
        _saveAllImages = saveAllImagesaddToDocumentRadioButton.Checked

        _multiPage = addToDocumentRadioButton.Checked

        If noneCompressionRadioButton.Checked Then
            _compression = TiffCompression.None
        ElseIf ccittCompressionRadioButton.Checked Then
            _compression = TiffCompression.CCITGroup4
        ElseIf lzwCompressionRadioButton.Checked Then
            _compression = TiffCompression.LZW
        ElseIf jpegCompressionRadioButton.Checked Then
            _compression = TiffCompression.JPEG
            _jpegQuality = CInt(Math.Truncate(jpegQualityNumericUpDown.Value))
        ElseIf zipCompressionRadioButton.Checked Then
            _compression = TiffCompression.ZIP
        ElseIf autoCompressionRadioButton.Checked Then
            _compression = TiffCompression.Auto
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
