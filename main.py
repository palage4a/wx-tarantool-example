import tarantool
import wx
import os

ID_CTRL = 1

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MyFrame, self).__init__(*args, **kwargs)
        self.tarantool = tarantool.connect('localhost', 3301, user='admin', password='pass')
        panel = wx.Panel(self)

        main = wx.BoxSizer(wx.VERTICAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        spacer = wx.BoxSizer(wx.HORIZONTAL)
        footer = wx.BoxSizer(wx.HORIZONTAL)

        id_sizer = wx.BoxSizer(wx.HORIZONTAL)
        get_by_id_btn = wx.Button(panel, -1, 'get')
        self.Bind(wx.EVT_BUTTON, self.OnGetRecord, get_by_id_btn)
        report_btn = wx.Button(panel, -1, 'report')
        self.Bind(wx.EVT_BUTTON, self.OnGenerateReport, report_btn)
        all_report_btn = wx.Button(panel, -1, 'all')
        self.Bind(wx.EVT_BUTTON, self.OnAllReport, all_report_btn)

        id_sizer.Add(wx.SpinCtrl(panel, ID_CTRL), wx.ALIGN_CENTER|wx.ALL, 10)
        id_sizer.Add(get_by_id_btn, wx.ALIGN_CENTER|wx.ALL, 10)

        # footer
        ok_btn = wx.Button(panel, -1, 'ok')
        close_btn = wx.Button(panel, -1, 'Close')
        self.Bind(wx.EVT_BUTTON, self.OnExit, close_btn)
        self.Bind(wx.EVT_BUTTON, self.OnExit, ok_btn)

        vbox.Add(id_sizer, wx.ALIGN_CENTER, 10)
        vbox.Add(report_btn, wx.ALIGN_CENTER, 10)
        vbox.Add(all_report_btn, wx.ALIGN_CENTER)

        footer.Add(ok_btn, wx.RIGHT | wx.BOTTOM, 10)
        footer.Add(close_btn, wx.RIGHT | wx.BOTTOM, 10)

        spacer.Add(wx.Panel(panel))

        main.Add(vbox, 1, wx.ALIGN_CENTER)
        main.Add(spacer, 1, wx.EXPAND)
        main.Add(footer, 0 ,  wx.ALIGN_RIGHT | wx.BOTTOM | wx.RIGHT, 10)

        panel.SetSizer(main, wx.EXPAND | wx.ALIGN_CENTER)
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
            f"""ID: {record[0]}
            Brand: {record[1]}
            Model: {record[2]}
            Price: {record[3]}
            Count: {record[4]}""", f"Record #{record_id}: {record[1]} {record[2]}",
            wx.OK|wx.ICON_INFORMATION)

    # model functions
    def GetRecord(self, identifier):
        assert identifier > 0, 'id must be a positive integer'
        response = self.tarantool.eval(f'return box.space.products:get({identifier})')
        return response[0]

    def OnAllReport(self, *args, **kwargs):
        c_products = self.tarantool.eval(f'return box.space.products:count()')[0]
        c_orders = self.tarantool.eval(f'return box.space.orders:count()')[0]
        c_positions = self.tarantool.eval(f'return box.space.positions:count()')[0]
        c_customers = self.tarantool.eval(f'return box.space.customers:count()')[0]
        wx.MessageBox(f"""Products: {c_products}
        Orders: {c_orders}
        Positions: {c_positions}
        Customers: {c_customers}
        """, "Count of entities", wx.OK|wx.ICON_INFORMATION)

    def OnGenerateReport(self, *args, **kwargs):
        all_records = self.tarantool.eval(f'return box.space.products:select()')[0]
        count = 0 
        avg_prc = 0
        max_cnt = 0
        min_cnt = 1000
        sum_of_prices = 0
        for rcd in all_records:
            count = count + 1 
            sum_of_prices = sum_of_prices + rcd[3]
            if max_cnt < rcd[4]:
                max_cnt = rcd[4]
            if min_cnt > rcd[4]:
                min_cnt = rcd[4]
        avg_prc = sum_of_prices / count
        wx.MessageBox(
            f"""Count: {count}
            Average price: {avg_prc}
            Minimal count of the product: {min_cnt}
            Maximum count of the product: {max_cnt}
            Sum of prices: {sum_of_prices}""", f"Report",
            wx.OK|wx.ICON_INFORMATION)

if __name__ == '__main__':
    app = wx.App()
    frm = MyFrame(None, title = 'Mobile Shop')
    app.MainLoop()
