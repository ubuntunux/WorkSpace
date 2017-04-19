# Thu 08 Nov 2012 05:07:44 PM EST
#
# NeHe Tut 7 - Implement lights and rotate a textured cube
#
# Q - quit
# L - turn lights on/off
# F - change texture filter (linear, nearest, mipmap)
# PageUp/Down - move camera closer/further away from cube
# Left/Right - increase/decrease y-rotation speed
# Up/Down - increase/decrease x-rotation speed


# load necessary GLUT/OpenGL routines

using OpenGL
@OpenGL.version "1.0"
@OpenGL.load
using GLUT

### auxiliary functions

function cube(size)  # the cube function now includes surface normal specification for proper lighting
  glBegin(GL_QUADS)
    # Front Face
    glNormal(0.0,0.0,1.0)
    glTexCoord(0.0, 0.0)
    glVertex(-size, -size, size)
    glTexCoord(1.0, 0.0)
    glVertex(size, -size, size)
    glTexCoord(1.0, 1.0)
    glVertex(size, size, size)
    glTexCoord(0.0, 1.0)
    glVertex(-size, size, size)

    # Back Face
    glNormal(0.0,0.0,-1.0)
    glTexCoord(1.0, 0.0)
    glVertex(-size, -size, -size)
    glTexCoord(1.0, 1.0)
    glVertex(-size, size, -size)
    glTexCoord(0.0, 1.0)
    glVertex(size, size, -size)
    glTexCoord(0.0, 0.0)
    glVertex(size, -size, -size)

    # Top Face
    glNormal(0.0,1.0,0.0)
    glTexCoord(0.0, 1.0)
    glVertex(-size, size, -size)
    glTexCoord(0.0, 0.0)
    glVertex(-size, size, size)
    glTexCoord(1.0, 0.0)
    glVertex(size, size, size)
    glTexCoord(1.0, 1.0)
    glVertex(size, size, -size)

    # Bottom Face
    glNormal(0.0,-1.0,0.0)
    glTexCoord(1.0, 1.0)
    glVertex(-size, -size, -size)
    glTexCoord(0.0, 1.0)
    glVertex(size, -size, -size)
    glTexCoord(0.0, 0.0)
    glVertex(size, -size, size)
    glTexCoord(1.0, 0.0)
    glVertex(-size, -size, size)

    # Right Face
    glNormal(1.0,0.0,0.0)
    glTexCoord(1.0, 0.0)
    glVertex(size, -size, -size)
    glTexCoord(1.0, 1.0)
    glVertex(size, size, -size)
    glTexCoord(0.0, 1.0)
    glVertex(size, size, size)
    glTexCoord(0.0, 0.0)
    glVertex(size, -size, size)

    # Left Face
    glNormal(-1.0,0.0,0.0)
    glTexCoord(0.0, 0.0)
    glVertex(-size, -size, -size)
    glTexCoord(1.0, 0.0)
    glVertex(-size, -size, size)
    glTexCoord(1.0, 1.0)
    glVertex(-size, size, size)
    glTexCoord(0.0, 1.0)
    glVertex(-size, size, -size)
  glEnd()
end

### end of auxiliary functions

# initialize variables

global window

global filter        = 3
global light         = true

global xrot          = 0.0
global yrot          = 0.0
global xspeed        = 0.0
global yspeed        = 0.0

global tex           = Array(Uint32,3) # generating 3 textures

global cube_size     = 1.0

global z             = -5.0

width                = 640
height               = 480

global LightAmbient  = [0.5f0, 0.5f0, 0.5f0, 1.0f0]
global LightDiffuse  = [1.0f0, 1.0f0, 1.0f0, 1.0f0]
global LightPosition = [0.0f0, 0.0f0, 2.0f0, 1.0f0]

# load textures from images

function LoadGLTextures()
    global tex

    img, w, h = glimread(expanduser("~/.julia/GLUT/Examples/NeHe/tut7/crate.bmp"))

    glGenTextures(3,tex)
    glBindTexture(GL_TEXTURE_2D,tex[1])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, img)

    glBindTexture(GL_TEXTURE_2D,tex[2])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, img)

    glBindTexture(GL_TEXTURE_2D,tex[3])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, img)

    gluBuild2DMipmaps(GL_TEXTURE_2D, 3, w, h, GL_RGB, GL_UNSIGNED_BYTE, img)
end

# function to init OpenGL context

function initGL(w::Integer,h::Integer)
    global LightAmbient 
    global LightDiffuse 
    global LightPosition

    glViewport(0,0,w,h)
    LoadGLTextures()

    # enable texture mapping
    glEnable(GL_TEXTURE_2D)

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)			 
    glDepthFunc(GL_LESS)	 
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45.0,w/h,0.1,100.0)

    glMatrixMode(GL_MODELVIEW)
    
    # initialize lights
    glLightfv(GL_LIGHT1, GL_AMBIENT, LightAmbient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, LightDiffuse)
    glLightfv(GL_LIGHT1, GL_POSITION, LightPosition)

    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHTING)
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
    global xrot
    global yrot
    global tex
    global cube_size
    global xspeed
    global yspeed
    global filter

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslate(0.0,0.0,z)

    glRotate(xrot,1.0,0.0,0.0)
    glRotate(yrot,0.0,1.0,0.0)

    glBindTexture(GL_TEXTURE_2D,tex[filter])
    cube(cube_size)

    xrot +=xspeed
    yrot +=yspeed

    glutSwapBuffers()
   
    return nothing
end
   
_DrawGLScene = cfunction(DrawGLScene, Void, ())

function keyPressed(the_key::Char,x::Int32,y::Int32)
    global filter
    global light

    if the_key == int('q')
        glutDestroyWindow(window)
    elseif the_key == int('l')
        println("Light was: $light")
        light = (light ? false : true)
        println("Light is now: $light")
        if light
            glEnable(GL_LIGHTING)
        else
            glDisable(GL_LIGHTING)
        end
    elseif the_key == int('f')
        println("Filter was: $filter")
        filter += 1
        if filter > 3
            filter = 1
        end
        println("Filter is now: $filter")
    end

    return nothing # keyPressed returns "void" in C. this is a workaround for Julia's "automatically return the value of the last expression in a function" behavior.
end

_keyPressed = cfunction(keyPressed, Void, (Char, Int32, Int32))

function specialKeyPressed(the_key::Int32,x::Int32,y::Int32)
    global z
    global xspeed
    global yspeed

    if the_key == GLUT_KEY_PAGE_UP
        z -= 0.02
    elseif the_key == GLUT_KEY_PAGE_DOWN
        z += 0.02
    elseif the_key == GLUT_KEY_UP
        xspeed -= 0.01
    elseif the_key == GLUT_KEY_DOWN
        xspeed += 0.01
    elseif the_key == GLUT_KEY_LEFT
        yspeed -= 0.01
    elseif the_key == GLUT_KEY_RIGHT
        yspeed += 0.01
    end

    return nothing # specialKeyPressed returns "void" in C. this is a workaround for Julia's "automatically return the value of the last expression in a function" behavior.
end

_specialKeyPressed = cfunction(specialKeyPressed, Void, (Int32, Int32, Int32))

# run GLUT routines

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)

window = glutCreateWindow("NeHe Tut 7")

glutDisplayFunc(_DrawGLScene)
glutFullScreen()

glutIdleFunc(_DrawGLScene)
glutReshapeFunc(_ReSizeGLScene)
glutKeyboardFunc(_keyPressed)
glutSpecialFunc(_specialKeyPressed)

initGL(width, height)

glutMainLoop()
