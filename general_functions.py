def alarm():
    HOST = "172.20.10.242"
    PORT = 4223
    UID = "R7M"

    from tinkerforge.ip_connection import IPConnection
    from tinkerforge.bricklet_piezo_speaker_v2 import BrickletPiezoSpeakerV2

    if __name__ == "__main__":
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