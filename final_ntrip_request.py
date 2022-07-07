from serial import Serial
import socket
import time
import base64

def send_nmea():
    username = "Visystem1"
    password = "stem21"
    port = 2101
    host = "192.168.43.29"
    pwd = base64.b64encode("{}:{}".format(username, password).encode('ascii'))
    pwd = pwd.decode('ascii')
    header = \
        "GET /U-BLOX HTTP/1.1\r\n" + \
        "Host: 192.168.43.29\r\n" + \
        "Ntrip-Version: Ntrip/2.0\r\n" + \
        "User-Agent: NTRIP NtripClientPOSIX/1.51\r\n" + \
        "Connection: close\r\n" + \
        "Authorization: Basic {}\r\n\r\n".format(pwd)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    s.send(header.encode('ascii'))
    time.sleep(2) # Промежуток для получения gnss даты
    data = s.recv(4096)
    ser = Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.write(data)
    ser.close()
    print(data)
    return data

# Промежуток между отправкой gnss даты
send_nmea()
