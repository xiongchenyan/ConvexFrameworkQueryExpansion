'''
Created on May 28, 2014
classify query to domain:
in: web q (qid\tquery) not stemmed
out: qid\tquery\tjson.dumps(list[domain:score])
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/ConvexFrameworkQueryExpansion')

from FbDomainDespLm.DomainLm import *
from cxBase.Vector import *
import sys,json


if 4 != len(sys.argv):
    print "3para: query + lm + out"
    sys.exit()
    
DomainLm = DomainLmC()
DomainLm.load(sys.argv[2])
out = open(sys.argv[3],'w')

for line in open(sys.argv[1]):
    qid,query = line.strip().split('\t')
    query = query.lower()
    
    lQTerm = query.split()
    
    ResVector = VectorC()
    for term in lQTerm:
        lPre = DomainLm.Predict(term)
        Vector = VectorC()
        Vector.hDim = dict(lPre)
        ResVector += Vector
    ResVector /= float(len(lQTerm))
    lRes = ResVector.hDim.items()
    lRes.sort(key = lambda item:item[1],reverse = True)
    print >>out, qid + '\t' + query + '\t' + json.dumps(lRes)
    
out.close()

print "done" 
