import os
from ctypes import c_void_p

import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *

from PIL import Image

import pygame
from pygame.locals import *


SIMPLE_VERTEX_SHADER = '''
#version 430 core

struct VERTEX_INPUT
{
    layout(location=0) vec3 position;
    layout(location=1) vec2 tex_coord;
};

struct VERTEX_OUTPUT
{
    vec2 tex_coord;
    vec3 position;
};

in VERTEX_INPUT vs_input;
out VERTEX_OUTPUT vs_output;

void main() {
    vs_output.tex_coord = vs_input.tex_coord;
    vs_output.position = vs_input.position;
    gl_Position = vec4(vs_input.position, 1.0);
}'''

SIMPLE_PIXEL_SHADER = '''
#version 430 core

uniform sampler2D texture_check;

struct VERTEX_OUTPUT
{
    vec2 tex_coord;
    vec3 position;
};

in VERTEX_OUTPUT vs_output;
out vec4 fs_output;

void main(void)
{
    vec2 tex_coord = vs_output.tex_coord.xy * 5.0;
    fs_output = texture(texture_check, tex_coord);
}
'''


def Run():
    screen_width, screen_height = 512, 512
    pygame.init()
    pygame.display.set_mode((screen_width, screen_height), OPENGL | DOUBLEBUF | RESIZABLE | HWPALETTE | HWSURFACE)

    # GL setting    
    glFrontFace(GL_CCW)
    glEnable(GL_TEXTURE_2D)
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)
    glDisable(GL_LIGHTING)
    glDisable(GL_BLEND)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Create Shader
    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader, SIMPLE_VERTEX_SHADER)
    glCompileShader(vertex_shader)

    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader, SIMPLE_PIXEL_SHADER)
    glCompileShader(fragment_shader)

    # Create Program
    program = glCreateProgram()

    # Link Shaders
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)

    # delete shader
    glDetachShader(program, vertex_shader)
    glDetachShader(program, fragment_shader)
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    # Vertex Array Data
    dtype = np.float32
    positions = np.array([(-1, 1, 0), (-1, -1, 0), (1, -1, 0), (1, 1, 0)], dtype=np.float32)
    texcoords = np.array([(0, 1), (0, 0), (1, 0), (1, 1)], dtype=np.float32)
    indices = np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32)

    # data serialize
    vertex_datas = np.hstack([positions, texcoords]).astype(dtype)

    # crate vertex array
    vertex_array = glGenVertexArrays(1)
    glBindVertexArray(vertex_array)

    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glBufferData(GL_ARRAY_BUFFER, vertex_datas, GL_STATIC_DRAW)

    index_buffer_size = indices.nbytes
    index_buffer = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, index_buffer)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_buffer_size, indices, GL_STATIC_DRAW)

    # Create Texture
    image = Image.open(os.path.join('resources', 'check.png'))
    image_data = image.tobytes("raw", image.mode, 0, -1)
    texture_format = GL_RGBA
    if image.mode == 'RGB':
        texture_format = GL_RGB

    texture_buffer = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_buffer)
    glTexImage2D(GL_TEXTURE_2D, 0, texture_format, image.size[0], image.size[1], 0, texture_format, GL_UNSIGNED_BYTE, image_data)
    glGenerateMipmap(GL_TEXTURE_2D)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glBindTexture(GL_TEXTURE_2D, 0)

    # Create RenderTarget
    render_target_buffer = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, render_target_buffer)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, screen_width, screen_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, ctypes.c_void_p(0))
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glBindTexture(GL_TEXTURE_2D, 0)

    # Create FrameBuffer
    frame_buffer = glGenFramebuffers(1)

    gl_error = glCheckFramebufferStatus(GL_FRAMEBUFFER)
    if gl_error != GL_FRAMEBUFFER_COMPLETE:
        logger.error("glCheckFramebufferStatus error %d." % gl_error)

    while True:
        done = False
        for event in pygame.event.get():
            eventType = event.type
            if eventType == KEYDOWN:
                keyDown = event.key
                if keyDown == K_ESCAPE:
                    done = True
        if done:
            break

        # Bind Frame Buffer
        glBindFramebuffer(GL_FRAMEBUFFER, frame_buffer)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, render_target_buffer, 0)
        glReadBuffer(GL_COLOR_ATTACHMENT0)
        glDrawBuffers(1, [GL_COLOR_ATTACHMENT0, ])
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_TEXTURE_2D, 0, 0)

        glViewport(0, 0, screen_width, screen_height)
        glClearColor(1.0, 1.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # bind program
        glUseProgram(program)

        # bind texture
        texture_location = glGetUniformLocation(program, "texture_font")
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture_buffer)
        glUniform1i(texture_location, 0)

        # Bind Vertex Array
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)

        vertex_position_size = positions[0].nbytes
        vertex_texcoord_size = texcoords[0].nbytes
        vertex_buffer_size = vertex_position_size + vertex_texcoord_size

        location = 0
        offset = 0
        stride = len(positions[0])
        glEnableVertexAttribArray(location)
        glVertexAttribPointer(location, stride, GL_FLOAT, GL_FALSE, vertex_buffer_size, c_void_p(offset))

        location = 1
        offset += vertex_position_size
        stride = len(positions[0])
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(location, stride, GL_FLOAT, GL_FALSE, vertex_buffer_size, c_void_p(offset))


        # bind index buffer
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, index_buffer)

        # Draw Quad
        glDrawElements(GL_TRIANGLES, index_buffer_size, GL_UNSIGNED_INT, ctypes.c_void_p(0))

        # blit frame buffer
        glBindFramebuffer(GL_DRAW_FRAMEBUFFER, 0)  # the default framebuffer active
        glBlitFramebuffer(0, 0, screen_width, screen_height, 0, 0, screen_width, screen_height, GL_COLOR_BUFFER_BIT, GL_LINEAR)

        pygame.display.flip()


if __name__ == '__main__':
    Run()
