import cymunk as cy
from os.path import dirname, join
from kivy.properties import DictProperty, ListProperty
from kivy.lang import Builder
from Utility import *
from kivy.core.image import Image
from kivy.graphics import Scale, Rotate, PushMatrix, PopMatrix, Translate, \
                          UpdateNormalMatrix
from random import random

class Playground(Widget):
    cbounds = ListProperty([])
    cmap = DictProperty({})
    blist = ListProperty([])
    circleRadius = 50.0

    def __init__(self, **kwargs):
        self._hue = 0
        super(Playground, self).__init__(**kwargs)
        self.init_physics() 
        self.bind(size=self.update_bounds, pos=self.update_bounds)
        self.texture = Image(join(dirname(__file__), 'star.png'), mipmap=True).texture
        Clock.schedule_interval(self.step, 1 / 60.)
        
    def init_physics(self):
        # create the space for physics simulation
        self.space = space = cy.Space()
        space.iterations = 30
        space.gravity = (0, -700)
        space.sleep_time_threshold = 0.5
        space.collision_slop = 0.5

        # create 4 segments that will act as a bounds
        for x in xrange(4):
            seg = cy.Segment(space.static_body,
                    cy.Vec2d(0, 0), cy.Vec2d(0, 0), 0)
            seg.elasticity = 0.6
            seg.friction = 0.7
            self.cbounds.append(seg)
            space.add_static(seg)

        # update bounds with good positions
        self.update_bounds()
        
    def clear(self, *args):
      for body, circle in self.blist:
        self.space.remove(body)
        self.space.remove(circle)
        radius, color, rect, pos, rot = self.cmap.pop(body)
        self.canvas.clear()
        for child in self.canvas.children:
          self.canvas.remove(child)
      self.cmap = {}
      self.blist = []

    def update_bounds(self, *largs):
        assert(len(self.cbounds) == 4)
        a, b, c, d = self.cbounds
        x0, y0 = self.pos
        x1 = self.right
        y1 = self.top

        self.space.remove_static(a)
        self.space.remove_static(b)
        self.space.remove_static(c)
        self.space.remove_static(d)
        a.a = (x0, y0)
        a.b = (x1, y0)
        b.a = (x1, y0)
        b.b = (x1, y1)
        c.a = (x1, y1)
        c.b = (x0, y1)
        d.a = (x0, y1)
        d.b = (x0, y0)
        self.space.add_static(a)
        self.space.add_static(b)
        self.space.add_static(c)
        self.space.add_static(d)

    def step(self, dt):
        self.space.step(1 / 60.)
        self.update_objects()

    def update_objects(self):
        for body, obj in self.cmap.iteritems():
            p = body.position
            radius, color, rect, pos, rot = obj
            rot.angle = body.angle
            pos.x = p.x - radius
            pos.y = p.y - radius

    def add_random_circle(self):
        self.add_circle(
            self.x + random() * self.width,
            self.y + random() * self.height,
            10 + self.circleRadius * random())

    def add_circle(self, x, y, radius):
        if len(self.blist) >= 500:
          return
        
        # create a falling circle
        body = cy.Body(100, 1e9)
        body.position = x, y
        body.angle = random() * 360.0
        body.angular_velocity = random() * 720.0 - 360.0
        body.apply_impulse((random() * 100000 - 50000, random() * 100000 - 50000),cXY)
        circle = cy.Circle(body, radius) 
        circle.elasticity = 0.6
        circle.friction = 0.7
        self.space.add(body, circle)
        # create object
        with self.canvas:
            PushMatrix()
            boxPos = Translate(self.x - radius, self.y - radius)
            boxRot = Rotate(angle=0, axis=(0,0,1), origin =(radius,radius))
            # add object
            self._hue = (self._hue + 0.01) % 1
            color = Color(self._hue, 1, 1, mode='hsv')
            rect = Rectangle(
                texture=self.texture,
                pos=(0,0),
                size=(radius * 2, radius * 2))
            # pop matrix
            PopMatrix()
        self.cmap[body] = (radius, color, rect, boxPos, boxRot)

        # remove the oldest one
        self.blist.append((body, circle))
        
    def on_touch_down(self, touch):
        self.add_circle(touch.x, touch.y, 10 + self.circleRadius * random())

    def on_touch_move(self, touch):
        self.add_circle(touch.x, touch.y, 10 + self.circleRadius * random())

class main:
  lastCount = 0
  physicWorld = Playground(size=WH)
  
  def start(self): 
    widget = Widget()
  
    # physic world
    widget.add_widget(self.physicWorld)
  
    # label
    self.label = Label(text = "", width="200dp", halign='left')
    widget.add_widget(self.label)  
    
    # button
    btn=Button(text="clear", width="90dp", pos_hint={"left":None})
    btn.x = W - btn.width
    btn.bind(on_release=self.physicWorld.clear)
    widget.add_widget(btn)
    
    # add to root
    gMyRoot.add_widget(widget)
    
  def update(self, dt):
    nCount = len(self.physicWorld.blist)
    if self.lastCount != nCount:
      self.lastCount = nCount
      self.label.text = 'circles: %d' % len(self.physicWorld.blist)

if __name__ == '__main__':
    gMyRoot.run( main() )
