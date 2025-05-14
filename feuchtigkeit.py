from general_functions import *
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_humidity_v2 import BrickletmidityV2

HOST = "172.20.10.242"
PORT = 4223
UID = "ViW"

#Grenzwerte
MIN_HUMIDITY = 30.0
MAX_HUMIDITY = 70.0

#Einmalige Benachrichtigung verhindern
alarm_triggered = False

# Callback function for humidity callback
def cb_humidity(humidity):
  global alarm_triggered

  feuchtigkeit = humidity / 100.0
  print(f"Humidity: {feuchtigkeit:.2f} %RH")

  if feuchtigkeit < MIN_HUMIDITY or feuchtigkeit > MAX_HUMIDITY:
    if not alarm_triggered:
      print("Grenzwert überschritten.")
      sende_email(
        empfaenger="serverraumueberwachungstest@gmail.com",
        betreff="Feuchtigkeit außerhalb des Bereichs",
        text=f"Achtung, die Luftfeuchtigkeit liegt bei {feuchtigkeit:.2f}%RH – außerhalb des zulässigen Bereichs."     
      )
      alarm_triggered = True

    else:
      #Wert wieder normal
      alarm_triggered = False

def start_humidityWatch
    ipcon = IPConnection()
    humidity = BrickletHumidityV2(UID, ipcon)

    ipcon.connect(HOST, PORT)
    # Don't use device before ipcon is connected

    # Register humidity callback to function cb_humidity
    humidity.register_callback(hhumidity.CALLBACK_HUMIDITY, cb_humidity)
    # Set period for humidity callback to 1s (1000ms) without a threshold
    humidity.set_humidity_callback_configuration(1000, False, "x", 0, 0)

    ipcon.disconnect()
