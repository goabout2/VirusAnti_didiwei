import os
import sys
import time
import json
import paramiko
import threading

#########
'''
mylock = threading.RLock()
remotepath = "/tmp/didiwei.sh"
localpath = "D:\\tool\\python_script\\samplescan\\sh\\top_check.sh"
command = "chmod 777 /tmp/didiwei.sh&&/tmp/didiwei.sh check"
removecommand = "rm -rf /tmp/didiwei.sh"
allresutlpath = "D:\\tool\\python_script\\samplescan\\sh\\all_result.txt"
targetresultpath = "D:\\tool\\python_script\\samplescan\\sh\\target_result.txt"

lincommand = "ls"
wincommand = "dir"
'''
#########

mylock = threading.RLock()

lindetectcommand = "uname -a"

linremotecorepath = "/tmp/didiwei"
linremotecfgpath = "/tmp/config.conf"
linlocalcorepath = ""
lincommand = "chmod 777 /tmp/didiwei&&/tmp/didiwei"
linremovecommand = "rm -rf /tmp/didiwei&&rm -rf /tmp/config.conf"

windetectcommand = "notepad"

winremotecorepath = "C:\\didiwei"
winremotecfgpath = "C:\\config.conf"
winlocalcorepath = ""
wincommand = "C:\\didiwei"
winremovecommand = "del C:\\didiwei"

localcfgpath = ""

allresutlpath = ""
targetresultpath = ""

#init the global param
def initpath(lpath,apath,tpath):
	global localpath
	localpath = lpath
	global allresutlpath 
	allresutlpath = apath
	global targetresultpath
	targetresultpath = tpath

#get specify param of the path 
def getpath(osx):
	global linlocalcorepath
	global winlocalcorepath
	global allresutlpath
	global targetresultpath
	global localcfgpath
	scriptpath = os.path.split(os.path.realpath(sys.argv[0]))[0]
	print "the script is :" + scriptpath
	localcfgpath = os.path.join(scriptpath,"config.conf")
	if osx == 'Linux':
		linlocalcorepath = os.path.join(scriptpath,"lindidiwei")
	if osx == 'Windows':
		winlocalcorepath = os.path.join(scriptpath,"windidiwei")
	allresutlpath = os.path.join(scriptpath,"all_resutl.txt")
	targetresultpath = os.path.join(scriptpath,"target_result.txt")
	
	
#record the check result into the logfile 
def writefile(path,content):
	file = open(path,'a+')
	try:
		file.write(content)
	finally:
		file.close()

#uploader the checkmodule into the target machine
def uploader(ip,port,user,password,remotepath,localpath):
	t = paramiko.Transport((ip,22))     #the port must 22
	t.connect(username = user, password = password)
	sftp = paramiko.SFTPClient.from_transport(t)
	sftp.put(localpath,remotepath)
	t.close()

#download the resule of the checkmoduel
def download(ip,port,user,password,remotepath,localpath):
	t = paramiko.Transport((ip,22))
	t.connect(username = user,password = password)
	sftp = paramiko.SFTPClient.from_transport(t)
	sftp.get(remotepath,localpath)
	t.close()

#login run the checkmodule and return the result
def executecmd(ip,port,user,password,command):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ip,username = user,password = password)
	stdin,stdout,stderr = ssh.exec_command(command)
	return stdout.read()

def executecmd1(ip,port,user,password,command):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ip,port,username = user,password = password)
	stdin,stdout,stderr = ssh.exec_command(command)
	#print stdout.read()
	return stdout.read()

#detect the os
def detectos(list):
	result = executecmd(list[0],list[1],list[2],list[3],lindetectcommand)
	if 'Linux' in result:
		return 'Linux'

	result = executecmd(list[0],list[1],list[2],list[3],windetectcommand)
	if result is None:
		return 'Windows'

def launch(list,osx):
	if 'none' in osx:
		osx = detectos(list)

	getpath(osx)

	if 'Linux' in osx:
		print "target is linux"
		remotepath1 = linremotecorepath
		remotepath2 = linremotecfgpath
		localpath1 = linlocalcorepath
		localpath2 = localcfgpath
		command = lincommand
		removecommand = linremovecommand
	if 'Window' in osx:
		print "target is window"
		remotepath1 = winremotecorepath
		remotepath2 = winremotecfgpath
		localpath1 = winlocalcorepath
		localpath2 = localcfgpath
		command = wincommand
		removecommand = winremovecommand

	print "the remotepath1 is " + remotepath1
	print "the remotepath2 is " + remotepath2
	print "the localpath1 is " + localpath1
	print "the localpath2 is " + localpath2
	print "the command is " + command
	print "the removecommand is " + removecommand
	print "the linlocalcorepath is " + linlocalcorepath


	uploader(list[0],list[1],list[2],list[3],remotepath1,localpath1)
	time.sleep(2)
	uploader(list[0],list[1],list[2],list[3],remotepath2,localpath2)
	time.sleep(2)

	print "the command is " + command
	result = executecmd(list[0],list[1],list[2],list[3],command)
	print "the result is " + result
	
	if result.index("xxooxxoo"):
		index = result.index("xxooxxoo")
		print index
		result = result[index+len("xxooxxoo")+1:]
		print result

	josnresult = json.loads(result)
	checkresult = josnresult["Result"]
	print "checkresult is " 
	print checkresult
	lines = list[0] + ' ' + list[1] + ' ' + list[2] + ' ' + list[3] + ' ' + str(checkresult)
	alllines = list[0] + ' ' + list[1] + ' ' + list[2] + ' ' + list[3] + ' ' + result

	print "lines is "
	print lines
	print "alllines is " 
	print alllines

	#mylock.acquire()
	if checkresult == 1:
		print "the targetresultpath is " + targetresultpath
		writefile(targetresultpath,lines)
		executecmd(list[0],list[1],list[2],list[3],removecommand)
	writefile(allresutlpath,alllines)
    #mylock.release()

	return lines

def filecouter(path):
	fp = open(path,'rb')
	try:
		counter = len(fp.readlines())
	finally:
		fp.close()
	return counter

#read the config and start upload
def readfileandload(osx):
	i = 1
	linelist = []
	defaultcouter = 5
	#linecounter = 10
	currentdir = os.path.split(os.path.realpath(sys.argv[0]))[0]
	path = currentdir + '\\' + 'ip.txt'

	f = open(path,'rb')
	
	linecounter = filecouter(path)
	
	print linecounter
	if linecounter < defaultcouter:
		defaultcouter = linecounter
	
	print "the defaultcouter is %d"  %defaultcouter
	
	try:
		for line in f:
			print "the lines is :" + line
			list = line.split()
			linelist.append(list)

			if len(linelist) == defaultcouter:
				print "get 5"
				print linelist

				thread_pool = []
				for item in range(defaultcouter):
					print "the current 1 defaultcouter %d" %defaultcouter
					arg = linelist[item]
					th = threading.Thread(target = launch,args = (arg,osx))
					thread_pool.append(th)

				for item in range(defaultcouter):
					print "the current 2 defaultcouter %d" %defaultcouter
					thread_pool[item].start()

				for item in range(defaultcouter):
					print "the current 3 defaultcouter %d" %defaultcouter
					threading.Thread.join(thread_pool[item])

				linelist = []	

			
			if len(linelist) < defaultcouter and i == linecounter:
				print "the i is %d" %i
				thread_pool = []
				defaultcouter = len(linelist)
				for item in range(defaultcouter):
					print "the current 4 defaultcouter %d" %defaultcouter
					arg = linelist[item]
					th = threading.Thread(target = launch,args = (arg,osx))
					thread_pool.append(th)

				for item in range(defaultcouter):
					print "the current 5 defaultcouter %d" %defaultcouter
					thread_pool[item].start()

				for item in range(defaultcouter):
					print "the current 6 defaultcouter %d" %defaultcouter
					threading.Thread.join(thread_pool[item])

				linelist = []

			i = i +1
			print "curret i is :%d" %i
			
	finally:
		f.close()
	

#readfileandload(sys.argv[1])
#uploader()


#result = executecmd("192.168.105.141",22,"root","toor","dir")

#print "the result is " + result



	