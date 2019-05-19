#!/usr/bin/env python
import requests
import os
import io

TIMEOUT = 0.3

class PrintHead:
	def __init__(self, printer):
		self.printer = printer
		self.url = "http://%s/api/printer/printhead" % self.printer.getIpAddr()
		self.header = {"X-Api-Key": self.printer.getApiKey()}
			
	def jog(self, vector, absolute=False, speed=None, to=TIMEOUT):
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
		
		r = requests.post(self.url, headers=self.header, json=payload, timeout=to)
		return r.status_code
	
	def home(self, xyz, to=TIMEOUT):
		axes = []
		if xyz[0]:
			axes.append("x")
		if xyz[1]:
			axes.append("y")
		if xyz[2]:
			axes.append("z")
			
		payload = { "command": "home", "axes": axes }
		r = requests.post(self.url, headers=self.header, json=payload, timeout=to)
		return r.status_code
	
	def feedrate(self, factor, to=TIMEOUT):
		payload = { "command": "feedrate", "factor": factor }
		r = requests.post(self.url, headers=self.header, json=payload, timeout=to)
		return r.status_code
	
class Tool:
	def __init__(self, printer):
		self.printer = printer
		self.url = "http://%s/api/printer/tool" % self.printer.getIpAddr()
		self.header = {"X-Api-Key": self.printer.getApiKey()}
	
	def state(self, to=TIMEOUT):
		r = requests.get(self.url, data={}, headers=self.header, timeout=to)
		return r.status_code, r.json()
	
	def target(self, targetVals, to=TIMEOUT):
		targets = {}
		for t in targetVals.keys():
			targets["tool%s" % t] = targetVals[t]
			
		payload = { "command": "target", "targets": targets }
		r = requests.post(self.url, headers=self.header, json=payload, timeout=to)
		return r.status_code
	
	def offset(self, offsetVals, to=TIMEOUT):
		offsets = {}
		for i in range(len(offsetVals)):
			offsets["tool%d" % i] = offsetVals[i]
			
		payload = { "command": "offset", "offsets": offsets }
		r = requests.post(self.url, headers=self.header, json=payload, timeout=to)
		return r.status_code
	
	def select(self, toolx, to=TIMEOUT):
		payload = { "command": "select", "tool": "tool%d" % toolx }
		r = requests.post(self.url, headers=self.header, json=payload, timeout=to)
		return r.status_code
	
	def extrude(self, length, to=TIMEOUT):
		payload = { "command": "extrude", "amount": length }
		r = requests.post(self.url, headers=self.header, json=payload, timeout=to)
		return r.status_code
	
	def retract(self, length, to=TIMEOUT):
		payload = { "command": "extrude", "amount": -length }
		r = requests.post(self.url, headers=self.header, json=payload, timeout=to)
		return r.status_code

class Bed:
	def __init__(self, printer):
		self.printer = printer
		self.url = "http://%s/api/printer/bed" % self.printer.getIpAddr()
		self.header = {"X-Api-Key": self.printer.getApiKey()}
	
	def state(self, to=TIMEOUT):
		r = requests.get(self.url, data={}, headers=self.header, timeout=to)
		try:
			rv = r.json()
		except:
			rv = None
		return r.status_code, rv
	
	def target(self, targetVal, to=TIMEOUT):
		payload = { "command": "target", "target": targetVal }
		r = requests.post(self.url, headers=self.header, json=payload, timeout=to)
		return r.status_code
	
	def offset(self, offsetVal, to=TIMEOUT):
		payload = { "command": "offset", "offset": offsetVal }
		r = requests.post(self.url, headers=self.header, json=payload, timeout=to)
		return r.status_code

class Job:
	def __init__(self, printer):
		self.printer = printer
		self.url = "http://%s/api/job" % self.printer.getIpAddr()
		self.header = {"X-Api-Key": self.printer.getApiKey()}
	
	def state(self, to=TIMEOUT):
		r = requests.get(self.url, data={}, headers=self.header, timeout=to)
		try:
			rv = r.json()
		except:
			rv = None
		return r.status_code, rv

	def start(self, to=TIMEOUT):
		payload = { "command": "start" }
		r = requests.post(self.url, json=payload, headers=self.header, timeout=to)
		return r.status_code

	def cancel(self, to=TIMEOUT):
		payload = { "command": "cancel" }
		r = requests.post(self.url, json=payload, headers=self.header, timeout=to)
		return r.status_code

	def restart(self, to=TIMEOUT):
		payload = { "command": "restart" }
		r = requests.post(self.url, json=payload, headers=self.header, timeout=to)
		return r.status_code

	def pause(self, to=TIMEOUT):
		payload = { "command": "pause", "action": "pause" }
		r = requests.post(self.url, json=payload, headers=self.header, timeout=to)
		return r.status_code

	def resume(self, to=TIMEOUT):
		payload = { "command": "pause", "action": "resume" }
		r = requests.post(self.url, json=payload, headers=self.header, timeout=to)
		return r.status_code
	
class GFile:
	def __init__(self, printer):
		self.printer = printer
		self.url = "http://%s/api/files" % self.printer.getIpAddr()
		self.header = {"X-Api-Key": self.printer.getApiKey()}
		
	def uploadFile(self, fn, n=None, to=TIMEOUT):
		if n is None:
			bn = os.path.basename(fn)
		else:
			bn = n
			
		location = "/local"

		files = {'file': (bn, open(fn, 'rb'), 'application/octet-stream')}
		r = requests.post(self.url+location, files=files, headers=self.header, timeout=to)
		try:
			rv = r.json()
		except:
			rv = None
		return r.status_code, rv
		
	def uploadString(self, s, n, to=TIMEOUT):
		files = {'file': (n, io.StringIO(s), 'application/octet-stream')}
		location = "/local"
		r = requests.post(self.url+location, files=files, headers=self.header, timeout=to)
		try:
			rv = r.json()
		except:
			rv = None
		return r.status_code, rv
		
	def listFiles(self, local=True, sd=False, recursive=False, to=TIMEOUT):
		location = ""
		if local and not sd:
			location = "/local"
		elif sd and not local:
			location = "/sdcard"
			
		if recursive:
			location += "?recursive=true"
		
		try:	
			req = requests.get(self.url+location, headers=self.header, timeout=to)
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
	
	def downloadFile(self, url, to=TIMEOUT):
		req = requests.get(url, headers=self.header, timeout=to)
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
	
	def state(self, to=TIMEOUT):
		url = "http://%s/api/printer" % self.ipAddr
		r = requests.get(url, data={}, headers=self.header, timeout=to)
		try:
			rv = r.json()
		except:
			rv = None
		return r.status_code, rv
	
