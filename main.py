#! /usr/bin/env python3
import string
import requests
import json
import math
import time
from evdev import InputDevice
from select import select

incdb = 1
inc = 10 ** (incdb / 20)
maxvol = 10 ** -(3/20)

keys = "X^1234567890XXXXqwertzuiopXXXXasdfghjklXXXXXyxcvbnmXXXXXXXXXXXXXXXXXXXXXXX"
dev = InputDevice('/dev/input/by-id/usb-flirc.tv_flirc-if01-event-kbd')
url = 'http://192.168.0.10/datastore/mix/chan/2/matrix/fader'
t =  time.time()
while True:
   r,w,x = select([dev], [], [])
   for event in dev.read():
        print(event, time.time()-t)
        if (time.time() - t) > 0.15 and event.type==1 and (event.value==1 or event.value==2):
            t= time.time()
            r = requests.get(url)
            valdct = r.json()
            oldvol = valdct['value']
            if event.code == 103:
                newvol = oldvol * inc
            elif event.code == 108:
                newvol = oldvol / inc
            newvol = min(maxvol, newvol)
            payload = {'value': newvol}
            post_r = requests.post(url, data={'json': json.dumps(payload)})
            
            print(oldvol, newvol)
