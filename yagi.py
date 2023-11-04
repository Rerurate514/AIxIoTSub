from Maix import GPIO
from fpioa_manager import *
from board import board_info
import sensor, image, lcd, time
import KPU as kpu
import lcd
import image
import sys
import random

lcd.init()
lcd.rotation(2)
lcd.clear()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
sensor.run(1)

labels=['1','2']
task = kpu.load("yagi2.kmodel")

fm.register(board_info.BUTTON_B, fm.fpioa.GPIO1)
but_b=GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP)

but_b_pressed = 0

while(True):
    img = sensor.snapshot()
    lcd.display(img)
    if (but_b.value() == 0 and but_b_pressed == 0):
        but_b_pressed=1
        break

while(True):
    img = sensor.snapshot()
    lcd.display(img)

    fmap = kpu.forward(task, img)
    plist=fmap[:]
    pmax=max(plist)
    max_index=plist.index(pmax)

    a=int(labels[max_index].strip())

    lcd.draw_string(30,30,"a=%d"%(a),lcd.WHITE, lcd.BLACK)

    if( a == 1):
        lcd.draw_string(30,50,'kina',lcd.WHITE, lcd.BLACK)
    else:
        lcd.draw_string(30,50,'kuro',lcd.WHITE, lcd.BLACK)


    time.sleep(2)

kpu.deinit(task)
