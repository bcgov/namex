using System;

namespace CustomControls
{
    /// <summary>
    /// Represents a Windows spin box (also known as an up-down control) 
    /// that displays numeric values.
    /// </summary>
    /// <remarks>
    /// Equivalent of <see cref="System.Windows.Forms.NumericUpDown"/> class.
    /// </remarks>
    public partial class NumericUpDown : System.Windows.Controls.UserControl
    {

        #region Fields

        bool _updateText = false;
        
        #endregion



        #region Constructor

        /// <summary>
        /// Initializes a new instance of the <see cref="NumericUpDown"/> class.
        /// </summary>
        public NumericUpDown()
        {
            InitializeComponent();
            
            _value = _minimum;
            
            UpdateText();

            valueText.TextChanged += new System.Windows.Controls.TextChangedEventHandler(valueText_TextChanged);
            valueText.LostFocus += new System.Windows.RoutedEventHandler(valueText_LostFocus);
        }

        #endregion



        #region Properties

        private int _maximum = 100;
        /// <summary>
        /// Gets or set the maximum value.
        /// </summary>
        public int Maximum
        {
            get
            {
                return _maximum;
            }
            set
            {
                if (_maximum != value)
                {
                    if (value < _minimum)
                        value = _minimum;
                    _maximum = value;
                    if (_value > _maximum)
                        Value = _maximum;
                    else
                        UpdateUpDownButtonsEnabled();
                }
            }
        }        

        private int _minimum = 0;
        /// <summary>
        /// Gets or set the min value.
        /// </summary>
        public int Minimum
        {
            get
            {
                return _minimum;
            }
            set
            {
                if (_minimum != value)
                {
                    if (value > _maximum)
                        value = _maximum;
                    _minimum = value;
                    if (_value < _minimum)
                        Value = _minimum;
                    else
                        UpdateUpDownButtonsEnabled();
                }
            }
        }

        private int _value;
        /// <summary>
        /// Gets or sets the value assigned to the control.
        /// </summary>
        public int Value
        {
            get { return _value; }
            set
            {
                if (value != _value)
                {
                    if (Minimum <= value && value <= Maximum)
                    {
                        _value = value;
                        UpdateText();
                        UpdateUpDownButtonsEnabled();
                        OnValueChanged(EventArgs.Empty);
                    }
                }
            }
        }

        #endregion



        #region Methods

        /// <summary>
        /// Raises the ValueChanged event.
        /// </summary>
        /// <param name="args">An EventArgs that contains the event data.</param>
        protected virtual void OnValueChanged(EventArgs args)
        {
            EventHandler<EventArgs> handler = ValueChanged;
            if (handler != null)
            {
                handler(this, args);
            }
        }

        /// <summary>
        /// Update enable of up/down buttons.
        /// </summary>
        private void UpdateUpDownButtonsEnabled()
        {
            if (_value == _minimum)
            {
                downButton.IsEnabled = false;
            }
            else if (_value == _maximum)
            {
                upButton.IsEnabled = false;
            }
            else
            {
                if (upButton.IsEnabled == false)
                    upButton.IsEnabled = true;
                if (downButton.IsEnabled == false)
                    downButton.IsEnabled = true;
            }
        }

        /// <summary>
        /// upButton.Click event handler.
        /// </summary>
        private void upButton_Click(object sender, EventArgs e)
        {
            if (Value < Maximum)
            {
                Value++;
            }
        }

        /// <summary>
        /// downButton.Click event handler.
        /// </summary>
        private void downButton_Click(object sender, EventArgs e)
        {
            if (Value > Minimum)
            {
                Value--;
            }
        }

        /// <summary>
        /// Update value text.
        /// </summary>
        private void UpdateText()
        {
            _updateText = true;
            valueText.Text = Value.ToString();
            _updateText = false;
        }

        /// <summary>
        /// valueText.TextChanged event handler.
        /// </summary>
        private void valueText_TextChanged(object sender, System.Windows.Controls.TextChangedEventArgs e)
        {
            if (_updateText)
                return;
            if (valueText.Text == "" || valueText.Text == "-")
                return;
            int value;
            if (int.TryParse(valueText.Text, out value))
            {
                if (value >= Minimum && value <= Maximum)
                {
                    _value = value;
                    if (_value != value)
                        SetValueTextInternal(_value);
                    UpdateUpDownButtonsEnabled();
                    OnValueChanged(EventArgs.Empty);
                }
            }
        }

        /// <summary>
        /// valueText.LostFocus event handler.
        /// </summary>
        private void valueText_LostFocus(object sender, System.Windows.RoutedEventArgs e)
        {
            int value;
            if (int.TryParse(valueText.Text, out value))
            {
                if (_value != value)
                {
                    if (value > Maximum)
                        value = Maximum;
                    else if (_value < Minimum)
                        value = Minimum;
                    _value = value;
                    SetValueTextInternal(_value);
                    UpdateUpDownButtonsEnabled();
                    OnValueChanged(EventArgs.Empty);
                }
            }
            else
            {
                SetValueTextInternal(_value);
            }
        }

        /// <summary>
        /// Sets a value in the TextBox.
        /// </summary>
        private void SetValueTextInternal(int value)
        {            
            valueText.Text = value.ToString();
            valueText.CaretIndex = valueText.Text.Length;
        }

        #endregion



        #region Events

        /// <summary>
        /// Occurs when the Value property changes.
        /// </summary>
        public event EventHandler<EventArgs> ValueChanged;

        #endregion

    }
}