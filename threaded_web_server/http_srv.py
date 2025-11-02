
import socket as soc
import gc, time, network, esp32
import _thread as th
from time import sleep_ms
from cred import cred

ssid, pwd = cred
# setup Wifi
network.WLAN(network.AP_IF).active(False)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.config(pm=0) # disable power management
wlan.config(txpower=20)
wlan.connect(ssid, pwd)
sleep_ms(5000)
ip = wlan.ifconfig()[0]

def cln_handler(w, cs):  # per client cs socket
   blk = 512
   ok = True
   try:
      q = cs.recv(blk) # read at most 512 char
   except Exception as e:
      print('Read Error:', e)
      print('Sleep for 3 sec')
      sleep_ms(3000)
      ok = False
   if ok:
      if w == 80:
         th.start_new_thread(file_uploader, (cs,)) # new thread to send big file
      elif w == 88:
         th.start_new_thread(cmd_rep, (cs,)) # new thread to send reply
      else: pass
   else:
      cs.close()
      del cs

def cmd_rep(cs):
    msg = b'The core temperature is %f\n' % ((esp32.raw_temperature() - 32) / 1.8)
    # --- Send headers ---
    cs.write(b"HTTP/1.1 200 OK\r\n")
    cs.write(b"Content-Type: text/html\r\n")
    cs.write(b"Connection: close\r\n")
    cs.write(b"Content-Length: %i\r\n"%len(msg))
    cs.write(b"\r\n")
    cs.write(msg)
    #
    cs.close()

def file_uploader(cs):
    CHUNK_SIZE = 512
    # 
    f = open("/kakilima.png", 'rb') # 152449 bytes

    # --- Send headers ---
    cs.write(b"HTTP/1.1 200 OK\r\n")
    cs.write(b"Content-Type: image/png\r\n")
    cs.write(b"Transfer-Encoding: chunked\r\n")
    cs.write(b"Connection: close\r\n")
    cs.write(b"\r\n")

    # --- Send file in chunks ---
    while True:
        chunk = f.read(CHUNK_SIZE)
        if not chunk:
            break
        cs.write(b"%x\r\n" % len(chunk))
        cs.write(chunk + b"\r\n")
        sleep_ms(10)

    # --- End of chunks ---
    cs.write(b"0\r\n\r\n")

    # close to release resources
    f.close()
    cs.close()

def server(port):
   srv = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
   srv.setsockopt(soc.SOL_SOCKET, soc.SO_REUSEADDR, 1)
   ai = soc.getaddrinfo(ip, port)
   addr = ai[0][4]
   srv.bind(addr)
   return srv

def web_server(cln):  # cln is number of client we want cache at connect
   # start listening for telnet connections on port 80
   port = 80
   print("Starting WEB,", ip, "listening on port", port)
   srv = server(port)
   srv.listen(cln) # cache 5 clients connection request
   while(True):
      cs, ca = srv.accept() # this will block
      th.start_new_thread(cln_handler, (port,cs)) # new thread to serve client
      sleep_ms(1000)

def cmd_server(cln):  # cln is number of client we want cache at connect
   # start listening for telnet connections on port 88
   port = 88
   print("Starting CMD,", ip, "listening on port", port)
   srv = server(port)
   srv.listen(cln) # cache 5 clients connection request
   while(True):
      cs, ca = srv.accept() # this will block
      th.start_new_thread(cln_handler, (port,cs)) # new thread to serve client
      sleep_ms(100)

# start cmd-server on a new thread
th.start_new_thread(cmd_server, (5,))

# start web-server on main task
web_server(5)

# New reach
print('System Aborted')

