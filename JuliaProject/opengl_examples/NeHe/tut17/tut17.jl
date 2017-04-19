# Mon 31 Dec 2012 01:40:11 PM EST
#
# NeHe Tut 17 - 2D texture font
#
# Q - quit
# L - turn lights on/off
# F - change texture filter (linear, nearest, mipmap)
# PageUp/Down - move camera closer/further away
# Up/Down - increase/decrease x-rotation speed
# Left/Right - increase/decrease y-rotation speed

# TODO: This example runs, but it produces a very glitchy output. 


# load necessary GLUT/OpenGL routines

using OpenGL
@OpenGL.version "1.0"
@OpenGL.load
using GLUT

### auxiliary functions

function glPrint(x::Integer, y::Integer, string::String, set::Integer)
    global base

    if set > 1
        set = 1
    end

    glBindTexture(GL_TEXTURE_2D, tex[1])
    glDisable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glpushmatrix()

    glLoadIdentity()
    glOrtho(0, 640, 0, 480, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glTranslate(x, y, 0)
    glListBase(uint32(base-32+(128*set)))
    glCallLists(strlen(string), GL_BYTE, string)

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()

    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
end

### end of auxiliary functions

# initialize variables

global window
global base

global tex       = Array(Uint32,2) # generating 2 textures

T0                 = 0
Frames             = 0

cnt1               = 0
cnt2               = 0

width            = 640
height           = 480

# load textures from images

function LoadGLTextures()
    global tex

    imgFont, wFont, hFont = glimread(expanduser("~/.julia/SDL/Examples/NeHe/tut17/font.bmp"))

    imgBumps, wBumps, hBumps = glimread(expanduser("~/.julia/SDL/Examples/NeHe/tut17/bumps.bmp"))

    glGenTextures(2,tex)
    glBindTexture(GL_TEXTURE_2D,tex[1])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, wFont, hFont, 0, GL_RGB, GL_UNSIGNED_BYTE, imgFont)

    glBindTexture(GL_TEXTURE_2D,tex[2])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, wBumps, hBumps, 0, GL_RGB, GL_UNSIGNED_BYTE, imgBumps)
end

# function to init OpenGL context

function initGL(w::Integer,h::Integer)
    global base

    glViewport(0,0,w,h)
    LoadGLTextures()
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)			 
    glDepthFunc(GL_LEQUAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # enable texture mapping & blending
    glEnable(GL_TEXTURE_2D)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)

    gluPerspective(45.0,w/h,0.1,100.0)

    glMatrixMode(GL_MODELVIEW)
    
    # build the fonts

    base = glGenLists(256)
    glBindTexture(GL_TEXTURE_2D, tex[1])

    for loop = 1:256
        cx = (loop%16)/16
        cy = (loop/16)/16

        glNewList(uint32(base+(loop-1)), GL_COMPILE)
            glBegin(GL_QUADS)
                glTexCoord(cx, 1-cy-0.0625)
                glVertex(0, 0)
                glTexCoord(cx+0.0625, 1-cy-0.0625)
                glVertex(16, 0)
                glTexCoord(cx+0.0625, 1-cy)
                glVertex(16, 16)
                glTexCoord(cx, 1-cy)
                glVertex(0, 16)
            glEnd()
            glTranslate(10, 0, 0)
        glEndList()
    end
end

# prepare Julia equivalents of C callbacks that are typically used in GLUT code

function ReSizeGLScene(w::Int32,h::Int32)
    if h == 0
        h = 1
    end

    glViewPort(0,0,w,h)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45.0,w/h,0.1,100.0)

    glMatrixMode(GL_MODELVIEW)
   
    return nothing
end

_ReSizeGLScene = cfunction(ReSizeGLScene, Void, (Int32, Int32))

function DrawGLScene()
    global tex
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    glBindTexture(GL_TEXTURE_2D,tex[2])

    glTranslate(0.0,0.0,-5.0)
    glRotate(45.0, 0.0, 0.0, 1.0)
    glRotate(cnt1*30.0, 1.0, 1.0, 0.0)

    glDisable(GL_BLEND)
    glColor(1.0, 1.0, 1.0)

    glBegin(GL_QUADS)
        glTexCoord(0.0, 0.0)
        glVertex(-1.0, 1.0)
        glTexCoord(1.0, 0.0)
        glVertex(1.0, 1.0)
        glTexCoord(1.0, 1.0)
        glVertex(1.0, -1.0)
        glTexCoord(0.0, 1.0)
        glVertex(-1.0, -1.0)
    glEnd()

    glRotate(90.0, 1.0, 1.0, 0.0)
    glBegin(GL_QUADS)
        glTexCoord(0.0, 0.0)
        glVertex(-1.0, 1.0)
        glTexCoord(1.0, 0.0)
        glVertex(1.0, 1.0)
        glTexCoord(1.0, 1.0)
        glVertex(1.0, -1.0)
        glTexCoord(0.0, 1.0)
        glVertex(-1.0, -1.0)
    glEnd()

    glEnable(GL_BLEND)
    glLoadIdentity()

    glColor(1.0cos(cnt1), 1.0sin(cnt2), 1.0-0.5cos(cnt1+cnt2))
    glPrint(int(280+250cos(cnt1)), int(235+200sin(cnt2)), "NeHe", 0)
    glColor(1.0sin(cnt2), 1.0-0.5cos(cnt1+cnt2), 1.0cos(cnt1))
    glPrint(int(280+230cos(cnt2)), int(235+200sin(cnt1)), "OpenGL", 1)

    glColor(0.0, 0.0, 1.0)
    glPrint(int(240+200cos((cnt2+cnt1)/5)), 2, "JuliaLang", 0)
    glColor(1.0, 1.0, 1.0)
    glPrint(int(242+200cos((cnt2+cnt1)/5)), 2, "JuliaLang", 0)

    cnt1 +=0.01
    cnt2 +=0.0081

    glutSwapBuffers()
   
    return nothing
end
   
_DrawGLScene = cfunction(DrawGLScene, Void, ())

function keyPressed(key::Char,x::Int32,y::Int32)
    global base

    if key == int('q')
        glDeleteLists(base,256)
        glDeleteTextures(2,tex)
        glutDestroyWindow(window)
    end

    return nothing # keyPressed returns "void" in C. this is a workaround for Julia's "automatically return the value of the last expression in a function" behavior.
end

_keyPressed = cfunction(keyPressed, Void, (Char, Int32, Int32))

# run GLUT routines

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)

window = glutCreateWindow("NeHe Tut 17")

glutDisplayFunc(_DrawGLScene)
glutFullScreen()

glutIdleFunc(_DrawGLScene)
glutReshapeFunc(_ReSizeGLScene)
glutKeyboardFunc(_keyPressed)

initGL(width, height)

glutMainLoop()
