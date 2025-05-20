from general_functions import *

def show_temperature():
    HOST = "172.20.10.242"
    PORT = 4223
    UIDT = "Wcg"

    from tinkerforge.ip_connection import IPConnection
    from tinkerforge.bricklet_ptc_v2 import BrickletPTCV2

    ipcon = IPConnection()
    ptc = BrickletPTCV2(UIDT, ipcon)

    ipcon.connect(HOST, PORT)

    temperature = ptc.get_temperature()
    temperature = int(temperature/100.0)
    temperature_array = zerlege_zahl_in_ziffern(temperature)

    UIDS = "Tre"

    from tinkerforge.bricklet_segment_display_4x7_v2 import BrickletSegmentDisplay4x7V2

    sd = BrickletSegmentDisplay4x7V2(UIDS, ipcon)

    sd.set_brightness(10)

    sd.set_numeric_value(temperature_array)

    ipcon.disconnect()



def show_illuminance():
    HOST = "172.20.10.242"
    PORT = 4223
    UID = "Pdw" 

    from tinkerforge.ip_connection import IPConnection
    from tinkerforge.bricklet_ambient_light_v3 import BrickletAmbientLightV3

    ipcon = IPConnection()
    al = BrickletAmbientLightV3(UID, ipcon) 

    ipcon.connect(HOST, PORT)
    illuminance = al.get_illuminance()
    illuminance = int(illuminance/100.0)
    illuminance_array = zerlege_zahl_in_ziffern(illuminance)

    UIDS = "Tre"

    from tinkerforge.bricklet_segment_display_4x7_v2 import BrickletSegmentDisplay4x7V2

    sd = BrickletSegmentDisplay4x7V2(UIDS, ipcon)

    sd.set_brightness(10)

    sd.set_numeric_value(illuminance_array)

    ipcon.disconnect()



def show_humidity():
    HOST = "172.20.10.242"
    PORT = 4223
    UID = "ViW"

    from tinkerforge.ip_connection import IPConnection
    from tinkerforge.bricklet_humidity_v2 import BrickletHumidityV2

    ipcon = IPConnection()
    h = BrickletHumidityV2(UID, ipcon)

    ipcon.connect(HOST, PORT)

    humidity = h.get_humidity()
    print("Humidity: " + str(humidity/100.0) + " %RH")
    humidity = int(humidity/100.0)
    humidity_array = zerlege_zahl_in_ziffern(humidity)

    UIDS = "Tre"

    from tinkerforge.bricklet_segment_display_4x7_v2 import BrickletSegmentDisplay4x7V2

    sd = BrickletSegmentDisplay4x7V2(UIDS, ipcon)

    sd.set_brightness(10)

    sd.set_numeric_value(humidity_array)

    ipcon.disconnect()

HOST = "172.20.10.242"
PORT = 4223
UID = "Vd8"

index = 0
order = [1, 2, 3]

def cb_state_changed(button_l, button_r, led_l, led_r):
    from tinkerforge.bricklet_dual_button_v2 import BrickletDualButtonV2

    global index

    if button_l == BrickletDualButtonV2.BUTTON_STATE_RELEASED:
        index = (index - 1) % 3
        if order[index] == 1:
            show_temperature()
        elif order[index] == 2:
            show_illuminance()
        elif order[index] == 3:
            show_humidity()
        print("Left Button gedrückt")

    if button_r == BrickletDualButtonV2.BUTTON_STATE_RELEASED:
        index = (index + 1) % 3
        if order[index] == 1:
            show_temperature()
        elif order[index] == 2:
            show_illuminance()
        elif order[index] == 3:
            show_humidity()
        print("Right Button gedrückt")

def buttons():
    show_temperature()

    from tinkerforge.ip_connection import IPConnection
    from tinkerforge.bricklet_dual_button_v2 import BrickletDualButtonV2

    ipcon = IPConnection()
    db = BrickletDualButtonV2(UID, ipcon)

    ipcon.connect(HOST, PORT)

    db.register_callback(db.CALLBACK_STATE_CHANGED, cb_state_changed)
    db.set_state_changed_callback_configuration(True)

    print("Warte auf Tastendrücke... (zum Beenden Strg+C drücken)")
    input()  # hält das Programm offen

    ipcon.disconnect()



def zerlege_zahl_in_ziffern(zahl: int) -> list:
    ziffern = [int(stelle) for stelle in str(abs(zahl))]
    while len(ziffern) < 4:
        ziffern.insert(0, 0)
    return ziffern



buttons()
