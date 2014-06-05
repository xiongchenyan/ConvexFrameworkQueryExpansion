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
from cxBase.TextBase import *
import json
class QObjClusterC(object):
    def Init(self):
        self.qid = ""
        self.query = ""
        self.ClusterId = 1
        self.lObjId = []
        self.lObjScore = [] #Obj's ranking score
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
            Lm = LmBaseC(TextBaseC.RawClean(desp))
            self.ClusterLm += Lm * self.lObjScore[i]
        return self.ClusterLm
        
    
    
    def DumpsClusterLm(self):
        res = self.qid + '\t' + self.query + '\t%d\t' %(self.ClusterId) + self.ClusterLm.dumps()
        return res
    
    
    def LoadsClusterLm(self,line):
        vCol = line.strip().split('\t')
        self.qid = vCol[0]
        self.query = vCol[1]
        self.ClusterId = int(vCol[2])
        self.ClusterLm.loads('\t'.join(vCol[3:]))
        return True
    
    
    def MaxRankingScore(self):
        return max(self.lObjScore)
    
    def MeanRankingScore(self):
        if len(self.lObjScore) == 0:
            return 0
        return sum(self.lObjScore) / float(len(self.lObjScore))
    
    
    def ClusterSize(self):
        return len(self.lObjId)
    
    @staticmethod
    def LoadClusterLms(InName):
        #read clusters
        #lQCluster[(qid)[clusters]]
        reader = KeyFileReaderC()
        reader.open(InName)
        llQCluster = []
        for lvCol in reader:
            lQCluster = []
            for vCol in lvCol:
                Cluster = QObjClusterC()
                Cluster.LoadsClusterLm('\t'.join(vCol))
                lQCluster.append(Cluster)
            llQCluster.append(lQCluster)
        llQCluster.sort(key=lambda item:int(item[0].qid))
        reader.close()
        return llQCluster
        
        
        
        
        
    
    def FormObjScore(self,hObjScore = {}):
        #ObjScore fill as ranking score
        if [] == self.lObjId:
            return
        self.lObjScore = [1.0/len(self.lObjId)] * len(self.lObjId)
        if {} != hObjScore:
            for i in range(len(self.lObjId)):
                Key = self.qid + "\t" + self.lObjId[i]
                if Key in hObjScore:
                    self.lObjScore[i] = hObjScore[Key]
                else:
                    self.lObjScore[i] = 0
        return

    
    
    
    
    
    
    
    @staticmethod
    def SetObjRankingScore(llQCluster,QObjRankingScoreIn):
        #form hObjScore
        #set for each cluster
        hObjScore = {}
        for line in open(QObjRankingScoreIn):
            vCol = line.strip().split('\t')
            Key = vCol[0] + '\t' + vCol[2]
            score = float(vCol[4])
            hObjScore[Key] = score
            
        for  i in range(len(llQCluster)):
            for j in range(len(llQCluster[i])):
                llQCluster[i][j].FormObjScore(hObjScore)
                
        return llQCluster
    
        
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
                while len(lQCluster) <= p:
                    Id = len(lQCluster) + 1
                    lQCluster.append(QObjClusterC(qid,query,Id))
                lQCluster[p].lObjId.append(ObjId)
                lQCluster[p].lObjName.append(ObjName)
            llQCluster.append(lQCluster)
        reader.close()
        
        return llQCluster
    


        