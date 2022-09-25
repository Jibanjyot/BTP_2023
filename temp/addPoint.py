import wx

class addNewPoint(wx.Frame):

    def __init__(self,parent, *args, **kwargs):
        ttl = 'Fluid Information.'

        super(addNewPoint, self).__init__(*args, **kwargs)
        
        super().__init__(parent, title=ttl, size = (300, 300))

        # self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.parent = parent
        self.InitUI()


    def InitUI(self):
        panel = wx.Panel(self)
            
        hbox = wx.BoxSizer(wx.VERTICAL)
            
        fgs = wx.FlexGridSizer(4, 2, 10,10)
            
        start_point = wx.StaticText(panel, label = "Start Point") 
        end_point_x = wx.StaticText(panel, label = "End X") 
        end_point_y = wx.StaticText(panel, label = "End Y")
        tc1 = wx.TextCtrl(panel) 
        tc2 = wx.TextCtrl(panel) 
        tc3 = wx.TextCtrl(panel)
        fgs.AddMany([(start_point), (tc1, 1, wx.EXPAND), (end_point_x),  
            (tc2, 1, wx.EXPAND), (end_point_y, 1, wx.EXPAND), (tc3, 1, wx.EXPAND)])  
        
        
        hbox.Add(fgs)
        # fgs.Add(drw)
        drw = wx.Button(panel, label="SAVE")
        # drw.Bind(wx.EVT_BUTTON,self.OnAddPoint)
        hbox.Add(drw)     
        panel.SetSizer(hbox)
        self.Centre() 
        self.Show()                
    