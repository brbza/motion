import utime
import usocket
import network
from mpu6050 import MPU6050
from machine import Pin, I2C

# https://gist.github.com/pharzan/5bb643b383bfea1049eefe44116dcbb1


def do_connect(essid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(essid, password)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


def http_post(method='update', data='{"test":"post"}'):
    url = 'postman-echo.com'
    addr = usocket.getaddrinfo(url, 443)[0][-1]
    s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    s.connect(addr)
    request = 'POST /{method} HTTP/1.1\r\nHost: {address}\r\nContent-Length:'.format(method=method,address=url) + str(len(data)) + ' \r\nContent-Type: application/json\r\n\r\n' + data + '\r\n\r\n'
    print(request)

    bytes_sent = s.send(request)
    print(bytes_sent)
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()
    print("Socket closed.")


def http_get(path='tracked.html'):
    addr = usocket.getaddrinfo('vanhalen.local', 8754)[0][-1]
    s = usocket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, 'vanhalen.local'), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()


def main():
    led = Pin(2, Pin.OUT)
    i2c = I2C(scl=Pin(5), sda=Pin(4))

    accelerometer = MPU6050(i2c)
    accelerometer.get_values()

    enabled = False
    while True:
        if enabled:
            led.off()
        else:
            led.on()
        utime.sleep_ms(1000)
        enabled = not enabled


if __name__ == '__main__':
    main()
