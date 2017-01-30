import Utility as Util
from Utility import *

#---------------------#
# Global variable
#---------------------#
gRadian2Degree = 180.0 / 3.141592
gCheckAngle = 0.707
gFriction = 10.0
gMaxSpeed = 60.0
gOutsideDist = Util.W * 0.2
gGround = Util.H * 0.05
gJump = Util.H * 0.5
gVelocity = Util.W * 0.8
gWalk = Util.W * 0.3
gIncVel = Util.W * 1.6
gDecVel = Util.W * 2.5
gRange = Util.W * 0.3
gUnitSize = [Util.H*.18]*2
gCenter = mul(Util.WH, 0.5)
gWorldSize = mul(Util.WH, (1.0, 1.0))
gGravity = H * 2.5
gMaxObj = 100000

gSaveCount = 5
gSaveDir = "Save"
gSaveFile = []
for i in range(gSaveCount):
  gSaveFile.append(os.path.join(gSaveDir, ("SaveFile%03d" % i) + ".bin"))