'''
Created on 02/07/2014
S2 Building Block
@author: victor
'''
from MultipleOMR_S1.FastAlignmentArrays import AlignmentArrays
from music21 import converter
from music21 import note
from music21 import chord
from music21 import meter
from music21 import key
from music21 import stream
from music21 import tie
from music21 import bar
from music21 import harmony
from music21 import clef




class PipelineAlignment:
    def align(self,omr_files):
        
        OMRs=[]
        OMRs_symbols=[]
        print omr_files
        for f in omr_files:
            OMRs.append(converter.parse(f, forceSource=True))

        omr_symbolsAlign=[]
        for omr in OMRs:
            omr_filtered,omr_symbols=self.filterOMR(omr)
            OMRs_symbols.append(omr_symbols)
            omr_symbolsAlign.append([])
        
        ar=AlignmentArrays()
        
        omr_symbolsAlign[0]=OMRs_symbols[0]

        for i in range(len(OMRs_symbols)):         
            for j in range(0,len(OMRs_symbols)):
                if(i!=j):
                    if len(omr_symbolsAlign[j])==0:
                        omr_symbolsAlign[j]=OMRs_symbols[j]
                    print i,j
                    out,d=ar.needleman_wunsch(omr_symbolsAlign[i], omr_symbolsAlign[j])
                    omr_symbolsAlign[i]=out[0]
                    omr_symbolsAlign[j]=out[1]
                
        return omr_symbolsAlign
    
    def getIndicesFromValue(self,value, qlist):
        indices = []
        idx = -1
        while True:
            try:
                idx = qlist.index(value, idx+1)
                indices.append(idx)
            except ValueError:
                break
        return indices
    
    def vote(self,omr_symbolsAlign):  
        
        voteArr=self.getArrayVotation(omr_symbolsAlign)    
        outArr=self.getVotationResult(omr_symbolsAlign,voteArr)
        return outArr
    
    def getArrayVotation(self,omr_symbolsAlign):
        voteArr=[] 
        for i in range(len(omr_symbolsAlign[0])):
            voteArr.append([])
            for j in range(len(omr_symbolsAlign)):
                vote=0
                voteArr[i].append([])
                for k in range(len(omr_symbolsAlign)):
                    symbol1=omr_symbolsAlign[j][i]
                    symbol2=omr_symbolsAlign[k][i]
                    if isinstance(symbol1,list):
                        symbol1=symbol1[0]
                    if isinstance(symbol2,list):
                        symbol2=symbol2[0]
                    if(symbol1==symbol2):
                        vote+=1.0
                voteArr[i][j].append(vote)  
        return voteArr
    
    def getVotationResult(self,omr_symbolsAlign,voteArr):
        outArr=[]
        for i in range(len(voteArr)):
            indexMax_array=self.getIndicesFromValue(max(voteArr[i]),voteArr[i])
            for j in indexMax_array:
                indexMax=j
                s=omr_symbolsAlign[j][i]
                duration=self.getSymbolDuration(s)
                if duration!=None:  
                    if float(duration[0])>duration[1]:# is a tuplet
                        break
                bar=self.getSymbolMesure(s)
                if bar!=None:
                    if bar[2]!="": #is a repetition
                        break
                      
            maxValue=max(voteArr[i])
            perc=maxValue[0]/len(voteArr[i])
            if perc>=0.5:
                outArr.append(omr_symbolsAlign[indexMax][i])
        print "out",outArr
        return outArr
    
    def getSymbolDuration(self,symbol):
        if isinstance(symbol,list):
            s=symbol[0]
            realDuration=symbol[1]
        else:
            s=symbol
            
        if s.find('N:')!=-1: 
            sep=s.index("_")
            duration=s[sep+1:]

            return duration,realDuration
    def getSymbolMesure(self,symbol):
        if isinstance(symbol,list):
            if symbol[0].find('!')!=-1: 
                return symbol
                
    def convertM21(self,outVote,arrError,ground):
        errorColor="#ff0000"
        missingColor="#00ff00"
#         sOut=stream.Stream()
        sOut=stream.Score()
        sPart=stream.Part()
        measureIndex=1
        measure=stream.Measure()
        measure.number=measureIndex
        indexS=0
       
        for symbol in outVote:
            mytie=""
            realDuration=None
            s=symbol
            isError=False
            isMissing=False
            if(len(ground)>indexS):
                sGround=ground[indexS]
            
            if(indexS in arrError):
                isError=True
                if s=="*":
                    s=sGround
                    isMissing=True
                            
            if isinstance(s,list):
                s=s[0]             
            if s.find('TS:')!=-1:
                ts=meter.TimeSignature(s[3:])
                if isError:
                    ts.color = errorColor
                if isMissing:
                    ts.color = missingColor
                measure.append(ts)
            if s.find('KS:')!=-1:
                k=key.KeySignature(int(s[3:]))
                if isError:
                    k.color = errorColor
                if isMissing:
                    k.color = missingColor
                measure.append(k)
            if s.find('CL:')!=-1:
                c=clef.clefFromString(str(s[3:]))
                if isError:
                    c.color = errorColor
                if isMissing:
                    c.color = missingColor
                measure.append(c)
            if s.find('N:')!=-1: 
                try:  
                    if isinstance(symbol,list):
                        realDuration=symbol[1]
                        mytie=symbol[2]
                        
                    sep=s.index("_")
                    duration=s[sep+1:]
#                     if realDuration!=None:
#                         duration=realDuration
                    if(float(duration)>0):
                        n=note.Note(s[2:sep],quarterLength=float(duration))
                        if isError:
                            n.color = errorColor
                        if isMissing:
                            n.color = missingColor
                        if mytie!="":
                            n.tie=tie.Tie(mytie)
                        measure.append(n)
                except:
                    print "error"+s
                    
            if s.find('R:')!=-1: 
                try:
                    if isinstance(symbol,list):
                        realDuration=symbol[1]
                        mytie=symbol[2]
                    duration=s[2:]
#                     if realDuration!=None:
#                         duration=realDuration
                    n=note.Rest(quarterLength=float(duration))
                    if isError:
                        n.color = errorColor
                    if isMissing:
                        n.color = missingColor
                    measure.append(n)
                except:
                    print "error"+s
                
            if s.find('C:')!=-1: 
                notes=s.split("[:")
                cPitch=[]
                for n in notes:
                    if n!='C:':
                        sep=n.index("_")
                        duration=n[sep+1:]
                        pitch= n[0:sep]
                        cPitch.append(pitch)
                c=chord.Chord(cPitch)
                c.duration.quarterLength=float(duration)
                if isError:
                    c.color = errorColor
                if isMissing:
                    c.color = missingColor
                measure.append(c)    
            if s.find('!')!=-1:
                
                if isinstance(symbol,list):
                    barType= symbol[1]
                    barRepeat= symbol[2]
                    if barType!="":
                        mybartype=bar.styleToMusicXMLBarStyle(barType)
                        myBar=bar.Barline(style=mybartype)
                        measure.rightBarline=myBar
    
                    if barRepeat!="":
                        myBar=bar.Repeat(direction=barRepeat)
                        if barRepeat=="start":
                            measure.leftBarline=myBar
                        if barRepeat=="end":
                            measure.rightBarline=myBar
                sPart.append(measure)
                measureIndex+=1
                measure=stream.Measure()
                measure.number=measureIndex
            indexS+=1        
        
        sOut.append(sPart)   
        return sOut
                
            
        
    def getStringSequenceFromArray(self,omr_symbols):  
        out=""  
        for symbol in omr_symbols:
            
            if not isinstance(symbol,list):
                out+="''"+symbol
            else:
                out+="''["
                for s in symbol:
                    out+=s
                out+="]"

#         print out
        return out
    def orderChord(self,mychord):
            midi=[]
            midi2=[]
            orderC=[]
            for n in mychord:
                midi.append(n.midi)
                midi2.append(n.midi)
                
            while len(midi)>0:
                indexMin=midi2.index(min(midi))
                indexPop=midi.index(min(midi))
                orderC.append(mychord[indexMin])
                midi.pop(indexPop)
                
            myOrderChord=chord.Chord(orderC)
            myOrderChord.duration.quarterLength=mychord.duration.quarterLength
            return myOrderChord
                  
    def filterOMR(self,omr):
        omr_filtered=stream.Stream()
        omr_symbols=[]
        for measure in omr.parts[0].getElementsByClass(stream.Measure):
            symbols=measure.flat
            newMeasure=stream.Measure()
            styleBarline=""
            directionRepeat=""
            for s in symbols:
                if 'TimeSignature' in s.classes:
                    newMeasure.append(s)
                    omr_symbols.append("TS:"+str(s.numerator)+"/"+str(s.denominator))
                    
                elif 'KeySignature' in s.classes:
                    newMeasure.append(s)
                    omr_symbols.append("KS:"+str(s.sharps))
                    
                elif 'Clef' in s.classes:
                    newMeasure.append(s)
                    omr_symbols.append("CL:"+str(s.sign))

                elif 'Note' in s.classes:
                    newMeasure.append(s)
                    mytype=s.duration.type
                    duration=note.duration.convertTypeToQuarterLength(mytype)
                    realDuration=s.duration.quarterLength
                    if realDuration==duration+duration/2: #dot case
                        duration=realDuration
                    n="N:"+s.pitch.nameWithOctave+"_"+str(duration)
                    # Ties case
                    mytie=""
                    if s.tie!=None:
                        mytie=s.tie.type
                        
                   
                    omr_symbols.append([n,realDuration,mytie] )

                elif 'Rest' in s.classes:
                    newMeasure.append(s)
                    mytype=s.duration.type
                    if mytype!="complex":
                        duration=note.duration.convertTypeToQuarterLength(mytype)
                    else:
                        duration=s.duration.quarterLength
                        
                    n="R:"+str(duration)
                    realDuration=s.duration.quarterLength
                    omr_symbols.append([n,realDuration,False])
                    
                elif 'Chord' in s.classes:
                    if type(s) is not harmony.ChordSymbol:
                        newMeasure.append(s)  
                        chord="C:"
                        sOrder=self.orderChord(s)
                        for n in sOrder:
                            chord+="[:"+n.pitch.nameWithOctave+"_"+str(sOrder.duration.quarterLength)
                        omr_symbols.append(chord)
                elif 'Barline' in s.classes:
                    styleBarline=s.style
                    try:
                        directionRepeat=s.direction
                    except:
                        directionRepeat=""


            omr_symbols.append(['!',styleBarline,directionRepeat])
            omr_filtered.append(newMeasure)
        return omr_filtered,omr_symbols
    
    def removeExtraTies(self,arraySymbols):
        for s in arraySymbols:
            if isinstance(s,list):
                mainSymbol=s[0]
                if mainSymbol.find('N:')!=-1: 
                    tie1=s[2]
                    if arraySymbols.index(s)<len(arraySymbols):
                        sNext=arraySymbols[arraySymbols.index(s)+1]
                        if isinstance(sNext,list):
                            mainSymbol2=sNext[0]
                            if mainSymbol2.find('N:')!=-1: 
                                tie2=sNext[2]
                                if tie1=='start' and tie2!='end':
                                    s[2]=''

        return arraySymbols
     
     
       
                
        
        
        