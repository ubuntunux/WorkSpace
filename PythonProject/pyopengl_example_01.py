from OpenGL.GL import *
from OpenGL.GL.shaders import *
from sdl2 import *
import numpy
import math
import mathutils
import ctypes
import sys

vs = """
#version 330 core

layout(location=0) in vec3 position;
layout(location=1) in vec3 normal;
layout(location=2) in vec2 uv;
layout(location=3) in vec3 color;

layout(std140) uniform pvMatrix
{
  mat4 pMatrix;
  mat4 vMatrix;
};

uniform mat4 mMatrix0;
uniform mat4 mMatrix1;
uniform float offset[5];

out vec3 vColor;
out vec2 vUv;

void main(void)
{
  vColor = color * max(dot(vec3(1.0), (vMatrix * mMatrix0 * vec4(normal, 0.0)).xyz), 0.4);
  vUv  = uv;
  vec4 pos = mMatrix0 * vec4(position, 1.0);
  pos.y += offset[gl_InstanceID] * 5.0 - 10.0;
  pos = mMatrix1 * pos;
  gl_Position = pMatrix * vMatrix * pos;
}
"""

fs = """
#version 330 core

in vec3 vColor;
in vec2 vUv;
out vec4 fragColor;

void main(void) 
{
  fragColor = vec4(vColor * vec3(vUv, 0.5), 1.0);
}
"""

def perspective(fovy, aspect, near, far):
  top = near * math.tan(math.radians(fovy) / 2)
  right = top * aspect
  u = right * 2
  v = top * 2
  w = far - near
  return numpy.array((
    near * 2 / u, 0, 0, 0, 0,                  
    near * 2 / v, 0, 0, 0, 0,             
    -(far + near) / w, -1, 0, 0,
    -(far * near * 2) / w, 0)
    ).astype(numpy.float32)

def lookAt(eye, center, up):
  eye = mathutils.Vector(eye)
  center = mathutils.Vector(center)
  up = mathutils.Vector(up)
  z = (eye- center).normalized()
  x = up.cross(z).normalized()
  y = z.cross(x).normalized()
  return numpy.array((
    x[0], y[0], z[0], 0,
    x[1], y[1], z[1], 0,
    x[2], y[2], z[2], 0,
    -x.dot(eye), -y.dot(eye), -z.dot(eye), 1)
    ).astype(numpy.float32)
    
class FPS:
  def __init__(self, fps = 60): 
    self.interval = 1000 // fps 
    self.time = SDL_GetTicks()
  def delay(self):
    d = self.time - SDL_GetTicks()
    if d > 0:
      SDL_Delay(d)
      ret = True
    else :
      ret = False
    self.time += self.interval
    return ret

def glInit():
  global program
  program = compileProgram(
    compileShader(vs, GL_VERTEX_SHADER),
    compileShader(fs, GL_FRAGMENT_SHADER))
  glUseProgram(program)
  
  position = [
    -1, -1, -1, -1, -1,  1,  1, -1,  1,  1, -1, -1,
    -1,  1, -1, -1,  1,  1,  1,  1,  1,  1,  1, -1,
    -1, -1, -1, -1,  1, -1,  1,  1, -1,  1, -1, -1,
    -1, -1,  1, -1,  1,  1,  1,  1,  1,  1, -1,  1,
    -1, -1, -1, -1, -1,  1, -1,  1,  1, -1,  1, -1,
     1, -1, -1,  1, -1,  1,  1,  1,  1,  1,  1, -1 ]          

  normal = [
     0, -1,  0,  0, -1,  0,  0, -1,  0,  0, -1,  0,
     0,  1,  0,  0,  1,  0,  0,  1,  0,  0,  1,  0,
     0,  0, -1,  0,  0, -1,  0,  0, -1,  0,  0, -1,
     0,  0,  1,  0,  0,  1,  0,  0,  1,  0,  0,  1,
    -1,  0,  0, -1,  0,  0, -1,  0,  0, -1,  0,  0,
     1,  0,  0,  1,  0,  0,  1,  0,  0,  1,  0,  0 ]

  uv = [
      0, 0, 1, 0, 1, 1, 0, 1,
      0, 0, 1, 0, 1, 1, 0, 1,
      0, 0, 1, 0, 1, 1, 0, 1,
      0, 0, 1, 0, 1, 1, 0, 1,
      0, 0, 1, 0, 1, 1, 0, 1,
      0, 0, 1, 0, 1, 1, 0, 1 ]

  color = numpy.ones(72)

  indices = [
     0,  2,  1,  0,  3,  2,
     4,  5,  6,  4,  6,  7,
     8,  9, 10,  8, 10, 11,
    12, 15, 14, 12, 14, 13,
    16, 17, 18, 16, 18, 19,
    20, 23, 22, 20, 22, 21 ]

  position = numpy.array(position).reshape((len(position)//3, 3))
  normal = numpy.array(normal).reshape((len(normal)//3, 3))
  uv = numpy.array(uv).reshape((len(uv)//2, 2))
  color = numpy.array(color).reshape((len(color)//3, 3))
  vertices = numpy.hstack((position, normal, uv, color)).astype(numpy.float32)
  indices = numpy.array(indices).astype(numpy.ushort)
  global indexCount
  indexCount = len(indices)

  # VAO
  glBindVertexArray(glGenVertexArrays(1))
  glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
  glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)
  glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, glGenBuffers(1))
  glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

  byteSize = numpy.nbytes[numpy.float32]
  strides = [3, 3, 2, 3]
  unitSize = sum(strides) * byteSize
  glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, unitSize, None)
  glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, unitSize, ctypes.c_void_p(sum(strides[:1]) * byteSize))
  glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, unitSize, ctypes.c_void_p(sum(strides[:2]) * byteSize))
  glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, unitSize, ctypes.c_void_p(sum(strides[:3]) * byteSize))
  glEnableVertexAttribArray(0)
  glEnableVertexAttribArray(1)
  glEnableVertexAttribArray(2)
  glEnableVertexAttribArray(3)

  # Uniform Array
  global instanceCount
  instanceCount = 5
  data = numpy.array(range(instanceCount)).astype(numpy.float32)
  glUniform1fv(glGetUniformLocation(program, "offset"), instanceCount, data)

  # Uniform Block
  bindingPoint = 1
  glUniformBlockBinding(program, glGetUniformBlockIndex(program, 'pvMatrix' ), bindingPoint)
  
  buffer = glGenBuffers(1)
  glBindBuffer(GL_UNIFORM_BUFFER, buffer)
  data = numpy.hstack((
    perspective(45, w / h, 0.1, 100),
    lookAt((0, 0, 30), (0, 0, 0), (0, 1, 0))
  ))
  print(data)
  glBufferData(GL_UNIFORM_BUFFER, data.nbytes, data, GL_DYNAMIC_DRAW)
  glBindBufferBase(GL_UNIFORM_BUFFER, bindingPoint, buffer)

  glClearDepth(1)
  glClearColor(0, 0, 0, 1)
  glEnable(GL_CULL_FACE)
  glCullFace(GL_BACK)
  glEnable(GL_DEPTH_TEST)
  glDepthFunc(GL_LEQUAL)

def glUpdate(time):
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  data = mathutils.Matrix.Rotation(-time * 0.5, 4, 'X') * mathutils.Matrix.Rotation(time * 1.5, 4, 'Y')
  data = numpy.array(data).astype(numpy.float32)
  glUniformMatrix4fv(glGetUniformLocation(program, 'mMatrix0'), 1, GL_FALSE, data)
  data = mathutils.Matrix.Rotation(time * 0.5, 4, 'Z') * mathutils.Matrix.Rotation(time * 0.5, 4, 'Y')
  data = numpy.array(data).astype(numpy.float32)
  glUniformMatrix4fv(glGetUniformLocation(program, 'mMatrix1'), 1, GL_FALSE, data)
  glDrawElementsInstanced(GL_TRIANGLES, indexCount, GL_UNSIGNED_SHORT, None, instanceCount)
      
def main():
  global w, h
  w, h = 350, 250
  SDL_Init(SDL_INIT_VIDEO)
  SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 1)
  window = SDL_CreateWindow(b"pySDL2 DE OpenGL",
                            SDL_WINDOWPOS_UNDEFINED,
                            SDL_WINDOWPOS_UNDEFINED, w, h,
                            SDL_WINDOW_OPENGL)
  SDL_GL_CreateContext(window)

  glInit()

  """
  # make gif file
  import os
  tmpDir = "tmp/"
  if not os.path.exists(tmpDir): os.mkdir(tmpDir)
  second = 6
  fps = 10
  for i in range(second * fps):
    time = i / fps
    glUpdate(time)
    pixels = glReadPixels(0, 0, w, h, GL_RGBA, GL_UNSIGNED_BYTE)
    surface = SDL_CreateRGBSurfaceFrom(pixels, w, h, 32, w * 4, 0, 0, 0, 0)
    SDL_SaveBMP(surface, ("{0}img{1}.bmp".format(tmpDir, "%03d"%(i + 1))).encode(sys.stdout.encoding))
    SDL_FreeSurface(surface)
  os.system("convert -delay {0} -loop 0 {1}img*.bmp movie.gif".format(100 / fps, tmpDir))
  #for f in os.listdir(tmpDir): os.remove(tmpDir + f)
  """
  
  event = SDL_Event()
  fps = FPS()
  while True:
    if fps.delay():
      time = SDL_GetTicks() / 1000
      glUpdate(time)
      SDL_GL_SwapWindow(window)
    while SDL_PollEvent(ctypes.byref(event)) != 0:
      if event.type == SDL_QUIT: sys.exit()
      if event.type == SDL_KEYDOWN and event.key.keysym.sym == SDLK_ESCAPE: sys.exit()

if __name__ == '__main__':
  main()
