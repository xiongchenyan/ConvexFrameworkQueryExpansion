'''
Created on Jun 4, 2014
input: object ranking score + object cluster res
output: object ranking score \t cluster id \t average ranking score in this cluster
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from cxBase.KeyFileReader import *
import sys



def FormObjScoreHash(lObjvCol):
    h = {}
    for vCol in lObjvCol:
        h[vCol[2]] = float(vCol[4])    
    return h

def FormObjClusterHash(lClustervCol):
    h = {}
    for vCol in lClustervCol:
        h[vCol[2]] = vCol[4]    
    return h

def CalcClusterRankScore(hObjScore,hObjCluster):
    hClusterScore = {}
    
    hClusterSize = {}
    
    for ObjId,ClusterId in hObjCluster.items():
        ObjScore = hObjScore[ObjId]
        if not ClusterId in hClusterScore:
            hClusterScore[ClusterId] = ObjScore
            hClusterSize[ClusterId] = 1
        else:
            hClusterScore[ClusterId] += ObjScore
            hClusterSize[ClusterId] += 1
    
    for item in hClusterScore:
        hClusterScore[item] /= hClusterSize[item]
    return hClusterScore

def ProcessOneQuery(lObjvCol,lClustervCol):
    hObjRankScore = FormObjScoreHash(lObjvCol)
    hObjCluster = FormObjClusterHash(lClustervCol)
    hClusterScore = CalcClusterRankScore(hObjRankScore,hObjCluster)
    
    
    lResvCol = []
    for vCol in lObjvCol:
        ClusterId = hObjCluster[vCol[2]]
        ClusterScore = hClusterScore[ClusterId]
        vCol.extend([ClusterId,str(ClusterScore)])
        lResvCol.append(vCol)
    return lResvCol



if 4 != len(sys.argv):
    print "3 para: ObjScore + ObjCluster + output"
    sys.exit()
    
    
ScoreReader = KeyFileReaderC()
ScoreReader.open(sys.argv[1])
ClusterReader = KeyFileReaderC()
ClusterReader.open(sys.argv[2])

out = open(sys.argv[3],'w')

llScorevCol = []
for lvCol in ScoreReader:
    llScorevCol.append(lvCol)
    
llClustervCol = []
for lvCol in ClusterReader:
    llClustervCol.append(lvCol)
    
llScorevCol.sort(key=lambda item:int(item[0][0]))
llClustervCol.sort(key=lambda item:int(item[0][0]))



p = 0
q = 0

while (p < len(llScorevCol)) &(q < len(llClustervCol)):
    if int(llScorevCol[p][0][0]) < int(llClustervCol[q][0][0]):
        p += 1
        continue
    if int(llScorevCol[p][0][0]) > int(llClustervCol[q][0][0]):
        q += 1
        continue
    
    lResvCol = ProcessOneQuery(llScorevCol[p],llClustervCol[q])
    
    for vCol in lResvCol:
        print >>out, '\t'.join(vCol)
    p += 1
    q += 1
    

out.close()
ScoreReader.close()
ClusterReader.close()



    
