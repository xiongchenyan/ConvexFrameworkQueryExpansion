'''
Created on May 28, 2014

@author: cx
'''


from Clustering.KMeans import *
from cxBase.Vector import *
from cxBase.base import cxConf,cxBaseC

class ObjectKmeansC(cxBaseC):
    def Init(self):
        self.InName = ""
        self.OutName = ""
        self.k = 8

    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.InName = conf.GetConf('in')
        self.OutName = conf.GetConf('out')
        self.k = int(conf.GetConf('k',self.k))