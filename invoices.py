import sys
import os

from subprocess import check_output
from subprocess import CalledProcessError
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance

import pytesseract
import time
import random

IN_PATH = "/cygdrive/c/Documents and Settings/pgallagherjr/My Documents/Dropbox/invoices/Incoming/"
OUT_PATH = "/cygdrive/c/Documents and Settings/pgallagherjr/My Documents/Dropbox/invoices/Outgoing/"
DIGITS = ["1"	,"2"	,"3"	,"4"	,"5"	,"6"	,"7"	,"8"	,"9"	,"0"]	


def main():

	#Check if there are new files in "incoming" directory
	while True:
	
		#Wait patiently for new files to arrive
		#idle_loop()
	
		#convert those files to jpg
		#convert_pdfs()

		#OCR to find the invoice number and rename the pdf
		OCR()
		
		#move pdf to "outgoing" directory
		#move()
		
		#remove temp tiles JPEG Pages
		#cleanup()
		
		quit()
def idle_loop():
#Patiently wait for new files to arrive in the directory.
	print("\n\n\n\n\n================================\n\tWAITING\n==============================="	)
	s=""
	while True:
		print(check_output(["/usr/bin/ls", IN_PATH]).decode("ascii").split("\n").__len__())
		print(check_output(["/usr/bin/ls", IN_PATH]).decode("ascii").split("\n"))
	#	quit()

		if check_output(["/usr/bin/ls", IN_PATH]).decode("ascii").split("\n").__len__() == 4:
			time.sleep(5)
			continue
		print("found files")
		
		f = check_output(["/usr/bin/ls", IN_PATH]).decode("ascii").split("\n")
		for i in range(0, f.__len__()):
			if f[i] != "jpegs" and f[i] != "txt" and f[i] != "" and f[i] != "backup":
				return [IN_PATH, f[i]]
		
		
		
def convert_pdfs():
	print("\n\n\n\n\n================================\n\tCONVERTING\n===============================")

	
	dir = check_output(["/usr/bin/ls", IN_PATH]).decode("ascii").split("\n")
	
	
	firstline = "#!/bin/sh\n"

	cd = "cd \"%sbackup\"\n" % IN_PATH
	burs = ""
	cat = ""
	for i, each in enumerate(dir):
		print(each)
		if each == "jpegs" or each== "txt"or each == ""or each == "backup":
			continue
			
		cat = cat + " \"../" + each + "\""
		#burs = burs + "exec /usr/bin/pdftk \"../" + each + "\" burst \"" + each+"\n echo \" bursted " + each +"\""
	
	print(cat)

	rm = "rm doc_data.txt"
	cat = "exec /usr/bin/pdftk "+cat +" cat output " +"\"../out.pdf\"\n"
	burs = "exec /usr/bin/pdftk \"../out.pdf\" burst"
	bash_script = firstline + cd +  cat
			
	f=open(IN_PATH + "../burst1", 'w')
	
	f.write(bash_script)
	
	f.close()
	
	
	f=open(IN_PATH + "../burst2", 'w')
	
	f.write(firstline + cd + burs)
	
	f.close()
	

				

		
	try:
		check_output(["/bin/sh", "/cygdrive/c/Documents and Settings/pgallagherjr/My Documents/Dropbox/invoices/burst1"])
		check_output(["/bin/sh", "/cygdrive/c/Documents and Settings/pgallagherjr/My Documents/Dropbox/invoices/burst2"])
	except:
		print("Burst error")
	
	dir = check_output(["/usr/bin/ls", IN_PATH]).decode("ascii").split("\n")
		
	try:
		for each in dir:
			if each == "jpegs" or each== "txt"or each == ""or each == "backup":
				continue
			check_output(["/bin/rm", "/cygdrive/c/Documents and Settings/pgallagherjr/My Documents/Dropbox/invoices/Incoming/"+each])
		check_output(["/bin/rm", "/cygdrive/c/Documents and Settings/pgallagherjr/My Documents/Dropbox/invoices/Incoming/backup/doc_data.txt"])


	except:
		print("original file removal error")
	firstline = "#!/bin/sh\n"
	convert = ""
	for each in check_output(["/usr/bin/ls", IN_PATH+"backup"]).decode("ascii").split("\n"):
		#print("bbb"+ each)
		if each == "jpegs" or each== "txt"or each == "" or each == "backup":
			continue
		print(each)
		#template for a bash script that will run to convert each file one at a time.
		#this is truly a pain in the ass and all of this scripts-writing-scripts is the easiest way i can think of.
		convert = convert + "/usr/bin/convert -density 600x600 \"" + IN_PATH+"backup/"+each + "\" \"" + IN_PATH +"jpegs/" + each[:-4]+".jpg\"\n"
	
	
	bash_script = firstline + convert
			
	f=open(IN_PATH + "../conv", 'w')
	
	f.write(bash_script)
	
	f.close()
			
	#input("...")
	
	try:
		check_output(["/bin/sh", "/cygdrive/c/Documents and Settings/pgallagherjr/My Documents/Dropbox/invoices/conv"])
	except CalledProcessError:
		print("conversion error on file %s" % each)

	try:
		check_output(["/usr/bin/rm", "/cygdrive/c/Documents and Settings/pgallagherjr/My Documents/Dropbox/invoices/conv"])
		pass
	except CalledProcessError:
		print("Warning: removal error")

def OCR():
	
	print("\n\n\n\n\n================================\n\tOCR-ING\n===============================")
	path = IN_PATH + "jpegs/"

	dir = check_output(["/usr/bin/ls", path]).decode("ascii").split("\n")
	print(dir)
	firstline = "#!/bin/sh\n"
	
	ocr = ""
	
	for each in dir:
		print(each)
		if each == "":
			continue
		
		j = 0
		a = 1
		img = Image.open(path + each)
		if upright(path, each, img) == False:
			img = img.rotate(180)
			print("rotating")
				
		box = (int(img.width * .53), int(img.height*.07), int(img.width*.62), int(img.height*.1))
		print("box")
		print(box)
		first = True
		#while True:
			
		img2 = img.crop(box)
		img2.save(path+"figuremeout.jpg")

		#img2=img
		img2 = img2.filter(ImageFilter.GaussianBlur(radius=2))

		enh = ImageEnhance.Contrast(img2)
		img2 = enh.enhance(6.0)
		enh = ImageEnhance.Sharpness(img2)
		img2 = enh.enhance(6.0)
		
		img2.save(path + "z"+each[:-4]+".jpg") 
		
		if not first:
			input("look at %s-2.jpg" % each)

           #another stupid bash script because python and cygwin is stupid.

		ocr = "/usr/bin/tesseract \"" + path + "z"+each[:-4]+".jpg" + "\" stdout > \"" + IN_PATH + "txt/"+ each[:-4] + ".txt\" \"letters\"\n"
		f=open(IN_PATH+"../ocrscript", "w")
		f.write(firstline+ocr)
		f.close()
		try:

			check_output(["/bin/sh", "/cygdrive/c/Documents and Settings/pgallagherjr/My Documents/Dropbox/invoices/ocrscript"])
		
		except CalledProcessError:
			print("OCR Error")
		
		
		try:
			check_output(["/usr/bin/rm", "/cygdrive/c/Documents and Settings/pgallagherjr/My Documents/Dropbox/invoices/ocrscript"])
		except CalledProcessError:
			print("File deletion Error")
			
		f =open(IN_PATH +  "txt/" +each[:-4] + ".txt", 'r')
		txt = f.read()
		print(txt)
		
		
	'''	if move(path, each, txt) == False:
			if first == False:
				break
			box =	(int(img.width * .53), int(img.height*.07), int(img.width*.62)-13, int(img.height*.1)-54)
			first = False
			continue
		else: 
			break
		
	if first == False:
		
		print("Couldn't find a valid name for this one.")'''
		
		
#print(pytesseract.image_to_string(img2))
	
	return
def upright(path,each, img):
	box = (int(img.width * .45), int(img.height*.94), int(img.width*.56), int(img.height*.97))
	print(box)
	
	
	img2 = img.crop(box)
	img2.save(path+"figuremeout.jpg")
	

	firstline = "#!/bin/sh\n"	
	ocr = "/usr/bin/tesseract \"" + path +"figuremeout.jpg" + "\" stdout > \"" + IN_PATH + "txt/"+ "figure.txt\"\n"
	f=open(IN_PATH+"../ocrscript", "w")
	f.write(firstline+ocr)
	f.close()
	try:

		check_output(["/bin/sh", "/cygdrive/c/Documents and Settings/pgallagherjr/My Documents/Dropbox/invoices/ocrscript"])
	
	except CalledProcessError:
		print("OCR Error")
			
	
	f =open(IN_PATH +  "txt/" +"figure.txt", 'r')
	txt = f.read()
	if txt.strip() == "POSTING COPY":
		return True
	return False


	
def move(path, each, txt):
	'''print("\n\n\n\n\n================================\n\tMOVING\n===============================")
	path = IN_PATH + "txt/"
	dir = check_output(["/usr/bin/ls", IN_PATH+"backup/"]).decode("ascii").split("\n")
	for each in dir:
	
	
	#if each == "jpegs" or each== "txt"or each == "" or each == "backup":
	#	continue
	print(each)
	f =open(path +each[:-4] + ".txt", 'r')

	txt = f.read()'''
	

	'''row = 1	
	index = txt.__len__()
	#name = ""
	for i in range(0, txt.__len__()):
		#print(txt[i])
		if row == 6:
			index = i+1
			break
		if txt[i] in DIGITS:
			row+=1
			continue
		else:
			#print("reset")
			row=1
			continue'''
	savepath = OUT_PATH
	name = ""
	for i in range(0, txt.__len__()):
		if txt[i] in DIGITS:
			name = name+txt[i]
	try:
		if name[0] is not "4":
			name = name[name.find('4', name.find('4'))+1:]
	except IndexError:
		return False
	print(name)
	if name.__len__() > 11:
		return False
		
	else:
		print(name[-6:])
		name = name[-6:]
			
	print("Name: %s" % name)
	#input("...")	
		
	outdir = check_output(["/usr/bin/ls", OUT_PATH]).decode("ascii").split("\n")

	move = ""
	if name+".pdf" in outdir:
	
		firstline = "#!/bin/sh\n"
		move =  "/usr/bin/pdftk  \"" + IN_PATH+"backup/"+each[:-4] +  ".pdf\" \"" + OUT_PATH + name+".pdf\" cat output  \""+ OUT_PATH + name+ "2.pdf\"\n"	 	
		rm = "/usr/bin/rm \"" + OUT_PATH + name+".pdf\"\n"
		ren = "/usr/bin/mv \"" + OUT_PATH + name+"2.pdf\" \"" + OUT_PATH + name+".pdf\""
		bash_script = firstline + move + rm + ren
				
		f=open(IN_PATH + "../move", 'w')
		
		f.write(bash_script)
		
		f.close()
		
		try:
			check_output(["/bin/sh", "/cygdrive/c/Documents and Settings/pgallagherjr/My Documents/Dropbox/invoices/move"])
		except CalledProcessError:
			print("merge error")
			
	else:
		try:	
			check_output(["/usr/bin/cp", IN_PATH +"backup/" + each, savepath + name + ".pdf" ])		
		except CalledProcessError:
			print("moving Error")
			
		
	'''try:
		check_output(["/usr/bin/rm", path+each[:-4]+".txt"])			
		pass
	except CalledProcessError:
		print("File Deletion Error")'''
			
		
def cleanup():
	
	#remove jpeg pages
	try:
		dir =  check_output(["/usr/bin/ls", IN_PATH+"jpegs/"]).decode("ascii").split("\n")
		for each in dir:
			check_output(["/usr/bin/rm", IN_PATH+"jpegs/"+each])
			
			
		dir =  check_output(["/usr/bin/ls", IN_PATH+"txt/"]).decode("ascii").split("\n")
		for each in dir:
			check_output(["/usr/bin/rm", IN_PATH+"txt/"+each])	
		
		dir =  check_output(["/usr/bin/ls", IN_PATH+"backup/"]).decode("ascii").split("\n")
		for each in dir:
			check_output(["/usr/bin/rm", IN_PATH+"backup/"+each])	
			
	except CalledProcessError:
		print("Cleanup Error")
		

	
	
main()