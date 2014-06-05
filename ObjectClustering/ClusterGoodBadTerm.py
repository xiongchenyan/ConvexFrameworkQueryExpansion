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

'''
update: allow multiple input and output will be used as an initial
add Good-bad score
sort cluster by good-bad
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
import ntpath


class ClusterGoodBadTermC(cxBaseC):
    def Init(self):
        self.QExpInName = ""
        self.lClusterLmInName = []
        self.OutName = ""
        
    @staticmethod
    def ShowConf():
        print "qexp\nclusterlm\nout"
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.QExpInName = conf.GetConf('qexp')
        self.lClusterLmInName = conf.GetConf('clusterlm')
        if type(self.lClusterLmInName) != list:
            self.lClusterLmInName = [self.lClusterLmInName]
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
        
        for term in QCluster.ClusterLm.hTermTF:
            Prob = QCluster.ClusterLm.GetTFProb(term)
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
        
        
    def MatchExpTermAndCluster(self,llExpTerm,llQCluster):
        lA = []
        lB = []
        
        a = 0
        b = 0
        while (a < len(llExpTerm)) & (b < len(llQCluster)):
            if int(llExpTerm[a][0].qid) < int(llQCluster[b][0].qid):
                a += 1
                continue
            if int(llExpTerm[a][0].qid) > int(llQCluster[b][0].qid):
                b += 1
                continue
            lA.append(llExpTerm[a])
            lB.append(llQCluster[b])
            a += 1
            b += 1        
        return lA,lB
        
    
    def Process(self):
        llExpTerm = ReadQExpTerms(self.QExpInName)
        llExpTerm.sort(key=lambda item:int(item[0].qid))
        
        for ClusterLmInName in self.lClusterLmInName:                
            llQCluster = QObjClusterC().LoadClusterLms(ClusterLmInName)
            #llExpTerm and llQCluster are matched by qid sorted
            llThisExpTerm,llQCluster = self.MatchExpTermAndCluster(llExpTerm,llQCluster)
            out = open(self.OutName + "_%s" %(ntpath.basename(ClusterLmInName)),'w')

            for i in range(len(llThisExpTerm)):
                lExpTerm = llThisExpTerm[i]
                lQCluster = llQCluster[i]            
                hTerm = self.FormTermPerformDict(lExpTerm)
                lRes = []
                for QCluster in lQCluster:
                    GoodProb,BadProb,NeutralProb = self.CalcClusterGoodBadFrac(QCluster, hTerm)
                    lRes.append(QCluster.qid + '\t' + QCluster.query + '\t%d\t' %(QCluster.ClusterId) + '%f\t%f\t%f\t%f' %(GoodProb,BadProb,NeutralProb,GoodProb - BadProb))
                lRes.sort(key=lambda item:float(item.split('\t')[6]),reverse = True)    
                print >>out, '\n'.join(lRes)
            
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
        
    
    
        