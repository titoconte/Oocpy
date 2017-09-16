import wx
from DetInput import DetInput


class Main(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Main, self).__init__(*args, **kwargs)

        self.cw = 75

        self.DetInput = DetInput(self)
        self.DetInput.Hide()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.DetInput, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        self.InitUI()

    def InitUI(self):

        self.MenuUI()
        #self.MyPanel()
        # set window size
        self.SetSize((600, 400))
        # set window title
        self.SetTitle('OOC Drill Model')
        # centerd window in the screen
        self.Centre()
        # shows frame
        self.Show(True)

    def MenuUI(self):
        # creates menubar
        menubar = wx.MenuBar()
        # FILE BAR
        # Creates file menu to inserts in menubar
        fileMenu = wx.Menu()
        # inserts options in menubar

        NewDet = fileMenu.Append(wx.ID_NEW, 'New &Determinitic','text')
        self.Bind(wx.EVT_MENU, self.CreateDet, NewDet)

        NewStoc = fileMenu.Append(wx.ID_NEW, 'New &Stochastic')
        self.Bind(wx.EVT_MENU, self.CreateStoc, NewStoc)

        OpenScenario = fileMenu.Append(wx.ID_OPEN, '&Open')
        self.Bind(wx.EVT_MENU, self.OpenScenario, OpenScenario)

        fileMenu.AppendSeparator()
        SaveScenario = fileMenu.Append(wx.ID_SAVE, '&Save')
        #self.Bind(wx.EVT_MENU, self.Save, SaveScenario)
        # QUIT OPTION
        quit = fileMenu.Append(wx.ID_EXIT, '&Quit\tCtrl+W')
        self.Bind(wx.EVT_MENU, self.OnQuit, quit)
        # inputsMenu
        UtilsMenu = wx.Menu()
        ExportLocation = UtilsMenu.Append(wx.ID_ANY, '&Export Location Point')
        #self.Bind(wx.EVT_MENU, self.Save, SaveScenario)
        WOA13 = UtilsMenu.Append(wx.ID_ANY, '&Density Profile from WOA13')
        #self.Bind(wx.EVT_MENU, self.Save, SaveScenario)
        CurrentConvert = UtilsMenu.Append(wx.ID_ANY, '&Current Profile')
        #self.Bind(wx.EVT_MENU, self.Save, SaveScenario)
        UtilsMenu.Append(wx.ID_ANY, '&Grain Size DataBase')
        #self.Bind(wx.EVT_MENU, self.Save, SaveScenario)

        # output menu
        outputMenu = wx.Menu()
        outputMenu.Append(wx.ID_ANY, '&Calculates Probability')
        outputMenu.AppendSeparator()
        Pln = outputMenu.Append(wx.ID_ANY, 'Open &Deposit File')
        self.Bind(wx.EVT_MENU, self.Pln, Pln)
        Dyn = outputMenu.Append(wx.ID_ANY, 'Open &Plume File')
        self.Bind(wx.EVT_MENU, self.Dyn, Dyn)
        outputMenu.Append(wx.ID_ANY, '&Export Results')
        outputMenu.Append(wx.ID_ANY, 'Gets &Statistics')

        # MENU BAR
        # inserts file option in menubar
        menubar.Append(fileMenu, '&File')
        menubar.Append(UtilsMenu, '&Input Options')
        menubar.Append(outputMenu, '&Output Options')
        # inserts menu bar in the frame
        self.SetMenuBar(menubar)

    # function of quit option
    def OnQuit(self, e):
        self.Close()

    def HideAll(self):
        self.DetInput.Hide()

    def Dyn(self,e):
        self.HideAll()
        self.DetInput.Show()
        self.Layout()

    def Pln(self,e):
        self.HideAll()
        self.DetInput.Show()
        self.Layout()

    def CreateDet(self,e):
        self.HideAll()
        self.DetInput.Show()
        self.Layout()

    def CreateStoc(self,e):
        self.HideAll()
        self.DetInput.Show()
        self.Layout()

    def OpenScenario(self,e):
        self.HideAll()
        self.DetInput.Show()
        self.Layout()

def main():

    ex = wx.App()
    Main(None)
    ex.MainLoop()


if __name__ == '__main__':
    main()
