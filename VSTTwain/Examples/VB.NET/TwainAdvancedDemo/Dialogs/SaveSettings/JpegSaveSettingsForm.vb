Imports System.Windows.Forms

Partial Public Class JpegSaveSettingsForm
    Inherits Form
    Private _quality As Integer = 90
    Public ReadOnly Property Quality() As Integer
        Get
            Return _quality
        End Get
    End Property

    Public Sub New()
        InitializeComponent()
    End Sub

    Private Sub okButton_Click(ByVal sender As Object, ByVal e As EventArgs)
        _quality = CInt(Math.Truncate(qualityNumericUpDown.Value))
        DialogResult = DialogResult.OK
    End Sub
End Class
