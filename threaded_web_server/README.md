Web servers listening to port 80 and 88 using _thread on ESP32 MicroPython v1.27.0-preview.317

Start in REPL
```
>>> import http_srv
Starting WEB, 192.168.4.85 listening on port 80
Starting CMD, 192.168.4.85 listening on port 88
```

Test port 88
```
$ curl -v http://192.168.4.85:88
*   Trying 192.168.4.85:88...
* TCP_NODELAY set
* Connected to 192.168.4.85 (192.168.4.85) port 88 (#0)
> GET / HTTP/1.1
> Host: 192.168.4.85:88
> User-Agent: curl/7.68.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Content-Type: text/html
< Connection: close
< Content-Length: 34
< 
The core temperature is 55.000000
* Closing connection 0
```

Test port 80
```
$ curl -v http://192.168.4.85:80 --output pix.png
*   Trying 192.168.4.85:80...
* TCP_NODELAY set
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0* Connected to 192.168.4.85 (192.168.4.85) port 80 (#0)
> GET / HTTP/1.1
> Host: 192.168.4.85
> User-Agent: curl/7.68.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Content-Type: image/png
< Transfer-Encoding: chunked
< Connection: close
< 
{ [519 bytes data]
100  148k    0  148k    0     0  39382      0 --:--:--  0:00:03 --:--:-- 39372
* Closing connection 0
$ ls -l pix.png
-rw-rw-r-- 1 sharil sharil 152449 Nov  2 16:59 pix.png
```

