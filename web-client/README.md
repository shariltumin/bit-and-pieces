
This is a copy of the urequests library with a very slight modification to the ```content()``` method, using ```socket.recv(blk)``` instead of ```socket.read()```.

The urequests/requests is a frozen module in the standard MicroPython firmware. The modified version is named "requests_1.py" so as not to conflict with the standard version. To make use of this modified version:

1. copy requests_1.py to your flash
2. import requests_1 as request
3. req = requests.get(URL, timeout=10)

This is not an official version of the library and it is probably not good practice to use a modified version of the standard library. Please use the modified version of the library as a learning tool. If you find that this solves your problem, please request a modification from the MicroPython development team.

