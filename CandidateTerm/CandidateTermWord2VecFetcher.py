'''
Created on May 30, 2014
fetch candidate term word2vec
input: qexp term
output: add qexp term word2vec feature (300 dimension)
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/ConvexFrameworkQueryExpansion')

from base.ExpTerm    import *
from word2vec.WordVecBase import *
from word2vec.WordVecBatchFetcher import *

import sys

if 4 != len(sys.argv):
    print "3 para: q exp term + word2vec data + output"
    sys.exit()
    
    
llExpTerm = ReadQExpTerms(sys.argv[1])

lExpTerm = []
for item in llExpTerm:
    lExpTerm.extend(item)
    
lTerm = [item.term for item in lExpTerm]
lWordVec = WordVecBatchFetcher(lTerm,sys.argv[2])


out = open(sys.argv[3],'w')
for i in range(len(lExpTerm)):
    hFeature = {}
    for item,value in lWordVec[i].hDim.items():
        hFeature['word2vec_' + str(item)] = value
    lExpTerm[i].AddFeature(hFeature)
    print >> out, lExpTerm[i].dumps()
    
out.close()
        