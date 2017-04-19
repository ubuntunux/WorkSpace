# Mon 31 Dec 2012 01:39:42 PM EST
#
# NeHe Tut 18 - Make quadrics with GLU commands (builds on tut7)
#
# Q - quit
# L - turn lights on/off
# F - change texture filter (linear, nearest, mipmap)
# PageUp/Down - move camera closer/further away
# Up/Down - increase/decrease x-rotation speed
# Left/Right - increase/decrease y-rotation speed
# Space - change the currently rendered object (cube, cylinder, sphere, tapered cylinder, disc, animated disk)


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
global blend         = false

global quadratic     = 0

global part1         = 0
global part2         = 0
global p1            = 0
global p2            = 1

global object        = 0

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

    img, w, h = glimread(expanduser("~/.julia/GLUT/Examples/NeHe/tut18/crate.bmp"))

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
    global quadratic

    glViewport(0,0,w,h)
    LoadGLTextures()

    # enable texture mapping & blending
    glEnable(GL_TEXTURE_2D)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    glColor(1.0, 1.0, 1.0, 0.5)

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)			 
    glDepthFunc(GL_LEQUAL)	 
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

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

    # enable texture mapping & blending
    glEnable(GL_TEXTURE_2D)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    glColor(1.0, 1.0, 1.0, 0.5)

    # intialize quadric info
    quadratic = gluNewQuadric()

    gluQuadricNormals(quadratic, GLU_SMOOTH)
    gluQuadricTexture(quadratic, GL_TRUE)
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
    global z
    global part1
    global part2
    global quadratic
    global p1
    global p2
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

    if object == 0
        cube(cube_size)
    elseif object == 1
        glTranslate(0.0, 0.0, -1.5)
        gluCylinder(quadratic, 1.0, 1.0, 3.0, 32, 32)
    elseif object == 2
        gluDisk(quadratic, 0.5, 1.5, 32, 32)
    elseif object == 3
        gluSphere(quadratic, 1.3, 32, 32)
    elseif object == 4
        glTranslate(0.0, 0.0, -1.5)
        gluCylinder(quadratic, 1.0, 0.2, 3.0, 32, 32)
    elseif object == 5
        part1 +=p1
        part2 +=p2

        if part1 > 359
            p1    = 0
            part1 = 0
            p2    = 1
            part2 = 0
        end

        if part2 > 359
            p1 = 1
            p2 = 0
        end
        gluPartialDisk(quadratic,0.5,1.5,32,32,part1,part2-part1)
    end

    xrot +=xspeed
    yrot +=yspeed

    glutSwapBuffers()
   
    return nothing
end
   
_DrawGLScene = cfunction(DrawGLScene, Void, ())

function keyPressed(the_key::Char,x::Int32,y::Int32)
    global filter
    global light
    global blend
    global object

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
    elseif the_key == int('b')
        println("Blend was: $blend")
        blend = (blend ? false : true)
        if blend
            glEnable(GL_BLEND)
            glDisable(GL_DEPTH_TEST)
        else
            glDisable(GL_BLEND)
            glEnable(GL_DEPTH_TEST)
        end
        println("Blend is now: $blend")
    elseif the_key == int(' ')
        object +=1
        if object > 5
            object = 0
        end
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

window = glutCreateWindow("NeHe Tut 18")

glutDisplayFunc(_DrawGLScene)
glutFullScreen()

glutIdleFunc(_DrawGLScene)
glutReshapeFunc(_ReSizeGLScene)
glutKeyboardFunc(_keyPressed)
glutSpecialFunc(_specialKeyPressed)

initGL(width, height)

glutMainLoop()
