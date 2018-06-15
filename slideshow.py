import os, sys
from tkinter import Tk, Label
from PIL import Image, ImageTk
import argparse

class ArgsContainer:
	def __init__(self, args):
		self.args = args
		self.filePaths = args['filePaths'][0]
		self.transitionTime = int(args['transition'] * 1000)
		self.stopTime = args['stopTime'] * 1000
		self.goToNextDir = args['goToNextDir']
	
	
class PicLister:
	def __init__(self, filePaths):	
		self.filePaths = self.formatAsDirString(filePaths)
		self.picListings = self.generateListings()
	
		
	def	formatAsDirString(self, filePaths):
		
		for i in range(0, len(filePaths)):
			if os.path.isdir(filePaths[i]):
				if filePaths[i][-1] != '/':
					filePaths[i] += '/'
			else:
				if os.path.isfile(filePaths[i]):
					print("Error: {} should be a directory.".format(filePaths[i]))
				else:
					print("Error: {} not found.".format(filePaths[i]))
				sys.exit()
		
		return filePaths


	def generateListings(self):
		picTypes = [".gif", ".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
		dirListings = []
		picListings = []

		for p in self.filePaths:
			dirListings.append(os.listdir(p))	
			picList = []
			for item in dirListings[-1]:
				ext = os.path.splitext(item)[1]
				if ext.lower() in picTypes:
					picList.append(p + item)
					
			if picList:
				picListings.append(picList)
			else:
				print("Error: directory {} has no image files.".format(p))
				sys.exit()	
				
		return picListings
			
class SlideshowData:
	def __init__(self, picList):
		self.slides = picList
		self.numSlides = len(picList)
		self.maxIndex = self.numSlides - 1
		self.isStart = True
		self.slideCounter = 0
		
	
	def actionWillLoop(self, direction):
		if direction == 'increment':			
			return self.slideCounter == self.maxIndex
			
		elif direction == 'decrement':
			return self.slideCounter == 0
		
		else:
			raise ValueError("Only increment and decrement commands allowed.")
	
			
	def currentSlide(self):
		return self.slides[self.slideCounter]
	
	
	def firstSlide(self):
		self.slideCounter = 0
		return self.slides[self.slideCounter]
		
		
	def lastSlide(self):
		self.slideCounter = self.maxIndex
		return self.slides[self.slideCounter]
	
	
	def nextSlide(self):
		self.incrementCounter()
		return self.slides[self.slideCounter]
	
	
	def previousSlide(self):
		self.decrementCounter()
		return self.slides[self.slideCounter]
		
	
	def decrementCounter(self):
		self.slideCounter = (self.slideCounter - 1) % self.numSlides
		
	
	def getCounter(self):
		return self.slideCounter
		
				
	def incrementCounter(self):
		self.slideCounter = (self.slideCounter + 1) % self.numSlides
	
	
	def setCounter(self, counter):
		self.slideCounter = counter
	
	
	
class SlideshowModel:
	def __init__(self, picListings):
		self.slideshows = []
		self.slideshowCounter = 0
		
		for p in picListings:
			mySlideData = SlideshowData(p)
			self.slideshows.append(mySlideData)
	
		self.numSlideshows = len(picListings)
	
		
	def decrementCounter(self):
		self.slideshowCounter = (self.slideshowCounter - 1) % self.numSlideshows
		
			
	def incrementCounter(self):
		self.slideshowCounter = (self.slideshowCounter + 1) % self.numSlideshows
	
		
	def getCounter(self):
		return self.slideshowCounter
	
		
	def setCounter(self, counter):
		self.slideshowCounter = counter
	
		
	def getIndexes(self):
		indexList = []
		
		for i in range(self.numSlideshows):
			indexList.append((i, self.slideshows[i].getCounter()))
			
		return indexList
	
	
	def setIndexes(self, indexList):
		for index in indexList:
			self.slideshows[index[0]].setCounter(index[1])
	
			
	def getCurrentSlide(self):
		slide = self.slideshows[self.slideshowCounter].currentSlide()	
		return slide
		
		
	def getNextSlide(self, goToNextDir):
		if self.slideshows[self.slideshowCounter].actionWillLoop('increment'):
			if goToNextDir:
				self.incrementCounter()
				slide = self.slideshows[self.slideshowCounter].firstSlide()
				return slide
		
		slide = self.slideshows[self.slideshowCounter].nextSlide()
		return slide
	
	
	def getPreviousSlide(self, goToNextDir):
		if self.slideshows[self.slideshowCounter].actionWillLoop('decrement'):
			if goToNextDir:
				self.decrementCounter()
				slide = self.slideshows[self.slideshowCounter].lastSlide()
				return slide
		
		slide = self.slideshows[self.slideshowCounter].previousSlide()
		return slide
		
	
	def getNextSlideshow(self):
		self.incrementCounter()
		return self.getCurrentSlide()
	
	
	def getPreviousSlideshow(self):
		self.decrementCounter()
		return self.getCurrentSlide()
		
	

class SlideshowView:
	def __init__(self, master):
		self.w, self.h = master.winfo_screenwidth(), master.winfo_screenheight()
		master.geometry("%dx%d+0+0" % (self.w, self.h))
		master.attributes('-fullscreen', True)
		master.focus_set()
		
		self.bgLabel = Label(master)
		self.bgLabel.configure(background='black')
		self.bgLabel.place(x=0,y=0,width=self.w, height=self.h)
	
		self.image = None
	
	
	def getViewHandle(self):
		return self.bgLabel
		
		
	def updateView(self, slideData):
		if self.image:
			self.image.close()
		self.image = Image.open(slideData)
		self.fitImageToScreen()
		tkpi = ImageTk.PhotoImage(self.image)
		self.bgLabel.image = tkpi
		self.bgLabel.configure(image=tkpi)
		
		
	def fitImageToScreen(self):
		im_width, im_height = self.image.size
		
		if (im_width > self.w) or (im_height > self.h):
			if im_width > im_height:
				im_height = int(im_height * (self.w / im_width))
				im_width = self.w
			else:
				im_width = int(im_width * (self.h / im_height))
				im_height = self.h
			
		self.image = self.image.resize((im_width, im_height), Image.ANTIALIAS)
	
			
		
class SlideshowControl:
	def __init__(self, clArgsContainer):
		self.args = clArgsContainer
		ssPicLister = PicLister(self.args.filePaths)
		
		self.root = Tk()
		self.view = SlideshowView(self.root)
		self.viewHandle = self.view.getViewHandle()
		self.model = SlideshowModel(ssPicLister.picListings)
		
		self.isSaved = False
		self.bindKBEvents()
	
		
	def bindKBEvents(self):
		self.root.bind('<Escape>', self.esc)
		self.root.bind('<Left>', self.previousSlideManual)
		self.root.bind('<Right>', self.nextSlideManual)
		self.root.bind('s', self.stopStartSlideshow)
		self.root.bind('v', self.saveCallback)
		self.root.bind('n', self.nextSlideshow)
		self.root.bind('p', self.previousSlideshow)
		
		
	def nextSlide(self):
		slideData = self.model.getNextSlide(self.args.goToNextDir)
		self.view.updateView(slideData)

		if self.activeSlideshow:
			self.activeSlideshow = self.viewHandle.after(self.args.transitionTime, self.nextSlide)
		
		
	def previousSlide(self):
		slideData = self.model.getPreviousSlide(self.args.goToNextDir)
		self.view.updateView(slideData)
		
		
	def runSlideshow(self):
		slideData = self.model.getCurrentSlide()
		self.view.updateView(slideData)
		self.activeSlideshow = self.viewHandle.after(self.args.transitionTime, self.nextSlide)
		
		self.setSlideshowTerminate()
		self.root.mainloop(0)
	
	
	def setSlideshowTerminate(self):
		if self.args.stopTime != 0:
			self.viewHandle.after(self.args.stopTime, self.quitSlideshow)
	
	
	def savePosition(self):
		self.savedCounter = self.model.getCounter()
		self.savedIndexes = self.model.getIndexes()
		self.isSaved = True
		
		
	def restorePosition(self):
		self.model.setIndexes(self.savedIndexes)
		self.model.setCounter(self.savedCounter)
		self.isSaved = False
		
		
		#Assumes handle has been checked by calling function	
	def startSlideshow(self, transitionTime):
		if self.isSaved == True:
			self.restorePosition()
			
		self.activeSlideshow = self.viewHandle.after(transitionTime, self.nextSlide)
			
			
		#Assumes handle has been checked by calling function	
	def stopSlideshow(self):
		self.viewHandle.after_cancel(self.activeSlideshow)
		self.activeSlideshow = None
	
		
	def quitSlideshow(self):
		self.root.destroy()
		sys.exit()
	
	
		#Keyboard Event callbacks
	def nextSlideManual(self, event):
		if self.activeSlideshow:
			self.stopSlideshow()
		
		if self.isSaved == False:
			self.savePosition()
			
		self.nextSlide()
	
	
	def previousSlideManual(self, event):
		if self.activeSlideshow:
			self.stopSlideshow()
		
		if self.isSaved == False:
			self.savePosition()
			
		self.previousSlide()
		
		
	def nextSlideshow(self, event):
		if self.activeSlideshow:
			self.stopSlideshow()
			
		if self.isSaved == True:
			self.restorePosition()
				
		slideData = self.model.getNextSlideshow()
		self.view.updateView(slideData)
		
		self.startSlideshow(self.args.transitionTime)
		
		
	def previousSlideshow(self, event):
		if self.activeSlideshow:
			self.stopSlideshow()

		if self.saved == True:
			self.restorePosition()
			
		slideData = self.model.getPreviousSlideshow()
		self.view.updateView(slideData)
		
		self.startSlideshow(self.args.transitionTime)
		
		
	def stopStartSlideshow(self, event):
		if self.activeSlideshow:
			self.stopSlideshow()	
		else:
			self.startSlideshow(0)
		
			
	def saveCallback(self, event):
		savePosition()
				
				
	def esc(self, event):
		self.quitSlideshow()	



def parserInit():
	desc = """
	Run a slideshow for as many folders as you like.	
	Press 'n' to go to the next folder in the list.
	Press 'p' to go to the previous folder in the list
	Press 's' to stop and start the slideshow.
	Press the left and right arrows to activate manual mode.
		The slideshow will save your position and return when
		you start again.
	Press 'v' to save a spot to return to when starting the
		slideshow again.
	Press 'Escape' to exit the application."""

	parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("filePaths",  action='append', help="Paths to picture folders", nargs='+', metavar=('paths'))
	parser.add_argument("-t", "--transition", help="Image transition time in seconds.\nDefault is 5 seconds.", metavar=('seconds'), type=float, default=5)
	parser.add_argument("-g", "--goToNextDir", help="Go to next slideshow after the last picture is reached.", action="store_true")
	parser.add_argument("-s", "--stopTime", help="Number of seconds until slideshow stops.\nSelect 0 if you don't want it to stop automatically.\nDefault is 1800 seconds (20 minutes)", type=int, default=1800)
	
	return vars(parser.parse_args())
	
	
def argsTestFunc(clArgsContainer):
	#ArgsContainer Test
	print(clArgsContainer.filePaths)
	print(clArgsContainer.transitionTime)
	print(clArgsContainer.stopTime)
	print(clArgsContainer.goToNextDir)
	
	#Piclist Test
	myPicLister = PicLister(clArgsContainer.filePaths)
	print(myPicLister.filePaths)
	print(myPicLister.picListings)
	
	#Slideshowdata Test
	mySlide = SlideshowData(myPicLister.picListings[0])
	print(mySlide.slides)
	slide = mySlide.nextSlide()
	print("slide is {} isloop is {}".format(slide.slide, slide.isLoop))
	slide = mySlide.nextSlide()
	print("slide is {} isloop is {}".format(slide.slide, slide.isLoop))


def ssTestFunc(slideshowCtrl):
	print("width is {}, height is {}".format(slideshowCtrl.view.w, slideshowCtrl.view.h))
	print("bgLabel handle is {}".format(slideshowCtrl.view.getViewHandle))
	
	
if __name__ == '__main__':
	myArgs = ArgsContainer(parserInit())
	
	#argsTestFunc(myArgs)
	
	#Slideshow Test	
	mySlideshow = SlideshowControl(myArgs)
	mySlideshow.runSlideshow()
