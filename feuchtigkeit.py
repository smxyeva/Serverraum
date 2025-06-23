
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

def start_humidityWatch():
    ipcon = IPConnection()
    humidity = BrickletHumidityV2(UID, ipcon)

    ipcon.connect(HOST, PORT)
    # Don't use device before ipcon is connected

    # Register humidity callback to function cb_humidity
    humidity.register_callback(hhumidity.CALLBACK_HUMIDITY, cb_humidity)
    # Set period for humidity callback to 1s (1000ms) without a threshold
    humidity.set_humidity_callback_configuration(1000, False, "x", 0, 0)

    ipcon.disconnect()

  def alarm():
    HOST = "172.20.10.242"
    PORT = 4223
    UID = "R7M"

    from tinkerforge.ip_connection import IPConnection
    from tinkerforge.bricklet_piezo_speaker_v2 import BrickletPiezoSpeakerV2

    
    ipcon = IPConnection()
    ps = BrickletPiezoSpeakerV2(UID, ipcon)

    ipcon.connect(HOST, PORT)

    ps.set_alarm(800, 2000, 10, 1, 0, 2000)

    ipcon.disconnect()
 
def sende_email(empfaenger, betreff, text):
    import smtplib
    from email.message import EmailMessage

    absender_email = 'Serverraumueberwachungstest@gmail.com'
    absender_passwort = 'zotb dtnq xwaj opxl'

    nachricht = EmailMessage()
    nachricht['From'] = absender_email
    nachricht['To'] = empfaenger
    nachricht['Subject'] = betreff
    nachricht.set_content(text)
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(absender_email, absender_passwort)
            smtp.send_message(nachricht)
        print("E-Mail erfolgreich gesendet.")
    except Exception as e:
        print(f"Fehler beim Senden der E-Mail: {e}")
