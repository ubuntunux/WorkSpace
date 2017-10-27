import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


def genComputeProg(texHandle):
    progHandle = glCreateProgram()
    cs = glCreateShader(GL_COMPUTE_SHADER)

    csSrc = """
    #version 430
    "uniform float roll;
     uniform image2D destTex;
     layout (local_size_x = 16, local_size_y = 16) in;
     void main() {
         ivec2 storePos = ivec2(gl_GlobalInvocationID.xy);
         float localCoef = length(vec2(ivec2(gl_LocalInvocationID.xy)-8)/8.0);
         float globalCoef = sin(float(gl_WorkGroupID.x+gl_WorkGroupID.y)*0.1 + roll)*0.5;
         imageStore(destTex, storePos, vec4(1.0-globalCoef*localCoef, 0.0, 0.0, 0.0));
     }
     """

    glShaderSource(cs, 2, csSrc, None)
    glCompileShader(cs)
    rvalue = glGetShaderiv(cs, GL_COMPILE_STATUS)
    if not rvalue:
        print("Error in compiling the compute shader")
        
    glAttachShader(progHandle, cs)
    
    glLinkProgram(progHandle)
    rvalue = glGetProgramiv(progHandle, GL_LINK_STATUS)
    
    if not rvalue:
        print("Error in linking compute shader program\n")
        
    glUseProgram(progHandle)    
    glUniform1i(glGetUniformLocation(progHandle, "destTex"), 0)
    return progHandle

    
def updateTex(frame):
    glUseProgram(computeHandle)
    glUniform1f(glGetUniformLocation(computeHandle, "roll"), float(frame) * 0.01)
    # 512^2 threads in blocks of 16^2
    glDispatchCompute(512/16, 512/16, 1)

    
def draw():
    glUseProgram(renderHandle);
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)


def main():
    pygame.init()
    pygame.display.set_mode((640,480), OPENGL | DOUBLEBUF)
    glEnable(GL_DEPTH_TEST)        #use our zbuffer

    #setup the camera
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0,640/480.0,0.1,100.0)    #setup lens
    glTranslatef(0.0, 0.0, -3.0)                #move back
    glRotatef(25, 1, 0, 0)                       #orbit higher
    
    #clear screen and move camera
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
    texHandle = glGenTextures(1)
    renderHandle = genRenderProg(texHandle)
    computeHandle = genComputeProg(texHandle)

    for i in range(1024):
        updateTex(i)
        draw()
        pygame.display.flip()
        pygame.time.wait(10)

main()