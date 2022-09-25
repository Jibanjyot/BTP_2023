import wx
import matplotlib.colors as mcolors
from matplotlib.figure import Figure
from matplotlib.text import Text
import wx.grid as gridlib
import wx.lib.mixins.gridlabelrenderer as glr
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import string
import numpy as np
class LftGrd(gridlib.Grid, glr.GridWithLabelRenderersMixin):
    def __init__(self, *args, **kw):
        gridlib.Grid.__init__(self, *args, **kw)
        glr.GridWithLabelRenderersMixin.__init__(self)




class InputForm(wx.Frame):
    def VarifyData(self, row):
        print(row)
        points2 = []
        points1 = []
        points = []
        alpha_pts = []
        nd_pt1 = ''
        nd_pt2 = ''
        New_EndPt = True
        LnLbl = self.grd.GetRowLabelValue(row)

        if self.pts=={}:
            print("here")
            self.pts['origin'] = [0, 0]
            txt=self.ax.annotate('origin',(0,0),
                    color=self.colours['purple'],
                    textcoords='offset points',
                    xytext=(3,3), ha='right',
                    picker=True)
            self.plt_txt['origin'] = txt

        # use the specified row and get the values for the 3
        for i in range(0, 3):
            pt = self.grd.GetCellValue(row, i)
            # if a letter is entered in X or Y use its
            # end points for the start of the new line
            if pt != '':
                if pt.isalpha():
                    # first step is to capitalize aplha characters
                    pt = pt.lower()
                    # change the grid value to lowercase
                    self.grd.SetCellValue(row, i, pt)

                    # first column always specifies the start point1
                    if i == 0:
                        # if origin is specified then
                        # point1 is (0,0)
                        if pt == 'origin':
                            nd_pt1 = 'origin'
                            # if 1st column has "origin" as value
                            # then start point is (0,0)
                            points1 = [0, 0]
                        else:
                            # use specified alpha character to determine point
                            # see if it exists in pts dictionary if so assign
                            # it to point1 else show warning dialog
                            nd_pt1 = pt
                            if nd_pt1 in list(self.pts.keys()) or \
                                    nd_pt1 == 'origin':
                                points1 = self.pts[nd_pt1]
                            else:
                                self.WarnData()
                                return

                    # get the x,y values in column 1 & 2
                    # designate them as points2
                    else:
                        New_EndPt = False
                        # if "origin" is in 2nd or 3rd column then
                        # the end point is the origin
                        if pt == 'origin':
                            points2 = [0, 0]
                            nd_pt2 = 'origin'
                        else:
                            # use specified alpha character to determine end
                            # point see if it exists if so assign it to point2
                            # else issue warning
                            nd_pt2 = pt
                            if nd_pt2 in list(self.pts.keys()):
                                points2 = self.pts[nd_pt2]
                            else:
                                self.WarnData()
                                return
                # this cell contains a digit which means
                # it can only be point2 as numeric
                else:
                    points2.append(float(pt))

        points.append(points1)
        points.append(points2)

        # confirm that point2 has two values in tuple and
        # that it has no label associated with it
        if len(points2) == 2:
            # create a reverse dictionary of self.pts to search by coordinates
            rev_pts = {}
            for k, v in self.pts.items():
                v = tuple(v)
                rev_pts[v] = k

            if nd_pt2 == '':
                # this will provide the next available node letter
                nds = [*self.pts]
                # if end points have been specified as (0, 0) then
                # reset node label to 'origin' and New Line status to False
                if points2 == [0, 0]:
                    New_EndPt = False
                    nd_pt2 = 'origin'
                # if the coordinates for an existing point are entered
                # into the grid then change to coordinates to that alpha point
                # and set New_EndPt to false so the point is not printed on
                # the graph twice
                elif tuple(points2) in rev_pts:
                    nd_pt2 = rev_pts[tuple(points2)]
                    New_EndPt = False
                    self.grd.SetCellValue(row, 1, nd_pt2)
                    self.grd.SetCellValue(row, 2, '')
                # if the node lable has already been used based on the
                # lowercase of the line lbl then find the next available letter
                elif LnLbl.lower() in nds:
                    for i in range(97, 123):
                        if chr(i) not in nds:
                            nd_pt2 = chr(i)
                            break
                # all else passed then use the line lbl lowercase
                # for the node label
                else:
                    nd_pt2 = LnLbl.lower()

            self.pts[nd_pt2] = points2
            # add the varified data to the lines dictionary self.runs
            alpha_pts.append(nd_pt1)
            alpha_pts.append(nd_pt2)
            self.runs[LnLbl] = [alpha_pts, New_EndPt]
            return points, LnLbl, New_EndPt


    def DrawLine(self, points, LnLbl, New_EndPt):
        # draw the plot lines and related label

        rnd = np.random.randint(len(self.clrs))
        color_name = self.clrs[int(rnd)]
        # draw the line based on points supplied
        # and populate the dictionay with the control information
        x = [i[0] for i in points]
        y = [i[1] for i in points]
        line = self.ax.plot(x, y, marker='.', markersize=10,
                            color=self.colours[color_name])
        self.plt_lines[LnLbl] = line

        # locate the center of the new line for the label location
        # and populate the dictionay with the control information
        x_mid, y_mid = ((x[0]+x[1])/2, (y[0]+y[1])/2)
        Txt=self.ax.annotate(LnLbl,(x_mid, y_mid),
                            color=self.colours[color_name],
                            textcoords='offset points',
                            xytext=(3,3), ha='left',
                            picker=True)
        self.plt_Txt[LnLbl] = Txt

        # label the end point of the line in lower case
        # and populate the dictionay with the control information
        if New_EndPt is True:
            txt = self.ax.annotate(LnLbl.lower(), (x[1], y[1]),
                                color=self.colours[color_name],
                                textcoords='offset points',
                                xytext=(3,3), ha='left',
                                picker=True)
            self.plt_txt[LnLbl.lower()] = txt

        self.canvas.draw()

    def OnCellChanging(self, evt):
        row = evt.GetRow()
        x_val = self.grd.GetCellValue(row, 1)
        y_val = self.grd.GetCellValue(row, 2)

        self.old_cell = [x_val,y_val]

    def OnCellChange(self, evt):
        # provides the new row, col value after change
        # if value is unchanged nothing
        row = evt.GetRow()
        LnLbl = self.grd.GetRowLabelValue(row)

        # if one of the cells in col 1 or 2 has a value
        # check if it is an alpha value
        # a empty cell will return false
        x_val = self.grd.GetCellValue(row, 1)
        y_val = self.grd.GetCellValue(row, 2)

        if self.old_cell == [x_val, y_val]:
            return

        if x_val.isalpha() or y_val.isalpha() and \
                self.grd.GetCellValue(row, 0) != '':
            if LnLbl in self.runs:
                self.MoveNode(x_val + y_val, LnLbl)
            else:
                self.DrawLine(*self.VarifyData(row))
        # confirm data in all 3 cells then get points
        elif x_val != '' and y_val != '' and \
                self.grd.GetCellValue(row, 0) != '':
            if LnLbl in self.runs:
                nd = [float(x_val), float(y_val)]
                self.MoveNode(nd, LnLbl)
            else:
                self.DrawLine(*self.VarifyData(row))
        elif self.grd.GetCellValue(row, 0) not in [*self.pts] and \
            self.grd.GetCellValue(row, 0) != 'origin':
            self.WarnData()
            self.grd.SetCellValue(row, 0, '')
        # if data is not complete then return
        else:
            return

    def __init__(self):

        super().__init__(None, wx.ID_ANY,
                         title='Plot Lines',
                         size=(1300, 840))

        # set up a list of dark colors suitable for the graph
        self.clrs = ['indianred', 'darkred', 'red',
                     'orangered', 'navy',
                     'chocolate', 'saddlebrown','brown',
                     'darkorange', 'orange','darkgreen', 'green',
                     'darkslategray', 'darkcyan',
                     'darkturquoise', 'darkkhaki', 'purple',
                     'darkblue', 'steelblue', 'mediumpurple',
                     'blueviolet', 'darkorchid', 'darkviolet'
                     ]

        self.colours = mcolors.CSS4_COLORS

        # inital file name to empty tring
        self.file_name = ''

        self.loop_pts = []
        self.cursr_set = False
        # list used to track changes in grid cell
        self.old_cell = []

        # set flags for deleting drawing elements
        self.dlt_loop = False
        self.dlt_line = False
        self.dlt_node = False
        self.dlt_pump = False

        # flags to indicate if warning message is to show
        self.show_line = False
        self.show_node = False
        self.show_loop = False
        self.show_pump = False

        # dictionary files for the lines and text plotted
        # used to remove specific items from plot
        self.plt_lines = {}
        # line labels
        self.plt_Txt = {}
        # node labels
        self.plt_txt = {}
        # loop circles
        self.crcl = {}
        # loop circle arrows
        self.arrw = {}
        # loop circle numbers
        self.plt_lpnum = {}
        # line direction arrows
        self.plt_arow = {}
        # pump dictionary
        self.plt_pump = {}
        # valve marked dictionary
        self.plt_vlv = {}
        self.plt_vlv_lbl = {}
        # plot lines and arrows for psuedo loops
        self.plt_pseudo = {}
        self.plt_psarow = {}

        # set dictionary of points; key node letter, value tuple of point,
        self.pts = {}
        # set dictionary of lines key line letter, value list of tuple start
        # point, end point and Boolean if first time end point is used
        self.runs = {}
	    # set dictionary of loops; key loop number, value list of centroid
        # point radius and list of all associated lines by key
        self.Loops = {}
        # dictionary for the tracking of the pseudo loops by number
        # with list of points and lines
        self.Pseudo = {}
        self.wrg_pt = ''
        # dictionary of the points moving around a given loop
        self.poly_pts = {}
        # dictionary of nodes indicating key as node and value lst indicating
        # line lbl and flow into (+) or out of node (-)
        self.nodes = {}
        # dictionary of the elevations fo the nodes
        # used in the Q energy equations
        self.elevs = {}
        # dictionary of the pump circuits
        # used in the Q energy equations
        self.pumps = {}
        # dictionary of the tank circuits
        # used in the Q energy equations
        self.tanks = {}
        # dictionary of the control valves circuits
        # used in the Q energy equations
        self.vlvs = {}

        # list of lines selected to form a loop
        self.Ln_Select = []
        # list of points in a specified direction defining the polygon loop
        self.Loop_Select = False
        # list of points redrawn
        self.redraw_pts = []

        mb = wx.MenuBar()

        fileMenu = wx.Menu()
        fileMenu.Append(103, '&Save To Database')
        fileMenu.Append(106, '&Open Database')
        fileMenu.Append(107, '&Reread Database')
        fileMenu.Append(101, '&Calculate')
        fileMenu.Append(105, '&View Report')
        fileMenu.AppendSeparator()
        fileMenu.Append(104, '&Exit')

        fluidMenu = wx.Menu()
        fluidMenu.Append(301, '&Fluid Properties')

        deleteMenu = wx.Menu()
        deleteMenu.Append(201, '&Node')
        deleteMenu.Append(202, '&Line')
        deleteMenu.Append(203, 'L&oop')
        deleteMenu.Append(204, '&Pump or Tank')

        mb.Append(fileMenu, 'File')
        mb.Append(fluidMenu, 'Fluid Data')
        mb.Append(deleteMenu, '&Delete Element')
        self.SetMenuBar(mb)

        # self.Bind(wx.EVT_MENU, self.OnCalc, id=101)
        # self.Bind(wx.EVT_MENU, self.OnExit, id=104)
        # self.Bind(wx.EVT_MENU, self.OnView, id=105)
        # self.Bind(wx.EVT_MENU, self.OnDB_Save, id=103)
        # self.Bind(wx.EVT_MENU, self.OnOpen, id=106)
        # self.Bind(wx.EVT_MENU, self.OnReread, id=107)

        # self.Bind(wx.EVT_MENU, self.OnFluidData, id=301)

        # self.Bind(wx.EVT_MENU, self.OnDeleteNode, id=201)
        # self.Bind(wx.EVT_MENU, self.OnDeleteLine, id=202)
        # self.Bind(wx.EVT_MENU, self.OnDeleteLoop, id=203)
        # self.Bind(wx.EVT_MENU, self.OnDeletePump, id=204)

        # create the form level sizer
        Main_Sizer = wx.BoxSizer(wx.HORIZONTAL)

        # add the sizer for the left side widgets
        sizerL = wx.BoxSizer(wx.VERTICAL)
        # add the grid and then set it to the left panel
        self.grd = LftGrd(self)
        # define the grid to be 3 columns and 26 rows
        self.grd.CreateGrid(26, 3)

        # set column widths
        for n in range(0, 3):
            self.grd.SetColSize(n, 80)

        self.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.OnCellChange)
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGING, self.OnCellChanging)

        # set the first column fonts and alignments
        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(wx.RED)

        attr.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL,
                             wx.FONTWEIGHT_BOLD))
        attr.SetAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.grd.SetColAttr(0, attr)
        self.dflt_grd_clr = (211,211,211)

        #freeze the grid size
        self.grd.EnableDragGridSize(False)

        # set the column headers and format
        self.grd.SetColLabelAlignment(wx.ALIGN_CENTER_HORIZONTAL,
                                      wx.ALIGN_CENTER_VERTICAL)
        self.grd.SetColLabelValue(0, "Start\nPoint")
        self.grd.SetColLabelValue(1, "End\nX")
        self.grd.SetColLabelValue(2, "End\nY")
        self.default_color = self.grd.GetLabelBackgroundColour()
        print(self.default_color)
        # set the left column lables alphabetic
        rowNum = 0
        for c in string.ascii_uppercase:
            self.grd.SetRowLabelValue(rowNum, c)
            rowNum += 1

        # default the first cell to the origin
        self.grd.SetCellValue(0, 0, "origin")
        self.grd.SetReadOnly(0, 0, True)

        editor = wx.grid.GridCellTextEditor()
        editor.SetParameters('10')
        self.grd.SetCellEditor(10, 2, editor)

        btnsizer = wx.BoxSizer(wx.HORIZONTAL)
        drw = wx.Button(self, -1, label="Redraw\nLines")
        self.loop = wx.Button(self, id=0, label="Select\nReal Loop")
        self.pseudo = wx.Button(self, id=1, label="Select\nPseudo Loop")
        xit = wx.Button(self, -1, "Exit")
        btnsizer.Add(drw, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        btnsizer.Add(self.loop, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        btnsizer.Add(self.pseudo, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        btnsizer.Add(xit, 0, wx.ALL|wx.ALIGN_CENTER, 5)

        # bind the button events to handlers
        # self.Bind(wx.EVT_BUTTON, self.OnReDraw, drw)
        # self.Bind(wx.EVT_BUTTON, self.OnLoop, self.loop)
        # self.Bind(wx.EVT_BUTTON, self.OnLoop, self.pseudo)
        # self.Bind(wx.EVT_BUTTON, self.OnExit, xit)

        sizerL.Add((10, 20))
        sizerL.Add(self.grd, 1, wx.EXPAND)
        sizerL.Add(btnsizer, 1, wx.ALIGN_CENTER, wx.EXPAND)

        sizerR = wx.BoxSizer(wx.VERTICAL)
        # add the draw panel
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.ax = self.canvas.figure.axes[0]
        self.ax.grid()
        self.ax.set(xlabel='X Direction', ylabel='Y Direction',
                    title='General 2D Network layout')
        # self.add_toolbar()
        # self.figure.canvas.mpl_connect('pick_event', self.OnLeftSelect)

        sizerR.Add(self.canvas, 1, wx.EXPAND)
        # sizerR.Add(self.toolbar)

        Main_Sizer.Add(sizerL, 0, wx.EXPAND)
        Main_Sizer.Add((10, 10))
        Main_Sizer.Add(sizerR, 1, wx.EXPAND)
        self.SetSizer(Main_Sizer)

        self.Center()
        self.Show(True)
        self.Maximize(True)


if __name__ == "__main__":
    app = wx.App(False)
    frm = InputForm()
    app.MainLoop()
