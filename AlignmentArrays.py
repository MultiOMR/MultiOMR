"""
Contains an implementation of the Needleman Wunsch algorithm.
Based on Michael Hamilton implementation.

Several changes made by Victor Padilla
    - Array adaptation
    - double loop to check distances between measures
"""

import numpy as np
from Alignment import Alignment
# -*- coding: utf-8 -*-

class AlignmentArrays:
    
    def __init__(self):
        
        self.verbose = False  # in verbose mode the DP and traceback will be printed        
         
        # the three directions you can go in the traceback:
        self.DIAG = 0 
        self.UP = 1 
        self.LEFT = 2

        self.arrows = [u"\u2196", u"\u2191", u"\u2190"]
        self.score=0;
     
     
   
     
    def needleman_wunsch_matrix(self,seq1, seq2):
        """
        fill in the DP matrix according to the Needleman-Wunsch algorithm.
        Returns the matrix of scores and the matrix of pointers
        """
     
        indel = -1 # indel penalty
     
        n = len(seq1)
        m = len(seq2)

        s = np.zeros( (n+1, m+1) ) # DP matrix
        ptr = np.zeros( (n+1, m+1), dtype=int  ) # matrix of pointers
     
        ##### INITIALIZE SCORING MATRIX (base case) #####
     
        for i in range(1, n+1) :
            s[i,0] = indel * i
        for j in range(1, m+1):
            s[0,j] = indel * j
     
        ########## INITIALIZE TRACEBACK MATRIX ##########
     
        # Tag first row by LEFT, indicating initial "-"s
        ptr[0,1:] = self.LEFT
     
        # Tag first column by UP, indicating initial "-"s
        ptr[1:,0] = self.UP
     
        #####################################################
     
        for i in range(1,n+1):
            for j in range(1,m+1): 
                # match
                simpleAlign=Alignment()
                simpleAlign.needleman_wunsch(seq1[i-1], seq2[j-1])
                score=simpleAlign.score
                s[i,j] = s[i-1,j-1]+ score
                

                # indel penalty
                if s[i-1,j] + indel > s[i,j] :
                    s[i,j] = s[i-1,j] + indel
                    ptr[i,j] = self.UP
                # indel penalty
                if s[i, j-1] + indel > s[i,j]:
                    s[i,j] = s[i, j-1] + indel
                    ptr[i,j] = self.LEFT
     
        return s, ptr
     
    def needleman_wunsch_trace(self,seq1, seq2, s, ptr) :
     
        #### TRACE BEST PATH TO GET ALIGNMENT ####
        align1 = []
        align2 = []
        n, m = (len(seq1), len(seq2))
        i = n
        j = m
        curr = ptr[i, j]
        while (i > 0 or j > 0):        
            ptr[i,j] += 3
            if curr == self.DIAG :            
                align1.append(seq1[i-1]) 
                align2.append(seq2[j-1]) 
                i -= 1
                j -= 1            
            elif curr == self.LEFT:
                align1.append("*") 
                align2.append(seq2[j-1]) 
                j -= 1            
            elif curr == self.UP:
                align1.append(seq1[i-1]) 
                align2.append("*") 
                i -= 1
     
            curr = ptr[i,j]
        align1.reverse()
        align2.reverse()
        return align1, align2
     
    def needleman_wunsch(self,seq1, seq2) :
        """
        computes an optimal global alignment of two sequences using the Needleman-Wunsch
        algorithm
        returns the alignment and its score
        """
        s,ptr = self.needleman_wunsch_matrix(seq1, seq2)
        alignment = self.needleman_wunsch_trace(seq1, seq2, s, ptr)
     
        if self.verbose :
            print "Alignment:"
            print alignment[0]
            print alignment[1]
        self.score=s[len(seq1), len(seq2)]/len(seq1)
        return alignment, s[len(seq1), len(seq2)]
    
   
    