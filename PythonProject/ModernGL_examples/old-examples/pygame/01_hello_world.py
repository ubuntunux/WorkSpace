import struct

import ModernGL
import pygame
from pygame.locals import DOUBLEBUF, OPENGL

pygame.init()
pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)

ctx = ModernGL.create_context()

vert = ctx.vertex_shader('''
    #version 330
    in vec2 vert;
    void main() {
        gl_Position = vec4(vert, 0.0, 1.0);
    }
''')

frag = ctx.fragment_shader('''
    #version 330
    out vec4 color;
    void main() {
        color = vec4(0.30, 0.50, 1.00, 1.0);
    }
''')

prog = ctx.program([vert, frag])

vbo = ctx.buffer(struct.pack('6f', 0.0, 0.8, -0.6, -0.8, 0.6, -0.8))
vao = ctx.simple_vertex_array(prog, vbo, ['vert'])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ctx.clear(0.9, 0.9, 0.9)
    vao.render()

    pygame.display.flip()
    pygame.time.wait(10)
