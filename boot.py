from Maix import GPIO
from fpioa_manager import *
from board import board_info
import sensor, image, lcd, time
import KPU as kpu
import lcd
import image
import sys
import random

try:
    lcd.init()
    lcd.rotation(2)
    lcd.clear()
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_windowing((224, 224))
    sensor.run(1)

    labels=['1','2','3']
    task = kpu.load("/sd/gutyokipa.kmodel")
    img0 = image.Image("/sd/jyanken.jpg")
    img1=image.Image("/sd/gu.jpg")
    img2=image.Image("/sd/tyoki.jpg")
    img3=image.Image("/sd/pa.jpg")
    aiko = image.Image("/sd/aiko.jpg")
    kati = image.Image("/sd/kati.jpg")
    make=  image.Image("/sd/make.jpg")
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
        lcd.display(img0)
        time.sleep(1)
        img = sensor.snapshot()
        lcd.display(img)

        fmap = kpu.forward(task, img)
        plist=fmap[:]
        pmax=max(plist)
        max_index=plist.index(pmax)

        a=int(labels[max_index].strip())
        comp=random.randrange(1, 4)

        if( comp == 1):
            lcd.display(img1)
            time.sleep(2)
        elif( comp ==2):
            lcd.display(img2)
            time.sleep(2)
        else:
            lcd.display(img3)
            time.sleep(2)

        if( a == comp):
            lcd.display(aiko)
        elif(a ==((comp+1)%3+1)):
            lcd.display(kati)
        else:
            lcd.display(make)

        time.sleep(1)

    kpu.deinit(task)

except:
    lcd.clear()
    ch.deinit()
    sys.exit()
