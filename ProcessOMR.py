'''
Created on 09/06/2014

@author: victor
'''
from AlignmentArrays import AlignmentArrays
from music21 import converter
from Music21Functions import Music21Functions
from Music21OMR import correctors
from music21 import stream

class ProcessOMR:
        
    def align(self,OMR):
        hashArray=[]
#         OMR=[]
#         for f in omr_files:
#             OMR.append(converter.parse(f))
        myAlignment=AlignmentArrays()
        m21F=Music21Functions()
        
        print "...Obtaining Hash of measures..."
        for i in range(len(OMR)):
            hashArray.append(m21F.getHashArrayFromPart(OMR[i].parts[0]))
            print hashArray[i]
        
        
        hashOrdered,s=myAlignment.needleman_wunsch(hashArray[0], hashArray[1])
        
        print "...reconstruct the scores..."
        streams=[]
        for i in range(len(OMR)):
            partReconstruct=m21F.reconstructScore(OMR[i].parts[0], hashOrdered[i])
            sc=stream.Score()
            sc.append(partReconstruct)
            streams.append(sc)
        return streams
    
    def vote(self,OMR):
        incorrectMeasures=[]
        for omr in OMR:
            sc=correctors.ScoreCorrector(omr)
            part=sc.getSinglePart(0)
            im=part.getIncorrectMeasureIndices(True)
            incorrectMeasures.append(im)
            
  
        m21F=Music21Functions()
        print incorrectMeasures
        for i in range(len(incorrectMeasures)):
            incorrectMeasures[i]=m21F.correctIncorrectMeasuresArray(OMR[i],incorrectMeasures[i])
        print incorrectMeasures
        if len(incorrectMeasures[0])<len(incorrectMeasures[1]):
            betterOMR=0
            worstOMR=1
        else:
            betterOMR=1
            worstOMR=0
        print "better="+str(betterOMR)
        sOutStream=stream.Score()
        sOut=stream.Part()

        for barNumber in range(len(OMR[betterOMR].parts[0].getElementsByClass(stream.Measure))):
            myBarBetter=OMR[betterOMR].parts[0].getElementsByClass(stream.Measure)[barNumber]
            myBarWorst=OMR[worstOMR].parts[0].getElementsByClass(stream.Measure)[barNumber]
            try:
                if (barNumber) in incorrectMeasures[betterOMR]:
                    sOut.append(myBarWorst)
                else:
                    sOut.append(myBarBetter)
            except:
                print "error vote bar:"+str(barNumber)
        sOutStream.append(sOut)
        sOutFiltered=m21F.filterExtraMeasures(sOutStream)
    
        return sOutFiltered 

    def order(self,omr_files):
        OMR=[]
        OMR_out=[]
        IM=[]
        lenIM=[]
        m21F=Music21Functions()
        for f in omr_files:
            OMR.append(converter.parse(f))
        for omr in OMR:
            sc=correctors.ScoreCorrector(omr)
            part=sc.getSinglePart(0)
            im=part.getIncorrectMeasureIndices(True)
            imOK=m21F.correctIncorrectMeasuresArray(omr,im)
            IM.append(imOK)
            lenIM.append(len(imOK))

        print IM
        for i in range(len(OMR)):
            indexBetter=lenIM.index( min(lenIM))
            OMR_out.append(OMR[indexBetter])
            OMR.pop(indexBetter)
            lenIM.pop(indexBetter)

        return OMR_out
            
        


