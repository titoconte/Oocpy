# import wx
#
# class NotebookPanel(wx.Panel):
#     # Subclass to get everything the normal panel can do
#     def __init__(self,parent,name,menu,menuName):
#         wx.Panel.__init__(self,parent=parent)
#         ### Attaching the menu to the panel is one way to make sure
#         ###  the panel and menu stay together
#         self.Menu = menu
#         self.MenuName = menuName
#         ### All the panels will have the same information
#         ### In a real-world app, delete these lines from this class
#         ###  and populate the subclasses of this class
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         label = wx.StaticText(self,label="This is a sample notebook panel")
#         sizer.Add(label)
#
# class Grid(NotebookPanel):
#     ### The Blue Panel has a menu
#     def __init__(self,parent):
#         blueMenu = wx.Menu()
#         blueMenu.Append(wx.ID_ANY,"This is the blue menu","Dummy Help")
#         NotebookPanel.__init__(self,
#                                parent=parent,
#                                name="Grid")
#
# class ModelParameters(NotebookPanel):
#     ### The Blue Panel has a menu
#     def __init__(self,parent):
#         blueMenu = wx.Menu()
#         blueMenu.Append(wx.ID_ANY,"This is the blue menu","Dummy Help")
#         NotebookPanel.__init__(self,
#                                parent=parent,
#                                name="Grid")
#
#
#
# class MyNotebook(wx.Notebook):
#     ### For this demo, we don't need to subclass
#     ### Notebook at all.
#     def __init__(self,parent):
#         wx.Notebook.__init__(self,parent=parent)
#         self.AddPage(BluePanel(self),"Blue")
#         self.AddPage(RedPanel(self),"Red")
#
# class MyFrame(wx.Frame):
#     def __init__(self,parent):
#         wx.Frame.__init__(self,parent=parent,title="Notebook and Menu Test")
#         mbar = wx.MenuBar()
#         self.SetMenuBar(mbar)
#
#         sbar = self.CreateStatusBar()
#         self.Notebook = MyNotebook(self)
#
#         ### Create a menu that allows user to select tabs as well
#         ###  This uses ID values of 0 and 1 for the menu items.
#         tabmenu = wx.Menu()
#         for p in range(self.Notebook.GetPageCount()):
#             name = self.Notebook.GetPageText(p)
#
#             tabmenu.Append(p,"%s\tCtrl+%d" % (name,p+1),"Go to the %s page" % (name))
#             self.Bind(wx.EVT_MENU,self.GoToPage,id=p)
#         tabmenu.AppendSeparator()
#         tabmenu.Append(wx.ID_CLOSE,"Close\tCtrl+X","Exit the demo")
#         self.Bind(wx.EVT_MENU,self.Goodbye,id=wx.ID_CLOSE)
#         mbar.Append(tabmenu,"&Tabs")
#
#         ### Add the current page's menu to the bar
#         m = self.Notebook.GetCurrentPage().Menu
#         n = self.Notebook.GetCurrentPage().MenuName
#
#         mbar.Append(m,n)
#
#
#         self.SetMenuBar(mbar)
#         sizer = wx.BoxSizer()
#         sizer.Add(self.Notebook,1,wx.EXPAND)
#         self.SetSizerAndFit(sizer)
#         self.Layout()
#
#         ### The EVT_NOTEBOOX_PAGE_CHANGED is registered
#         ###  at the frame level
#         self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED,self.AdjustMenus)
#         self.Bind(wx.EVT_MENU,self.OnMenu)
#
#         ### This disables the currently selected menu item
#         mbar.Enable(self.Notebook.GetSelection(),False)
#
#     def GoToPage(self,evt):
#         ### This is the reaction to selecting a tab from
#         ###   the tab menu
#         self.Notebook.ChangeSelection(evt.GetId())
#         self.AdjustMenus(evt)
#
#     def Goodbye(self,evt):
#         self.Close(True)
#
#     def AdjustMenus(self,evt):
#         ### Menubar position 1 is the swapping menu
#
#         m = self.Notebook.GetCurrentPage().Menu
#         n = self.Notebook.GetCurrentPage().MenuName
#         mbar = self.GetMenuBar()
#         mbar.Replace(1,m,n)
#         ### Disable current page on tab menu
#         ### because the tabmenu item id's match the index
#         ### of the notebook page index, this works
#         for page in range(self.Notebook.GetPageCount()):
#             if page == self.Notebook.GetSelection():
#                 ### The Menubar can enable any menu item by ID alone
#                 mbar.Enable(page,False)
#             else:
#                 mbar.Enable(page,True)
#         ### If you don't enable this, trying to
#         ###  Change a notebook panel to the current panel
#         ###  raises an error
#
#
#     def OnMenu(self,evt):
#         ### While not used in this demo, if the other menus
#         ### actually did anything, this method would catch them
#         evt.Skip()
#
# class App(wx.App):
#     def OnInit(self):
#         frame = MyFrame(None)
#         self.SetTopWindow(frame)
#         frame.Show()
#         return 1
#
# A = App(0)
# A.MainLoop()
