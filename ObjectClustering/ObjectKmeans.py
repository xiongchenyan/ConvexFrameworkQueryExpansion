'''
Created on May 28, 2014

@author: cx
'''


from Clustering.KMeans import *
from cxBase.Vector import *
from cxBase.base import cxConf,cxBaseC
from cxBase.KeyFileReader import *
class ObjectKMeansC(cxBaseC):
    def Init(self):
        self.InName = ""
        self.OutName = ""
        self.k = 8
    
    @staticmethod
    def ShowConf():
        print "in\nout\nk"
    
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.InName = conf.GetConf('in')
        self.OutName = conf.GetConf('out')
        self.k = int(conf.GetConf('k',self.k))
        self.Model = KMeans(np_cluster = self.k)
    
    
    def SegDataFromLine(self,line):
        vCol = line.strip().split('\t')
        if len(vCol) < 5:
            return ""
        Vector = VectorC()
        Vector.loads(vCol[4])
        l = Vector.hDim.items()
        l.sort(key=lambda item:item[0])
        res = [item[1] for item in l]
        return res
        
        
    def ProcessOneQ(self,lLines):
        lData = []
        for line in lLines:
            data = self.SegDataFromLine(line)
            if "" != data:
                lData.append(data)
        lData = np.array(lData)
        lLabel = list(self.Model.fit_predict(lData))
        
        return lLabel
    
    
    def Process(self):
        
        Reader = KeyFileReaderC()
        Reader.open(self.InName)
        
        out = open(self.OutName,'w')
        
        for lLines in Reader:
            lLabel = self.ProcessOneQ(lLines)
            cnt = 0
            for i in range(len(lLines)):
                line = lLines[i]
                vCol = line.strip().split('\t')
                if len(vCol) < 5:
                    continue
                vCol[4] = str(lLabel[cnt])
                cnt += 1
                print >> out,'\t'.join(vCol)
                
                
        out.close()
        Reader.close()
        
        print "done"
        return True