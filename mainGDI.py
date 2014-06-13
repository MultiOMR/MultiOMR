'''
Created on 09/06/2014

@author: victor
'''
import os
import wx
from ProcessOMR import ProcessOMR
from music21 import converter



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
        
        menuViewMusicXimple = utilsmenu.Append(wx.ID_ANY, "&View MusicXiMpLe"," View MusicXiMpLe")

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") 
        menuBar.Append(utilsmenu,"&Utils") 
        self.SetMenuBar(menuBar)  

        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnViewMusicXimple, menuViewMusicXimple)

        self.Show(True)

    def OnAbout(self,e):
        dlg = wx.MessageDialog( self, "Multiple OMR Processing", "Multiple OMR Processingr", wx.OK)
        dlg.ShowModal() 
        dlg.Destroy()

    def OnExit(self,e):
        self.Close(True)  
    
    def trace(self,txt):
        self.control.SetValue(self.control.GetValue()+"\n"+txt)
    def OnViewMusicXimple(self,e):
        self.filename = ''
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            wildcard="",
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )

        # Show the dialog and retrieve the user response. If it is the OK response, 
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            paths = dlg.GetPaths()

            for path in paths:
                xml = converter.parse(path)
                xml.show()

        
        dlg.Destroy()

    def getFiles(self,path):
        omr_files=[]
        dir_content = os.listdir(path)
        for myfile in dir_content:
                directory = os.path.join(path,myfile)
                if myfile !="result.xml" and myfile!="ground.xml" :
                    print("-:"+myfile)
                    omr_files.append(os.path.abspath(directory))
        return omr_files
    
    def OnOpen(self,e):
        self.dirname = ''
        dlg = wx.DirDialog(None, "Choose a directory","",wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.dirname = dlg.GetPath()
            processOMR=ProcessOMR()
            
            path = self.dirname
            print("Path:"+path)
            omr_files=self.getFiles(path)
            
            omrOrdered=processOMR.order(omr_files)
            for i in range(len(omrOrdered)-1):
                oProcess=[]
                oProcess.append(omrOrdered[0])
                oProcess.append(omrOrdered[1])
                print("....xml Alignment....")         
                alignedArrays=processOMR.align(oProcess)
                
                print("....xml Voting....")
                out=processOMR.vote(alignedArrays)
                print("Output: ", path+'/result.xml')
                omrOrdered[1]=out
                omrOrdered.pop(0)
            
            out.write("musicxml", path+'/result.xml')
            

        dlg.Destroy()

app = wx.App(False)
frame = MainWindow(None, "Multiple OMR Project")
app.MainLoop()