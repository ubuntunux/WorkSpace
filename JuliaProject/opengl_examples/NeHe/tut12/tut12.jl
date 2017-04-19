# Mon 31 Dec 2012 01:39:13 PM EST
#
# NeHe Tut 12 - Rotate a textured cube
#
# Q - quit
# Up/Down - increase/decrease rotation of each cube about it's own x-axis
# Left/Right - increase/decrease rotation of each cube about it's own y-axis


# load necessary GLUT/OpenGL routines

using OpenGL
@OpenGL.version "1.0"
@OpenGL.load
using GLUT

# initialize variables

global window

global xrot = 0
global yrot = 0

global box  = 0
global top  = 0

boxcol      = [1.0 0.0 0.0;
               1.0 0.5 0.0;
               1.0 1.0 0.0;
               0.0 1.0 0.0;
               0.0 1.0 1.0]

topcol      = [0.5 0.0  0.0;
               0.5 0.25 0.0;
               0.5 0.5  0.0;
               0.0 0.5  0.0;
               0.0 0.5  0.5]

global tex  = Array(Uint32,1) # generating 1 texture

width       = 640
height      = 480

# load textures from images

function LoadGLTextures()
    global tex

    img, w, h = glimread(expanduser("~/.julia/GLUT/Examples/NeHe/tut12/cube.bmp"))

    glGenTextures(1,tex)
    glBindTexture(GL_TEXTURE_2D,tex[1])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR_MIPMAP_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, img)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 3, w, h, GL_RGB, GL_UNSIGNED_BYTE, img)
end

# function to init OpenGL context

function initGL(w::Integer,h::Integer)
    global box
    global top

    glViewport(0,0,w,h)
    LoadGLTextures()
    glClearColor(0.0, 0.0, 0.0, 0.5)
    glClearDepth(1.0)			 
    glDepthFunc(GL_LEQUAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    # enable texture mapping
    glEnable(GL_TEXTURE_2D)

    #enable simple lighting
    glEnable(GL_LIGHT0)         
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45.0,w/h,0.1,100.0)

    glMatrixMode(GL_MODELVIEW)

    # build the display lists

    box = glGenLists(2)

    glNewList(box, GL_COMPILE)
        glBegin(GL_QUADS)
            # Bottom Face
            glTexCoord(0.0, 1.0)
            glVertex(-1.0, -1.0, -1.0)
            glTexCoord(1.0, 1.0)
            glVertex(1.0, -1.0, -1.0)
            glTexCoord(1.0, 0.0)
            glVertex(1.0, -1.0,  1.0)
            glTexCoord(0.0, 0.0)
            glVertex(-1.0, -1.0,  1.0)

            # Front Face
            glTexCoord(1.0, 0.0)
            glVertex(-1.0, -1.0,  1.0)
            glTexCoord(0.0, 0.0)
            glVertex(1.0, -1.0,  1.0)
            glTexCoord(0.0, 1.0)
            glVertex(1.0,  1.0,  1.0)
            glTexCoord(1.0, 1.0)
            glVertex(-1.0,  1.0,  1.0)

            # Back Face
            glTexCoord(0.0, 0.0)
            glVertex(-1.0, -1.0, -1.0)
            glTexCoord(0.0, 1.0)
            glVertex(-1.0,  1.0, -1.0)
            glTexCoord(1.0, 1.0)
            glVertex(1.0,  1.0, -1.0)
            glTexCoord(1.0, 0.0)
            glVertex(1.0, -1.0, -1.0)

            # Right Face
            glTexCoord(0.0, 0.0)
            glVertex(1.0, -1.0, -1.0)
            glTexCoord(0.0, 1.0)
            glVertex(1.0,  1.0, -1.0)
            glTexCoord(1.0, 1.0)
            glVertex(1.0,  1.0,  1.0)
            glTexCoord(1.0, 0.0)
            glVertex(1.0, -1.0,  1.0)

            # Left Face
            glTexCoord(1.0, 0.0)
            glVertex(-1.0, -1.0, -1.0)
            glTexCoord(0.0, 0.0)
            glVertex(-1.0, -1.0,  1.0)
            glTexCoord(0.0, 1.0)
            glVertex(-1.0,  1.0,  1.0)
            glTexCoord(1.0, 1.0)
            glVertex(-1.0,  1.0, -1.0)
        glEnd()
    glEndList()

    top = uint32(box+1)

    glNewList(top, GL_COMPILE)
        glBegin(GL_QUADS)
            # Top Face
            glTexCoord(1.0, 1.0)
            glVertex(-1.0, 1.0, -1.0)
            glTexCoord(1.0, 0.0)
            glVertex(-1.0, 1.0,  1.0)
            glTexCoord(0.0, 0.0)
            glVertex(1.0, 1.0,  1.0)
            glTexCoord(0.0, 1.0)
            glVertex(1.0, 1.0, -1.0)
        glEnd()
    glEndList()
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
    global tex
    global xrot
    global yrot
    global box
    global top

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glBindTexture(GL_TEXTURE_2D, tex[1])

    for yloop = 1:5
	      for xloop = 1:yloop
            glLoadIdentity()

            glTranslate(1.4+2.8xloop-1.4yloop, ((6.0-yloop)*2.4)-7.0, -20.0)

            glRotate(45.0-(2.0yloop)+xrot, 1.0, 0.0, 0.0)
            glRotate(45.0+yrot, 0.0, 1.0, 0.0)

            glColor(boxcol[yloop,:])
            glCallList(box)
            
            glColor(topcol[yloop,:])
            glCallList(top)
        end
    end

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

function specialKeyPressed(the_key::Int32,x::Int32,y::Int32)
    global xrot
    global yrot

    if the_key == GLUT_KEY_UP
        xrot -=0.2
    elseif the_key == GLUT_KEY_DOWN
        xrot +=0.2
    elseif the_key == GLUT_KEY_LEFT
        yrot -=0.2
    elseif the_key == GLUT_KEY_RIGHT
        yrot +=0.2
    end

    return nothing # specialKeyPressed returns "void" in C-GLUT. this is a workaround for Julia's "automatically return the value of the last expression in a function" behavior.
end

_specialKeyPressed = cfunction(specialKeyPressed, Void, (Int32, Int32, Int32))

# run GLUT routines

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)

window = glutCreateWindow("NeHe Tut 12")

glutDisplayFunc(_DrawGLScene)
glutFullScreen()

glutIdleFunc(_DrawGLScene)
glutReshapeFunc(_ReSizeGLScene)
glutKeyboardFunc(_keyPressed)
glutSpecialFunc(_specialKeyPressed)

initGL(width, height)

glutMainLoop()
