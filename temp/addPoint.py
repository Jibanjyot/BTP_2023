import wx

class addNewPoint(wx.Frame):

    def __init__(self,parent, *args, **kwargs):
        ttl = 'Add Point'

        super(addNewPoint, self).__init__(*args, **kwargs)
        
        super().__init__(parent, title=ttl, size = (300, 300))

        # self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.parent = parent
        self.InitUI()

    def onPointSave(self,parent):
        # print(self.tc1.GetValue())
        start = self.tc1.GetValue()
        x1 = self.tc2.GetValue()
        y1 = self.tc3.GetValue()
        # print("hello")
        print(start,x1,y1)

        row_n = 0
        while self.parent.grd.GetCellValue(row_n, 0) != "":
            # print(self.parent.grd.GetCellValue(row_n, 0))
            row_n = row_n + 1
            # print("here",row_n)
        
        print(row_n)
        self.parent.grd.SetCellValue(row_n,0,start)
        self.parent.grd.SetCellValue(row_n,1,x1)
        self.parent.grd.SetCellValue(row_n,2,y1)

        # self.parent.grd.get
        point_arr = [start,x1,y1]
        # self.parent.drawLine()
        self.parent.DrawLine(*self.parent.VarifyData(row_n))
        return

    def InitUI(self):
        # print(self.parent.grd.GetCellValue(1, 0))

        panel = wx.Panel(self)
        
        hbox = wx.BoxSizer(wx.VERTICAL)
            
        fgs = wx.FlexGridSizer(4, 2, 10,10)
            
        start_point = wx.StaticText(panel, label = "Start Point") 
        end_point_x = wx.StaticText(panel, label = "End X") 
        end_point_y = wx.StaticText(panel, label = "End Y")
        self.tc1 = wx.TextCtrl(panel) 
        self.tc2 = wx.TextCtrl(panel) 
        self.tc3 = wx.TextCtrl(panel)
        fgs.AddMany([(start_point), (self.tc1, 1, wx.EXPAND), (end_point_x),  
            (self.tc2, 1, wx.EXPAND), (end_point_y, 1, wx.EXPAND), (self.tc3, 1, wx.EXPAND)])  
        
        
        hbox.Add(fgs)
        # fgs.Add(drw)
        drw = wx.Button(panel, label="SAVE")
        drw.Bind(wx.EVT_BUTTON,self.onPointSave)
        # drw.Bind(wx.EVT_BUTTON,self.OnAddPoint)
        hbox.Add(drw)     
        panel.SetSizer(hbox)
        self.Centre() 
        self.Show()      
        # print(tc1.GetValue())         
    