import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.label import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rotate, Color, Line, Rectangle, PushMatrix, PopMatrix
from kivy.config import Config
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen
import json
import time
import redis
import threading

with open('config.json') as f:
    config = json.load(f)


Window.size = (config['windowSizeX'], config['windowSizeY'])
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 0)
Config.set('graphics', 'top', 100)

Builder.load_file('dash1.kv')
Builder.load_file('dash2.kv')
global pthread

def validateData(data):
    newData = {
        "speed": 0,
        "odometer": 0,
        "rpm": 0,
        "coolantTemp": 0,
        "fuelLevel": 0,
        "volts": 0,
        "oilPressure": 0,
        "leftArrow": False,
        "rightArrow": False,
        "bright": False,
        "battery": False,
        "checkEngine": False,
        "seatBelt": False,
        "airBag": False,
        "parking": False,
        "coolant": False,
        "lowOil": False
        }

    for k,v in data.items():
        newData[k] = v

    return newData

def lightOn(item):
    with item.canvas.before:
        PushMatrix()
        item.canvas.opacity = 1.0
    with item.canvas.after:
        PopMatrix()

def lightOff(item):
    with item.canvas.before:
        PushMatrix()
        item.canvas.opacity = 0.0
    with item.canvas.after:
        PopMatrix()

def updatePointer(pointer, origin, angle, axis):
    print("old angle: " + str(pointer.angle))
    print("new angle: " + str(angle))

    moveAgnle = angle - pointer.angle

    pointer.angle = angle
    with pointer.canvas.before:
        PushMatrix()
        Rotate(origin=origin, angle=moveAgnle * -1, axis=axis)
    with pointer.canvas.after:
        PopMatrix()


class Dash2Layout(Screen):
    def __init__(self, **kwargs):
        super(Dash2Layout, self).__init__(**kwargs)
        #runTach = ObjectProperty()
        leftArrow = ObjectProperty()
        rightArrow = ObjectProperty()
        bright = ObjectProperty()
        battery = ObjectProperty()
        checkEngine = ObjectProperty()
        seatBelt = ObjectProperty()
        airBag = ObjectProperty()
        parking = ObjectProperty()
        coolant = ObjectProperty()
        lowOil = ObjectProperty()
        tachPointer = ObjectProperty()
        tempPointer = ObjectProperty()
        fuelPointer = ObjectProperty()
        voltsPointer = ObjectProperty()
        oilPointer = ObjectProperty()
        speed = ObjectProperty()
        shift = ObjectProperty()

        r = redis.Redis(host=config['redis']['ip'], port=config['redis']['port'])
        p = r.pubsub()
        p.subscribe(**{'data':self.processQueue})
        global pthread
        pthread = p.run_in_thread(sleep_time=0.1)

    def processQueue(self, message=None, **kwargs):
        pass

class Dash1Layout(Screen):
    def __init__(self, **kwargs):
        super(Dash1Layout, self).__init__(**kwargs)
        #runTach = ObjectProperty()
        leftArrow = ObjectProperty()
        rightArrow = ObjectProperty()
        bright = ObjectProperty()
        battery = ObjectProperty()
        checkEngine = ObjectProperty()
        seatBelt = ObjectProperty()
        airBag = ObjectProperty()
        parking = ObjectProperty()
        coolant = ObjectProperty()
        lowOil = ObjectProperty()
        tachPointer = ObjectProperty()
        tempPointer = ObjectProperty()
        fuelPointer = ObjectProperty()
        voltsPointer = ObjectProperty()
        oilPointer = ObjectProperty()
        speed = ObjectProperty()
        shift = ObjectProperty()


        r = redis.Redis(host=config['redis']['ip'], port=config['redis']['port'])
        p = r.pubsub()
        p.subscribe(**{'data':self.processQueue})
        global pthread
        pthread = p.run_in_thread(sleep_time=0.1)


    def processQueue(self, message=None, **kwargs):

        try:
            dataRaw = json.loads(message['data'].decode('UTF-8'))
            data = validateData(dataRaw)
        except:
            data = validateData(dataRaw)

        print(data)

        if data['leftArrow'] == True:
            #self.blinkLeft()
            #nblinkLeft(self.leftArrow)
            lightOn(self.leftArrow)
        elif data['leftArrow'] == False:
            #self.blinkLeftOff()
            lightOff(self.leftArrow)

        if data['rightArrow'] == True:
            lightOn(self.rightArrow)
        elif data['rightArrow'] == False:
            lightOff(self.rightArrow)

        if data['bright'] == True:
            lightOn(self.bright)
        elif data['bright'] == False:
            lightOff(self.bright)

        if data['battery'] == True:
            lightOn(self.battery)
        elif data['battery'] == False:
            lightOff(self.battery)

        if data['checkEngine'] == True:
            lightOn(self.checkEngine)
        elif data['checkEngine'] == False:
            lightOff(self.checkEngine)

        if data['seatBelt'] == True:
            lightOn(self.seatBelt)
        elif data['seatBelt'] == False:
            lightOff(self.seatBelt)

        if data['airBag'] == True:
            lightOn(self.airBag)
        elif data['airBag'] == False:
            lightOff(self.airBag)

        if data['parking'] == True:
            lightOn(self.parking)
        elif data['parking'] == False:
            lightOff(self.parking)

        if data['coolant'] == True:
            lightOn(self.coolant)
        elif data['coolant'] == False:
            lightOff(self.coolant)

        # convert rpm to pointer angle
        # 0 - 240 degrees
        # 1000rpm = 30degrees
        # 240/8000 = 0.03
        # 0.03 * 1000
        # or 30degrees = (240/8000) * 1000rpm
        if data['rpm'] > 7500 and data['rpm'] < 7700:
            print('RED!!!!!!!!!!!!!!!!!!!!!!')
            with self.shift.canvas.before:
                Color(rgba=[1,0,0,.2])
        elif data['rpm'] > 7700:
            print('RED!!!!!!!!!!!!!!!!!!!!!!')
            with self.shift.canvas.before:
                Color(rgba=[1,0,0,.5])
        else:
            with self.shift.canvas.before:
                Color(rgba=[1,0,0,0])


        if data['rpm'] < 0:
            neededAngle = 0
        elif data['rpm'] > 8000:
            neededAngle = 240
        else:
            neededAngle = 0.03 * data['rpm']
        print("tachPointer")
        updatePointer(self.tachPointer, self.tachPointer.origin, neededAngle, (0,0,1))

        # convert temp to pointer angle
        # 0 - 240 angle degrees
        # 100 - 280 temp degrees
        # adjust input temp to 0 base by subtracing 100
        #0 - 180 = 0 - 240

        if data['coolantTemp'] < 100:
            neededAngle = 0
        elif data['coolantTemp'] > 280:
            neededAngle = 240
        else:
            correctedTemp = data['coolantTemp'] - 100
            neededAngle = correctedTemp * 1.33
        print("coolantTemp")
        updatePointer(self.tempPointer, self.tempPointer.origin, neededAngle, (0,0,1))

        # convert fuel to pointer angle
        # 0 - 240 angle degrees
        # 0 - 1 tank fullness
        # fullness * 240
        if data['fuelLevel'] < 0:
            neededAngle = 0
        elif data['fuelLevel'] > 1:
            neededAngle = 240
        else:
            neededAngle = data['fuelLevel'] * 240
        print("fuelLevel")
        updatePointer(self.fuelPointer, self.fuelPointer.origin, neededAngle, (0,0,1))

        # convert volts to pointer angle
        # 0 - 24 angle degrees
        # 8 - 16 volts range
        if data["volts"] < 8:
            neededAngle = 0
        elif data["volts"] > 16:
            neededAngle = 240
        else:
            v = data["volts"] - 8
            neededAngle = v * 30
        print("Volts")
        updatePointer(self.voltsPointer, self.voltsPointer.origin, neededAngle * -1, (0,0,1))

        # convert oil to pointer angle
        # 0 - 240 angle degrees
        # 0 - 1 pressure 1 = 100psi
        # pressure * 240
        if data['oilPressure'] < 0:
            neededAngle = 0
        elif data['oilPressure'] > 1:
            neededAngle = 240
        else:
            neededAngle = data['oilPressure'] * 240
        print("oilPointer")
        updatePointer(self.oilPointer, self.oilPointer.origin, neededAngle * -1, (0,0,1))

        self.speed.text = str(data['speed'])



class MyBackground(Widget):
    def __init__(self, **kwargs):
        super(MyBackground, self).__init__(**kwargs)
        with self.canvas:
            self.bg = Rectangle(source=config['backgroundImage'],
                                allow_stretch=True)

        self.bind(pos=self.update_bg)
        self.bind(size=self.update_bg)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size


class FireflyApp(App):

    def build(self):
        Window.borderless = True
        #parent = MyBackground()
        #dash = BaseGridLayout()
        #parent.add_widget(dash)
        #return parent
        #return BaseGridLayout()
        sm = ScreenManager()
        sm.add_widget(Dash1Layout(name='dash1'))
        sm.add_widget(Dash2Layout(name='dash2'))
        return sm

if __name__ == '__main__':
    #BaseGridLayout.turnLeft(self.root)
    LabelBase.register(name="DSEG7Classic",
                       fn_regular='font/DSEG7Classic-Regular.ttf')
    FireflyApp().run()

    pthread.stop()
