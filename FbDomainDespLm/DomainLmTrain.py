'''
Created on May 28, 2014
train it
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/ConvexFrameworkdQueryExpansion')

from FbDomainDespLm.DomainLm import *

import sys

if 3 != len(sys.argv):
    print "in + out"
    sys.exit()
    
    
DomainLm = DomainLmC()
DomainLm.Train(sys.argv[1])
print "trained"
DomainLm.dump(sys.argv[2])
print "done"
