from general_functions import *
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_ptc_v2 import BrickletPTCV2

#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "172.20.10.242"
PORT = 4223
UID = "Wcg" # Change XYZ to the UID of your PTC Bricklet 2.0

#Grenzwerte
Min_Temperature = 10.0
Max_Temperature = 30.0

# Callback function for temperature callback
def cb_temperature(temperature):
    if temperature/100.0 > Max_Temperature or temperature/100.0 < Min_Temperature:
        print("Temperature: " + str(temperature/100.0) + " °C")
        # alarm()
        # sende_email("Serverraumueberwachungstest@gmail.com", "Temperatur im kritischen Bereich", "Hier wichtige Nachricht einfügen")

def start_tempWatch():
    ipcon = IPConnection() # Create IP connection
    ptc = BrickletPTCV2(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected
 
    # Register temperature callback to function cb_temperature
    ptc.register_callback(ptc.CALLBACK_TEMPERATURE, cb_temperature)

    # Set period for temperature callback to 1s (1000ms) without a threshold
    ptc.set_temperature_callback_configuration(1000, False, "x", 0, 0)

    ipcon.disconnect()
