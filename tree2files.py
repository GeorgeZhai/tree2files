from weasyprint import HTML
from weasyprint import CSS
from pprint import pprint
from time import sleep

import tinys3
import json
import os
import re
import sys



tmpdir = 'tmp'
rootdir = 'tmproot'
dirarray = ['','','','','','','','','','','','','','']


filecount = 0

with open('tree.txt') as f:
	for line in f:
		mlv = re.search('(^.+?)([^\s\|]+[^\r\n]*)',line)
		slv = mlv.group(1) if mlv is not None else ''
		lv = len(slv)/4
		md1 = re.search('(?<=\+---)([^\s\|]+[^\r\n]*)',line)
		md2 = re.search('(?<=\\---)([^\s\|]+[^\r\n]*)',line)
		dir1 = md1.group(1) if md1 is not None else ''
		dir2 = md2.group(1) if md2 is not None else ''
		newdir = dir1 if len(dir1) > 0 else dir2
		filename = ''
		if len(newdir) > 0:
			dirarray[lv+1] = newdir
			lv = lv + 1
		else:
			fm = re.search('\| *([^\s\|]+[^\r\n]*)', line)
			filename = fm.group(1) if fm is not None else ''

		fullpath = rootdir
		if lv > 0:
			for i in range(1, lv):
				sd = dirarray[i]
				if len(sd) > 0:
					fullpath = fullpath+'/'+sd

		if len(filename) > 0:
			fullpathfname = fullpath + '/' + filename
			root,ext = os.path.splitext(fullpathfname)
			if ext in ['.pdf', '.PDF']:
   				CSS(string='@page { size: A3; margin: 1cm }')
				html_str = '''
				    <h1>Auto Generated Dummy pdfs</h1>
				    <p>this is not a standard<p>
				    <p>file name: <p>
				    <p>
				''' + filename + ''' <p>
				'''
				HTML(string=html_str).write_pdf( tmpdir + '/' + filename)
			else:
				os.system('cp \'' + tmpdir + '/' + 'defaulttempfile\'' + ' \'' + tmpdir + '/' + filename + '\'')



			oscommstr1 = 'mkdir -p '+ '\''+ fullpath + '\''
			oscommstr2 = 'cp \''+ tmpdir + '/' + filename + '\' \'' + fullpathfname + '\''


			sys.stdout.write('\r')


			os.system(oscommstr1)
			os.system(oscommstr2)
			os.remove(tmpdir + '/' + filename)

			filecount = filecount + 1
			sys.stdout.write(str(filecount))
			sys.stdout.flush()




# Creating a simple connection
#conn = tinys3.Connection(confdata["accessKeyId"],confdata["secretAccessKey"])

# Uploading a single file
#f = open('tmp/'+ filename,'rb')
# conn.upload('tmp/'+ filename,f,confdata["bucket"])

#f .close()
#os.remove('tmp/'+ filename)

