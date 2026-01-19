Imports System.Windows
Imports System.Windows.Input
Imports System.Windows.Controls

''' <summary>
''' Interaction logic for JpegSaveSettingForm.xaml
''' </summary>
Partial Public Class JpegSaveSettingsWindow
    Inherits Window

#Region "Properties"

    Private _quality As Integer = 90
    Public ReadOnly Property Quality() As Integer
        Get
            Return _quality
        End Get
    End Property

#End Region



#Region "Constructors"

    Public Sub New(ByVal owner As Window)
        InitializeComponent()

        Me.Owner = owner
    End Sub

#End Region



#Region "Methods"

    Private Sub bOk_Click(ByVal sender As Object, ByVal e As RoutedEventArgs)
        _quality = nJpegQuality.Value
        DialogResult = True
    End Sub

    Private Sub bCancel_Click(ByVal sender As Object, ByVal e As RoutedEventArgs)
        DialogResult = False
        Close()
    End Sub

#End Region

End Class
