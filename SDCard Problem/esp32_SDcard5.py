
import esp
esp.osdebug(esp.LOG_VERBOSE)

import machine, vfs, os

# These PINs were defined in machine_sdcard.c
# sd = machine.SDCard(slot=3, sck=14, mosi=13, miso=12, cs=15)
# sd = machine.SDCard(slot=2, sck=18, mosi=23, miso=19, cs=5)
sd = machine.SDCard(slot=2)

print('Mounting SDCARD')
vfs.mount(sd, '/sd')

print('Listing /sd')
print(os.listdir('/sd'))

print('Open test.txt for read')
with open('/sd/test.txt', 'r') as fr:
     r = fr.read()
     if len(r) > 0: print(r)

print('Open test.txt for append')
with open('/sd/test.txt', 'a') as fw:
     msg = 'Hello there!\r\n'
     fw.write(msg)

