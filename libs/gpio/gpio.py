# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO

# 使うPIN番号
IO_NO = 3

class Gpio:
    def __init__(self):
        self.state = 'off'
        # GPIOピン番号を用いる
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(IO_NO,GPIO.OUT)
        print "init GPIO"

    def on(self):
        try:
            GPIO.output(IO_NO, True)
            self.state = 'on'
        except KeyboardInterrupt:
            self.state = 'off'

    def off(self):
        try:
            GPIO.output(IO_NO, False)
            self.state = 'off'
        except KeyboardInterrupt:
            self.state = 'on'


if __name__ == '__main__':
    gpio_obj = Gpio()
    gpio_obj.off()
