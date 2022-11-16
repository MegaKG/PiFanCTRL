#!/usr/bin/env python3
import RPi.GPIO as GPIO
import json
import sys
import os
import time

GPIO.setmode(GPIO.BCM)


def DefaultMapping():
    MaxTemp = 0
    for i in os.listdir('/sys/class/thermal/'):
        if 'thermal_zone' in i:
            f = open('/sys/class/thermal/' + i + '/temp','r')
            Temp = int(f.read())/1000
            f.close()

            if Temp > MaxTemp:
                MaxTemp = Temp
    return MaxTemp

class lineEq:
    def __init__(self,LinePoints):
        self.Equations = {}

        LastX = 0
        LastY = 0
        for i in sorted(list(LinePoints.keys())):
            X,Y = (int(i),LinePoints[i])

            self.Equations[int(i)] = (X,Y,LastX,LastY)

            LastX = X
            LastY = Y

    def point(self,X):
        Key = list(self.Equations.keys())[0]
        for i in self.Equations:
            if X < i:
                Key = i
                break

        Dat = self.Equations[Key]
        M = (Dat[3]-Dat[1])/(Dat[2]-Dat[0])
        return M * (X - Dat[0]) + Dat[1]


class fancontrol:
    def __init__(self,Mapping,FetchFunction,PIN):
        GPIO.setup(PIN,GPIO.OUT)

        self.p = GPIO.PWM(PIN,400)
        self.p.start(0)

        self.fetcher = FetchFunction
        self.PIN = PIN
        self.Mapping = Mapping

        self.EQ = lineEq(self.Mapping)

    def run(self):
        while True:
            Temperature = self.fetcher()
            
            Y = self.EQ.point(Temperature)

            self.p.ChangeDutyCycle(int(round(Y,0)))
            time.sleep(10)



if __name__ == '__main__':
    #Load Config
    f = open(sys.argv[1],'r')
    Config = json.loads(f.read())
    f.close()

    ctrl = fancontrol(Config['Curve'],DefaultMapping,Config['GPIOPin'])
    ctrl.run()