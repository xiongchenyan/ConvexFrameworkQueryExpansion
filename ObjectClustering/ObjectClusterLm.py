'''
Created on Jun 2, 2014
form object cluster lm from despcrition
the weighted average of its object's lms
weighting:
    uniform (for now june 2nd)
    by reverse distance with the cluster centroid (require the input vector) 
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/ConvexFrameworkQueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
from cxBase.base import cxBaseC,cxConf
from IndriRelate.IndriInferencer import LmBaseC
from FbObjCenter.FbObjCacheCenter import *
from cxBase.KeyFileReader import KeyFileReaderC 
from ObjectClustering.ObjClusterBase import *

import ntpath
import sys

if 2 > len(sys.argv):
    print "conf"
    FbObjCacheCenterC.ShowConf()
    print "in\nout"
    sys.exit()
    
    
ObjCenter = FbObjCacheCenterC(sys.argv[1])
conf = cxConf(sys.argv[1])
lInName=conf.GetConf('in')

if type(lInName) != list:
    lInName = [lInName]

OutName = conf.GetConf('out')
for InName in lInName:
    print "working [%s]" %(InName)
    out = open(OutName + "_" + ntpath.basename(InName),'w')
    llQCluster = QObjClusterC.LoadQObjCluster(InName)
    for i in range(len(llQCluster)):
        for j in range(len(llQCluster[i])):
            print "working on q[%s][%d]" %(llQCluster[i][j].qid,llQCluster[i][j].ClusterId)
            print "contain [%d] obj" %(len(llQCluster[i][j].lObjId))
            llQCluster[i][j].FormLmForCluster(ObjCenter)
            print >>out, llQCluster[i][j].DumpsClusterLm()
    out.close()
print "done"

    

    
    
    
    
        
        
            