Imports System.Windows.Forms
Imports System.Drawing
Imports Vintasoft.Twain
Imports Vintasoft.Twain.ImageProcessing

Partial Public Class ImageProcessingForm
    Inherits Form

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

        UpdateImage()
    End Sub

#End Region



#Region "Methods"

    ''' <summary>
    ''' Update the image on a form.
    ''' </summary>
    Private Sub UpdateImage()
        SyncLock _image
            If pictureBox1.Image IsNot Nothing Then
                pictureBox1.Image.Dispose()
                pictureBox1.Image = Nothing
            End If

            pictureBox1.Image = _image.GetAsBitmap()

            Me.Text = String.Format("Image Processing - {0} bpp, {1}x{2}, {3}x{4} dpi", _image.ImageInfo.BitCount, _image.ImageInfo.Width, _image.ImageInfo.Height, _image.ImageInfo.Resolution.Horizontal, _image.ImageInfo.Resolution.Vertical)
        End SyncLock
    End Sub

    ''' <summary>
    ''' Value of stretch check box is changed.
    ''' </summary>
    ''' <param name="sender"></param>
    ''' <param name="e"></param>
    Private Sub stretchImageCheckBox_CheckedChanged(ByVal sender As Object, ByVal e As EventArgs)
        If stretchImageCheckBox.Checked Then
            pictureBox1.Size = New Size(pictureBoxPanel.Size.Width - 2, pictureBoxPanel.Size.Height - 2)
            pictureBox1.SizeMode = PictureBoxSizeMode.StretchImage
        Else
            pictureBox1.SizeMode = PictureBoxSizeMode.AutoSize
        End If
    End Sub

    ''' <summary>
    ''' Form is resized.
    ''' </summary>
    ''' <param name="sender"></param>
    ''' <param name="e"></param>
    Private Sub ImageProcessingForm_Resize(ByVal sender As Object, ByVal e As EventArgs)
        If stretchImageCheckBox.Checked Then
            pictureBox1.Size = New Size(pictureBoxPanel.Size.Width - 2, pictureBoxPanel.Size.Height - 2)
        End If
    End Sub

    ''' <summary>
    ''' Processing command is changed.
    ''' </summary>
    ''' <param name="sender"></param>
    ''' <param name="e"></param>
    Private Sub commandsComboBox_SelectedIndexChanged(ByVal sender As Object, ByVal e As EventArgs)
        param1Label.Visible = False
        param1NumericUpDown.Visible = False

        param2Label.Visible = False
        param2NumericUpDown.Visible = False

        param3Label.Visible = False
        param3NumericUpDown.Visible = False

        param4Label.Visible = False
        param4NumericUpDown.Visible = False

        Select Case commandsComboBox.Text
            Case "Is Image Blank?"
                param1Label.Text = "Max Noise Level (%):"
                param1Label.Visible = True
                param1NumericUpDown.Minimum = 0
                param1NumericUpDown.Maximum = 100
                param1NumericUpDown.Value = 1
                param1NumericUpDown.Visible = True
                Exit Select

            Case "Change Brightness"
                param1Label.Text = "Brightness:"
                param1Label.Visible = True
                param1NumericUpDown.Minimum = -100
                param1NumericUpDown.Maximum = 100
                param1NumericUpDown.Value = 0
                param1NumericUpDown.Visible = True
                Exit Select

            Case "Change Contrast"
                param1Label.Text = "Contrast:"
                param1Label.Visible = True
                param1NumericUpDown.Minimum = -100
                param1NumericUpDown.Maximum = 100
                param1NumericUpDown.Value = 0
                param1NumericUpDown.Visible = True
                Exit Select

            Case "Crop"
                param1Label.Text = "Left:"
                param1Label.Visible = True
                param1NumericUpDown.Minimum = 0
                param1NumericUpDown.Maximum = _image.ImageInfo.Width - 1
                param1NumericUpDown.Value = 0
                param1NumericUpDown.Visible = True

                param2Label.Text = "Top:"
                param2Label.Visible = True
                param2NumericUpDown.Minimum = 0
                param2NumericUpDown.Maximum = _image.ImageInfo.Height - 1
                param2NumericUpDown.Value = 0
                param2NumericUpDown.Visible = True

                param3Label.Text = "Width:"
                param3Label.Visible = True
                param3NumericUpDown.Minimum = 0
                param3NumericUpDown.Maximum = _image.ImageInfo.Width
                param3NumericUpDown.Value = _image.ImageInfo.Width
                param3NumericUpDown.Visible = True

                param4Label.Text = "Height:"
                param4Label.Visible = True
                param4NumericUpDown.Minimum = 0
                param4NumericUpDown.Maximum = _image.ImageInfo.Height
                param4NumericUpDown.Value = _image.ImageInfo.Height
                param4NumericUpDown.Visible = True
                Exit Select

            Case "Resize Canvas"
                param1Label.Text = "Canvas Width:"
                param1Label.Visible = True
                param1NumericUpDown.Minimum = _image.ImageInfo.Width
                param1NumericUpDown.Maximum = 2 * _image.ImageInfo.Width
                param1NumericUpDown.Value = _image.ImageInfo.Width
                param1NumericUpDown.Visible = True

                param2Label.Text = "Canvas Height:"
                param2Label.Visible = True
                param2NumericUpDown.Minimum = _image.ImageInfo.Height
                param2NumericUpDown.Maximum = 2 * _image.ImageInfo.Height
                param2NumericUpDown.Value = _image.ImageInfo.Height
                param2NumericUpDown.Visible = True

                param3Label.Text = "Image X Pos:"
                param3Label.Visible = True
                param3NumericUpDown.Minimum = 0
                param3NumericUpDown.Maximum = _image.ImageInfo.Width
                param3NumericUpDown.Value = 0
                param3NumericUpDown.Visible = True

                param4Label.Text = "Image Y Pos:"
                param4Label.Visible = True
                param4NumericUpDown.Minimum = 0
                param4NumericUpDown.Maximum = _image.ImageInfo.Height
                param4NumericUpDown.Value = 0
                param4NumericUpDown.Visible = True
                Exit Select

            Case "Rotate"
                param1Label.Text = "Angle:"
                param1Label.Visible = True
                param1NumericUpDown.Minimum = 0
                param1NumericUpDown.Maximum = 360
                param1NumericUpDown.Value = 90
                param1NumericUpDown.Visible = True
                Exit Select

            Case "Despeckle"
                param1Label.Text = "Level1:"
                param1Label.Visible = True
                param1NumericUpDown.Minimum = 0
                param1NumericUpDown.Maximum = 100
                param1NumericUpDown.Value = 8
                param1NumericUpDown.Visible = True

                param2Label.Text = "Level2:"
                param2Label.Visible = True
                param2NumericUpDown.Minimum = 0
                param2NumericUpDown.Maximum = 100
                param2NumericUpDown.Value = 25
                param2NumericUpDown.Visible = True

                param3Label.Text = "Radius:"
                param3Label.Visible = True
                param3NumericUpDown.Minimum = 0
                param3NumericUpDown.Maximum = 100
                param3NumericUpDown.Value = 30
                param3NumericUpDown.Visible = True

                param4Label.Text = "Level3:"
                param4Label.Visible = True
                param4NumericUpDown.Minimum = 0
                param4NumericUpDown.Maximum = 3000
                param4NumericUpDown.Value = 400
                param4NumericUpDown.Visible = True
                Exit Select

            Case "Deskew"
                param1Label.Text = "Scan Interval X:"
                param1Label.Visible = True
                param1NumericUpDown.Minimum = 1
                param1NumericUpDown.Maximum = 31
                param1NumericUpDown.Value = 5
                param1NumericUpDown.Visible = True

                param2Label.Text = "Scan Interval Y:"
                param2Label.Visible = True
                param2NumericUpDown.Minimum = 1
                param2NumericUpDown.Maximum = 31
                param2NumericUpDown.Value = 5
                param2NumericUpDown.Visible = True
                Exit Select

            Case "Remove Border"
                param1Label.Text = "Border Size:"
                param1Label.Visible = True
                param1NumericUpDown.Minimum = 0
                param1NumericUpDown.Maximum = 100
                param1NumericUpDown.Value = 5
                param1NumericUpDown.Visible = True
                Exit Select
        End Select
    End Sub

    ''' <summary>
    ''' Run the processing command.
    ''' </summary>
    ''' <param name="sender"></param>
    ''' <param name="e"></param>
    Private Sub runCommandButton_Click(ByVal sender As Object, ByVal e As EventArgs)
        SyncLock _image
            AddHandler _image.Progress, New EventHandler(Of AcquiredImageProcessingProgressEventArgs)(AddressOf ImageProcessingProgress)

            Try
                Select Case commandsComboBox.Text
                    Case "Is Image Blank?"
                        Dim maxNoiseLevel As Integer = CInt(Math.Truncate(param1NumericUpDown.Value))
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
                        Dim brightness As Integer = CInt(Math.Truncate(param1NumericUpDown.Value))
                        _image.ChangeBrightness(brightness)
                        Exit Select

                    Case "Change Contrast"
                        Dim contrast As Integer = CInt(Math.Truncate(param1NumericUpDown.Value))
                        _image.ChangeContrast(contrast)
                        Exit Select

                    Case "Crop"
                        Dim left As Integer = CInt(Math.Truncate(param1NumericUpDown.Value))
                        Dim top As Integer = CInt(Math.Truncate(param2NumericUpDown.Value))
                        Dim width As Integer = CInt(Math.Truncate(param3NumericUpDown.Value))
                        Dim height As Integer = CInt(Math.Truncate(param4NumericUpDown.Value))
                        Try
                            _image.Crop(left, top, width, height)
                        Catch ex As ArgumentOutOfRangeException
                            MessageBox.Show(ex.Message)
                        End Try
                        Exit Select

                    Case "Resize Canvas"
                        Dim canvasWidth As Integer = CInt(Math.Truncate(param1NumericUpDown.Value))
                        Dim canvasHeight As Integer = CInt(Math.Truncate(param2NumericUpDown.Value))
                        Dim imageXPosition As Integer = CInt(Math.Truncate(param3NumericUpDown.Value))
                        Dim imageYPosition As Integer = CInt(Math.Truncate(param4NumericUpDown.Value))
                        Try
                            _image.ResizeCanvas(canvasWidth, canvasHeight, BorderColor.AutoDetect, imageXPosition, imageYPosition)
                        Catch ex As ArgumentOutOfRangeException
                            MessageBox.Show(ex.Message)
                        End Try
                        Exit Select

                    Case "Rotate"
                        Dim angle As Integer = CInt(Math.Truncate(param1NumericUpDown.Value))
                        _image.Rotate(angle, BorderColor.AutoDetect)
                        Exit Select

                    Case "Despeckle"
                        Dim level1 As Integer = CInt(Math.Truncate(param1NumericUpDown.Value))
                        Dim level2 As Integer = CInt(Math.Truncate(param2NumericUpDown.Value))
                        Dim radius As Integer = CInt(Math.Truncate(param3NumericUpDown.Value))
                        Dim level3 As Integer = CInt(Math.Truncate(param4NumericUpDown.Value))
                        _image.Despeckle(level1, level2, radius, level3)
                        Exit Select

                    Case "Deskew"
                        Dim scanIntervalX As Integer = CInt(Math.Truncate(param1NumericUpDown.Value))
                        Dim scanIntervalY As Integer = CInt(Math.Truncate(param2NumericUpDown.Value))
                        _image.Deskew(BorderColor.AutoDetect, scanIntervalX, scanIntervalY)
                        Exit Select

                    Case "Remove Border"
                        Dim borderSize As Integer = CInt(Math.Truncate(param1NumericUpDown.Value))
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
