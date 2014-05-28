'''
Created on May 28, 2014
estimate the lm from the category desp file
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/ConvexFrameworkdQueryExpansion')

from cxBase.base import cxBaseC,cxConf
from IndriRelate.IndriInferencer import LmBaseC

class DomainLmC(cxBaseC):
    def Init(self):
        self.lLm = []
        self.lDomain = []
        self.hDomain = {}
        
        
    def Train(self,InName):
        cnt = 0
        for line in open(InName):
            cate,text = line.strip().split('\t')
            if not cate in self.hDomain:
                p = len(self.lDomain)
                self.lDomain.append(cate)
                self.lLm.append(LmBaseC())
                self.hDomain[cate] = p
            else:
                p = self.hDomain[cate]
                
            self.lLm[p].AddRawText(text)       
            cnt += 1
            if 0 == (cnt % 1000):
                print "[%d] line [%d] cate" %(cnt,len(self.lDomain)) 
        
        return True
    
    
    def dump(self,OutName):
        out = open(OutName,'w')
        for i in range(len(self.lDomain)):
            print >>out, self.lDomain[i] + '\t' + self.lLm[i].dumps()
        out.close()
        return
    
    
    def load(self,InName):
        for line in open(InName):
            vCol = line.strip().split('\t')
            self.lDomain.append(vCol[0])
            self.hDomain[vCol[0]] = len(self.lDomain) - 1
            lm = LmBaseC()
            lm.loads('\t'.join(vCol[1:]))
            self.lLm.append(lm)
        return
    
    
    def Predict(self,term):
        #add one smoothing
        lProb = [1.0/len(self.lDomain)] * len(self.lDomain)
        
        Sum = 0
        for i in range(len(self.lLm)):
            TF = self.lLm[i].GetTF(term)
            total = self.lLm[i].len
            lProb[i] = float(TF + 1) / (total + 1)
            Sum += lProb[i]
            
        for i in range(len(lProb)):
            lProb[i] /= Sum 
        return lProb 