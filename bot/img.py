# Class for image processing functions

import requests
from PIL import Image

def Fech(embed):
	file = requests.get(embed, stream = True)
	file.raw.decode_content = True
	
	return file.raw

def Mask(overlayFile, maskFile, file):

	im = Image.open(file).copy()

	overlay = Image.open(overlayFile).copy()
	overlay = overlay.resize(im.size)
	im.paste(overlay, (0,0), overlay)

	return im