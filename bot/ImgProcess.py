from PIL import Image


class ImgProcess:
	def __init__(self, file, overlayFile, maskFile):
		self.file = file
		self.maskFile = maskFile
		self.overlayFile = overlayFile

	def process(self):

		im = Image.open(self.file).copy()

		overlay = Image.open(self.overlayFile).copy()
		overlay = overlay.resize(im.size)
		mask = Image.open(self.maskfile).convert('L').copy().resize(im.size)
		overlay.putalpha(mask)# apply mask
		im.paste(overlay, (0,0), overlay)
		