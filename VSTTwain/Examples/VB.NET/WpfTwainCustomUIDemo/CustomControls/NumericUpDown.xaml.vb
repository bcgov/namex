
Namespace CustomControls
    ''' <summary>
    ''' Represents a Windows spin box (also known as an up-down control) 
    ''' that displays numeric values.
    ''' </summary>
    ''' <remarks>
    ''' Equivalent of System.Windows.Forms.NumericUpDown class.
    ''' </remarks>
    Partial Public Class NumericUpDown
        Inherits System.Windows.Controls.UserControl

#Region "Fields"

        Private _updateText As Boolean = False

#End Region



#Region "Constructor"

        ''' <summary>
        ''' Initializes a new instance of the <see cref="NumericUpDown"/> class.
        ''' </summary>
        Public Sub New()
            InitializeComponent()

            _value = _minimum

            UpdateText()

            AddHandler valueText.TextChanged, New System.Windows.Controls.TextChangedEventHandler(AddressOf valueText_TextChanged)
            AddHandler valueText.LostFocus, New System.Windows.RoutedEventHandler(AddressOf valueText_LostFocus)
        End Sub

#End Region



#Region "Properties"

        Private _maximum As Integer = 100
        ''' <summary>
        ''' Gets or set the maximum value.
        ''' </summary>
        Public Property Maximum() As Integer
            Get
                Return _maximum
            End Get
            Set(ByVal value As Integer)
                If _maximum <> Value Then
                    If Value < _minimum Then
                        Value = _minimum
                    End If
                    _maximum = Value
                    If _value > _maximum Then
                        Value = _maximum
                    Else
                        UpdateUpDownButtonsEnabled()
                    End If
                End If
            End Set
        End Property

        Private _minimum As Integer = 0
        ''' <summary>
        ''' Gets or set the min value.
        ''' </summary>
        Public Property Minimum() As Integer
            Get
                Return _minimum
            End Get
            Set(ByVal value As Integer)
                If _minimum <> Value Then
                    If Value > _maximum Then
                        Value = _maximum
                    End If
                    _minimum = Value
                    If _value < _minimum Then
                        Value = _minimum
                    Else
                        UpdateUpDownButtonsEnabled()
                    End If
                End If
            End Set
        End Property

        Private _value As Integer
        ''' <summary>
        ''' Gets or sets the value assigned to the control.
        ''' </summary>
        Public Property Value() As Integer
            Get
                Return _value
            End Get
            Set(ByVal value As Integer)
                If Value <> _value Then
                    If Minimum <= Value AndAlso Value <= Maximum Then
                        _value = Value
                        UpdateText()
                        UpdateUpDownButtonsEnabled()
                        OnValueChanged(EventArgs.Empty)
                    End If
                End If
            End Set
        End Property

#End Region



#Region "Methods"

        ''' <summary>
        ''' Raises the ValueChanged event.
        ''' </summary>
        ''' <param name="args">An EventArgs that contains the event data.</param>
        Protected Overridable Sub OnValueChanged(ByVal args As EventArgs)
            RaiseEvent ValueChanged(Me, args)
        End Sub

        ''' <summary>
        ''' Update enable of up/down buttons.
        ''' </summary>
        Private Sub UpdateUpDownButtonsEnabled()
            If _value = _minimum Then
                downButton.IsEnabled = False
            ElseIf _value = _maximum Then
                upButton.IsEnabled = False
            Else
                If upButton.IsEnabled = False Then
                    upButton.IsEnabled = True
                End If
                If downButton.IsEnabled = False Then
                    downButton.IsEnabled = True
                End If
            End If
        End Sub

        ''' <summary>
        ''' upButton.Click event handler.
        ''' </summary>
        Private Sub upButton_Click(ByVal sender As Object, ByVal e As EventArgs)
            If Value < Maximum Then
                Value += 1
            End If
        End Sub

        ''' <summary>
        ''' downButton.Click event handler.
        ''' </summary>
        Private Sub downButton_Click(ByVal sender As Object, ByVal e As EventArgs)
            If Value > Minimum Then
                Value -= 1
            End If
        End Sub

        ''' <summary>
        ''' Update value text.
        ''' </summary>
        Private Sub UpdateText()
            _updateText = True
            valueText.Text = Value.ToString()
            _updateText = False
        End Sub

        ''' <summary>
        ''' valueText.TextChanged event handler.
        ''' </summary>
        Private Sub valueText_TextChanged(ByVal sender As Object, ByVal e As System.Windows.Controls.TextChangedEventArgs)
            If _updateText Then
                Return
            End If
            If valueText.Text = "" OrElse valueText.Text = "-" Then
                Return
            End If
            Dim value As Integer
            If Integer.TryParse(valueText.Text, value) Then
                If value >= Minimum AndAlso value <= Maximum Then
                    _value = value
                    If _value <> value Then
                        SetValueTextInternal(_value)
                    End If
                    UpdateUpDownButtonsEnabled()
                    OnValueChanged(EventArgs.Empty)
                End If
            End If
        End Sub

        ''' <summary>
        ''' valueText.LostFocus event handler.
        ''' </summary>
        Private Sub valueText_LostFocus(ByVal sender As Object, ByVal e As System.Windows.RoutedEventArgs)
            Dim value As Integer
            If Integer.TryParse(valueText.Text, value) Then
                If _value <> value Then
                    If value > Maximum Then
                        value = Maximum
                    ElseIf _value < Minimum Then
                        value = Minimum
                    End If
                    _value = value
                    SetValueTextInternal(_value)
                    UpdateUpDownButtonsEnabled()
                    OnValueChanged(EventArgs.Empty)
                End If
            Else
                SetValueTextInternal(_value)
            End If
        End Sub

        ''' <summary>
        ''' Sets a value in the TextBox.
        ''' </summary>
        Private Sub SetValueTextInternal(ByVal value As Integer)
            valueText.Text = value.ToString()
            valueText.CaretIndex = valueText.Text.Length
        End Sub

#End Region



#Region "Events"

        ''' <summary>
        ''' Occurs when the Value property changes.
        ''' </summary>
        Public Event ValueChanged As EventHandler(Of EventArgs)

#End Region

    End Class
End Namespace
