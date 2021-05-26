import wx
import cv2 as cv
import numpy

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(parent = None, title = "Main Menu")
        self.frame.Show()

        return True

class MyFrame(wx.Frame):
    def __init__(self,parent,title):
        super(MyFrame, self).__init__(parent, title=title)

        panel = MainMenu(self)

class MainMenu(wx.Panel):
    def __init__(self, parent):
        super(MainMenu, self).__init__(parent)

        self.trainingList = ['Pace', 'Dribble', 'Shooting', 'Passing', 'Defense', 'Physical']

        titleText = wx.StaticText(self, wx.ID_ANY,'Soccer Training Technology')

        nameText = wx.StaticText(self, wx.ID_ANY,'Enter Name : ')
        self.nameInput = wx.TextCtrl(self, wx.ID_ANY, value='John Doe')

        trainingText = wx.StaticText(self, wx.ID_ANY, 'Choose Training : ')
        self.trainingChoice = wx.Choice(self, choices = self.trainingList)
        trainingBtn = wx.Button(self, wx.ID_ANY, 'Enter')
        self.Bind(wx.EVT_BUTTON, self.onEnter, trainingBtn)

        settingsBtn1 = wx.Button(self, wx.ID_ANY, 'Calibrate')
        self.Bind(wx.EVT_BUTTON, self.onCalibrate, settingsBtn1)
        settingsBtn2 = wx.Button(self, wx.ID_ANY, 'Exit')
        self.Bind(wx.EVT_BUTTON, self.onExit, settingsBtn2)

        mainBox = wx.BoxSizer(wx.VERTICAL)
        titleBox = wx.BoxSizer(wx.HORIZONTAL)
        nameBox = wx.BoxSizer(wx.HORIZONTAL)
        trainingBox = wx.BoxSizer(wx.HORIZONTAL)
        settingsBox = wx.BoxSizer(wx.HORIZONTAL)

        titleBox.Add(titleText, 0, wx.ALL, 5)

        nameBox.Add(nameText, 0, wx.ALL, 5)
        nameBox.Add(self.nameInput, 0, wx.ALL, 5)

        trainingBox.Add(trainingText, 0 , wx.ALL, 5)
        trainingBox.Add(self.trainingChoice, 0 , wx.ALL, 5)
        trainingBox.Add(trainingBtn, 0 , wx.ALL, 5)

        settingsBox.Add(settingsBtn1, 0 , wx.ALL, 5)
        settingsBox.Add(settingsBtn2, 0 , wx.ALL, 5)

        mainBox.Add(titleBox, 0, wx.CENTER)
        mainBox.Add(wx.StaticLine(self,), 0, wx.ALL|wx.EXPAND, 5)
        mainBox.Add(nameBox, 0, wx.ALL|wx.EXPAND)
        mainBox.Add(trainingBox, 0, wx.ALL|wx.EXPAND)
        mainBox.Add(settingsBox, 0, wx.CENTER)

        self.SetSizer(mainBox)
        mainBox.Fit(self)
        self.Layout()

    def getData(self):

        data = []
        data.append(self.nameInput.GetValue())
        selection = self.trainingChoice.GetSelection()
        data.append(self.trainingChoice.GetString(selection)) 

        return data

    def onEnter(self,event):

        data = self.getData()
        msg = str('Hello ' + str(data[0]) + ', Your ' + str(data[1]) + ' training will begin shortly.')
        print( msg )
    
    def onExit(self,event):

        print('Goodbye')
        self.GetParent().Close()

    def onCalibrate(self,event):

        print('Calibrating... ')
        print('Calibrating... ')
        print('Calibrating... ')
        print('Calibrating... ')
        print('Calibrating... ')
        print('Calibrating... ')
        print('Calibrating... ')
        print('Calibrating Complete!')

app = MyApp()
app.MainLoop()