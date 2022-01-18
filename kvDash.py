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
from kivy.properties import ObjectProperty


#Config.set('graphics', 'resizable', '0')
#Config.set('graphics', 'width', '1920')
Window.size = (1920, 720)
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 0)
Config.set('graphics', 'top', 100)

Builder.load_file('dash1.kv')
#Builder.load_file('my.kv')


class BaseGridLayout(Widget):
    runTach = ObjectProperty()
    tachPointer = ObjectProperty()
    tempPointer = ObjectProperty()
    fuelPointer = ObjectProperty()


    def doFuel(self):
        print('running fuel!!!!!!!')

        with self.fuelPointer.canvas.before:
            PushMatrix()
            (200,20)
            Rotate(origin=(350,170), angle=-30.0, axis= (0,0,1))
            #self.fuelPointer.canvas.opacity = 0.0
        with self.fuelPointer.canvas.after:
            PopMatrix()

    def doTach(self):
        print('running tach!!!!!!!')
        print(self.tachPointer.canvas)

        with self.tachPointer.canvas.before:
            PushMatrix()
            print(self.tachPointer.origin)
            Rotate(origin=(990,335), angle=-30.0, axis= (0,0,1))
        with self.tachPointer.canvas.after:
            PopMatrix()

#1000 = 26
#2000 = 53
#3000 = 82
#4000 = 108
            #PushMatrix()
            #Rotate(origin=self.tachPointer.canvas.rotate_origin, angle=self.tachPointer.canvas.angle)
            #Color(rgb=(1,255,0))
            #Rectangle(pos=self.tachPointer.canvas.rect_pos, size=self.tachPointer.canvas.rect_size)
            #PopMatrix()
            #self.tachPointer.canvas.pos = self.tachPointer.canvas.rect_pos
            #self.tachPointer.canvas.size = self.tachPointer.canvas.rect_size

        #with self.tachPointer.canvas.before:
            #PushMatrix()
            #self.rot = Rotate()
            #self.pos = (self.center_x, self.center_y)
            #print(self.pos)
            #self.rot.origin = self.tachPointer.center
            #self.rot.axis = (0,0,1)
            #self.rot.angle = 45
            #self.rect_bg = Rectangle(source="pointer.png",
                                     #pos=self.pos,
                                     #size=(580,580))
            #
            #Rotate(angle=45)
            #Rectangle(pos=self.tachPointer.canvas.rect_pos, size=self.tachPointer.canvas.rect_size)
            #PopMatrix()
        self.runTach.text = "done"


class MyBackground(Widget):
    def __init__(self, **kwargs):
        super(MyBackground, self).__init__(**kwargs)
        with self.canvas:
            self.bg = Rectangle(source="images/cf-background.jpg",
                                pos=self.pos,
                                size_hint_y=None,
                                width=1920,
                                allow_stretch=True)

        self.bind(pos=self.update_bg)
        self.bind(size=self.update_bg)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size


class FireflyApp(App):

    def build(self):
        Window.borderless = True
        parent = MyBackground()
        dash = BaseGridLayout()
        parent.add_widget(dash)
        return parent
        #return BaseGridLayout()

if __name__ == '__main__':
    LabelBase.register(name="DSEG7Classic",
                       fn_regular='font/DSEG7Classic-Regular.ttf')
    FireflyApp().run()
