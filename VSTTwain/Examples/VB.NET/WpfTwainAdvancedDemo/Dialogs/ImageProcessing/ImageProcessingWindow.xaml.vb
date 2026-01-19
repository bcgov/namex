Imports System.Windows
Imports System.Windows.Media
Imports Vintasoft.WpfTwain
Imports Vintasoft.WpfTwain.ImageProcessing

''' <summary>
''' Interaction logic for ImageProcessingWindow.xaml
''' </summary>
Partial Public Class ImageProcessingWindow
    Inherits Window

#Region "Fields"

    Private _image As AcquiredImage

#End Region



#Region "Constructors"

    Public Sub New()
        InitializeComponent()
    End Sub

    Public Sub New(ByVal image As AcquiredImage)
        Me.New()
        _image = image
    End Sub

#End Region



#Region "Methods"

    ''' <summary>
    ''' Windows is loaded.
    ''' </summary>
    ''' <param name="sender"></param>
    ''' <param name="e"></param>
    Private Sub Window_Loaded(ByVal sender As Object, ByVal e As RoutedEventArgs)
        commandsComboBox.Items.Add("Is Image Blank?")
        commandsComboBox.Items.Add("Invert")
        commandsComboBox.Items.Add("Change Brightness")
        commandsComboBox.Items.Add("Change Contrast")
        commandsComboBox.Items.Add("Crop")
        commandsComboBox.Items.Add("Resize Canvas")
        commandsComboBox.Items.Add("Rotate")
        commandsComboBox.Items.Add("Despeckle")
        commandsComboBox.Items.Add("Deskew")
        commandsComboBox.Items.Add("Remove Border")

        UpdateImage()
    End Sub

    ''' <summary>
    ''' Update the image on a window.
    ''' </summary>
    Private Sub UpdateImage()
        SyncLock _image
            ' dispose previous image if necessary
            If pictureBox1.Source IsNot Nothing Then
                'pictureBox1.Source.Dispose();
                pictureBox1.Source = Nothing
            End If

            '
            pictureBox1.Source = _image.GetAsBitmapSource()
            '
            UpdateImageScrolls()

            '
            Me.Title = String.Format("Image Processing - {0} bpp, {1}x{2}, {3}x{4} dpi", _image.ImageInfo.BitCount, _image.ImageInfo.Width, _image.ImageInfo.Height, _image.ImageInfo.Resolution.Horizontal, _image.ImageInfo.Resolution.Vertical)
        End SyncLock
    End Sub

    ''' <summary>
    ''' Update the scrolls of image.
    ''' </summary>
    Private Sub UpdateImageScrolls()
        If pictureBox1 IsNot Nothing AndAlso pictureBox1.Source IsNot Nothing Then
            If chkStretchImage.IsChecked = True Then
                pictureBox1.Width = imageScrollViewer.ViewportWidth
                pictureBox1.Height = imageScrollViewer.ViewportHeight
                pictureBox1.Stretch = Stretch.Fill
            Else
                pictureBox1.Width = pictureBox1.Source.Width
                pictureBox1.Height = pictureBox1.Source.Height
                pictureBox1.Stretch = Stretch.None
            End If
        End If
    End Sub

    ''' <summary>
    ''' Value of stretch check box is changed.
    ''' </summary>
    ''' <param name="sender"></param>
    ''' <param name="e"></param>
    Private Sub chkStretchImage_Checked(ByVal sender As Object, ByVal e As RoutedEventArgs)
        UpdateImageScrolls()
    End Sub

    ''' <summary>
    ''' Scrolls of the image scroll viewer is changed.
    ''' </summary>
    ''' <param name="sender"></param>
    ''' <param name="e"></param>
    Private Sub imageScrollViewer_ScrollChanged(ByVal sender As Object, ByVal e As System.Windows.Controls.ScrollChangedEventArgs)
        UpdateImageScrolls()
    End Sub

    ''' <summary>
    ''' Processing command is changed.
    ''' </summary>
    ''' <param name="sender"></param>
    ''' <param name="e"></param>
    Private Sub commandsComboBox_SelectionChanged(ByVal sender As Object, ByVal e As System.Windows.Controls.SelectionChangedEventArgs)
        param1Label.Visibility = Visibility.Hidden
        param1NumericUpDown.Visibility = Visibility.Hidden

        param2Label.Visibility = Visibility.Hidden
        param2NumericUpDown.Visibility = Visibility.Hidden

        param3Label.Visibility = Visibility.Hidden
        param3NumericUpDown.Visibility = Visibility.Hidden

        param4Label.Visibility = Visibility.Hidden
        param4NumericUpDown.Visibility = Visibility.Hidden

        Select Case DirectCast(commandsComboBox.SelectedValue, String)
            Case "Is Image Blank?"
                param1Label.Content = "Max Noise Level (%):"
                param1Label.Visibility = Visibility.Visible
                param1NumericUpDown.Minimum = 0
                param1NumericUpDown.Maximum = 100
                param1NumericUpDown.Value = 1
                param1NumericUpDown.Visibility = Visibility.Visible
                Exit Select

            Case "Change Brightness"
                param1Label.Content = "Brightness:"
                param1Label.Visibility = Visibility.Visible
                param1NumericUpDown.Minimum = -100
                param1NumericUpDown.Maximum = 100
                param1NumericUpDown.Value = 0
                param1NumericUpDown.Visibility = Visibility.Visible
                Exit Select

            Case "Change Contrast"
                param1Label.Content = "Contrast:"
                param1Label.Visibility = Visibility.Visible
                param1NumericUpDown.Minimum = -100
                param1NumericUpDown.Maximum = 100
                param1NumericUpDown.Value = 0
                param1NumericUpDown.Visibility = Visibility.Visible
                Exit Select

            Case "Crop"
                param1Label.Content = "Left:"
                param1Label.Visibility = Visibility.Visible
                param1NumericUpDown.Minimum = 0
                param1NumericUpDown.Maximum = _image.ImageInfo.Width - 1
                param1NumericUpDown.Value = 0
                param1NumericUpDown.Visibility = Visibility.Visible

                param2Label.Content = "Top:"
                param2Label.Visibility = Visibility.Visible
                param2NumericUpDown.Minimum = 0
                param2NumericUpDown.Maximum = _image.ImageInfo.Height - 1
                param2NumericUpDown.Value = 0
                param2NumericUpDown.Visibility = Visibility.Visible

                param3Label.Content = "Width:"
                param3Label.Visibility = Visibility.Visible
                param3NumericUpDown.Minimum = 0
                param3NumericUpDown.Maximum = _image.ImageInfo.Width
                param3NumericUpDown.Value = _image.ImageInfo.Width
                param3NumericUpDown.Visibility = Visibility.Visible

                param4Label.Content = "Height:"
                param4Label.Visibility = Visibility.Visible
                param4NumericUpDown.Minimum = 0
                param4NumericUpDown.Maximum = _image.ImageInfo.Height
                param4NumericUpDown.Value = _image.ImageInfo.Height
                param4NumericUpDown.Visibility = Visibility.Visible
                Exit Select

            Case "Resize Canvas"
                param1Label.Content = "Canvas Width:"
                param1Label.Visibility = Visibility.Visible
                param1NumericUpDown.Minimum = _image.ImageInfo.Width
                param1NumericUpDown.Maximum = 2 * _image.ImageInfo.Width
                param1NumericUpDown.Value = _image.ImageInfo.Width
                param1NumericUpDown.Visibility = Visibility.Visible

                param2Label.Content = "Canvas Height:"
                param2Label.Visibility = Visibility.Visible
                param2NumericUpDown.Minimum = _image.ImageInfo.Height
                param2NumericUpDown.Maximum = 2 * _image.ImageInfo.Height
                param2NumericUpDown.Value = _image.ImageInfo.Height
                param2NumericUpDown.Visibility = Visibility.Visible

                param3Label.Content = "Image X Pos:"
                param3Label.Visibility = Visibility.Visible
                param3NumericUpDown.Minimum = 0
                param3NumericUpDown.Maximum = _image.ImageInfo.Width
                param3NumericUpDown.Value = 0
                param3NumericUpDown.Visibility = Visibility.Visible

                param4Label.Content = "Image Y Pos:"
                param4Label.Visibility = Visibility.Visible
                param4NumericUpDown.Minimum = 0
                param4NumericUpDown.Maximum = _image.ImageInfo.Height
                param4NumericUpDown.Value = 0
                param4NumericUpDown.Visibility = Visibility.Visible
                Exit Select

            Case "Rotate"
                param1Label.Content = "Angle:"
                param1Label.Visibility = Visibility.Visible
                param1NumericUpDown.Minimum = 0
                param1NumericUpDown.Maximum = 360
                param1NumericUpDown.Value = 90
                param1NumericUpDown.Visibility = Visibility.Visible
                Exit Select

            Case "Despeckle"
                param1Label.Content = "Level1:"
                param1Label.Visibility = Visibility.Visible
                param1NumericUpDown.Minimum = 0
                param1NumericUpDown.Maximum = 100
                param1NumericUpDown.Value = 8
                param1NumericUpDown.Visibility = Visibility.Visible

                param2Label.Content = "Level2:"
                param2Label.Visibility = Visibility.Visible
                param2NumericUpDown.Minimum = 0
                param2NumericUpDown.Maximum = 100
                param2NumericUpDown.Value = 25
                param2NumericUpDown.Visibility = Visibility.Visible

                param3Label.Content = "Radius:"
                param3Label.Visibility = Visibility.Visible
                param3NumericUpDown.Minimum = 0
                param3NumericUpDown.Maximum = 100
                param3NumericUpDown.Value = 30
                param3NumericUpDown.Visibility = Visibility.Visible

                param4Label.Content = "Level3:"
                param4Label.Visibility = Visibility.Visible
                param4NumericUpDown.Minimum = 0
                param4NumericUpDown.Maximum = 3000
                param4NumericUpDown.Value = 400
                param4NumericUpDown.Visibility = Visibility.Visible
                Exit Select

            Case "Deskew"
                param1Label.Content = "Scan Interval X:"
                param1Label.Visibility = Visibility.Visible
                param1NumericUpDown.Minimum = 1
                param1NumericUpDown.Maximum = 31
                param1NumericUpDown.Value = 5
                param1NumericUpDown.Visibility = Visibility.Visible

                param2Label.Content = "Scan Interval Y:"
                param2Label.Visibility = Visibility.Visible
                param2NumericUpDown.Minimum = 1
                param2NumericUpDown.Maximum = 31
                param2NumericUpDown.Value = 5
                param2NumericUpDown.Visibility = Visibility.Visible
                Exit Select

            Case "Remove Border"
                param1Label.Content = "Border Size:"
                param1Label.Visibility = Visibility.Visible
                param1NumericUpDown.Minimum = 0
                param1NumericUpDown.Maximum = 100
                param1NumericUpDown.Value = 5
                param1NumericUpDown.Visibility = Visibility.Visible
                Exit Select
        End Select
    End Sub

    ''' <summary>
    ''' Run the processing command.
    ''' </summary>
    ''' <param name="sender"></param>
    ''' <param name="e"></param>
    Private Sub runCommandButton_Click(ByVal sender As Object, ByVal e As RoutedEventArgs)
        SyncLock _image
            AddHandler _image.Progress, New EventHandler(Of AcquiredImageProcessingProgressEventArgs)(AddressOf ImageProcessingProgress)

            Try
                Select Case commandsComboBox.Text
                    Case "Is Image Blank?"
                        Dim maxNoiseLevel As Integer = CInt(param1NumericUpDown.Value)
                        Dim currentNoiseLevel As Single = 0
                        If _image.IsBlank(maxNoiseLevel, currentNoiseLevel) Then
                            MessageBox.Show(String.Format("Image is blank. Current noise level = {0}%", currentNoiseLevel))
                        Else
                            MessageBox.Show(String.Format("Image is NOT blank. Current noise level = {0}%", currentNoiseLevel))
                        End If
                        Exit Select

                    Case "Invert"
                        _image.Invert()
                        Exit Select

                    Case "Change Brightness"
                        Dim brightness As Integer = CInt(param1NumericUpDown.Value)
                        _image.ChangeBrightness(brightness)
                        Exit Select

                    Case "Change Contrast"
                        Dim contrast As Integer = CInt(param1NumericUpDown.Value)
                        _image.ChangeContrast(contrast)
                        Exit Select

                    Case "Crop"
                        Dim left As Integer = CInt(param1NumericUpDown.Value)
                        Dim top As Integer = CInt(param2NumericUpDown.Value)
                        Dim width As Integer = CInt(param3NumericUpDown.Value)
                        Dim height As Integer = CInt(param4NumericUpDown.Value)
                        Try
                            _image.Crop(left, top, width, height)
                        Catch ex As ArgumentOutOfRangeException
                            MessageBox.Show(ex.Message)
                        End Try
                        Exit Select

                    Case "Resize Canvas"
                        Dim canvasWidth As Integer = CInt(param1NumericUpDown.Value)
                        Dim canvasHeight As Integer = CInt(param2NumericUpDown.Value)
                        Dim imageXPosition As Integer = CInt(param3NumericUpDown.Value)
                        Dim imageYPosition As Integer = CInt(param4NumericUpDown.Value)
                        Try
                            _image.ResizeCanvas(canvasWidth, canvasHeight, BorderColor.AutoDetect, imageXPosition, imageYPosition)
                        Catch ex As ArgumentOutOfRangeException
                            MessageBox.Show(ex.Message)
                        End Try
                        Exit Select

                    Case "Rotate"
                        Dim angle As Integer = CInt(param1NumericUpDown.Value)
                        _image.Rotate(angle, BorderColor.AutoDetect)
                        Exit Select

                    Case "Despeckle"
                        Dim level1 As Integer = CInt(param1NumericUpDown.Value)
                        Dim level2 As Integer = CInt(param2NumericUpDown.Value)
                        Dim radius As Integer = CInt(param3NumericUpDown.Value)
                        Dim level3 As Integer = CInt(param4NumericUpDown.Value)
                        _image.Despeckle(level1, level2, radius, level3)
                        Exit Select

                    Case "Deskew"
                        Dim scanIntervalX As Integer = CInt(param1NumericUpDown.Value)
                        Dim scanIntervalY As Integer = CInt(param2NumericUpDown.Value)
                        _image.Deskew(BorderColor.AutoDetect, scanIntervalX, scanIntervalY)
                        Exit Select

                    Case "Remove Border"
                        Dim borderSize As Integer = CInt(param1NumericUpDown.Value)
                        _image.DetectBorder(borderSize)
                        Exit Select
                End Select
            Catch ex As ImagingException
                MessageBox.Show(ex.Message)
            End Try

            RemoveHandler _image.Progress, New EventHandler(Of AcquiredImageProcessingProgressEventArgs)(AddressOf ImageProcessingProgress)

            UpdateImage()
        End SyncLock
    End Sub

    ''' <summary>
    ''' Progress of processing command is changed.
    ''' </summary>
    ''' <param name="sender"></param>
    ''' <param name="e"></param>
    Private Sub ImageProcessingProgress(ByVal sender As Object, ByVal e As AcquiredImageProcessingProgressEventArgs)
        processingCommandProgressBar.Value = e.Progress
    End Sub

#End Region

End Class
