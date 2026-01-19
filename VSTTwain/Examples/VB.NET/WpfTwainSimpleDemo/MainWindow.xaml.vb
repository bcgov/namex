Imports System.Windows
Imports Vintasoft.WpfTwain

''' <summary>
''' Interaction logic for MainWindow.xaml
''' </summary>
Public Partial Class MainWindow
	Inherits Window

	#Region "Constructor"

	Public Sub New()
		InitializeComponent()

		Me.Title = String.Format("VintaSoft WPF TWAIN Simple Demo v{0}", TwainGlobalSettings.ProductVersion)
	End Sub

	#End Region



	#Region "Methods"

	''' <summary>
	''' Scans images.
	''' </summary>
	Private Sub scanImagesButton_Click(sender As Object, e As RoutedEventArgs)
		Try
			' disable application UI
			scanImagesButton.IsEnabled = False

			' create TWAIN device manager
			Using deviceManager As New DeviceManager(Me)
				' try to find TWAIN device manager
				deviceManager.IsTwain2Compatible = CBool(twain2CheckBox.IsChecked)
				' if TWAIN device manager is not found
				If Not deviceManager.IsTwainAvailable Then
					' try to find another TWAIN device manager
					deviceManager.IsTwain2Compatible = CBool(Not twain2CheckBox.IsChecked)
					' if TWAIN device manager is not found
					If Not deviceManager.IsTwainAvailable Then
						MessageBox.Show("TWAIN device manager is not found.")
						Return
					End If
				End If

				' open the device manager
				deviceManager.Open()

				' if devices are NOT found
                If deviceManager.Devices.Count = 0 Then
                    MessageBox.Show("Devices are not found.")
                    Return
                End If

				' if device is NOT selected
				If Not deviceManager.ShowDefaultDeviceSelectionDialog() Then
					MessageBox.Show("Device is not selected.")
					Return
				End If

				' get reference to the selected device
                Dim device As Device = deviceManager.DefaultDevice

				' set scan settings
				device.ShowUI = CBool(showUiCheckBox.IsChecked)
				device.ShowIndicators = CBool(showIndicatorsCheckBox.IsChecked)
                device.DisableAfterAcquire = Not device.ShowUI
                device.CloseAfterModalAcquire = False

                Dim totalImageCount As Integer = 0
                Dim imageCount As Integer = 0
                Dim acquireModalState1 As AcquireModalState = AcquireModalState.None
                Do
                    ' synchronously acquire image from device
                    acquireModalState1 = device.AcquireModal()
                    Select Case acquireModalState1
                        Case AcquireModalState.ImageAcquired
                            ' dispose previous bitmap source in the picture box
                            If image1.Source IsNot Nothing Then
                                image1.Source = Nothing
                            End If

                            ' set a bitmap source in the image control
                            image1.Source = device.AcquiredImage.GetAsBitmapSource()

                            imageCount += 1
                            totalImageCount += 1

                            ' dispose an acquired image
                            device.AcquiredImage.Dispose()

                            MessageBox.Show("Image is acquired.")
                            Exit Select

                        Case AcquireModalState.ScanCompleted
                            MessageBox.Show(String.Format("Scan is completed. {0} images are acquired in session. Total {1} images are scanned.", imageCount, totalImageCount))
                            imageCount = 0
                            Exit Select

                        Case AcquireModalState.ScanCanceled
                            MessageBox.Show("Scan is canceled.")
                            Exit Select

                        Case AcquireModalState.ScanFailed
                            MessageBox.Show(String.Format("Scan is failed: {0}", device.ErrorString))
                            Exit Select

                        Case AcquireModalState.UserInterfaceClosed
                            MessageBox.Show("User interface is closed.")
                            Exit Select
                    End Select
                Loop While acquireModalState1 <> AcquireModalState.None

                ' close the device
                device.Close()

                ' close the device manager
                deviceManager.Close()
			End Using
		Catch ex As TwainException
			MessageBox.Show(ex.Message)
		Finally
			' enable application UI
			scanImagesButton.IsEnabled = True
		End Try
	End Sub

	#End Region

End Class
