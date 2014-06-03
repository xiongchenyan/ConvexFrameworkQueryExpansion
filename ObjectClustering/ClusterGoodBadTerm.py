'''
Created on Jun 3, 2014
check the performance of cluster's term.
p(good term | lm), p(bad term | lm), p(neutral term | lm) 

input:
expterm ground truth scores
cluster lm
output:
qid\tquery\tcluster id\tgood prob \t bad prob \t neutral prob
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/ConvexFrameworkQueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
from cxBase.base import cxConf,cxBaseC
from cxBase.KeyFileReader import KeyFileReaderC
from IndriRelate.IndriInferencer import LmBaseC
from ObjectClustering.ObjClusterBase import *
from base.ExpTerm import *

class ClusterGoodBadTermC(cxBaseC):
    def Init(self):
        self.QExpInName = ""
        self.ClusterLmInName = ""
        self.OutName = ""
        
    @staticmethod
    def ShowConf():
        print "qexp\nclusterlm\nout"
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.QExpInName = conf.GetConf('qexp')
        self.ClusterLmInName = conf.GetConf('clusterlm')
        self.OutName = conf.GetConf('out')
        
        
        
    def FormTermPerformDict(self,lExpTerm):
        hTerm = {}
        for ExpTerm in lExpTerm:
            if ExpTerm.score > 0:
                hTerm[ExpTerm.term] = 1
            if ExpTerm.score == 0:
                hTerm[ExpTerm.term] = 0
            if ExpTerm.score < 0:
                hTerm[ExpTerm.term] = -1
        return hTerm
    
    
    def CalcClusterGoodBadFrac(self,QCluster,hTerm):
        GoodProb = 0
        BadProb = 0
        NeutralProb = 0
        
        for term in QCluster.ClusterLm:
            Prob = QCluster.ClusterLm.GetTfProb(term)
            if not term in hTerm:
                continue
            value = hTerm[term]
            if value == 1:
                GoodProb += Prob
            if value == 0:
                NeutralProb += Prob
            if value == -1:
                BadProb += Prob
        return [GoodProb,BadProb,NeutralProb]
        
    
    def Process(self):
        llExpTerm = ReadQExpTerms(self.QExpInName)
        llExpTerm.sort(key=lambda item:int(item[0].qid))        
        llQCluster = QObjClusterC().LoadClusterLms(self.ClusterLmInName)
        #llExpTerm and llQCluster are matched by qid sorted
        
        out = open(self.OutName,'w')
        
        for i in range(len(llExpTerm)):
            lExpTerm = llExpTerm[i]
            lQCluster = llQCluster[i]            
            hTerm = self.FormTermPerformDict(lExpTerm)
            
            for QCluster in lQCluster:
                GoodProb,BadProb,NeutralProb = self.CalcClusterGoodBadFrac(QCluster, hTerm)
                print >>out, QCluster.qid + '\t' + QCluster.query + '\t%d\t' %(QCluster.ClusterId) + '%f\t%f\t%f' %(GoodProb,BadProb,NeutralProb) 
            
            
        out.close()
        
        return True
            
        
        
        
        
        
import sys


if 2 != len(sys.argv):
    print "conf"
    ClusterGoodBadTermC.ShowConf()
    sys.exit()
    
    
Processor = ClusterGoodBadTermC(sys.argv[1])

Processor.Process()

print "finished"   
        
    
    
        