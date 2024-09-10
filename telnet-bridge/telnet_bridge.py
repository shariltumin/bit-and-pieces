import network
import socket
import select
import time

# Set up the Access Point (AP Mode)
def setup_ap(ssid, pwd, ip):
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password=pwd, authmode=3)
    z = (ip, '255.255.255.0', ip, ip)
    ap.ifconfig(z)
    print("AP mode active with IP:", ap.ifconfig()[0])
    return ap.ifconfig()[0]  # Return the AP IP address

# Connect ESP32 to external Wi-Fi (STA Mode)
def connect_sta(ssid, pwd):
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    if not sta.isconnected():
        print('Connecting to external Wi-Fi...')
        sta.connect(ssid, pwd)
        while not sta.isconnected():
            time.sleep(1)
            print('Connecting...')
    print('Connected to external Wi-Fi with IP:', sta.ifconfig()[0])
    return sta.ifconfig()[0]  # Return the STA IP address

# Create Telnet Server on both AP and STA sides
def create_telnet_server(host, port=23):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f'Telnet server started on {host}:{port}, waiting for a client...')
    
    # Wait for a connection from a client
    conn, addr = server_socket.accept()
    print(f'Client connected from {addr}')
    _ = conn.recv(256) # ignore connection handshake/header
    return conn

# Relay data between the two Telnet clients using poll()
def relay_telnet_with_poll(ap_client_conn, sta_client_conn):
    # Create a poll object
    poller = select.poll()

    # Register both the AP client and the STA client socket for read events
    poller.register(ap_client_conn, select.POLLIN)  # POLLIN means the socket is ready to read
    poller.register(sta_client_conn, select.POLLIN)

    while True:
        # Poll for events (with a timeout of 1000 ms)
        events = poller.poll(1000)

        # Process each event
        for sc, event in events:
            #print('EVENT:', fd, event)
            if event & select.POLLIN:  # If there is data to read
                if sc == ap_client_conn:
                    # Data is available from the AP client
                    #data = ap_client_conn.recv(1024)
                    data = ap_client_conn.readline()
                    if not data:
                        print("AP client disconnected")
                        return
                    # Forward data to the STA client
                    sta_client_conn.send(data)
                    print("Forwarded data from AP client to STA client")
                elif sc == sta_client_conn:
                    # Data is available from the STA client
                    #data = sta_client_conn.recv(1024)
                    data = sta_client_conn.readline()
                    if not data:
                        print("STA client disconnected")
                        return
                    # Forward data to the AP client
                    ap_client_conn.send(data)
                    print("Forwarded data from STA client to AP client")

# Main function
def main():
    # Step 1: Set up the AP and STA connections, change these values
    ap_ip = setup_ap(AP_SSID, AP_PWD, '10.10.4.1') # AP: ssid, pwd, ip
    sta_ip = connect_sta(SSID, PWD)                # STA: ssid, pwd
    print('AP:', ap_ip, 'STA:', sta_ip)
    
    # Step 2: Start Telnet server on the AP side (listening for incoming connections)
    ap_client_conn = create_telnet_server(host=ap_ip, port=23)

    # Step 3: Start Telnet server on the STA side (listening for incoming connections)
    sta_client_conn = create_telnet_server(host=sta_ip, port=23)

    # Step 4: Start relaying data between the AP client and the STA client
    relay_telnet_with_poll(ap_client_conn, sta_client_conn)

# Execute the main function
if __name__ == "__main__":
    main()

