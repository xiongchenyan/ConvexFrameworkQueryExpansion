'''
Created on Jun 1, 2014
kmeans clustering of candidate terms
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/ConvexFrameworkQueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')

from Clustering.KMeans import *
from cxBase.Vector import *
from cxBase.base import cxConf,cxBaseC
from base.ExpTerm import *

class CandidateTermKMeansC(cxBaseC):
    def Init(self):
        self.Model = cxKMeansC()
        self.InName = ""
        self.OutName = ""
    
    @staticmethod
    def ShowConf():
        print "in\nout\nmiddir"
    
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.InName = conf.GetConf('in')
        self.OutName = conf.GetConf('out')
        
        self.Model.SetWorkDir(conf.GetConf('middir'))
        
    
    
    def CreateMtx(self,lExpTerm):
        data = []
        for i in range(len(lExpTerm)):
            for feature,value in lExpTerm[i].hFeature:
                if not 'word2vec' in feature:
                    continue
                p = int(feature.split('_')[1])
                data.append([i+1,p+1,value])
        return data
        
    def ProcessOneQ(self,lExpTerm):
        data = self.CreateMtx(lExpTerm)
        lLabel = self.Model.ProcessData(data)
        return lLabel
    
    
    def ExpTermHasWord2Vec(self,ExpTerm):
        for feature in ExpTerm.hFeature:
            if 'word2vec' in feature:
                return True
        return False
    
    def DiscardBadTerms(self,lExpTerm):
        lRes = []
        for ExpTerm in lExpTerm:
            if self.ExpTermHasWord2Vec(ExpTerm):
                lRes.append(ExpTerm)
        return lRes
    
    def Process(self):
        llExpTerm = ReadQExpTerms(self.InName)
        
        out = open(self.OutName,'w')
        
        for lExpTerm in llExpTerm:
            lExpTerm = self.DiscardBadTerms(lExpTerm)
            lLabel = self.ProcessOneQ(lExpTerm)
            if len(lLabel) != len(lExpTerm):
                print "label len [%d] != expterm [%d]" %(len(lLabel),len(lExpTerm))
            for i in range(len(lExpTerm)):
                ExpTerm = lExpTerm[i]
                ExpTerm.hFeature.clear()
                ExpTerm.hFeature['Cluster'] = lLabel[i]
                print >>out, ExpTerm.dumps()
                
        out.close()
        return True
    
    
    
import sys

if 2 != len(sys.argv):
    print "conf"
    CandidateTermKMeansC().ShowConf()
    sys.exit()
    
method = CandidateTermKMeansC(sys.argv[1])
method.Process()
print "done"
