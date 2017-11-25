
class CategoryEnum:
	fileProp = 1
	layerInfo = 2
	label = {fileProp: "File Properties", layerInfo: "Layer Information"}
	
class PropertyEnum:
	fileName = 11
	sliceTime = 15
	printEstimate = 16
	
	layerNum = 21
	minMaxXY = 22
	filamentUsed = 23
	filamentUsed0 = 230
	filamentUsed1 = 231
	filamentUsed2 = 232
	filamentUsed3 = 233
	gCodeRange = 24
	layerPrintTime = 25
	timeUntil = 26
	layerHeight = 27
	label = {fileName : "File Name", sliceTime: "Slice Time", printEstimate: "Print Time Estimate", layerHeight : "Layer Height",
			layerNum: "Layer Number", minMaxXY: "Min/Max X/Y", filamentUsed: "Filament Used", gCodeRange: "G Code Lines", layerPrintTime: "Layer Print Time", timeUntil: "Time Until",
			filamentUsed0: "Filament Used Tool 0:", filamentUsed1: "              Tool 1:", filamentUsed2: "              Tool 2:", filamentUsed3: "              Tool 3:"}
