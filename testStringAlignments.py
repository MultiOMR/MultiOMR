
from music21 import converter
from music21 import stream
from Alignment import Alignment
from Music21Functions import Music21Functions




smartscore = converter.parse('files/mozart/xml/smartscore.mozartquartetk298.18.simple.xml') #1
photoscore = converter.parse('files/mozart/xml/photoscore.mozartquartetk298.18.simple.xml') #2
sharpeye = converter.parse('files/mozart/xml/sharpeye.mozartquartetk298.18.simple.xml')     #3


# smartscore = converter.parse('C:/LICA/OMR_Python/files/CorpusA/achlieben/xml/smartscore.achlieben.9.simple.xml') #1
# photoscore = converter.parse('C:/LICA/OMR_Python/files/CorpusA/achlieben/xml/photoscore.achlieben.9.simple.xml') #2
# sharpeye = converter.parse('C:/LICA/OMR_Python/files/CorpusA/achlieben/xml/sharpeye.achlieben.9.simple.xml')     #3

# smartscore = converter.parse('C:/LICA/OMR_Python/files/CorpusA/achwie/xml/smartscore.achwie.simple.xml') #1
# photoscore = converter.parse('C:/LICA/OMR_Python/files/CorpusA/achwie/xml/photoscore.achwie.simple.xml') #2
# sharpeye = converter.parse('C:/LICA/OMR_Python/files/CorpusA/achwie/xml/sharpeye.achwie.simple.xml')     #3

# smartscore = converter.parse('C:/LICA/OMR_Python/files/CorpusA/adagioinsolminore/xml/smartscore.adagioinsolminore.9.simple.xml') #1
# photoscore = converter.parse('C:/LICA/OMR_Python/files/CorpusA/adagioinsolminore/xml/photoscore.adagioinsolminore.9.simple.xml') #2
# sharpeye = converter.parse('C:/LICA/OMR_Python/files/CorpusA/adagioinsolminore/xml/sharpeye.adagioinsolminore.9.simple.xml')     #3

# smartscore = converter.parse('C:/LICA/OMR_Python/files/CorpusA/banledebasque/xml/smartscore.banledebasque.simple.xml') #1
# photoscore = converter.parse('C:/LICA/OMR_Python/files/CorpusA/banledebasque/xml/smartscore.banledebasque.simple.xml') #2
# sharpeye = converter.parse('C:/LICA/OMR_Python/files/CorpusA/banledebasque/xml/sharpeye.banledebasque.simple.xml')     #3

# smartscore = converter.parse('C:/LICA/OMR_Python/files/CorpusA/derspiegel/xml/smartscore.derspiegel.simple.xml') #1
# photoscore = converter.parse('C:/LICA/OMR_Python/files/CorpusA/derspiegel/xml/photoscore.derspiegel.simple.xml') #2
# sharpeye = converter.parse('C:/LICA/OMR_Python/files/CorpusA/derspiegel/xml/sharpeye.derspiegel.simple.xml')     #3

# smartscore = converter.parse('C:/LICA/OMR_Python/files/CorpusA/dutchdance/xml/smartscore.dutchdance.simple.xml') #1
# photoscore = converter.parse('C:/LICA/OMR_Python/files/CorpusA/dutchdance/xml/photoscore.dutchdance.simple.xml') #2
# sharpeye = converter.parse('C:/LICA/OMR_Python/files/CorpusA/dutchdance/xml/sharpeye.dutchdance.simple.xml')     #3

# smartscore = converter.parse('C:/LICA/OMR_Python/files/CorpusA/emprisonnement/xml/capella.emprisonnement.simple.xml') #1
# photoscore = converter.parse('C:/LICA/OMR_Python/files/CorpusA/emprisonnement/xml/photoscore.emprisonnement.simple.xml') #2
# sharpeye = converter.parse('C:/LICA/OMR_Python/files/CorpusA/emprisonnement/xml/sharpeye.emprisonnement.simple.xml')     #3

# smartscore = converter.parse('C:/LICA/OMR_Python/files/CorpusA/french815/xml/photoscore.french815.4.simple.xml') #1
# photoscore = converter.parse('C:/LICA/OMR_Python/files/CorpusA/french815/xml/photoscore.french815.4.simple.xml') #2
# sharpeye = converter.parse('C:/LICA/OMR_Python/files/CorpusA/french815/xml/sharpeye.french815.4.simple.xml')     #3

# smartscore = converter.parse('C:/LICA/OMR_Python/files/CorpusA/fugue947/xml/smartscore.fugue947.2.simple.xml') #1
# photoscore = converter.parse('C:/LICA/OMR_Python/files/CorpusA/fugue947/xml/photoscore.fugue947.2.simple.xml') #2
# sharpeye = converter.parse('C:/LICA/OMR_Python/files/CorpusA/fugue947/xml/sharpeye.fugue947.2.simple.xml')     #3

# smartscore = converter.parse('C:/LICA/OMR_Python/files/CorpusA/funeralmarch/xml/smartscore.funeralmarch.2.simple.xml') #1
# photoscore = converter.parse('C:/LICA/OMR_Python/files/CorpusA/funeralmarch/xml/photoscore.funeralmarch.2.simple.xml') #2
# sharpeye = converter.parse('C:/LICA/OMR_Python/files/CorpusA/funeralmarch/xml/sharpeye.funeralmarch.2.simple.xml')     #3

# smartscore = converter.parse('C:/LICA/OMR_Python/files/CorpusA/gavotte/xml/smartscore.gavotte.1.simple.xml') #1
# photoscore = converter.parse('C:/LICA/OMR_Python/files/CorpusA/gavotte/xml/photoscore.gavotte.1.simple.xml') #2
# sharpeye = converter.parse('C:/LICA/OMR_Python/files/CorpusA/gavotte/xml/sharpeye.gavotte.1.simple.xml')     #3



Multiple_OMR= [smartscore,photoscore,sharpeye]

# mybar=photoscore.parts[0].measure(5)
# mybar.show('text')

          

m21F=Music21Functions()
 
strSequences=["","",""]
strDurations=["","",""]
strSequences[0]= m21F.getWholeNoteString(smartscore)
strSequences[1]= m21F.getWholeNoteString(photoscore)
strSequences[2]= m21F.getWholeNoteString(sharpeye)

strDurations[0]=m21F.getWholeDurations(smartscore)
strDurations[1]=m21F.getWholeDurations(photoscore)
strDurations[2]=m21F.getWholeDurations(sharpeye)
print(strDurations[0])
print(strDurations[1])
print(strDurations[2])
 
m21F.writeAlignmentMAFFT(strSequences)
f=open("outputLine.txt","r")
strOut=f.read()
f.close()
print(strOut)







# myAlignment=Alignment()
#  
# print("SmartScore vs Photoscore") 
# myAlignment.needleman_wunsch(strSequences[0],strSequences[1])
# print(myAlignment.score)
# print("Photoscore vs SharpEye") 
# myAlignment.needleman_wunsch(strSequences[1],strSequences[2])
# print(myAlignment.score)
# print("SharpEye vs Smartscore") 
# myAlignment.needleman_wunsch(strSequences[2],strSequences[0])
# print(myAlignment.score)

# myAlignment.verbose=False
# for i in range(len(Multiple_OMR[0].parts[0])):
#     strBar=getStringBar(Multiple_OMR,i+1)
#     multipleScore=myAlignment.needleman_wunsch_multiple(strBar)
#     print i, multipleScore,strBar
