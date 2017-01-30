from cymunk import *

def mycollide(arbiter):
    print "MY COLLIDE CALLED", arbiter
    try:
        print arbiter.contacts
        print arbiter.shapes
    except Exception, e:
        print e
        raise
    return True

# create the main space
space = Space()
space.set_default_collision_handler(begin=mycollide)
space.iterations = 30
space.gravity = (0, -100)
space.sleep_time_threshold = 0.5
space.collision_slop = 0.5

# create a falling circle
body = Body(100, 1e9)
body.position = (0, 100)
circle = Circle(body, 50)
circle.elasticity = 1.0
circle.friction = 1.0

# add bounds
seg1 = Segment(space.static_body, Vec2d(-320, -240), Vec2d(-320, 240), 0)
seg1.elasticity = 1.0
seg1.friction = 1.0

seg2 = Segment(space.static_body, Vec2d(320, -240), Vec2d(320, 240), 0)
seg2.elasticity = 1.0
seg2.friction = 1.0

seg3 = Segment(space.static_body, Vec2d(-320, -240), Vec2d(320, -240), 0)
seg3.elasticity = 1.0
seg3.friction = 1.0

# add everything into space
space.add_static(seg1, seg2, seg3)
space.add(circle, body)

from time import time
start = time()
while time() - start < 1.:
    space.step(1 / 30.)
    print circle.body.position

