#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smbus
import math
from time import sleep
import csv
import socket
import time
import sys

DEV_ADDR = 0x68

ACCEL_XOUT = 0x3b
ACCEL_YOUT = 0x3d
ACCEL_ZOUT = 0x3f
TEMP_OUT = 0x41
GYRO_XOUT = 0x43
GYRO_YOUT = 0x45
GYRO_ZOUT = 0x47

PWR_MGMT_1 = 0x6b
PWR_MGMT_2 = 0x6c   

bus = smbus.SMBus(1)
bus.write_byte_data(DEV_ADDR, PWR_MGMT_1, 0)

## udp setting
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_ip = "192.168.2.114"
server_port = 50008

## connection check
while True:
    try:
        s.connect((server_ip, server_port))
        # s.close()
        print("connection success")
        break
    except socket.error:
        print("connection failed")

def read_word(adr):
    high = bus.read_byte_data(DEV_ADDR, adr)
    low = bus.read_byte_data(DEV_ADDR, adr+1)
    val = (high << 8) + low
    return val

# Sensor data read
def read_word_sensor(adr):
    val = read_word(adr)
    if (val >= 0x8000):         # minus
        return -((65535 - val) + 1)
    else:                       # plus
        return val


def get_temp():
    temp = read_word_sensor(TEMP_OUT)
    x = temp / 340 + 36.53      # data sheet(register map)記載の計算式.
    return x


def getGyro():
    x = read_word_sensor(GYRO_XOUT)/ 131.0
    y = read_word_sensor(GYRO_YOUT)/ 131.0
    z = read_word_sensor(GYRO_ZOUT)/ 131.0
    return x, y, z


def getAccel():
    x = (read_word_sensor(ACCEL_XOUT)/ 16384.0) * 9.8
    y= (read_word_sensor(ACCEL_YOUT)/ 16384.0) * 9.8
    z= (read_word_sensor(ACCEL_ZOUT)/ 16384.0) * 9.8
    return x, y, z

status = 0
average = 0.0
readyCount = 0
with open("pitching.log", "w") as f:
    pit_log = csv.writer(f)
    while 1:
        try:
            ax, ay, az = getAccel()
            gx, gy, gz = getGyro()
            #print ('{0:4.3f},   {1:4.3f},    {2:4.3f},     {3:4.3f},      {4:4.3f},      {5:4.3f},' .format(gx, gy, gz, ax, ay, az))
            
            sumVec = math.sqrt((ax*ax)+(ay*ay)+(az*az))
            print ("sumVec = {0:4.3f}".format(sumVec))
            if sumVec > 30 and status is 1:
                print("swing!!!!!")
                s.sendto(b'swing', (server_ip, server_port))
                status = 0
                sleep(1.00)

            if status is 0:
                if sumVec > 9.6 and sumVec < 10.5:
                    readyCount += 1
                    if readyCount is 20:
                        status = 1
                        print("Ready")
                        s.sendto(b'ready', (server_ip, server_port))
                        readyCount = 0

            sleep(0.05)

        except KeyboardInterrupt:
            sys.exit(-1)
        except:
            pass
