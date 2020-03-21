import webbrowser, os.path

def strToFile(text, filename):
	"""Write a file with the given name and the given text."""
	output = open(filename,"w")
	output.write(text)
	output.close()

def browseLocal(webpageText, filename='tempBrowseLocal.html'):
	'''Start your webbrowser on a local file containing the text
	with given filename.'''
	strToFile(webpageText, filename)
	webbrowser.open("file:///" + os.path.abspath(filename)) #elaborated for Mac