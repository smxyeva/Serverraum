from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_lcd_128x64 import BrickletLCD128x64
from tinkerforge.bricklet_ptc_v2 import BrickletPTCV2

HOST = "172.20.10.242"
PORT = 4223

UID_LCD = "24Rh"
UID_PTC = "Wcg"

ipcon = IPConnection()
ipcon.connect(HOST, PORT)

lcd = BrickletLCD128x64(UID_LCD, ipcon)
ptc = BrickletPTCV2(UID_PTC, ipcon)

tarray = []
max_points = 60

def cb_temperature(temperature):
    current_temp = int(temperature / 100.0)
    print(current_temp)

    if len(tarray) >= max_points:
        tarray.pop(0)

    tarray.append(current_temp)

    lcd.set_gui_graph_data(0, tarray)

lcd.clear_display()
lcd.remove_all_gui()
lcd.set_gui_graph_configuration(0, lcd.GRAPH_TYPE_LINE, 62, 0, 60, 52, "Zeit", "°C")

ptc.register_callback(ptc.CALLBACK_TEMPERATURE, cb_temperature)

ptc.set_temperature_callback_configuration(0, True, "x", 0, 0)

try:
    print("Drücke Enter zum Beenden")
    input()
finally:
    ipcon.disconnect()
