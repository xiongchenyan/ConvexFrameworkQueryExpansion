'''
Created on May 25, 2014
call search API for top
@author: cx
'''





import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/QueryFreebaseSemantic')
site.addsitedir('/bos/usr0/cx/PyCode/ConvexFrameworkQueryExpansion')
import sys
from cxBase.base import cxBaseC,cxConf
from GoogleFreebaseAPI.APIBase import *
from GoogleFreebaseAPI.SearchAPI import *


class QueryGoogleAPIC(cxBaseC):
    def Init(self):
        self.InQuery = ""
        self.OutName = ""
        self.NumOfObjPerQ = 20 #now max is 20
        
    @staticmethod
    def ShowConf():
        print "in\nout"
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.InQuery = conf.GetConf('in')
        self.OutName = conf.GetConf('out')
        
        
    def Process(self):
        out = open(self.OutName,'w')
        for line in open(self.InQuery):
            qid,query = line.strip().split('\t')
            lObj = SearchFreebase(query)[:self.NumOfObjPerQ]
            for Obj in lObj:
                print >> out, qid + '\t' + query + '\t' + Obj.GetId() + '\t' + Obj.GetName() + '\t%f'%(Obj.GetScore())
        out.close()
        return True
    
    

if 2 != len(sys.argv):
    print "conf"
    QueryGoogleAPIC.ShowConf()
    sys.exit()
    
QueryGoogle = QueryGoogleAPIC(sys.argv[1])
QueryGoogle.Process()
print "done"        