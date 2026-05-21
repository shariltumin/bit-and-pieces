# wifi-switch (ESP8266)
import network, esp, time

# on esp32
# wlan.config(pm=network.WLAN.PM_PERFORMANCE)

# on esp8266
esp.sleep_type(esp.SLEEP_NONE) # alway stay awake, don't go to sleep

SSID = "Knight_Gate"
PWD = "LetMeInNow"
CNL = const(11)
AMODE = network.AUTH_WPA2_PSK

ap = network.WLAN(network.AP_IF)

def config(ap):
    ap.active(True)
    ap.config(txpower=20.5) # crash if bad power-supply
    ap.config(hidden=False) # don't hide me
    ap.config(essid=SSID, password=PWD, authmode=AMODE, channel=CNL)

def open_gate(w, ap):
    # check friendly w here
    print(f'>>>> gate open for {w}')
    # gate open, disable your phone Wifi  
    # you may need to rescan WiFi

config(ap)
w, cln = b'', []

while True:
    cln=ap.status('stations')
    if not (cln and ap.isconnected()): 
       time.sleep(1); 
       w = b''
       continue
    else:
       v = cln[0][0]           # simple one at a time
       # print('CLN:', cln) # debug
       if v != w:
          ap.active(False)  # Disable WiFi
          time.sleep(0.5)   # sleep a while before switching the relay 
          open_gate(v, ap)  # You need to disable your phone Wifi after gate opened
          w = v
          time.sleep(10)    # sleep total period of gate open and close
          config(ap)        # reconfigure AP and ready for next round

