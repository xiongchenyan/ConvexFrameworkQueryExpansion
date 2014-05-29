'''
Created on May 28, 2014

@author: cx
'''
import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/ConvexFrameworkQueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')

from Clustering.KMeans import *
from cxBase.Vector import *
from cxBase.base import cxConf,cxBaseC
from cxBase.KeyFileReader import *
class ObjectKMeansC(cxBaseC):
    def Init(self):
        self.InName = ""
        self.OutName = ""
        self.k = 8
        self.MidDir = ""
    
    @staticmethod
    def ShowConf():
        print "in\nout\nk\nmiddir"
    
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.InName = conf.GetConf('in')
        self.OutName = conf.GetConf('out')
        self.k = int(conf.GetConf('k',self.k))
        self.MidDir = conf.GetConf('middir')
        self.Model = cxKMeansC()
        self.Model.k = self.k
        self.Model.workdir = self.MidDir
        
    
    
    def CreateSpMtx(self,lvCol):
        data = []
        hFeatureIndex = {}
        
        DataIndex= 1
        for vCol in lvCol:
            hFeature = json.loads(vCol[4])
            for Feature in hFeature:
                FeatureP = len(hFeatureIndex) + 1
                if Feature in hFeatureIndex:
                    FeatureP = hFeatureIndex[Feature]
                else:
                    hFeatureIndex[Feature] = FeatureP
                data.append([DataIndex,FeatureP,hFeature[Feature]])
            DataIndex += 1
        return data 
            
        
        
    def ProcessOneQ(self,lvCol):
        data = self.CreateSpMtx(lvCol)
        lLabel = self.Model.ProcessData(data)
        return lLabel
    
    
    def DiscardBadLine(self,lvCol):
        lRes = []
        for vCol in lvCol:
            if len(vCol) < 5:
                continue
            if '{}' in vCol[4]:
                continue
            lRes.append(vCol)
        return lRes
        
    
    def Process(self):
        
        Reader = KeyFileReaderC()
        Reader.open(self.InName)
        
        out = open(self.OutName,'w')
        
        for lvCol in Reader:
            lvCol = self.DiscardBadLine(lvCol)
            lLabel = self.ProcessOneQ(lvCol)
            cnt = 0
            for i in range(len(lvCol)):
                vCol = lvCol[i]
                vCol[4] = str(lLabel[cnt])
                cnt += 1
                print >> out,'\t'.join(vCol)
                
                
        out.close()
        Reader.close()
        
        print "done"
        return True