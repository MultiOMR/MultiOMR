'''
Created on 02/06/2014

@author: Victor Padilla
@project: Multiple OMR Lancaster University


Functions to manipulate sequences of music in Music21
'''
import os
from music21 import stream
from Music21OMR import correctors
from music21 import note
class Music21Functions:

    def getStringNotesFromBar(self,mybar):
        '''
        return the string of pitches of a measure given a bar
        '''
        strOut=""
        for thisNote in mybar.notes:
            if(thisNote.isNote):
                strOut+=thisNote.pitch.name
            elif(thisNote.isChord):
                strOut+=thisNote[0].pitch.name
            else:
                print("unknown")
          
        return str
    
    def getStringBar(self,Multiple_OMR,barNumber):
        '''
        return the string of pitches of the same measure in a Multiple OMR slice
        '''
        i=0        
        strBar=["","",""]
        for OMR in Multiple_OMR:
            mybar=OMR.parts[0].measure(barNumber)
            strBar[i]=self.getStringNotesFromBar(mybar)
            i+=1
        return strBar
    
    def getSingleStringBar(self,OMR,barNumber):
        '''
        return the string of pitches of a measure given the score in Music21 Format and bar number
        '''
        strBar=""
        try:
            mybar=OMR.parts[0].measure(barNumber)
            strBar=self.getStringNotesFromBar(mybar)
        except:
            print ("Error bar:"+str(barNumber))
        return strBar
     
    def getWholeNoteString(self,OMR):
        strOut=""
        for i in range(len(OMR.parts[0])):
            strOut+=self.getSingleStringBar(OMR,i+1)
            strOut+="|"
        return strOut
    
    def getDuration(self,bar):
        duration=0
        try:
            for event in bar:
                try:
                    if(event.isNote):
                        duration+=event.duration.quarterLength
                    if(event.isRest):
                        duration+=event.duration.quarterLength
                except:
                    a=0 
        except:
            a=0
        return str(duration)
    
    def getWholeDurations(self,OMR):
        strOut=""
        for i in range(len(OMR.parts[0])):
            bar=OMR.parts[0].measure(i+1)
            strOut+=self.getDuration(bar)
            strOut+="|"
        return strOut
    
    def getHashArrayFromPart(self,part):
        '''
        get Hash string of a Part (music21)
        '''
        hashArray=[]
        lengthArray=len(part.measureOffsetMap())
        for i in range(lengthArray):
#             measure=part.measure(i+1)
            measure=part.getElementsByClass(stream.Measure)[i]
            hashMeasure=self.getHashFromMeasure(measure)
            hashArray.append(hashMeasure)
        return hashArray
    
    def getHashFromMeasure(self,measure):
        '''
        get Hash string of a measure. Library correctors.py of Michael Scott Cuthbert. Project OMR
        '''
        mh=correctors.MeasureHash(measure).getHashString()
        return mh
    def reconstructScore(self,part,hashPart): 
        partReconstructed=stream.Part()
        barNumber=1
        for i in range(len(hashPart)): 
            if hashPart[i]!="*":
#                 m=part.measure(barNumber)
                m=part.getElementsByClass(stream.Measure)[barNumber-1]
                partReconstructed.append(m)
                barNumber+=1
            else:
                m=stream.Measure()
                partReconstructed.append(m)
                
        myStream=self.reorderMeasures(partReconstructed)  
        return myStream
    
    def reorderMeasures(self,omr):
        s=stream.Part()
        barNumber=1
        for measure in omr.getElementsByClass(stream.Measure):
            measure.number=barNumber
            s.append(measure)
            barNumber+=1
    
        return s              
            

        
    def recombineBars(self,bar1,bar2):
        '''
        Not implemented yet
        '''
        s=stream.Stream()
        
        for element in bar1:
                s.append(element)
        for element in bar2:
                s.append(element)
        s=s.notesAndRests
        return s
    
    def correctIncorrectMeasuresArray(self,omr,incorrectMeasures):
        measures=omr.parts[0].getElementsByClass(stream.Measure)
        for barNumber in incorrectMeasures:
            if barNumber<len(measures)-1:
    #             measure=omr.parts[0].measure(barNumber+1)
                measure=measures[barNumber]
    #             measureNext=omr.parts[0].measure(barNumber+2)
                measureNext=measures[barNumber+1]
                duration=self.getDuration(measure)
                if(measureNext!=None):
                    durationNext=self.getDuration(measureNext)
                    if(float(duration)+float(durationNext)==4):
                        try:
                            incorrectMeasures.remove(barNumber)
                            incorrectMeasures.remove(barNumber+1)
                        except:
#                             print "error correctIncorrectmeasures bar:"+str(barNumber)
                            a=1
                        self.correctIncorrectMeasuresArray(omr,incorrectMeasures)
        return incorrectMeasures
    
    
    def filterExtraMeasures(self,omr):
        sco=stream.Score()
        s=stream.Part()
        for measure in omr.parts[0].getElementsByClass(stream.Measure):
            if measure.duration.quarterLength>0:
                s.append(measure)
        sco.append(s)
        return sco
    
    def writeAlignmentMAFFT(self,sequences):
        '''
        multi-alignment of strings using mafft.bat
        http://mafft.cbrc.jp/alignment/software/
        input file:     input.txt
        output file:    output.txt
        '''
        f=open("input.txt","w")
        for seq in sequences:
            f.write(">\n")
            f.write(seq+"\n")
        f.close()
        os.system("mafft.bat --localpair --text --out output.txt input.txt")
        fOut=open("output.txt","r")
        fOut2=open("outputLine.txt","w")
        for line in fOut:
            line=line.strip("\n")
            if(line==">"):
                fOut2.write("\n")
            else:
                fOut2.write(line) 
                
        fOut.close()
        fOut2.close()
             
                
        
        
        
            