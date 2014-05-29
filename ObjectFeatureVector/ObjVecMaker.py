'''
Created on May 27, 2014
in: FbApiObj
out: word vec, score is lm score tf-idf, need an idf center
@author: cx
'''
import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/ConvexFrameworkQueryExpansion')


from cxBase.base import cxConf,cxBaseC
from cxBase.Vector import *
from IndriRelate.IndriInferencer import LmBaseC
from GoogleFreebaseAPI.APIBase import *
from IndriRelate.CtfLoader import TermCtfC
from word2vec.WordVecBase import *
from FreebaseDump.CateAttCntDensityCenter import *
from FbObjCenter.FbObjCacheCenter import *
#an import of the category probability
#an import of the word2vec reader

import math,json



class ObjVecMakerC(cxBaseC):
    
    def Init(self):
        self.CtfCenter = TermCtfC()
        self.Word2VecFile = ""
        self.CateDenseCenter = CateAttCntDensityCenterC()#now is null
        self.FbObjCacheCenter = FbObjCacheCenterC()
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.CtfCenter.Load(conf.GetConf('termctf'))
        self.Word2VecFile = conf.GetConf('word2vec')
        self.CateDenseCenter.load(conf.GetConf('cateattdense'))
        self.FbObjCacheCenter.SetConf(ConfIn)
        print "inited"
        
    @staticmethod
    def ShowConf():
        print "termctf\nword2vec\ncateattdense"
        FbObjCacheCenterC.ShowConf()
    
    def MakeLmVec(self,lFbObj):
        lVector = []
        print "start make lm vec"
        for FbObj in lFbObj:
            desp = FbObj.GetDesp()
            Lm = LmBaseC()
            Lm.SetFromRawText(desp)
            Vector = VectorC()
            for term in Lm.hTermTF:
                score = Lm.GetTFProb(term) * math.log(1.0/self.CtfCenter.GetCtfProb(term))
                Vector.hDim[term] = score
            Vector.Key = FbObj.GetId()
            lVector.append(Vector)
        return lVector
    
    def MakeWord2Vec(self,lFbObj):
        print "start make word2vec [%s]" %(self.Word2VecFile)
        lObjId = [item.GetId() for item in lFbObj]
        hObjP = dict(zip(lObjId,range(len(lObjId))))
        lVector = []
        for i in range(len(lObjId)):
            Vector = VectorC()
            Vector.Key = lObjId[i]
            lVector.append(Vector)
        
        reader = Word2VecReaderC()
        reader.open(self.Word2VecFile)
        print "start tarverse word2vec file [%s]" %(self.Word2VecFile)
        for word2vec in reader:
            if not word2vec.word in hObjP:
                continue
            p = hObjP(word2vec.word)
            lVector[p].hDim = word2vec.hDim
            print "get [%s]" %(lVector[p].Key)
        reader.close()
        return lVector
    
    
    def IsStopCate(self,cate):
        lStop = ['/common']
        for item in lStop:
            if item == cate[:len(item)]:
                return False
        return True
    
    def MakeCateAttCntVec(self,lFbObj):
        #require the cate att cnt in APIBase
        #and the cate att distribution (empirical) center
        lVector = []
        print "start make cate att cnt vec"
        for FbObj in lFbObj:
            Vector = VectorC()
            Vector.Key = FbObj.GetId()
            hCate = FbObj.FormCategoryAttCnt()
            print "cate for [%s]: \n%s" %(Vector.Key,json.dumps(hCate))
            for cate in hCate:
                if self.IsStopCate(cate):
                    continue
                cnt = hCate[cate]
                cdf = self.CateDenseCenter.GetProb(cate, cnt)
                print "cate [%s] prob[%f]" %(cate,cdf)
                Vector.hDim[cate] = cdf
            Vector.Normalize()
            lVector.append(Vector)
        return lVector
            
            
        
    def ProcessQObjFile(self,InName,OutName):
        #in: qid    query    objid
        #out: OutName_desp,OutName_cate,OutName_word2vec
        
        OutDesp = open(OutName + "_desp",'w')
        OutCate = open(OutName + "_cate",'w')
        OutWord2Vec = open(OutName + "_word2vec","w")
        
        lQidQuery = []
        lFbObj = []
        
        #read objid
        for line in open(InName):
            vCol = line.strip().split('\t')
            lQidQuery.append([vCol[0],vCol[1]])
            lFbObj.append(FbApiObjectC(vCol[2],vCol[3])) #TBD: check if vCol[3] is name
            
        #obj read start fill
        print "start fetching obj's topics"
        for i in range(len(lFbObj)):
            print "fetching [%s]" %(lFbObj[i].GetId())
            lFbObj[i] = self.FbObjCacheCenter.FetchObj(lFbObj[i].GetId())
            lDespVec = self.MakeLmVec([lFbObj[i]])
            lCateVec = self.MakeCateAttCntVec([lFbObj[i]])
            try:
                print >> OutDesp,lQidQuery[i][0] + "\t" + lQidQuery[i][1] + '\t' + lFbObj[i].GetId() + '\t' + lFbObj[i].GetName() + '\t' + lDespVec[0].dumps()
                print >> OutCate,lQidQuery[i][0] + "\t" + lQidQuery[i][1] + '\t'+ lFbObj[i].GetId() + '\t' + lFbObj[i].GetName() + '\t' + lCateVec[0].dumps()
            except UnicodeEncodeError:
                print "unicode encode error, discard"

            
        
#         return True
        
        print "fetched, lm and cate vecs made, start make vecs from word2vec"
        #extract and dump
        
        lWord2Vec = self.MakeWord2Vec(lFbObj)
        print "dumping"
        for i in range(len(lQidQuery)):
            try:
                print >> OutWord2Vec,lQidQuery[i][0] + "\t" + lQidQuery[i][1] + '\t'+ lFbObj[i].GetId() + '\t' + lFbObj[i].GetName() + '\t' + lWord2Vec[i].dumps()
            except UnicodeEncodeError:
                print "unicode encode error, discard"
        
        OutDesp.close()
        OutCate.close()
        OutWord2Vec.close()
        print 'done'
        return True
            
        
        
def ObjVecMakerUnitRun(ConfIn):
    conf = cxConf(ConfIn)
    InName = conf.GetConf('in')
    OutName = conf.GetConf('out')
    
    Maker = ObjVecMakerC(ConfIn)
    Maker.ProcessQObjFile(InName, OutName)
    
    return True
        
        
            
        

    
    

