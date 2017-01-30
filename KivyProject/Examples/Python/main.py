import Utility as Util
from Utility import *

from PyInterpreter import PyInterpreter
    
if __name__ == '__main__':
  gMyRoot.show_debug(True)
  gMyRoot.run( PyInterpreter.instance() )