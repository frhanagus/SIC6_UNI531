import machine
import ujson
import network
import utime as time
import dht
import urequests as requests
import socket

DEVICE_ID = "esp-32-haha"
WIFI_SSID = "Kamunanya"
WIFI_PASSWORD = "kamunanya"
TOKEN = "BBUS-i09jiPeTq4iIGVMwp21ERoqOv4zrtH"
DHT_PIN = machine.Pin(5)
pir_sensor = machine.Pin(14, machine.Pin.IN)

def did_receive_callback(topic, message):
    print('\n\nData Received! \ntopic = {0}, message = {1}'.format(topic, message))

def create_json_data(temperature, humidity, motion_detected):
    data = ujson.dumps({
        "device_id": DEVICE_ID,
        "temp": temperature,
        "humidity": humidity,
        "Sensor": motion_detected,
        "type": "sensor"
    })
    return data

def send_data(temperature, humidity, motion_detected):
    url = "http://industrial.api.ubidots.com/api/v1.6/devices/" + DEVICE_ID
    urll = "http://127.0.0.1:5000/sensor1"
    headers = {"Content-Type": "application/json", "X-Auth-Token": TOKEN}
    data = {
        "temp": temperature,
        "humidity": humidity,
        "Sensor": motion_detected
    }
    #json_data = ujson.dumps(data)
    #try:
    response = requests.post(url, json=data, headers=headers)
    print("Done Sending Data!")
    print("Response:", response.text)

    # To mongoDB
    # responsee = requests.post(urll, json=data)
    # print("Server response:", responsee.text)
    # time.sleep(5)

wifi_client = network.WLAN(network.STA_IF)
wifi_client.active(True)
print("Connecting device to WiFi")
wifi_client.connect(WIFI_SSID, WIFI_PASSWORD)

while not wifi_client.isconnected():
    print("Connecting")
    time.sleep(0.1)
print("WiFi Connected!")
print(wifi_client.ifconfig())

dht_sensor = dht.DHT11(DHT_PIN) 
telemetry_data_old = ""

temp = dht_sensor.temperature()
humidity = dht_sensor.humidity()
motion_detected = pir_sensor.value()

while True:
    try:
        dht_sensor.measure()
    except:
        pass

    time.sleep(0.5)

    telemetry_data_new = create_json_data(dht_sensor.temperature(), dht_sensor.humidity(), motion_detected)

    print(telemetry_data_new)
    print(f"Temperature: {dht_sensor.temperature()}, Humidity: {dht_sensor.humidity()}")

    # if check_network():
    send_data(dht_sensor.temperature(), dht_sensor.humidity(), motion_detected)
    # else:
    #     print("Network is not available. Retry in 5 seconds.")
    
    time.sleep(5)

#---------------------------------------------------------------------------------------------------------

# import network
# import time
# import machine
# import dht
# import ujson
# import urequests as requests  # MicroPython compatible requests library

# # import datetime

# # Ubidots API URL and token
# API_URL = "https://industrial.api.ubidots.com/api/v1.6/devices/esp-32"
# API_TOKEN = "BBUS-i09jiPeTq4iIGVMwp21ERoqOv4zrtH"  # Replace with your Ubidots API Token
# DEVICE_LABEL = "esp-32-haha"  # Replace with your Ubidots Device label
# uri = "mongodb+srv://wahyum:7nQAAvkVttVRVy3o@tahu.ngvwt.mongodb.net/?retryWrites=true&w=majority&appName=tahu"
# urll = "http://127.0.0.1:5000/sensor1"



# # Wi-Fi credentials
# WIFI_SSID = "Kamunanya"
# WIFI_PASSWORD = "kamunanya"

# # DHT11 sensor initialization
# sensor = dht.DHT11(machine.Pin(5))

# # Connect to Wi-Fi
# print("Connecting to WiFi", end="")
# sta_if = network.WLAN(network.STA_IF)
# sta_if.active(True)
# sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
# while not sta_if.isconnected():
#     print(".", end="")
#     time.sleep(0.1)
# print(" Connected!")

# def did_receive_callback(topic, message):
#     print('\n\nData Received! \ntopic = {0}, message = {1}'.format(topic, message))

# def create_json_data(temperature, humidity):
#     data = ujson.dumps({
#         "device_id": DEVICE_LABEL,
#         "temp": temperature,
#         "humidity": humidity,
#         "type": "sensor"
#     })
#     return data

# def send_data(temperature, humidity):
#     url = "http://industrial.api.ubidots.com/api/v1.6/devices/" + DEVICE_LABEL
#     headers = {"Content-Type": "application/json", "X-Auth-Token": API_TOKEN}
#     data = {
#         "temp": temperature,
#         "humidity": humidity
#     }
#     response = requests.post(url, json=data, headers=headers)
#     print("Done Sending Data!")
#     print("Response:", response.text)

#     # To mongoDB
#     responsee = requests.post(urll, json=data)
#     print("Server response:", responsee.text)
#     time.sleep(5)

# prev_weather = ""
# while True:
#     print("Measuring weather conditions... ", end="")
#     try:
#         sensor.measure()  # Get the sensor reading
#         temp = sensor.temperature()  # Temperature in Celsius
#         humidity = sensor.humidity()  # Humidity percentage

#         message = create_json_data(temp, humidity)

#         # If the data is different from the previous one, send it to Ubidots
#         if message != prev_weather:
#             print("Updated!")
#             send_data(temp, humidity)  # Send the data to Ubidots
#             prev_weather = message
#         else:
#             print("No change")

#     except OSError as e:
#         print(f"Failed to read from sensor: {e}")  # Print error if reading fails

#     time.sleep(5)  # Delay between readings

#--------------------------------------------------------------------------------