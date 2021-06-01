import wx
import cv2 as cv
import matplotlib
import numpy

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(parent = None, title = "Main Menu")
        self.frame.Show()

        return True

class MyFrame(wx.Frame):
    def __init__(self,parent,title):
        super(MyFrame, self).__init__(parent, title=title)

        self._mainmenu = MainMenu(self)
        self._trainingmenu = TrainingPanel(self)
        self._trainingmenu.Hide()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self._mainmenu, 1, wx.EXPAND)
        self.sizer.Add(self._trainingmenu, 1, wx.EXPAND)

        self.Bind(wx.EVT_BUTTON, self.onEnter, self._mainmenu.trainingBtn)
        self.Bind(wx.EVT_BUTTON, self.onMM, self._trainingmenu.mainmenuBtn)

    def onMM(self,event):
        self.onSwitchPanels()

    def getData(self):

        data = []
        data.append(self._mainmenu.nameInput.GetValue())
        selection = self._mainmenu.trainingChoice.GetSelection()
        data.append(self._mainmenu.trainingChoice.GetString(selection)) 

        return data

    def onEnter(self,event):

        data = self.getData()
        msg = str('Hello ' + str(data[0]) + ', Your ' + str(data[1]) + ' training will begin shortly.')
        print( msg )
        self.onSwitchPanels()

    def onSwitchPanels(self):
        """"""
        if self._mainmenu.IsShown():
            self.SetTitle("Training Menu Showing")
            self._mainmenu.Hide()
            self._trainingmenu.Show()
        else:
            self.SetTitle("Main Menu Showing")
            self._mainmenu.Show()
            self._trainingmenu.Hide()
        self.Layout()

class MainMenu(wx.Panel):
    def __init__(self, parent):
        super(MainMenu, self).__init__(parent)

        self.trainingList = ['Pace', 'Dribble', 'Shooting', 'Passing', 'Defense', 'Physical']

        titleText = wx.StaticText(self, wx.ID_ANY,'Soccer Training Technology')

        nameText = wx.StaticText(self, wx.ID_ANY,'Enter Name : ')
        self.nameInput = wx.TextCtrl(self, wx.ID_ANY, value='John Doe')

        trainingText = wx.StaticText(self, wx.ID_ANY, 'Choose Training : ')
        self.trainingChoice = wx.Choice(self, choices = self.trainingList)
        self.trainingBtn = wx.Button(self, wx.ID_ANY, 'Enter')

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
        trainingBox.Add(self.trainingBtn, 0 , wx.ALL, 5)

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


class TrainingPanel(wx.Panel):
    def __init__(self, parent):
        super(TrainingPanel, self).__init__(parent)

        titleText = wx.StaticText(self, wx.ID_ANY, 'Pace Training')

        '''
        self.cam = cv.VideoCapture(0)
        ret, img = self.cam.read()

        length, height = img.shape[:2]
        parent.SetSize(length,height)
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.bmp = wx.Bitmap.FromBuffer(length,height,img)

        self.timer = wx.Timer(self)
        self.timer.Start(1000/60)

        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_TIMER, self.nextFrame)~
        '''

        convoOutput = wx.StaticText(self, wx.ID_ANY,'Press OK to Begin')
        convoBtn = wx.Button(self, wx.ID_ANY, 'OK')
        self.Bind(wx.EVT_BUTTON, self.onOK, convoBtn)

        yesBtn = wx.Button(self, wx.ID_ANY, 'Yes')
        self.Bind(wx.EVT_BUTTON, self.onYes, yesBtn)
        noBtn = wx.Button(self, wx.ID_ANY, 'No')
        self.Bind(wx.EVT_BUTTON, self.onNo, noBtn)
        
        self.mainmenuBtn = wx.Button(self, wx.ID_ANY, 'Main Menu')

        mainBox = wx.BoxSizer(wx.VERTICAL)
        titleBox = wx.BoxSizer(wx.HORIZONTAL)
        #displayBox = wx.BoxSizer(wx.HORIZONTAL)
        convoBox = wx.BoxSizer(wx.HORIZONTAL)
        buttonBox = wx.BoxSizer(wx.HORIZONTAL)

        titleBox.Add(titleText, 0, wx.ALL, 5)
        
        convoBox.Add(convoOutput, 0, wx.ALL, 5)
        convoBox.Add(convoBtn, 0, wx.ALL, 5)

        buttonBox.Add(yesBtn, 0, wx.ALL, 5)
        buttonBox.Add(noBtn, 0, wx.ALL, 5)
        buttonBox.Add(self.mainmenuBtn, 0, wx.ALL, 5)

        mainBox.Add(titleBox, 0, wx.CENTER)
        mainBox.Add(wx.StaticLine(self,), 0, wx.ALL|wx.EXPAND, 5)
        #mainBox.Add(self.bmp, 0, wx.CENTER)
        mainBox.Add(convoBox, 0, wx.CENTER)
        mainBox.Add(buttonBox, 0, wx.CENTER)
        
        self.SetSizer(mainBox)
        mainBox.Fit(self)
        self.Layout()

    def onPaint(self,event):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp,0,0)


    def nextFrame(self,event):
        ret, img = self.cam.read()
        if ret:
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            self.bmp.CopyFromBuffer(img)
            self.Refresh()


    def onOK(self,event):
        #do something
        return

    def onYes(self,event):
        #do something
        return
    
    def onNo(self,event):
        #do something
        return

app = MyApp()
app.MainLoop()