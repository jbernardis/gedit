#!/usr/bin/env python
import pprint

import requests
import os
import StringIO

class PrintHead:
	def __init__(self, printer):
		self.printer = printer
		self.url = "http://%s/api/printer/printhead" % self.printer.getIpAddr()
		self.header = {"X-Api-Key": self.printer.getApiKey()}
			
	def jog(self, vector, absolute=False, speed=None):
		x = 0
		y = 0
		z = 0
		if len(vector) >= 1:
			x = vector[0]
			
		if len(vector) >= 2:
			y = vector[1]
			
		if len(vector) >= 3:
			z = vector[2]
			
		payload = {"command": "jog", "x": x, "y": y, "z": z, "absolute": absolute }
		if not speed is None:
			payload["speed"] = speed
		
		r = requests.post(self.url, headers=self.header, json=payload, timeout=0.1)
		return r.status_code
	
	def home(self, xyz):
		axes = []
		if xyz[0]:
			axes.append("x")
		if xyz[1]:
			axes.append("y")
		if xyz[2]:
			axes.append("z")
			
		payload = { "command": "home", "axes": axes }
		r = requests.post(self.url, headers=self.header, json=payload, timeout=0.1)
		return r.status_code
	
	def feedrate(self, factor):
		payload = { "command": "feedrate", "factor": factor }
		r = requests.post(self.url, headers=self.header, json=payload, timeout=0.1)
		return r.status_code
	
class Tool:
	def __init__(self, printer):
		self.printer = printer
		self.url = "http://%s/api/printer/tool" % self.printer.getIpAddr()
		self.header = {"X-Api-Key": self.printer.getApiKey()}
	
	def state(self):
		r = requests.get(self.url, data={}, headers=self.header, timeout=0.1)
		return r.status_code, r.json()
	
	def target(self, targetVals):
		targets = {}
		for t in targetVals.keys():
			targets["tool%s" % t] = targetVals[t]
			
		payload = { "command": "target", "targets": targets }
		r = requests.post(self.url, headers=self.header, json=payload, timeout=0.1)
		return r.status_code
	
	def offset(self, offsetVals):
		offsets = {}
		for i in range(len(offsetVals)):
			offsets["tool%d" % i] = offsetVals[i]
			
		payload = { "command": "offset", "offsets": offsets }
		r = requests.post(self.url, headers=self.header, json=payload, timeout=0.1)
		return r.status_code
	
	def select(self, toolx):
		payload = { "command": "select", "tool": "tool%d" % toolx }
		r = requests.post(self.url, headers=self.header, json=payload, timeout=0.1)
		return r.status_code
	
	def extrude(self, length):
		payload = { "command": "extrude", "amount": length }
		r = requests.post(self.url, headers=self.header, json=payload, timeout=0.1)
		return r.status_code
	
	def retract(self, length):
		payload = { "command": "extrude", "amount": -length }
		r = requests.post(self.url, headers=self.header, json=payload, timeout=0.1)
		return r.status_code

class Bed:
	def __init__(self, printer):
		self.printer = printer
		self.url = "http://%s/api/printer/bed" % self.printer.getIpAddr()
		self.header = {"X-Api-Key": self.printer.getApiKey()}
	
	def state(self):
		r = requests.get(self.url, data={}, headers=self.header, timeout=0.1)
		try:
			rv = r.json()
		except:
			rv = None
		return r.status_code, rv
	
	def target(self, targetVal):
		payload = { "command": "target", "target": targetVal }
		r = requests.post(self.url, headers=self.header, json=payload, timeout=0.1)
		return r.status_code
	
	def offset(self, offsetVal):
		payload = { "command": "offset", "offset": offsetVal }
		r = requests.post(self.url, headers=self.header, json=payload, timeout=0.1)
		return r.status_code

class Job:
	def __init__(self, printer):
		self.printer = printer
		self.url = "http://%s/api/job" % self.printer.getIpAddr()
		self.header = {"X-Api-Key": self.printer.getApiKey()}
	
	def state(self):
		r = requests.get(self.url, data={}, headers=self.header, timeout=0.1)
		try:
			rv = r.json()
		except:
			rv = None
		return r.status_code, rv

	def start(self):
		payload = { "command": "start" }
		r = requests.post(self.url, json=payload, headers=self.header, timeout=0.1)
		return r.status_code

	def cancel(self):
		payload = { "command": "cancel" }
		r = requests.post(self.url, json=payload, headers=self.header, timeout=0.1)
		return r.status_code

	def restart(self):
		payload = { "command": "restart" }
		r = requests.post(self.url, json=payload, headers=self.header, timeout=0.1)
		return r.status_code

	def pause(self):
		payload = { "command": "pause", "action": "pause" }
		r = requests.post(self.url, json=payload, headers=self.header, timeout=0.1)
		return r.status_code

	def resume(self):
		payload = { "command": "pause", "action": "resume" }
		r = requests.post(self.url, json=payload, headers=self.header, timeout=0.1)
		return r.status_code
	
class GFile:
	def __init__(self, printer):
		self.printer = printer
		self.url = "http://%s/api/files" % self.printer.getIpAddr()
		self.header = {"X-Api-Key": self.printer.getApiKey()}
		
	def uploadFile(self, fn, n=None):
		if n is None:
			bn = os.path.basename(fn)
		else:
			bn = n
			
		location = "/local"

		files = {'file': (bn, open(fn, 'rb'), 'application/octet-stream')}
		r = requests.post(self.url+location, files=files, headers=self.header, timeout=5)
		try:
			rv = r.json()
		except:
			rv = None
		return r.status_code, rv
		
	def uploadString(self, s, n):
		files = {'file': (n, StringIO.StringIO(s), 'application/octet-stream')}
		location = "/local"
		r = requests.post(self.url+location, files=files, headers=self.header, timeout=5)
		try:
			rv = r.json()
		except:
			rv = None
		return r.status_code, rv
		
	def listFiles(self, local=True, sd=False, recursive=False):
		location = ""
		if local and not sd:
			location = "/local"
		elif sd and not local:
			location = "/sdcard"
			
		if recursive:
			location += "?recursive=true"
		
		try:	
			req = requests.get(self.url+location, headers=self.header, timeout=0.1)
		except:
			return None
		
		if req.status_code >= 400:
			return None
		
		finfo = req.json()
		if "files" not in finfo.keys():
			return []
		
		fl = finfo["files"]
		result = []
		for f in fl:
			if "name" in f.keys():
				if "refs" in f.keys() and "download" in f["refs"].keys():
					result.append((f["name"], f["refs"]["download"]))
				else:
					result.append((f["name"], None))
			
		return result
	
	def downloadFile(self, url):
		req = requests.get(url, headers=self.header, timeout=5)
		try:
			rv = req.text
		except:
			rv = None
			
		return req.status_code, rv
			

class PrinterServer:
	def __init__(self, apiKey, ipAddr):
		self.apiKey = apiKey
		self.ipAddr = ipAddr
		self.header = {"X-Api-Key": self.apiKey}
		self.printHead = PrintHead(self)
		self.tool = Tool(self)
		self.bed = Bed(self)
		self.job = Job(self)
		self.gfile = GFile(self)
		
	def getIpAddr(self):
		return self.ipAddr
	
	def getApiKey(self):
		return self.apiKey
	
	def state(self):
		url = "http://%s/api/printer" % self.ipAddr
		r = requests.get(url, data={}, headers=self.header, timeout=0.1)
		try:
			rv = r.json()
		except:
			rv = None
		return r.status_code, rv
	

	

# def do2():
# 	url = "%s/api/files" % urlPrefix
# 	print "sending request"
# 	req = requests.get(url, data=data, headers=headers)
# 	print "back from sending request"
# 	pprint.pprint(req)
# 	pprint.pprint(req.json())
# 
# 
# #requests.post('http://192.168.123.102/api/files/local', files={'file': open(sys.argv[1], 'rb')}, headers={'Host': '192.168.123.102', 'X-Api-Key': 'XXXXXXXXXXX'})
# def do3():
# 	fn = "test.gcode"
# 	files = {'file': ('test.gcode', open(fn, 'rb'), 'application/octet-stream')}
# 	url = "%s/api/files/local" % urlPrefix
# 	req = requests.post(url, files=files, headers=headers)
# 	pprint.pprint(req)
# 	pprint.pprint(req.json())
	

# ApiKeys = { "dbot" : "C01B6FFBFE8747EA80AACF809F7F7A04"}
# IPAddrs = { "dbot" : "192.168.1.190"}
# pname = "dbot"
# 
# ps = PrinterServer(ApiKeys[pname], IPAddrs[pname])
# 
# #ps.printHead.jog((50, 50, 0), speed=900)
# #ps.printHead.home(True, True, False)
# 
# rc, j = ps.state()
# print "status code: ", rc
# pprint.pprint(j)
# 
# rc, j = ps.tool.state()
# print "status code: ", rc
# pprint.pprint(j)
# 
# rc, j = ps.bed.state()
# print "status code: ", rc
# pprint.pprint(j)
# 
# rc, j = ps.job.state()
# print "status code: ", rc
# pprint.pprint(j)


