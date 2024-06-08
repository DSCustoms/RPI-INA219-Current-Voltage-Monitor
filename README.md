# RPI-INA219-Current-Voltage-Monitor
A simple local web access ina219 current and voltage monitoring solution


I just needed a way to have a device that could be plugged in between the battery and circuit of any of my projects to let me monitor the power consumption and charging characteristics in real time. The INA219 sensor is an excellent little board for this, very inexpensive. My setup for this project is a Raspberry Pi Zero 2W, an INA219 breakout pcb, and a battery pack. The INA219 has a variety of JST and power connectors on both sides for easy plug and play use. Don't forget the ground wire MUST be connected from the circuit you are monitoring to the ground on the ina219 and the raspberry pi, or it will ruin the results. Your network will need to be online for this to work, it uses an online service to generate the graphs. 

Here's a step by step guide to get this set up

### 1. Flash Raspberry Pi OS:

- Download the Raspberry Pi flasher from the official website. I only install the 32 bit lite OS for this project. Add your network settings and enable SSH in the installer.

### 2. Wiring Guide:

- Connect the INA219 to the Raspberry Pi Zero 2 W:
- VIN+: Connect to the positive terminal of the Circuit power supply
- VIN-: Connect to the positive terminal of the Circuit load
- GND: Connect to the ground (GND) of the Circuit
- VCC: Connect to 3.3V (Pin 1) on the Raspberry Pi
- GND: Connect to ground (Pin 6) on the Raspberry Pi
- SDA: Connect to SDA (Pin 3) on the Raspberry Pi
- SCL: Connect to SCL (Pin 5) on the Raspberry Pi

### 3. Install Python and pip:

- Open a terminal on the Raspberry Pi.
- Update the package list:  
  ```bash
  sudo apt update
  ```
- Install Python 3 and pip:  
  ```bash
  sudo apt install python3 python3-pip
  ```
- Don't forget to enable i2c on the pi, in the interface options menu on Raspi-Config:
  ```bash
  sudo raspi-config
  Interface Options
  I2C
  Yes
  ```

### 4. Create a Virtual Environment:

- Navigate to your project directory:
  ```bash
  cd /home/pi/
  ```
- Create a virtual environment named "venv":
  ```bash
  python3 -m venv venv
  ```
- Activate the virtual environment:
  ```bash
  source venv/bin/activate
  ```

### 5. Install Required Packages:

- Install Flask and other required packages using pip:
  ```bash
  pip install flask adafruit-blinka adafruit-circuitpython-ina219
  ```

### 6. Create Your Python Scripts:

- Add the Python scripts `server.py` and `vcmon.py` in your project directory. Create a directory called templates, and put the `index.html` file in there.
- The program vcmon.py will be creating a text file called sensor_data.txt in the project directory where it stores a log of the sensor data to be displayed on the web interface.

### 7. Configure systemd Service Units:

- Create a systemd service unit file for `vcmon.service`:
  ```bash
  sudo nano /etc/systemd/system/vcmon.service
  ```
  Populate the file with the following contents:
  ```plaintext
  [Unit]
  Description=vcmon Service
  After=multi-user.target

  [Service]
  Type=idle
  ExecStart=/home/pi/venv/bin/python /home/pi/vcmon.py
  Restart=always
  WorkingDirectory=/home/pi

  [Install]
  WantedBy=multi-user.target
  ```
- Similarly, create a systemd service unit file for `server.service`:
  ```bash
  sudo nano /etc/systemd/system/server.service
  ```
  Populate the file with the following contents:
  ```plaintext
  [Unit]
  Description=Flask Server Service
  After=network.target

  [Service]
  Type=simple
  User=pi
  WorkingDirectory=/home/pi
  ExecStart=/home/pi/venv/bin/python /home/pi/server.py
  Restart=always

  [Install]
  WantedBy=multi-user.target
  ```

### 8. Enable and Start the Services:

- Reload systemd to load the new service units:
  ```bash
  sudo systemctl daemon-reload
  ```
- Enable and start the services:
  ```bash
  sudo systemctl enable vcmon.service
  sudo systemctl enable server.service
  sudo systemctl start vcmon.service
  sudo systemctl start server.service
  ```

### 9. Verify Service Status:

- Check the status of the services to ensure they are running without errors:
  ```bash
  sudo systemctl status vcmon.service
  sudo systemctl status server.service
  ```

### 10. Reboot the Raspberry Pi:

- Reboot the Raspberry Pi to ensure that the services start automatically on boot:
  ```bash
  sudo reboot
  ```

### 11. Testing:

- Open a browser and go to your raspberry pi's IP  port 5000 (10.0.0.10:5000) to view the web page, Click the reset button to clear out the data file, refresh to update:

  
### 12. Troubleshooting:
- You might have an error trying to use the reset button on the web page Replace 'pi' in the following with your user name. 
  
Step 1: Change Ownership of sensor_data.txt

Run the following command to change the ownership of the file to the pi user:

```bash
  sudo chown pi:pi /home/pi/sensor_data.txt
  ```

Step 2: Verify Ownership
Verify the ownership of the file to ensure it has been correctly assigned to the pi user:

```bash
  ls -l /home/pi/sensor_data.txt
  ```


You should see something like this:

```bash
  -rw-r--r-- 1 pi pi 44231 Jun  8 07:41 /home/pi/sensor_data.txt
  ```


Step 3: Restart the Flask Service

Restart the Flask service to ensure that any changes are correctly loaded:

```bash
  sudo systemctl restart server.service
  ```

Step 4: Test the Reset again.
