#!/usr/bin/python
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



taskqueue = Queue.Queue()
qcount = Queue.Queue()
threads = []
threadevent = []

# Ture on testmode will reduce 1 thread every 100 sec to test out the best thread number
testmode = False

# Limitation to total file numbers
queuelimit = 5000000

# maximum create file thread
maxthread = 2

#Template folder
tmpdir = 'tmp'

#temporary root location
rootdir = 'tmproot'

#max 30 level directories
dirarray = ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']




# called by each thread, create file in tmproot
def createfile(dd, eventindex):
	# while taskqueue.qsize() > 0:
	# while True:
	if threadevent[eventindex]:
		print 'Thread started --------, I am createfile thread:  ' + str(eventindex)
	currentfullpath = ''
	while threadevent[eventindex]:
		sp = taskqueue.get()
		fullpath = sp[0]
		filename = sp[1]
		if currentfullpath != fullpath:
			currentfullpath = fullpath
			oscommstr1 = 'mkdir -p '+ '\''+ fullpath + '\''
			os.system(oscommstr1)

		fullpathfname = fullpath + '/' + filename
		root,ext = os.path.splitext(fullpathfname)

		if ext in ['.pdf', '.PDF']:
			tfn = tmpdir + '/tf' + str(eventindex)
			text_file = open(tfn, "w")
			text_file.write("Auto Generated Dummy pdfs, filename: %s   ." %filename)
			text_file.close()
			os.system('./lib/pyText2pdf.py \'' + tfn + '\' -o \'' + fullpathfname + '\' >/dev/null')
			os.remove(tfn)

			# CSS(string='@page { size: A3; margin: 1cm }')
			# html_str = '''
			#     <h1>Auto Generated Dummy pdfs</h1>
			#     <p>this is not a standard<p>
			#     <p>file name: <p>
			#     <p>
			# ''' + filename + ''' <p>
			# '''
			# HTML(string=html_str).write_pdf( tmpdir + '/' + filename)

		else:
			# os.system('cp \'' + tmpdir + '/' + 'defaulttempfile\'' + ' \'' + tmpdir + '/' + filename + '\'')
			os.system('cp \'' + tmpdir + '/' + 'defaulttempfile\'' + ' \'' + fullpathfname + '\'')


		# oscommstr1 = 'mkdir -p '+ '\''+ fullpath + '\''
		# os.system(oscommstr1)

		# oscommstr2 = 'cp \''+ tmpdir + '/' + filename + '\' \'' + fullpathfname + '\''
		# os.system(oscommstr2)
		# os.remove(tmpdir + '/' + filename)

		taskqueue.task_done()
		#print (filename)
	if threadevent[eventindex] == False:
		print 'Thread stopping--------, I was thread:  ' + str(eventindex)






def displaycount():
	firstrun = True
	dc1 = 0
	dc2 = 0
	t=0
	forcasthrs = 0
	keepalive = True
#	while firstrun or c > 0:
	while keepalive:
		c = taskqueue.qsize()
		ratemin = 1
		if c < dc1 and dc1 < dc2:
			ratemin = (dc1 - c) * 6
			forcasthrs = (c/ratemin)/60
		dc2 = dc1
		dc1 = c
		activeth = threadevent.count(True)

		print strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '  Threads: ' + str(activeth) + '  current queue : '+ str(c) + '  Processed per min: '+ str(ratemin) + '  done in hrs: '+ str(forcasthrs)
		time.sleep(10)
		t=t+1
		st = int(t/10) - 1

		if activeth < 1 and dc2 > 0:
			keepalive = False

		if st >= 0 and st < maxthread and testmode:
			if threadevent[st]:
				threadevent[st]= False
				activeth = threadevent.count(True)
				print '===========================>>>stopping thread num:   ' + str(st) + '   current active threads: ' + str(activeth)
			if activeth < 1:
				keepalive = False
	if keepalive == False:
		print '++   >>>stopping dispay thread <<<   ++'







dt = threading.Thread(target=displaycount)
threads.append(dt)
dt.daemon = True
dt.start()




queuesize = taskqueue.qsize()

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
		if len(filename) > 0 and queuesize < queuelimit:
			taskqueue.put([fullpath, filename])
			queuesize = queuesize + 1

print 'File queue has been built total files: ' + str(queuesize) + '   now start create file worker threads:  '


for i in range(0,maxthread+0):
	threadevent.append(True)
	t = threading.Thread(target=createfile, args=(1,i))
	threads.append(t)
	t.daemon = True
	t.start()




for t in threads:
	t.join()

print('-----------All Threads finished --------------------')

# with taskqueue.mutex:
# 	taskqueue.queue.clear()

# taskqueue.join()   

# print('-----------All queue done!---------------')







# Creating a simple connection
#conn = tinys3.Connection(confdata["accessKeyId"],confdata["secretAccessKey"])

# Uploading a single file
#f = open('tmp/'+ filename,'rb')
# conn.upload('tmp/'+ filename,f,confdata["bucket"])

#f .close()
#os.remove('tmp/'+ filename)

