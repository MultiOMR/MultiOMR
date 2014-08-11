'''
Created on 09/06/2014

@author: victor
'''
import os
import wx
from PipelineAlignment import PipelineAlignment
from CorrectingMeasures import CorrectingMeasures
from PitchCorrector.ProcessPitchCorrector import ProcessPitchCorrector
from music21 import converter
from MultipleOMR_S1.ProcessOMR import ProcessOMR
from MultipleOMR_S1.Music21Functions import Music21Functions


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(400,400))
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar() 

        filemenu= wx.Menu()
        utilsmenu=wx.Menu()

        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open and Process"," Process the MusicXML files in the folder")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
        
        menuWrongMeasures = utilsmenu.Append(wx.ID_ANY, "&Wrong measures"," Wrong measures")

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") 
        menuBar.Append(utilsmenu,"&Utils") 
        self.SetMenuBar(menuBar)  

        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        
        self.Bind(wx.EVT_MENU, self.OnViewWrongMeasures, menuWrongMeasures)

        self.Show(True)


    def OnAbout(self,e):
        dlg = wx.MessageDialog( self, "Ground Truth Processing", "Ground Truth Processing", wx.OK)
        dlg.ShowModal() 
        dlg.Destroy()

    def OnExit(self,e):
        self.Close(True)  
       

    def getFiles(self,path):
        omr_files=[]
        dir_content = os.listdir(path)
        for myfile in dir_content:
            directory = os.path.join(path,myfile)
            if myfile!="resultSymbolAlignment.xml" and myfile.find("result.")==-1 and myfile!="ground.xml":
                omr_files.append(os.path.abspath(directory))
        print omr_files
        return omr_files
    
    
    def getFileName(self,path,filename):
        dir_content = os.listdir(path)
        for myfile in dir_content:
                directory = os.path.join(path,myfile)
                if  myfile==filename:
                    return os.path.abspath(directory)
    
    def getResult(self,path):
        dir_content = os.listdir(path)
        for myfile in dir_content:
                directory = os.path.join(path,myfile)
                if myfile =="result.S1.xml":
                    return os.path.abspath(directory)
                
    def runPitchCorrector(self,dirname):
        path = dirname
        omr_files=self.getFiles(path)
        omr_result=self.getResult(path)
        
        filesArray=[]
        filesArray.append(omr_result)
        for files in omr_files:
            filesArray.append(files)
            
        ppc=ProcessPitchCorrector()
        omrResult=[]
        omrResult.append(omr_result)
        hashArrayResult=ppc.getHashFromOMRs(omrResult)
        hashArrayOMRs=ppc.getHashFromOMRs(omr_files)
        
        resultHashWithExtraRest,omrsWithExtraRest=ppc.alignHashResultWithOMR(hashArrayResult[0], hashArrayOMRs)
        resultHashWithExtraRest,omrsHashWithExtraRest=ppc.alignHashResultWithOMR(resultHashWithExtraRest, hashArrayOMRs)
        
        hashArrays=[]
        hashArrays.append(resultHashWithExtraRest)
        for hash in omrsHashWithExtraRest:
            hashArrays.append(hash)
        
        print filesArray
        OMRs=ppc.convertFilesToMusic21(filesArray)  
        omrJoinedParts=ppc.reconstructScores(OMRs,hashArrays)
        resultPitchCorrected=ppc.votePitch(omrJoinedParts)
        resultPitchCorrected.write("musicxml", path+'/result.S1.PC.xml')
        
    def runReplaceMeasures(self,dirname):
        processOMR=ProcessOMR()   
        path = dirname
        print("Path:"+path)
        omr_files=self.getFiles(path)   
        
        omrOrdered=processOMR.order(omr_files)
        print "..........Start process........."
        for i in range(len(omrOrdered)-1):
            oProcess=[]
            oProcess.append(omrOrdered[0])
            oProcess.append(omrOrdered[1])
           
            print("....xml Alignment....")         
            alignedArrays=processOMR.align(oProcess)
            print("....xml Voting....")
            out=processOMR.vote(alignedArrays)
            im=processOMR.flagIncorrectMeasures(out)[0]
            print "errors: ",len(im)
            if(len(im)==0):
                break
            print("Output: ", path+'/result.S1.xml')
            omrOrdered[1]=out
            omrOrdered.pop(0)
            
        
        out.write("musicxml", path+'/result.S1.xml')  
        
    def runResultS2(self,dirname):
        path = dirname
        files=self.getFiles(path)    
        pa=PipelineAlignment()
        omr_symbolsAlign=pa.align(files)
        outVote=pa.vote(omr_symbolsAlign)
        out=pa.removeExtraTies(outVote)
        resultS2=pa.convertM21(out,[],[])
        m21F=Music21Functions()
        resultS2_filter=m21F.filterExtraMeasures(resultS2)
        resultS2_filter.write("musicxml", path+'/result.S2.xml')
        
    def runCorrectingMeasures(self,dirname):
        path = dirname
        resultS1File=self.getFileName(dirname, "result.S1.xml")
        resultS1=converter.parse(resultS1File)
        resultS2File=self.getFileName(dirname, "result.S2.xml")
        resultS2=converter.parse(resultS2File)
        
        oProcess=[]
        oProcess.append(resultS1)
        oProcess.append(resultS2)
        processOMR=ProcessOMR()
        alignedArrays=processOMR.align(oProcess)
        resultS1=alignedArrays[0]
        resultS2=alignedArrays[1]

        cm=CorrectingMeasures()
        measuresIndex=processOMR.flagIncorrectMeasures(resultS2)[0]
#         measuresIndex=cm.getWrongMeasures(resultS2)
        print measuresIndex
        for mIndex in measuresIndex:
#             if(resultS2.parts[0].getElementsByClass(stream.Measure)[mIndex].duration.quarterLength<4):
            resultS2=cm.correctNotesInMeasure(resultS1,resultS2,mIndex)
        m21F=Music21Functions()
        resultS3=m21F.filterExtraMeasures(resultS2)
        resultS3.write("musicxml", path+'/result.S3.xml')
    def SubDirPath (self,d):
        return filter(os.path.isdir, [os.path.join(d,f) for f in os.listdir(d)])  
    
    def OnOpen(self,e):

        dlg = wx.DirDialog(None, "Choose a directory","",wx.DD_DEFAULT_STYLE)
        
        if dlg.ShowModal() == wx.ID_OK:
            dirGeneral = dlg.GetPath()
            subdirname=self.SubDirPath(dirGeneral)
            for dirname in subdirname:
                d=dirname+"/XML/"
#                 print "---------S1------------"
#                 self.runReplaceMeasures(d)
    #             print "---------S1 pitch corrector------------"
    #             self.runPitchCorrector(d)
                print "---------S2------------"
                self.runResultS2(d)
#                 print "---------S3------------"
#                 self.runCorrectingMeasures(d)
                print "---------END------------"

        dlg.Destroy()
    def runViewWrongMeasures(self,dirname):
        processOMR=ProcessOMR()   
        path = dirname
        print("Path:"+path)
        omr_files=self.getFiles(path)   
        for f in omr_files:
            omr=converter.parse(f)
            errorsCorrected,arrayErrors=processOMR.flagIncorrectMeasures(omr)
            for array in arrayErrors:
                for i in range(len(array)):
                    array[i]=array[i]+1
            print 
            print f
            print "Errors measures duration:"+str(arrayErrors[0])
            print "Errors measures estimated:"+str(arrayErrors[1])
            print "Errors based on beams:"+str(arrayErrors[2])
            print "Errors based on last notes:"+str(arrayErrors[3])
    
    def OnViewWrongMeasures(self,e):
        dirname = ''
        dlg = wx.DirDialog(None, "Choose a directory","",wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            dirname = dlg.GetPath()
            print "---------S1------------"
            self.runViewWrongMeasures(dirname)

        dlg.Destroy()

app = wx.App(False)
frame = MainWindow(None, "Symbol Alignment")
app.MainLoop()