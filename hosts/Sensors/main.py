import network
import socket
import machine
from machine import Pin
from PiicoDev_Unified import sleep_ms
from PiicoDev_BME280 import PiicoDev_BME280
from PiicoDev_SSD1306 import create_PiicoDev_SSD1306
import gc

# Pre-run setup
Pin("LED", Pin.OUT).high()
Pin(0, Pin.OUT).high()
Pin(1, Pin.OUT).high()

display = create_PiicoDev_SSD1306()
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Network credentials
ssid = 'notabomb.exe'
password = 'thisisforcoolthings,notyou.fuckoff'

def roundToTwo(num):
    return round(num * 100) / 100

# Function to generate sensor data string
def create_sensor_data(tempC, pres_hPa, humRH):
    return f"set_pico_w_sensors;{tempC:.2f} °C;{pres_hPa:.2f} hPa;{humRH:.2f} %RH;"

# Function to display data on OLED
def setDisplay(tempC, pres_hPa, humRH, waiting_post=False):
    display.fill(0)
    display.text(str(tempC), 0, 0, 1)  # Temperature
    display.text(f"{pres_hPa:.2f} hPa", 0, 10, 1)  # Pressure
    display.text(f"{humRH:.2f} %RH", 0, 20, 1)  # Humidity
    display.text(wlan.ifconfig()[0], 0, 57, 1)  # IP Address
    if waiting_post:
        display.text("POST", 97, 0, 1)
    display.show()

# Function to connect to Wi-Fi
def connect_network():
    for attempt in range(5):  # Limit connection attempts
        wlan.connect(ssid, password)
        sleep_ms(2000)  # Wait for connection
        if wlan.isconnected():
            print("Connected to Wi-Fi")
            return True
        print(f"Connection attempt {attempt + 1} failed")
    return False

# Main script setup
display.text("Connecting to:", 0, 0, 1)
display.text(ssid, 0, 10, 1)
display.show()

if not connect_network():
    machine.reset()

display.fill(0)
display.text("Connected to:", 0, 0, 1)
display.text(ssid, 0, 10, 1)
display.text(wlan.ifconfig()[0], 0, 57, 1)
display.show()

Pin("LED", Pin.OUT).low()

# Initialize sensor
sensor = PiicoDev_BME280()
zero_alt = sensor.altitude()

# Main loop
while True:
    gc.collect()  # Collect garbage periodically
    try:
        # Read sensor values
        tempC, presPa, humRH = sensor.values()
        pres_hPa = presPa / 100  # Convert Pa to hPa

        # Update display
        setDisplay(tempC, pres_hPa, humRH)

        # Reconnect if network is disconnected
        if not wlan.isconnected():
            print("Reconnecting to Wi-Fi...")
            if not connect_network():
                machine.reset()

        # Create sensor data string
        sensor_data = create_sensor_data(tempC, pres_hPa, humRH)

        # Send data via socket
        try:
            with socket.socket() as open_socket:
                addr = socket.getaddrinfo('arduino.declan-reid.me', 2052)[0][-1]
                open_socket.connect(addr)
                open_socket.send(sensor_data.encode())
        except Exception as e:
            print(f"Socket error: {e}")
            machine.reset()

    except Exception as e:
        print(f"Error in main loop: {e}")
        machine.reset()
