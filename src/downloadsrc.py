import wx
BUTTONDIM = (48, 48)

class DownloadSourceDlg(wx.Dialog):
	def __init__(self, parent, pname, ps):
		def cmpFlst(a, b):
			return cmp(a[0], b[0])
		
		wx.Dialog.__init__(self, parent, wx.ID_ANY, "Download from %s" % pname)
		
		self.parent = parent
		self.pname = pname
		self.ps = ps

		sizer = wx.BoxSizer(wx.VERTICAL)
		btnsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		flst = ps.gfile.listFiles()
		if flst is None:
			wx.CallAfter(self.notConnected)
			return
		
		if len(flst) == 0:
			wx.CallAfter(self.noDownloads)
			return
		
		self.flist = sorted(flst, cmpFlst)
		
		fl = [x[0] for x in self.flist]
		self.ch = wx.Choice(self, wx.ID_ANY, choices=fl, size=(300, -1))
		self.ch.SetSelection(0)
		
		sizer.AddSpacer(20)
		sizer.Add(wx.StaticText(self, wx.ID_ANY, "Choose a file:"),
				0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.LEFT, 10)
		sizer.Add(self.ch, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT|wx.RIGHT, 10)
		sizer.AddSpacer(20)
	
		btn = wx.BitmapButton(self, wx.ID_ANY, self.parent.images.pngOk, size=BUTTONDIM)
		btn.SetToolTip("Download")
		btnsizer.Add(btn)
		self.Bind(wx.EVT_BUTTON, self.onOk, btn)
		
		btnsizer.AddSpacer(30)

		btn = wx.BitmapButton(self, wx.ID_ANY, self.parent.images.pngCancel, size=BUTTONDIM)
		btn.SetToolTip("Cancel Download")
		btnsizer.Add(btn)
		self.Bind(wx.EVT_BUTTON, self.onCancel, btn)

		sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)
		sizer.AddSpacer(20)

		self.SetSizer(sizer)
		sizer.Fit(self)
		
	def noDownloads(self):
		dlg = wx.MessageDialog(self, "There are no files to download from %s" % self.pname,
					"No Files Available", wx.OK | wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()

		self.EndModal(wx.ID_CANCEL)
		
	def notConnected(self):
		dlg = wx.MessageDialog(self, "Unable to connect to %s" % self.pname,
					"Unable to connect", wx.OK | wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()

		self.EndModal(wx.ID_CANCEL)
		
	def getFn(self):
		idx = self.ch.GetSelection()
		if idx == wx.NOT_FOUND:
			return None
			
		return self.flist[idx][0]
		
	def getUrl(self):
		idx = self.ch.GetSelection()
		if idx == wx.NOT_FOUND:
			return None
			
		return self.flist[idx][1]
		
	def onOk(self, evt):
		self.EndModal(wx.ID_OK)
	
	def onCancel(self, evt):
		self.EndModal(wx.ID_CANCEL)

