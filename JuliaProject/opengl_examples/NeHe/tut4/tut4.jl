# Tue 23 Oct 2012 07:10:59 PM EDT
#
# NeHe Tut 4 - Rotate colored (rainbow) triangle and colored (cyan) square
#
# Q - quit


# load necessary GLUT/OpenGL routines

using OpenGL
@OpenGL.version "1.0"
@OpenGL.load
using GLUT

# initialize variables

global window

global rtri  = 0.0
global rquad = 0.0

width        = 640
height       = 480

# function to init OpenGL context

function initGL(w::Integer,h::Integer)
    glViewport(0,0,w,h)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)			 
    glDepthFunc(GL_LESS)	 
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45.0,w/h,0.1,100.0)

    glMatrixMode(GL_MODELVIEW)
end

# prepare Julia equivalents of C callbacks that are typically used in GLUT code

function ReSizeGLScene(w::Int32,h::Int32)
    if h == 0
        h = 1
    end

    glViewport(0,0,w,h)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45.0,w/h,0.1,100.0)

    glMatrixMode(GL_MODELVIEW)
   
    return nothing
end

_ReSizeGLScene = cfunction(ReSizeGLScene, Void, (Int32, Int32))

function DrawGLScene()
    global rtri
    global rquad

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslate(-1.5,0.0,-6.0)
    glRotate(rtri,0.0,1.0,0.0)

    glBegin(GL_POLYGON)
      glColor(1.0,0,0)
      glVertex(0.0,1.0,0.0)
      glColor(0,1.0,0)
      glVertex(1.0,-1.0,0.0)
      glColor(0,0,1.0)
      glVertex(-1.0,-1.0,0.0)
    glEnd()

    glLoadIdentity()

    glTranslate(1.5,0.0,-6.0)
    glRotate(rquad,1.0,0.0,0.0)

    glTranslate(0.8,0,0)

    glColor(0.5,0.5,1.0)
    glBegin(GL_QUADS)
        glVertex(-1.0,1.0,0.0)
        glVertex(1.0,1.0,0.0)
        glVertex(1.0,-1.0,0.0)
        glVertex(-1.0,-1.0,0.0)
    glEnd()

    rtri  +=0.2
    rquad -=0.2

    glutSwapBuffers()
   
    return nothing
end
   
_DrawGLScene = cfunction(DrawGLScene, Void, ())

function keyPressed(the_key::Char,x::Int32,y::Int32)
    if the_key == int('q')
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

window = glutCreateWindow("NeHe Tut 4")

glutDisplayFunc(_DrawGLScene)
glutFullScreen()

glutIdleFunc(_DrawGLScene)
glutReshapeFunc(_ReSizeGLScene)
glutKeyboardFunc(_keyPressed)

initGL(width, height)

glutMainLoop()
