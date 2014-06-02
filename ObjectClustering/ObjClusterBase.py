'''
Created on Jun 2, 2014

@author: cx
'''
import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/ConvexFrameworkQueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
from cxBase.base import cxBaseC,cxConf
from FbObjCenter.FbObjCacheCenter import *
from cxBase.KeyFileReader import KeyFileReaderC
from IndriRelate.IndriInferencer import LmBaseC

class QObjClusterC(object):
    def Init(self):
        self.qid = ""
        self.query = ""
        self.ClusterId = 1
        self.lObjId = []
        self.lObjScore = []
        self.lObjName = []
        self.ClusterLm = LmBaseC()
        
    def __init__(self,qid='',query='',ClusterId=""):
        self.Init()
        self.qid = qid
        self.query = query
        self.ClusterId = ClusterId
    
    
    
    def FormLmForCluster(self,ObjCenter):
        self.FormObjScore()
            
        for i in range(len(self.lObjId)):
            desp = ObjCenter.FetchObjDesp(self.lObjId[i])
            Lm = LmBaseC(desp)
            self.ClusterLm += Lm * self.lObjScore[i]
        return self.ClusterLm
        
    
    
    def DumpsClusterLm(self):
        res = self.qid + '\t' + self.query + '\t%d\t' %(self.ClusterId) + self.ClusterLm.dumps()
        return res
    
    
    def FormObjScore(self,VectorInName = ""):
        if [] == self.lObjId:
            return
        self.lObjScore = [1.0/len(self.lObjId)] * len(self.lObjId)
        if "" != VectorInName:
            print "not implemented"
        return
        
    
    
    
        
    @staticmethod
    def LoadQObjCluster(QObjClusterIn):
        reader = KeyFileReaderC()
        reader.open(QObjClusterIn)
        llQCluster = []
        
        for lvCol in reader:
            qid = lvCol[0][0]
            query = lvCol[0][1]
            lQCluster = []
            for vCol in lvCol:
                ObjId = vCol[2]
                ObjName = vCol[3]
                Cluster = int(vCol[4])
                p = Cluster - 1
                while len(lQCluster) < p:
                    lQCluster.append(QObjClusterC(qid,query,Cluster))
                lQCluster[p].lObjId.append(ObjId)
                lQCluster[p].lObjName.append(ObjName)
            llQCluster.append(lQCluster)
        reader.close()
        
        return llQCluster
    


        