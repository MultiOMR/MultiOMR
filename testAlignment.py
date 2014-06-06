
'''
Created on 05/06/2014

@author: Victor Padilla
@project: Multiple OMR Lancaster University

Main file only for testing purpose. This file takes two xml files and align them inserting extra bars if needed. 
The alignment is made with Needleman Wunsch algorithm but extended to arrays. The comparison is checking the distance between bars.
For doing that, the measures are reduced to chords and Hash codification using Music21. 
'''

from AlignmentArrays import AlignmentArrays
from music21 import converter
from Music21Functions import Music21Functions


hashArray=["",""]
OMR=[[],[]]

OMR[0] = converter.parse('files/mozart/xml/smartscore.mozartquartetk298.18.xml') #1
OMR[1] = converter.parse('files/mozart/xml/sharpeye.mozartquartetk298.18.xml') #2    #3


myAlignment=AlignmentArrays()


m21F=Music21Functions()
for i in range(len(OMR)):
    hashArray[i]=m21F.getHashArrayFromPart(OMR[i].parts[0])

hashOrdered,s=myAlignment.needleman_wunsch(hashArray[0], hashArray[1])
print hashOrdered[0]
print hashOrdered[1]


partReconstruct=m21F.reconstructScore(OMR[0].parts[0], hashOrdered[0])
partReconstruct.show()
partReconstruct=m21F.reconstructScore(OMR[1].parts[0], hashOrdered[1])
partReconstruct.show()










