Run AP+STA on ESP32 at the same time. Send text messages between two telnet clients, one on the AP side and the other on the STA side using the ESP32 as a bridge.

The script needs more work to be useful, it is just a proof of concept.

The run log below shows that we can run AP+STA on ESP32 at the same time.

```bash
Remount local directory ./ at /remote
>>> import telnet_bridge
>>> telnet_bridge.main()
AP mode active with IP: 10.10.4.1
Connected to external Wi-Fi with IP: 192.168.4.92
AP: 10.10.4.1 STA: 192.168.4.92
Telnet server started on 10.10.4.1:23, waiting for a client...
Client connected from ('10.10.4.2', 42582)
Telnet server started on 192.168.4.92:23, waiting for a client...
Client connected from ('192.168.4.27', 45704)
Forwarded data from AP client to STA client
Forwarded data from AP client to STA client
Forwarded data from STA client to AP client
Forwarded data from AP client to STA client
Forwarded data from STA client to AP client
Forwarded data from AP client to STA client
Forwarded data from AP client to STA client
AP client disconnected
>>>
```
