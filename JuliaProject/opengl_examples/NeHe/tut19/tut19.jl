# Mon 31 Dec 2012 01:41:39 PM EST
#
# NeHe Tut 19 - Make some colored stars and play w/ alpha blending a bit more
#
# Q - quit
# L - turn lights on/off
# F - change texture filter (linear, nearest, mipmap)
# PageUp/Down - move camera closer/further away
# Up/Down - increase/decrease x-rotation speed
# Left/Right - increase/decrease y-rotation speed
# Home/End - increase/decrease the amount of "friction" on particles
# Enter - turn rainbow effect on/off
# Space - step through colors for rainbow effect


# load necessary GLUT/OpenGL routines

using OpenGL
@OpenGL.version "1.0"
@OpenGL.load
using GLUT

# initialize variables

global window

global tilt    = 90.0
global zoom    = -15.0
global spin    = 0.0

global twinkle = false

global tex     = Array(Uint32,1) # generating 1 texture

width          = 640
height         = 480

colors = [1.0  0.5  0.5;
          1.0  0.75 0.5;
          1.0  1.0  0.5;
          0.75 1.0  0.5;
          0.5  1.0  0.5;
          0.5  1.0  0.75;
          0.5  1.0  1.0;
          0.5  0.75 1.0;
          0.5  0.5  1.0;
          0.75 0.5  1.0;
          1.0  0.5  1.0;
          1.0  0.5  0.75]

global rainbow       = true
global slowdown      = 2.0
global xspeed        = 0
global yspeed        = 0
global zoom          = -40.0
global color         = 1
global delay         = 0

global MAX_PARTICLES = 1000

global keystate = [false false false false false]

type particle
    active::Bool
    life::Float64
    fade::Float64
    red::Float64
    green::Float64
    blue::Float64
    xPos::Float64
    yPos::Float64
    zPos::Float64
    xSpeed::Float64
    ySpeed::Float64
    zSpeed::Float64
    xGrav::Float64
    yGrav::Float64
    zGrav::Float64
end

global particles = [particle(true,            # Julia doesn't like it when you try to initialize an empty array of
                      1.0,                    # a composite type and try to fill it afterwards, so we             
                      rand(1:100)/1000+0.003,  # start with a 1-element vector and tack on values                  
                      colors[1,1],
                      colors[1,2],
                      colors[1,3],
                      0.0,
                      0.0,
                      0.0,
                      (rand(1:50)-26.0)*10.0,
                      (rand(1:50)-26.0)*10.0,
                      (rand(1:50)-26.0)*10.0,
                      0.0,
                      -0.8,
                      0.0)]

for loop = 2:MAX_PARTICLES
    active = true
    life   = 1.0                              
    fade   = rand(1:100)/1000+0.003
    red    = colors[loop%size(colors,1)+1,1]
    green  = colors[loop%size(colors,1)+1,2]
    blue   = colors[loop%size(colors,1)+1,3]
    xPos   = 0.0
    yPos   = 0.0            
    zPos   = 0.0            
    xSpeed = (rand(1:50)-26.0)*10.0
    ySpeed = (rand(1:50)-26.0)*10.0
    zSpeed = (rand(1:50)-26.0)*10.0
    xGrav  = 0.0                  
    yGrav  = -0.8                 
    zGrav  = 0.0
    particles = push!(particles, particle(active,life,fade,red,green,blue,xPos,yPos,zPos,xSpeed,ySpeed,zSpeed,xGrav,yGrav,zGrav))
end

# load textures from images

function LoadGLTextures()
    global tex

    img, w, h = glimread(expanduser("~/.julia/GLUT/Examples/NeHe/tut19/Particle.bmp"))

    glGenTextures(1,tex)
    glBindTexture(GL_TEXTURE_2D,tex[1])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, img)
end

# function to init OpenGL context

function initGL(w::Integer,h::Integer)
    global tex

    glViewport(0,0,w,h)
    LoadGLTextures()
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)			 
    glDisable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)

    # enable texture mapping and alpha blending
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    glColor(1.0, 1.0, 1.0, 0.5)

    glBindTexture(GL_TEXTURE_2D,tex[1])

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
    global zoom
    global particles
    global MAX_PARTICLES
    global tex
    global rainbow 
    global slowdown
    global xspeed  
    global yspeed  
    global zoom    
    global color   
    global delay   
    global keystate

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    for loop = 1:MAX_PARTICLES
        if particles[loop].active
            x = particles[loop].xPos
            y = particles[loop].yPos
            z = particles[loop].zPos+zoom
            glColor(particles[loop].red, particles[loop].green, particles[loop].blue, particles[loop].life)
            glBegin(GL_TRIANGLE_STRIP)
                glTexCoord(1, 1)
                glVertex(x+0.5, y+0.5, z)
                glTexCoord(0, 1)
                glVertex(x-0.5, y+0.5, z)
                glTexCoord(1, 0)
                glVertex(x+0.5, y-0.5, z)
                glTexCoord(0, 0)
                glVertex(x-0.5, y-0.5, z)
            glEnd()
            particles[loop].xPos   += particles[loop].xSpeed/(slowdown*1000)
            particles[loop].yPos   += particles[loop].ySpeed/(slowdown*1000)
            particles[loop].zPos   += particles[loop].zSpeed/(slowdown*1000)
            particles[loop].xSpeed += particles[loop].xGrav
            particles[loop].ySpeed += particles[loop].yGrav
            particles[loop].zSpeed += particles[loop].zGrav
            particles[loop].life   -= particles[loop].fade
            if particles[loop].life < 0.0
                particles[loop].life   = 1.0
                particles[loop].fade   = (rand(1:100))/1000+0.003
                particles[loop].xPos   = 0.0
                particles[loop].yPos   = 0.0
                particles[loop].zPos   = 0.0
                particles[loop].xSpeed = xspeed+rand(1:60)-32.0
                particles[loop].ySpeed = yspeed+rand(1:60)-30.0
                particles[loop].zSpeed = rand(1:60)-30.0
                particles[loop].red    = colors[color,1]
                particles[loop].green  = colors[color,2]
                particles[loop].blue   = colors[color,3]
            end
            if keystate[1] == true && particles[loop].yGrav < 1.5
                particles[loop].yGrav +=0.01
                keystate[1] = false
            elseif keystate[2] == true && particles[loop].yGrav > -1.5
                particles[loop].yGrav -=0.01
                keystate[2] = false
            elseif keystate[3] == true && particles[loop].xGrav < 1.5
                particles[loop].xGrav +=0.01
                keystate[3] = false
            elseif keystate[4] == true && particles[loop].xGrav > -1.5
                particles[loop].xGrav -=0.01
                keystate[4] = false
            elseif keystate[5] == true
                particles[loop].xPos   = 0.0
                particles[loop].yPos   = 0.0
                particles[loop].zPos   = 0.0
                particles[loop].xSpeed = (rand(1:52)-26.0)*10
                particles[loop].ySpeed = (rand(1:50)-25.0)*10
                particles[loop].zSpeed = (rand(1:50)-25.0)*10
                keystate[5] = false
            end
        end
    end

    delay +=1

    glutSwapBuffers()
   
    return nothing
end
   
_DrawGLScene = cfunction(DrawGLScene, Void, ())

function keyPressed(the_key::Char,x::Int32,y::Int32)
    global delay
    global color
    global keystate
    global rainbow

    if the_key == int('q')
        glutDestroyWindow(window)
    elseif the_key == int(' ')
        delay = 0
        color +=1
        if color > 12
            color = 1
        end
    elseif the_key == int('2')
        keystate[1] = true
    elseif the_key == int('8')
        keystate[2] = true
    elseif the_key == int('4')
        keystate[3] = true
    elseif the_key == int('6')
        keystate[4] = true
    elseif the_key == int('\t')
        keystate[5] = true
    elseif the_key == int('\n')
        rainbow = (rainbow ? false : true)
    end

    return nothing # keyPressed returns "void" in C. this is a workaround for Julia's "automatically return the value of the last expression in a function" behavior.
end

_keyPressed = cfunction(keyPressed, Void, (Char, Int32, Int32))

function specialKeyPressed(the_key::Int32,x::Int32,y::Int32)
    global zoom
    global xspeed
    global yspeed
    global slowdown
    global keystate

    if the_key == GLUT_KEY_PAGE_UP
        zoom +=0.1
    elseif the_key == GLUT_KEY_PAGE_DOWN
        zoom -=0.1
    elseif the_key == GLUT_KEY_UP
        yspeed +=1.0
    elseif the_key == GLUT_KEY_DOWN
        yspeed -=1.0
    elseif the_key == GLUT_KEY_LEFT
        xspeed +=1.0
    elseif the_key == GLUT_KEY_RIGHT
        xspeed -=1.0
    elseif the_key == GLUT_KEY_HOME
        slowdown -=0.01
    elseif the_key == GLUT_KEY_END
        slowdown +=0.01
    end

    return nothing # specialKeyPressed returns "void" in C. this is a workaround for Julia's "automatically return the value of the last expression in a function" behavior.
end

_specialKeyPressed = cfunction(specialKeyPressed, Void, (Int32, Int32, Int32))

# run GLUT routines

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)

window = glutCreateWindow("NeHe Tut 19")

glutDisplayFunc(_DrawGLScene)
glutFullScreen()

glutIdleFunc(_DrawGLScene)
glutReshapeFunc(_ReSizeGLScene)
glutKeyboardFunc(_keyPressed)
glutSpecialFunc(_specialKeyPressed)

initGL(width, height)

glutMainLoop()
