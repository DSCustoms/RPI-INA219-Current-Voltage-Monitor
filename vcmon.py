import time
import board
import busio
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219
import os

# Initialize I2C bus
i2c_bus = busio.I2C(board.SCL, board.SDA)

# Initialize INA219 sensor
ina219 = INA219(i2c_bus)

# Configure INA219
ina219.bus_adc_resolution = ADCResolution.ADCRES_12BIT_128S
ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_128S
ina219.bus_voltage_range = BusVoltageRange.RANGE_16V

# Get the absolute path to sensor_data.txt
data_file_path = os.path.join(os.path.dirname(__file__), 'sensor_data.txt')

# Open file for appending sensor data
try:
    with open(data_file_path, 'a') as file:
        file.write("Timestamp,Bus Voltage (V),Current (mA),Power (mW)\n")
except FileNotFoundError:
    print("Error: Unable to open file for writing:", data_file_path)
    exit(1)

# Main loop to read sensor data and write to file
while True:
    try:
        # Get current timestamp
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        # Read sensor data
        bus_voltage = ina219.bus_voltage
        current = ina219.current
        power = ina219.power

        # Append data to file
        with open(data_file_path, 'a') as file:
            file.write(f"{timestamp},{bus_voltage:.3f},{current:.3f},{power:.3f}\n")

        # Delay for 0.5 seconds
        time.sleep(0.5)

    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exiting.")
        break
    except Exception as e:
        print("Error:", e)
