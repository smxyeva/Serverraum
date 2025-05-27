from general_functions import *
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_dual_button_v2 import BrickletDualButtonV2

HOST = "172.20.10.242"
PORT = 4223
UID = "Vd8"
index = 1
ipcon = IPConnection()
db = BrickletDualButtonV2(UID, ipcon)

def show_temperature(): # C
    UIDT = "Wcg"

    from tinkerforge.bricklet_ptc_v2 import BrickletPTCV2

    global ipcon
    ptc = BrickletPTCV2(UIDT, ipcon)

    temperature = ptc.get_temperature()
    temperature = int(temperature/100.0)
    temperature_array = zerlege_zahl_in_ziffern(temperature)
    print("temp")

    UIDS = "Tre"

    from tinkerforge.bricklet_segment_display_4x7_v2 import BrickletSegmentDisplay4x7V2

    sd = BrickletSegmentDisplay4x7V2(UIDS, ipcon)

    sd.set_brightness(10)

    sd.set_numeric_value(temperature_array)
    sd.set_selected_segment(1, False)
    sd.set_selected_segment(2, False)
    sd.set_selected_segment(6, False)



def show_illuminance(): # L
    UID = "Pdw" 

    from tinkerforge.bricklet_ambient_light_v3 import BrickletAmbientLightV3

    global ipcon
    al = BrickletAmbientLightV3(UID, ipcon) 

    illuminance = al.get_illuminance()
    illuminance = int(illuminance/100.0)
    illuminance_array = zerlege_zahl_in_ziffern(illuminance)
    print("illu")

    UIDS = "Tre"

    from tinkerforge.bricklet_segment_display_4x7_v2 import BrickletSegmentDisplay4x7V2

    sd = BrickletSegmentDisplay4x7V2(UIDS, ipcon)

    sd.set_brightness(10)

    sd.set_numeric_value(illuminance_array)
    sd.set_selected_segment(0, False)
    sd.set_selected_segment(1, False)
    sd.set_selected_segment(2, False)
    sd.set_selected_segment(6, False)



def show_humidity(): # P
    UID = "ViW"

    from tinkerforge.bricklet_humidity_v2 import BrickletHumidityV2

    global ipcon
    h = BrickletHumidityV2(UID, ipcon)

    humidity = h.get_humidity()
    humidity = int(humidity/100.0)
    humidity_array = zerlege_zahl_in_ziffern(humidity)
    print("humi")

    UIDS = "Tre"

    from tinkerforge.bricklet_segment_display_4x7_v2 import BrickletSegmentDisplay4x7V2

    sd = BrickletSegmentDisplay4x7V2(UIDS, ipcon)

    sd.set_brightness(10)

    sd.set_numeric_value(humidity_array)
    sd.set_selected_segment(2, False)
    sd.set_selected_segment(3, False)
    sd.set_selected_segment(6, True)



def cb_state_changed(button_l, button_r, led_l, led_r):
    from tinkerforge.bricklet_dual_button_v2 import BrickletDualButtonV2

    global index
    global db

    if button_l == BrickletDualButtonV2.BUTTON_STATE_PRESSED:
        db.set_led_state(2, 3)
        if index == 1:
            index = 3
        else:
            index = index - 1

        if index == 1:
            show_temperature()
        elif index == 2:
            show_illuminance()
        elif index == 3:
            show_humidity()
        print("Left Button gedrückt", index)

    elif button_r == BrickletDualButtonV2.BUTTON_STATE_PRESSED:
        db.set_led_state(3, 2)
        if index == 3:
            index = 1
        else:
            index = index + 1

        if index == 1:
            show_temperature()
        elif index == 2:
            show_illuminance()
        elif index == 3:
            show_humidity()
        print("Right Button gedrückt", index)

def buttons():
    global ipcon
    ipcon.connect(HOST, PORT)

    show_temperature()

    from tinkerforge.bricklet_dual_button_v2 import BrickletDualButtonV2

    global db

    db = BrickletDualButtonV2(UID, ipcon)

    db.register_callback(db.CALLBACK_STATE_CHANGED, cb_state_changed)
    db.set_state_changed_callback_configuration(True)

    print("Warte auf Tastendrücke... (zum Beenden Strg+C drücken)")
    input()

    ipcon.disconnect()



def zerlege_zahl_in_ziffern(zahl: int) -> list:
    ziffern = [int(stelle) for stelle in str(abs(zahl))]
    while len(ziffern) < 4:
        ziffern.insert(0, 0)
    return ziffern



buttons()
