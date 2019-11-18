#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import serial
import argparse
import socket
import sys

def waitPitching(bluetooth_serial):
    while True:
        char = bluetooth_serial.read()
        
        if char == '':
            continue
        else:
            print('recieve pitch')

def wait_signal(key):
    server_ip = "192.168.2.112"
    port = 50008
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #s.settimeout(30.0)
        s.bind((server_ip, port))
        data, addr = s.recvfrom(1024)
        print("data: {}, addr: {}".format(data, addr))
        if data == key:
            return True
    except socket.timeout:
        print("timeout")
    except KeyboardInterrupt:
        sys.exit(-1)
    except:
        print("except")
    return False

# init servo
gp_list = [4, 17]
servos = []
GPIO.setmode(GPIO.BCM)
for n in gp_list:
    GPIO.setup(n, GPIO.OUT)
    servo = GPIO.PWM(n, 50)
    servo.start(0)
    servos.append(servo)

while True:
    ret = wait_signal(b"ready")
    print(ret)
    
    if not ret:
        continue
    print("connect success")

    # wait signal
    servos[0].ChangeDutyCycle(6)
    time.sleep(1)
    servos[1].ChangeDutyCycle(4.7)    # batter 
    #servos[1].ChangeDutyCycle(12)    # pitcher
    #time.sleep(5)

    ret = wait_signal(b"pitching")
    print(ret)
    if not ret:
        continue
        
    time.sleep(0.55)
    # get signal
    servos[0].ChangeDutyCycle(1)    # about 80 degree
    time.sleep(2)
    servos[1].ChangeDutyCycle(9.3)    # batter
    #servos[1].ChangeDutyCycle(1)   # pitcher
    #time.sleep(3)

# term
for servo in servos:
    servo.stop()
GPIO.cleanup()
