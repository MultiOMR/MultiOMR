'''
Created on 07/07/2014
S3 Building Block
@author: victor
'''
from music21 import stream
from music21 import note
from Music21OMR import correctors
from PipelineAlignment import PipelineAlignment
from MultipleOMR_S1.FastAlignmentArrays import AlignmentArrays
from MultipleOMR_S1.Music21Functions import Music21Functions
class CorrectingMeasures:
    def getWrongMeasures(self,omr):
        sc=correctors.ScoreCorrector(omr)
        part=sc.getSinglePart(0)
        m21F=Music21Functions()
        
#         im=sc.getAllIncorrectMeasures()
#         im2=m21F.correctIncorrectMeasuresArray(omr,im[0])
        im=m21F.getIncorrectMeasureIndices(omr)
        im2=m21F.correctIncorrectMeasuresArray(omr,im)
        m21F=Music21Functions()
        
        
        
        return im2
    
    def correctNotesInMeasure(self,resultS1,resultS2,mIndex):

        measureS1=resultS1.parts[0].getElementsByClass(stream.Measure)[mIndex]
        measureS2=resultS2.parts[0].getElementsByClass(stream.Measure)[mIndex]
        
        if measureS1.hasVoices():
            voice1=measureS1.getElementsByClass(stream.Voice)[0]
            measureS1.removeByClass(stream.Voice)
            measureS1.append(voice1)
        
        mS1_Symbol=self.getSymbol(measureS1)
        mS2_Symbol=self.getSymbol(measureS2)
        
        alignment=AlignmentArrays()
        measuresAligned,score=alignment.needleman_wunsch(mS1_Symbol, mS2_Symbol)
        ma1= measuresAligned[0]
        ma2= measuresAligned[1]
        print "Measure",mIndex+1
        print ma1
        print ma2
        ma2_new=ma2
        for i in range(len(ma2_new)):
            if ma2_new[i]=="*":
                ma2_new[i]=ma1[i]
        
        pa=PipelineAlignment()
        ma2_M21=pa.convertM21(ma2_new,[],[])
        mybar=ma2_M21[0].getElementsByClass(stream.Measure)
        resultS2_new=self.replaceMeasure(resultS2,mybar,mIndex)
        
#         arrErrors=self.getWrongMeasures(resultS2_new)
#         print "wrong", arrErrors
#         if mIndex in arrErrors:
#             return resultS2
        return resultS2_new
    
    def replaceMeasure(self,omr,mybar,mIndex):
        s=stream.Score()
        p=stream.Part()
        for i in range(len(omr.parts[0].getElementsByClass(stream.Measure))):
            bar=omr.parts[0].getElementsByClass(stream.Measure)[i]
            if i==mIndex:
                p.append(mybar.getElementsByClass(stream.Measure)[0])
            else:
                p.append(bar)
        s.append(p)
        return s
                
    def getSymbol(self,measure):
        pa=PipelineAlignment()
        s=stream.Score()
        p=stream.Part()
#         if measure.hasVoices():
#             measure=measure.getElementsByClass(stream.Voice)[0]
        p.append(measure)
        s.append(p)
        symbol=pa.filterOMR(s)
        return symbol[1]
            
            
