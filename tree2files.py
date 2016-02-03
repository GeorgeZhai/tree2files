from weasyprint import HTML
from weasyprint import CSS
from pprint import pprint
from time import sleep

import tinys3
import json
import os
import re
import sys
import Queue
import threading
import urllib2
import time
from time import gmtime, strftime


# threading.stack_size(64*1024)



taskqueue = Queue.Queue()
qcount = Queue.Queue()
threads = []

# def worker():
#     while True:
#         item = q.get()
#         do_work(item)
#         q.task_done()




maxthread = 15
tmpdir = 'tmp'
rootdir = 'tmproot'
#max 15 level directories
dirarray = ['','','','','','','','','','','','','','','','']




# called by each thread, create file in tmproot
def createfile():
	# while taskqueue.qsize() > 0:
	while True:
		sp = taskqueue.get()
		fullpath = sp[0]
		filename = sp[1]

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

		os.system(oscommstr1)
		os.system(oscommstr2)
		os.remove(tmpdir + '/' + filename)
		taskqueue.task_done()
		#print (filename)






def displaycount():
	firstrun = True
	dc1 = 0
	dc2 = 0
	forcasthrs = 0
	ratemin = 0
#	while firstrun or c > 0:
	while True:
		c = taskqueue.qsize()
		if c < dc1 and dc1 < dc2:
			ratemin = (dc1 - c) * 6
			forcasthrs = (c/ratemin)/60
		dc2 = dc1
		dc1 = c
		print strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '  Threads: ' + str(len(threads)) + '  current queue length: '+ str(c) + '  Processing Rate per min: '+ str(ratemin) + '  forcast done in hrs: '+ str(forcasthrs)
		time.sleep(10)


dt = threading.Thread(target=displaycount)
threads.append(dt)
dt.daemon = True
dt.start()





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
			taskqueue.put([fullpath, filename])



for i in range(0,maxthread):
	t = threading.Thread(target=createfile)
	threads.append(t)
	t.daemon = True
	t.start()





taskqueue.join()   

print('-----------All done!---------------')







# Creating a simple connection
#conn = tinys3.Connection(confdata["accessKeyId"],confdata["secretAccessKey"])

# Uploading a single file
#f = open('tmp/'+ filename,'rb')
# conn.upload('tmp/'+ filename,f,confdata["bucket"])

#f .close()
#os.remove('tmp/'+ filename)

