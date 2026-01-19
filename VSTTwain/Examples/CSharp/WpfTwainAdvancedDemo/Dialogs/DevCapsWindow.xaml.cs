using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.ComponentModel;
using System.Text;
using Vintasoft.WpfTwain;

namespace WpfTwainAdvancedDemo
{
    /// <summary>
    /// Interaction logic for DevCapsWindow.xaml
    /// </summary>
    public partial class DevCapsWindow : Window
    {

        #region Internal structs

        struct DeviceCapabilityInfo
        {
            internal DeviceCapability DeviceCapability;

            internal DeviceCapabilityInfo(DeviceCapability deviceCapability)
            {
                DeviceCapability = deviceCapability;
            }

            public override string ToString()
            {
                return DeviceCapability.Name;
            }
        }

        #endregion



        #region Fields

        Device _device;

        #endregion



        #region Constructor

        public DevCapsWindow(Window owner, Device device)
        {
            InitializeComponent();

            this.Owner = owner;

            if (device.State != DeviceState.Closed)
                throw new ApplicationException("Device is used.");

            _device = device;

            this.Title = string.Format("{0} [TWAIN {1}] capabilities", _device.Info.ProductName, _device.Info.TwainVersion);
        }

        #endregion



        #region Methods

        /// <summary>
        /// Window is loaded.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            try
            {
                _device.Open();

                for (int i = 0; i < _device.Capabilities.Count; i++)
                    supportedCapabilitiesListBox.Items.Add(new DeviceCapabilityInfo(_device.Capabilities[i]));

                deviceManufacturerLabel.Content = string.Format("Manufacturer: {0}", _device.Info.Manufacturer);
                deviceProductFamilyLabel.Content = string.Format("Product family: {0}", _device.Info.ProductFamily);
                deviceProductNameLabel.Content = string.Format("Product name: {0}", _device.Info.ProductName);
                driverTwainVersionLabel.Content = string.Format("TWAIN version: {0}", _device.Info.TwainVersion);
                driverTwain2CompatibleLabel.Content = string.Format("TWAIN 2.0 compatible: {0}", _device.Info.IsTwain2Compatible);
                flatbedPresentLabel.Content = string.Format("Flatbed present: {0}", _device.HasFlatbed);
                feederPresentLabel.Content = string.Format("Feeder present: {0}", _device.HasFeeder);
            }
            catch (TwainDeviceException ex)
            {
                Close();
                MessageBox.Show(ex.Message, "Device error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        /// <summary>
        /// Close the window.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void closeButton_Click(object sender, RoutedEventArgs e)
        {
            DialogResult = false;
            Close();
        }

        /// <summary>
        /// Window is closing.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void Window_Closing(object sender, CancelEventArgs e)
        {
            if (_device.State == DeviceState.Opened)
                _device.Close();

        }


        #region Show capability value

        /// <summary>
        /// Gets information about selected capability.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void supportedCapabilitiesListBox_SelectedIndexChanged(object sender, SelectionChangedEventArgs e)
        {
            Cursor = Cursors.Wait;

            getMethodComboBox.Items.Clear();

            DeviceCapabilityInfo deviceCapabilityInfo = (DeviceCapabilityInfo)supportedCapabilitiesListBox.SelectedItem;
            DeviceCapability cap = deviceCapabilityInfo.DeviceCapability;

            DeviceCapabilityUsageMode usageMode = DeviceCapabilityUsageMode.Get;
            if (getMethodComboBox.SelectedItem != null)
                usageMode = (DeviceCapabilityUsageMode)getMethodComboBox.SelectedItem;

            GetCapValue(cap, usageMode);

            Cursor = Cursors.Arrow;
        }

        private void getMethodComboBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            Cursor = Cursors.Wait;

            DeviceCapabilityInfo deviceCapabilityInfo = (DeviceCapabilityInfo)supportedCapabilitiesListBox.SelectedItem;
            DeviceCapability cap = deviceCapabilityInfo.DeviceCapability;

            DeviceCapabilityUsageMode usageMode = DeviceCapabilityUsageMode.Get;
            if (getMethodComboBox.SelectedItem != null)
                usageMode = (DeviceCapabilityUsageMode)getMethodComboBox.SelectedItem;

            GetCapValue(cap, usageMode);

            Cursor = Cursors.Arrow;
        }

        /// <summary>
        /// Gets information about value of specified capability in specified usage mode.
        /// </summary>
        /// <param name="deviceCapability"></param>
        /// <param name="usageMode"></param>
        private void GetCapValue(DeviceCapability deviceCapability, DeviceCapabilityUsageMode usageMode)
        {
            usageModeTextBox.Text = "";
            containerTypeTextBox.Text = "";
            valueTypeTextBox.Text = "";
            currentValueTextBox.Text = "";
            minValueTextBox.Text = "";
            maxValueTextBox.Text = "";
            defaultValueTextBox.Text = "";
            stepSizeTextBox.Text = "";
            supportedValuesListBox.Items.Clear();

            try
            {
                TwainValueContainerBase deviceCapabilityValue = null;
                if (usageMode == DeviceCapabilityUsageMode.GetCurrent)
                    deviceCapabilityValue = deviceCapability.GetCurrentValue();
                else if (usageMode == DeviceCapabilityUsageMode.GetDefault)
                    deviceCapabilityValue = deviceCapability.GetDefaultValue();
                else
                    deviceCapabilityValue = deviceCapability.GetValue();

                if (getMethodComboBox.Items.Count == 0)
                {
                    //
                    usageModeTextBox.Text = deviceCapability.UsageMode.ToString();
                    //
                    if ((deviceCapability.UsageMode & DeviceCapabilityUsageMode.Get) != 0)
                        getMethodComboBox.Items.Add(DeviceCapabilityUsageMode.Get);
                    if ((deviceCapability.UsageMode & DeviceCapabilityUsageMode.GetCurrent) != 0)
                        getMethodComboBox.Items.Add(DeviceCapabilityUsageMode.GetCurrent);
                    if ((deviceCapability.UsageMode & DeviceCapabilityUsageMode.GetDefault) != 0)
                        getMethodComboBox.Items.Add(DeviceCapabilityUsageMode.GetDefault);
                }

                if (deviceCapabilityValue != null)
                {
                    //
                    containerTypeTextBox.Text = deviceCapabilityValue.ContainerType.ToString();
                    valueTypeTextBox.Text = deviceCapability.ValueType.ToString();

                    //
                    switch (deviceCapabilityValue.ContainerType)
                    {
                        case TwainValueContainerType.OneValue:
                            TwainOneValueContainer oneDeviceCapabilityValue = (TwainOneValueContainer)deviceCapabilityValue;
                            AddCapOneCurrentValueToForm(oneDeviceCapabilityValue);
                            break;

                        case TwainValueContainerType.Range:
                            TwainRangeValueContainer rangeDeviceCapabilityValue = (TwainRangeValueContainer)deviceCapabilityValue;
                            AddCapRangeCurrentValueToForm(rangeDeviceCapabilityValue);
                            AddCapRangeDefaultValueToForm(rangeDeviceCapabilityValue);
                            AddCapMinValueToForm(rangeDeviceCapabilityValue);
                            AddCapMaxValueToForm(rangeDeviceCapabilityValue);
                            AddCapStepSizeToForm(rangeDeviceCapabilityValue);
                            break;

                        case TwainValueContainerType.Enum:
                            TwainEnumValueContainer enumDeviceCapabilityValue = (TwainEnumValueContainer)deviceCapabilityValue;
                            AddCapEnumCurrentValueToForm(enumDeviceCapabilityValue);
                            AddCapEnumDefaultValueToForm(enumDeviceCapabilityValue);
                            AddCapValuesToForm(enumDeviceCapabilityValue);
                            break;

                        case TwainValueContainerType.Array:
                            TwainArrayValueContainer arrayDeviceCapabilityValue = (TwainArrayValueContainer)deviceCapabilityValue;
                            AddCapValuesToForm(arrayDeviceCapabilityValue);
                            break;
                    }
                }
            }
            catch (TwainDeviceCapabilityException ex)
            {
                currentValueTextBox.Text = ex.Message;
            }
        }

        /// <summary>
        /// Gets information about the current value stored in OneValue container.
        /// </summary>
        /// <param name="deviceCapabilityValue"></param>
        private void AddCapOneCurrentValueToForm(TwainOneValueContainer deviceCapabilityValue)
        {
            if (deviceCapabilityValue.EnumValue != null)
                currentValueTextBox.Text = string.Format("{0} [{1}]", deviceCapabilityValue.Value, deviceCapabilityValue.EnumValue);
            else
                currentValueTextBox.Text = deviceCapabilityValue.Value.ToString();
        }

        /// <summary>
        /// Gets information about the current value stored in Range container.
        /// </summary>
        /// <param name="deviceCapabilityValue"></param>
        private void AddCapRangeCurrentValueToForm(TwainRangeValueContainer deviceCapabilityValue)
        {
            currentValueTextBox.Text = deviceCapabilityValue.Value.ToString();
        }

        /// <summary>
        /// Gets information about the current value stored in Enum container.
        /// </summary>
        /// <param name="deviceCapabilityValue"></param>
        private void AddCapEnumCurrentValueToForm(TwainEnumValueContainer deviceCapabilityValue)
        {
            int valueIndex = deviceCapabilityValue.ValueIndex;
            if (valueIndex >= 0 && valueIndex < deviceCapabilityValue.Values.Length)
            {
                if (deviceCapabilityValue.EnumValues != null)
                    currentValueTextBox.Text = string.Format("{0} [{1}], Index={2}", deviceCapabilityValue.Values.GetValue(valueIndex), deviceCapabilityValue.EnumValues.GetValue(valueIndex), valueIndex);
                else
                    currentValueTextBox.Text = string.Format("{0}, Index={1}", deviceCapabilityValue.Values.GetValue(valueIndex), valueIndex);
            }
        }

        /// <summary>
        /// Gets information about the default value stored in Range container.
        /// </summary>
        /// <param name="deviceCapabilityValue"></param>
        private void AddCapRangeDefaultValueToForm(TwainRangeValueContainer deviceCapabilityValue)
        {
            defaultValueTextBox.Text = deviceCapabilityValue.DefaultValue.ToString();
        }

        /// <summary>
        /// Gets information about the default value stored in Enum container.
        /// </summary>
        /// <param name="deviceCapabilityValue"></param>
        private void AddCapEnumDefaultValueToForm(TwainEnumValueContainer deviceCapabilityValue)
        {
            int defaultValueIndex = deviceCapabilityValue.DefaultValueIndex;
            if (deviceCapabilityValue.EnumValues != null)
            {
                if (defaultValueIndex >= 0 && defaultValueIndex < deviceCapabilityValue.EnumValues.Length)
                {
                    defaultValueTextBox.Text = string.Format("{0} [{1}]", defaultValueIndex, deviceCapabilityValue.EnumValues.GetValue(defaultValueIndex));
                }
            }
            else
                defaultValueTextBox.Text = defaultValueIndex.ToString();
        }

        /// <summary>
        /// Gets information about the minimal value stored in Enum container.
        /// </summary>
        /// <param name="deviceCapabilityValue"></param>
        private void AddCapMinValueToForm(TwainRangeValueContainer deviceCapabilityValue)
        {
            minValueTextBox.Text = deviceCapabilityValue.MinValue.ToString();
        }

        /// <summary>
        /// Gets information about the maximal value stored in Enum container.
        /// </summary>
        /// <param name="deviceCapabilityValue"></param>
        private void AddCapMaxValueToForm(TwainRangeValueContainer deviceCapabilityValue)
        {
            maxValueTextBox.Text = deviceCapabilityValue.MaxValue.ToString();
        }

        /// <summary>
        /// Gets information about the step size of value stored in Enum container.
        /// </summary>
        /// <param name="deviceCapabilityValue"></param>
        private void AddCapStepSizeToForm(TwainRangeValueContainer deviceCapabilityValue)
        {
            stepSizeTextBox.Text = deviceCapabilityValue.StepSize.ToString();
        }

        /// <summary>
        /// Gets information about the supported values stored in Array container.
        /// </summary>
        /// <param name="deviceCapabilityValue"></param>
        private void AddCapValuesToForm(TwainArrayValueContainer deviceCapabilityValue)
        {
            if (deviceCapabilityValue.Values == null)
                return;

            if (deviceCapabilityValue.EnumValues != null)
            {
                for (int i = 0; i < deviceCapabilityValue.Values.Length; i++)
                    supportedValuesListBox.Items.Add(string.Format("{0} [{1}]", deviceCapabilityValue.Values.GetValue(i), deviceCapabilityValue.EnumValues.GetValue(i)));
            }
            else
            {
                for (int i = 0; i < deviceCapabilityValue.Values.Length; i++)
                    supportedValuesListBox.Items.Add(deviceCapabilityValue.Values.GetValue(i));
            }
        }

        #endregion


        #region Copy values of all capabilities to clipboard

        /// <summary>
        /// Copies information about all capabilities to the clipboard.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void copyToClipboardButton_Click(object sender, RoutedEventArgs e)
        {
            if (_device.State == DeviceState.Closed)
            {
                MessageBox.Show("Device is not open.");
                return;
            }

            Cursor = Cursors.Wait;

            StringBuilder capsInfo = new StringBuilder();

            capsInfo.Append(string.Format("Manufacturer: {0}{1}", _device.Info.Manufacturer, Environment.NewLine));
            capsInfo.Append(string.Format("Product family: {0}{1}", _device.Info.ProductFamily, Environment.NewLine));
            capsInfo.Append(string.Format("Product name: {0}{1}", _device.Info.ProductName, Environment.NewLine));
            capsInfo.Append(string.Format("Driver version: {0}{1}", _device.Info.DriverVersion, Environment.NewLine));
            capsInfo.Append(string.Format("TWAIN version: {0}{1}", _device.Info.TwainVersion, Environment.NewLine));
            capsInfo.Append(string.Format("TWAIN 2.0 compatible: {0}{1}", _device.Info.IsTwain2Compatible, Environment.NewLine));
            capsInfo.Append(string.Format("Flatbed present: {0}{1}", _device.HasFlatbed, Environment.NewLine));
            capsInfo.Append(string.Format("Feeder present: {0}{1}{1}", _device.HasFeeder, Environment.NewLine));

            DeviceCapability deviceCapability;
            for (int i = 0; i < _device.Capabilities.Count; i++)
            {
                try
                {
                    deviceCapability = _device.Capabilities[i];

                    capsInfo.Append(string.Format("Capability: {0}{1}", deviceCapability, Environment.NewLine));

                    TwainValueContainerBase capValue = deviceCapability.GetValue();

                    DeviceCapabilityUsageMode capUsageMode = deviceCapability.UsageMode;
                    capsInfo.Append(string.Format("  Supported usage modes: {0}{1}", capUsageMode, Environment.NewLine));

                    if (capValue != null)
                    {
                        if ((capUsageMode & DeviceCapabilityUsageMode.Get) != 0)
                            AddCapInfoToCapsInfo(DeviceCapabilityUsageMode.Get, capValue, capsInfo);
                        if ((capUsageMode & DeviceCapabilityUsageMode.GetCurrent) != 0)
                            AddCapInfoToCapsInfo(DeviceCapabilityUsageMode.GetCurrent, deviceCapability.GetCurrentValue(), capsInfo);
                        if ((capUsageMode & DeviceCapabilityUsageMode.GetDefault) != 0)
                            AddCapInfoToCapsInfo(DeviceCapabilityUsageMode.GetDefault, deviceCapability.GetDefaultValue(), capsInfo);
                    }
                    else
                    {
                        capsInfo.Append(string.Format("  Value: NULL{0}", Environment.NewLine));
                    }
                }
                catch (TwainDeviceException)
                {
                }
                catch (TwainDeviceCapabilityException)
                {
                }
                capsInfo.Append(Environment.NewLine);
            }
            capsInfo.Append(Environment.NewLine);

            // get information about image layout
            try
            {
                capsInfo.Append(string.Format("Default image layout: {0}{1}", _device.ImageLayout.GetDefault(), Environment.NewLine));
                capsInfo.Append(Environment.NewLine);
            }
            catch (TwainDeviceException)
            {
            }

            // get information about cameras of device
            DeviceCamera[] deviceCameras = _device.Cameras.GetCameras();
            if (deviceCameras.Length > 0)
            {
                for (int i = 0; i < deviceCameras.Length; i++)
                    capsInfo.Append(string.Format("Camera{0}: {1}{2}", i, deviceCameras[i], Environment.NewLine));
                capsInfo.Append(Environment.NewLine);
            }

            //
            Clipboard.SetText(capsInfo.ToString());

            Cursor = Cursors.Arrow;

            MessageBox.Show("Information about device capabilities is copied to clipboard.");
        }

        /// <summary>
        /// Adds information about the value of capability in specified usage mode to the string builder.
        /// </summary>
        /// <param name="capUsageMode"></param>
        /// <param name="capValue"></param>
        /// <param name="capsInfo"></param>
        private void AddCapInfoToCapsInfo(DeviceCapabilityUsageMode capUsageMode, TwainValueContainerBase capValue, StringBuilder capsInfo)
        {
            capsInfo.Append(string.Format("  Usage mode: {0}{1}", capUsageMode, Environment.NewLine));
            capsInfo.Append(string.Format("    Value container type: {0}{1}", capValue.ContainerType, Environment.NewLine));

            switch (capValue.ContainerType)
            {
                case TwainValueContainerType.OneValue:
                    TwainOneValueContainer oneDeviceCapabilityValue = (TwainOneValueContainer)capValue;
                    AddCapOneCurrentValueInfoToCapsInfo(oneDeviceCapabilityValue, capsInfo);
                    break;

                case TwainValueContainerType.Range:
                    TwainRangeValueContainer rangeDeviceCapabilityValue = (TwainRangeValueContainer)capValue;
                    AddCapRangeCurrentValueInfoToCapsInfo(rangeDeviceCapabilityValue, capsInfo);
                    AddCapRangeDefaultValueInfoToCapsInfo(rangeDeviceCapabilityValue, capsInfo);
                    AddCapMinValueInfoToCapsInfo(rangeDeviceCapabilityValue, capsInfo);
                    AddCapMaxValueInfoToCapsInfo(rangeDeviceCapabilityValue, capsInfo);
                    AddCapStepSizeInfoToCapsInfo(rangeDeviceCapabilityValue, capsInfo);
                    break;

                case TwainValueContainerType.Enum:
                    TwainEnumValueContainer enumDeviceCapabilityValue = (TwainEnumValueContainer)capValue;
                    AddCapEnumCurrentValueInfoToCapsInfo(enumDeviceCapabilityValue, capsInfo);
                    AddCapEnumDefaultValueInfoToCapsInfo(enumDeviceCapabilityValue, capsInfo);
                    AddCapValuesInfoToCapsInfo(enumDeviceCapabilityValue, capsInfo);
                    break;

                case TwainValueContainerType.Array:
                    TwainArrayValueContainer arrayDeviceCapabilityValue = (TwainArrayValueContainer)capValue;
                    AddCapValuesInfoToCapsInfo(arrayDeviceCapabilityValue, capsInfo);
                    break;
            }
        }

        /// <summary>
        /// Gets information about the current value stored in OneValue container.
        /// </summary>
        /// <param name="deviceCapabilityValue"></param>
        /// <param name="capsInfo"></param>
        private void AddCapOneCurrentValueInfoToCapsInfo(TwainOneValueContainer deviceCapabilityValue, StringBuilder capsInfo)
        {
            if (deviceCapabilityValue.EnumValue != null)
                capsInfo.Append(string.Format("    Current value: {0}[{1}] ({2}){3}", deviceCapabilityValue.Value, deviceCapabilityValue.EnumValue, deviceCapabilityValue.Value.GetType(), Environment.NewLine));
            else
                capsInfo.Append(string.Format("    Current value: {0} ({1}){2}", deviceCapabilityValue.Value, deviceCapabilityValue.Value.GetType(), Environment.NewLine));
        }

        /// <summary>
        /// Gets information about the current value stored in Range container.
        /// </summary>
        /// <param name="deviceCapabilityValue"></param>
        /// <param name="capsInfo"></param>
        private void AddCapRangeCurrentValueInfoToCapsInfo(TwainRangeValueContainer deviceCapabilityValue, StringBuilder capsInfo)
        {
            capsInfo.Append(string.Format("    Current value: {0} ({1}){2}", deviceCapabilityValue.Value, deviceCapabilityValue.Value.GetType(), Environment.NewLine));
        }

        /// <summary>
        /// Gets information about the current value stored in Enum container.
        /// </summary>
        /// <param name="deviceCapabilityValue"></param>
        /// <param name="capsInfo"></param>
        private void AddCapEnumCurrentValueInfoToCapsInfo(TwainEnumValueContainer deviceCapabilityValue, StringBuilder capsInfo)
        {
            if (deviceCapabilityValue.EnumValues != null)
            {
                if (deviceCapabilityValue.ValueIndex >= 0 && deviceCapabilityValue.ValueIndex < deviceCapabilityValue.EnumValues.Length)
                    capsInfo.Append(string.Format("    Current value index: {0}[{1}]{2}", deviceCapabilityValue.ValueIndex, deviceCapabilityValue.EnumValues.GetValue(deviceCapabilityValue.ValueIndex), Environment.NewLine));
                else
                    capsInfo.Append(string.Format("    Current value index: {0}[WRONG VALUE INDEX]{1}", deviceCapabilityValue.ValueIndex, Environment.NewLine));
            }
            else
                capsInfo.Append(string.Format("    Current value index: {0}{1}", deviceCapabilityValue.ValueIndex, Environment.NewLine));
        }

        /// <summary>
        /// Gets information about the default value stored in Range container.
        /// </summary>
        /// <param name="deviceCapabilityValue"></param>
        /// <param name="capsInfo"></param>
        private void AddCapRangeDefaultValueInfoToCapsInfo(TwainRangeValueContainer deviceCapabilityValue, StringBuilder capsInfo)
        {
            capsInfo.Append(string.Format("    Default value: {0} ({1}){2}", deviceCapabilityValue.DefaultValue, deviceCapabilityValue.DefaultValue.GetType(), Environment.NewLine));
        }

        /// <summary>
        /// Gets information about the default value stored in Enum container.
        /// </summary>
        /// <param name="deviceCapabilityValue"></param>
        /// <param name="capsInfo"></param>
        private void AddCapEnumDefaultValueInfoToCapsInfo(TwainEnumValueContainer deviceCapabilityValue, StringBuilder capsInfo)
        {
            if (deviceCapabilityValue.EnumValues != null)
            {
                if (deviceCapabilityValue.DefaultValueIndex >= 0 && deviceCapabilityValue.DefaultValueIndex < deviceCapabilityValue.EnumValues.Length)
                    capsInfo.Append(string.Format("    Default value index: {0}[{1}]{2}", deviceCapabilityValue.DefaultValueIndex, deviceCapabilityValue.EnumValues.GetValue(deviceCapabilityValue.DefaultValueIndex), Environment.NewLine));
                else
                    capsInfo.Append(string.Format("    Default value index: {0}[WRONG DEFAULT VALUE INDEX]{1}", deviceCapabilityValue.DefaultValueIndex, Environment.NewLine));
            }
            else
                capsInfo.Append(string.Format("    Default value index: {0}{1}", deviceCapabilityValue.DefaultValueIndex, Environment.NewLine));
        }

        /// <summary>
        /// Gets information about the minimal value stored in Enum container.
        /// </summary>
        /// <param name="deviceCapabilityValue"></param>
        /// <param name="capsInfo"></param>
        private void AddCapMinValueInfoToCapsInfo(TwainRangeValueContainer deviceCapabilityValue, StringBuilder capsInfo)
        {
            capsInfo.Append(string.Format("    Min value: {0} ({1}){2}", deviceCapabilityValue.MinValue, deviceCapabilityValue.MinValue.GetType(), Environment.NewLine));
        }

        /// <summary>
        /// Gets information about the maximal value stored in Enum container.
        /// </summary>
        /// <param name="deviceCapabilityValue"></param>
        /// <param name="capsInfo"></param>
        private void AddCapMaxValueInfoToCapsInfo(TwainRangeValueContainer deviceCapabilityValue, StringBuilder capsInfo)
        {
            capsInfo.Append(string.Format("    Max value: {0} ({1}){2}", deviceCapabilityValue.MaxValue, deviceCapabilityValue.MaxValue.GetType(), Environment.NewLine));
        }

        /// <summary>
        /// Gets information about the step size of value stored in Enum container.
        /// </summary>
        /// <param name="deviceCapabilityValue"></param>
        /// <param name="capsInfo"></param>
        private void AddCapStepSizeInfoToCapsInfo(TwainRangeValueContainer deviceCapabilityValue, StringBuilder capsInfo)
        {
            capsInfo.Append(string.Format("    Step size: {0} ({1}){2}", deviceCapabilityValue.StepSize, deviceCapabilityValue.StepSize.GetType(), Environment.NewLine));
        }

        /// <summary>
        /// Gets information about the supported values stored in Array container.
        /// </summary>
        /// <param name="deviceCapabilityValue"></param>
        /// <param name="capsInfo"></param>
        private void AddCapValuesInfoToCapsInfo(TwainArrayValueContainer deviceCapabilityValue, StringBuilder capsInfo)
        {
            if (deviceCapabilityValue.Values == null ||
                deviceCapabilityValue.Values.Length == 0)
            {
                capsInfo.Append(string.Format("    Supported values[0]:{0}", Environment.NewLine));
                return;
            }

            StringBuilder values = new StringBuilder();

            if (deviceCapabilityValue.Values.GetValue(0).GetType().Equals(typeof(string)))
            {
                for (int j = 0; j < deviceCapabilityValue.Values.Length; j++)
                    values.Append(string.Format("\"{0}\", ", deviceCapabilityValue.Values.GetValue(j)));
            }
            else
            {
                if (deviceCapabilityValue.EnumValues != null)
                {
                    for (int i = 0; i < deviceCapabilityValue.Values.Length; i++)
                        values.Append(string.Format("{0} [{1}], ", deviceCapabilityValue.Values.GetValue(i), deviceCapabilityValue.EnumValues.GetValue(i)));
                }
                else
                {
                    for (int i = 0; i < deviceCapabilityValue.Values.Length; i++)
                        values.Append(string.Format("{0}, ", deviceCapabilityValue.Values.GetValue(i)));
                }
            }

            capsInfo.Append(string.Format("    Supported values[{0}, {1}]: {2}{3}", deviceCapabilityValue.Values.Length, deviceCapabilityValue.Values.GetValue(0).GetType(), values, Environment.NewLine));
        }

        #endregion

        #endregion

    }
}
