'''
Created on May 27, 2014
run
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/ConvexFrameworkQueryExpansion')

from ObjVecMaker import *

import sys

if 2 != len(sys.argv):
    print "conf"
    ObjVecMakerC.ShowConf()
    sys.exit()
    
ObjVecMakerUnitRun(sys.argv[1])
print "done"
