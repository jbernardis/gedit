import wx
import wx.propgrid as wxpg

import os
import inspect

cmdFolder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))

from propenums import CategoryEnum, PropertyEnum
from printstateenum import PrintState

catOrder = [CategoryEnum.fileProp, CategoryEnum.layerInfo]
propertyMap = {
		CategoryEnum.fileProp : [ 
			PropertyEnum.fileName, PropertyEnum.sliceTime, PropertyEnum.printEstimate],
		CategoryEnum.layerInfo : [
			PropertyEnum.layerNum, PropertyEnum.layerHeight, PropertyEnum.minMaxXY, PropertyEnum.filamentUsed, PropertyEnum.gCodeRange,
			PropertyEnum.layerPrintTime, PropertyEnum.timeUntil]
		}

toolMap = [ PropertyEnum.filamentUsed0, PropertyEnum.filamentUsed1, PropertyEnum.filamentUsed2, PropertyEnum.filamentUsed3 ]

class PropertiesDlg(wx.Frame):
	def __init__(self, parent, wparent, cb=None):
		wx.Frame.__init__(self, wparent, wx.ID_ANY, size=(500, 500))
		ico = wx.Icon(os.path.join(cmdFolder, "images", "propsico.png"), wx.BITMAP_TYPE_PNG)
		self.SetIcon(ico)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.parent = parent
		self.callback = cb
		self.fileName = None
		self.sdTargetfn = None
		self.nextruders = parent.settings.nextruders
		self.printStatus = PrintState.idle
		self.setTitle()

		pgFont = wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
		self.pg = pg = wxpg.PropertyGrid(self,
						style=wxpg.PG_PROP_READONLY |
							  wxpg.PG_TOOLBAR)

		pg.SetFont(pgFont)

		pg.SetCaptionBackgroundColour(wx.Colour(215, 255, 215))
		pg.SetCaptionTextColour(wx.Colour(0, 0, 0))
		pg.SetMarginColour(wx.Colour(215, 255, 215))
		pg.SetCellBackgroundColour(wx.Colour(255, 255, 191))
		pg.SetCellTextColour(wx.Colour(0, 0, 0))
		pg.SetCellDisabledTextColour(wx.Colour(0, 0, 0))
		pg.SetEmptySpaceColour(wx.Colour(215, 255, 215))
		pg.SetLineColour(wx.Colour(0, 0, 0))
		
		self.properties = {}

		lines = 0		
		for cat in catOrder:
			pg.Append(wxpg.PropertyCategory(CategoryEnum.label[cat]))
			lines += 1
			for k in propertyMap[cat]:
				if k == PropertyEnum.filamentUsed:
					for tx in range(self.nextruders):
						pgp = wxpg.StringProperty(PropertyEnum.label[toolMap[tx]],value="")
						pg.Append(pgp)
						lines += 1
						self.properties[toolMap[tx]] = pgp
						pg.DisableProperty(pgp)
				else:
					pgp = wxpg.StringProperty(PropertyEnum.label[k],value="")
					pg.Append(pgp)
					lines += 1
					self.properties[k] = pgp
					pg.DisableProperty(pgp)

		n = pg.GetRowHeight()
		dlgVsizer = wx.BoxSizer(wx.VERTICAL)
		dlgHsizer = wx.BoxSizer(wx.HORIZONTAL)
		dlgHsizer.AddSpacer(10)
		dlgHsizer.Add(pg, 1, wx.EXPAND)
		dlgHsizer.AddSpacer(10)

		dlgVsizer.AddSpacer(10)
		dlgVsizer.Add(dlgHsizer, 1, wx.EXPAND)
		dlgVsizer.AddSpacer(10)
		self.SetSizer(dlgVsizer)
		self.SetClientSize((600, n*lines+24))
		pg.SetSplitterLeft()
		
	def onClose(self, _):
		if self.callback is not None:
			self.callback()
			self.Destroy()
		
	def setTitle(self):
		if self.fileName is not None:
			s = "G Code File %s" % self.fileName
		else:
			s = ""
			
		self.SetTitle(s)
		
	def setProperty(self, pid, value):
		if pid == PropertyEnum.filamentUsed:
			for tx in range(self.nextruders):
				self.pg.SetPropertyValueString(self.properties[toolMap[tx]], str(value[tx]))
			
			return

		if pid not in self.properties.keys():
			print("Unknown property key: %s" % pid)
			return
		
		if pid == PropertyEnum.fileName:
			self.fileName = value
			self.setTitle()

		self.pg.SetPropertyValueString(self.properties[pid], str(value))
			
	def clearAllProperties(self):
		self.sdTargetfn = None
		for cat in propertyMap.keys():
			for prop in propertyMap[cat]:
				self.pg.SetPropertyValueString(self.properties[prop], "")
