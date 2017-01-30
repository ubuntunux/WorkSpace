"""
The MIT License (MIT)

Copyright (c) 2014 Niko Skrypnik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""


from kivy.app import App
from kivy3 import Scene, Renderer, PerspectiveCamera
from kivy3.loaders import OBJLoader
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy3 import Mesh, Material, Object3D
from kivy3.extras.geometries import BoxGeometry
from kivy.uix.button import Button
from random import uniform

class MainApp(App):

    def build(self):
        root = FloatLayout()
        self.renderer = Renderer(shader_file="simple.glsl")
        scene = Scene()
        # load obj file
        loader = OBJLoader()
        obj = loader.load("monkey.obj")
        self.monkey = []
        for i in range(40):
          inst = Mesh(obj.children[0].geometry, obj.children[0].material)
          inst.pos.x = uniform(-3.0, 3.0)
          inst.pos.y = uniform(-3.0, 3.0)
          inst.pos.z = uniform(-10.0, -25.0)
          inst.speed = uniform(0.5, 3.0)
          scene.add(inst)
          self.monkey.append(inst)
        
        # add cube
        geometry = BoxGeometry(1, 1, 1)
        material = Material(color=(0., 1., 0.), diffuse=(0., 1., 0.),
                            specular=(.35, .35, .35))
        self.cube = Mesh(geometry, material)
        self.cube.pos.z = -10
        scene.add(self.cube)
        
        # setup renderer
        camera = PerspectiveCamera(75, 0.3, 1, 1000)
        self.renderer.render(scene, camera)
        root.add_widget(self.renderer)
        self.fps = Label(text="")
        root.add_widget(self.fps)
        Clock.schedule_interval(self._update_obj, 1. / 60)
        Clock.schedule_interval(self._rotate_cube, 1 / 60)
        self.renderer.bind(size=self._adjust_aspect)
        return root

    def _update_obj(self, dt):
        if dt > 0.0:
          self.fps.text = str(1.0/dt)
        for obj in self.monkey:
          obj.rotation.x += obj.speed
          obj.rotation.y += obj.speed
          obj.rotation.z += obj.speed

    def _adjust_aspect(self, inst, val):
        rsize = self.renderer.size
        aspect = rsize[0] / float(rsize[1])
        self.renderer.camera.aspect = aspect
    def _rotate_cube(self, dt):
        self.cube.rotation.x += 1
        self.cube.rotation.y += 1
        self.cube.rotation.z += 1

if __name__ == '__main__':
    MainApp().run()
