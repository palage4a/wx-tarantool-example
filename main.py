import tarantool
import wx
import os

ID_CTRL = 1

class HelloFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(HelloFrame, self).__init__(*args, **kwargs)
        self.tarantool = tarantool.connect('localhost', 3301, user='admin', password='pass')
        panel = wx.Panel(self)

        grid = wx.GridBagSizer(13, 4)

        get_by_id_btn = wx.Button(panel, -1, 'get')
        self.Bind(wx.EVT_BUTTON, self.OnGetRecord, get_by_id_btn)
        report_btn = wx.Button(panel, -1, 'report')
        self.Bind(wx.EVT_BUTTON, self.OnGenerateReport, report_btn)
        all_records_btn = wx.Button(panel, -1, 'all records')
        self.Bind(wx.EVT_BUTTON, self.OnGetAll, all_records_btn)


        # footer
        ok_btn = wx.Button(panel, -1, 'ok')
        close_btn = wx.Button(panel, -1, 'Close')

        grid.Add(wx.SpinCtrl(panel, ID_CTRL), wx.GBPosition(0, 5))
        grid.Add(get_by_id_btn, wx.GBPosition(0, 6))
        grid.Add(report_btn, wx.GBPosition(1, 6))
        grid.Add(all_records_btn, wx.GBPosition(2, 6))

        grid.Add(ok_btn, wx.GBPosition(3, 11))
        grid.Add(close_btn, wx.GBPosition(3, 12))

        panel.SetSizer(grid, wx.EXPAND | wx.ALIGN_CENTER)
        self.makeMenuBar()
        self.Show(True)

    def makeMenuBar(self):
        fileMenu = wx.Menu()
        exitItem = fileMenu.Append(wx.ID_EXIT)

        menuBar = wx.MenuBar()
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)

    # callbacks/controller functions
    def OnExit(self, event):
        self.Close(True)

    def OnGetRecord(self, event):
        idCtrl = self.FindWindow(ID_CTRL)
        record_id = idCtrl.GetValue()
        record = self.GetRecord(record_id)
        wx.MessageBox(
            f"""
            ID: {record[0]}
            Brand: {record[1]}
            Model: {record[2]}
            Price: {record[3]}
            Count: {record[4]}
            """, f"Record #{record_id}: {record[1]} {record[2]}",
            wx.OK|wx.ICON_INFORMATION)
        print(record)

    def OnGenerateReport(self, event):
        pass

    def OnGetAll(self, event):
        pass

    # model functions
    def GetRecord(self, identifier):
        assert identifier > 0, 'id must be a positive integer'
        response = self.tarantool.eval(f'return box.space.products:get({identifier})')
        return response[0]

    def ListRecords(self, *args, **kwargs):
        return self.tarantool.eval(f'return box.space.products:select()')[0]

    def Report(self, *args, **kwargs):
        pass

if __name__ == '__main__':
    app = wx.App()
    frm = HelloFrame(None, title = 'Hello')
    app.MainLoop()
