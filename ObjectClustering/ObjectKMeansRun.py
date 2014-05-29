'''
Created on May 28, 2014
run kmeans
@author: cx
'''
import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/ConvexFrameworkQueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')
from ObjectKMeans import *

import sys

if 2 != len(sys.argv):
    print "conf"
    ObjectKMeansC.ShowConf()
    sys.exit()
    
    
Maker = ObjectKMeansC(sys.argv[1])
Maker.Process()
print "finished"
