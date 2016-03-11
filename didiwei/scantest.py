#search.py
#############################################################################################################
#qiangludidiwei is a free anti-virus framework for researcher to removeing and killing specify              #
#virus in os(incloude the windows,linux so for),all you need to do is write a config file and               #
#leaving other thing to didiwei                                                                             #
#############################################################################################################
import os
import re
import sys
import time 
import json
import string
import _winreg
#import win32api
#import win32con
import ConfigParser

from ctypes import*

pidlist = []
viruslist = ""

#############################################################################################################
#commmand funcion                                                                                           #
#############################################################################################################
#get the config path
def getcfgpath():
	dirpath = os.path.split(os.path.realpath(sys.argv[0]))[0]
	configscriptpath = os.path.join(dirpath,"config.conf")
	return configscriptpath

#read file 
def readfile(path):
	print "the read path is :" + path 
	file = open(path)
	try:
		content = file.read()
	finally:
		file.close()
	return content

#scan the specifyname file 
def findrandomname(path,len,type):
	for filename in os.listdir(path):
		fp = os.path.join(path,filename)
		if os.path.isfile(fp):
			if len(filename) == len:
				if type == 'num':           #for num
					if re.match('^[0-9]+$',filename):
						return filename
				if type == 'word1':         #for a-z
					if re.match('^[a-z]+$',filename):   
						return filename
				if type == 'word2':         #for A-Z
				    if re.match('^[A-Z]+$',filename):   
						return filename
				if type == 'numword1':       #for num a-z
					if re.match('^[0-9a-z]+$',filename):
						return filename
				if type == 'numword2':       #for num A-Z
					if re.match('^[0-9A-Z]+$',filename):
						return filename
				if type == 'word1word2':     #for a-z A-Z
					if re.match('^[a-zA-Z]+$',filename):
						return filename
				if type == 'all':            #for a-z A-Z num
					if re.match('^[0-9a-zA-Z]+$',filename):
						return filename

#detect one file is sample or not 
def detectfile(path,word):
	flag = False
	with open(path) as f:
		for line in f:
			if word in line:
				flag = True
	if flag:
		return True
	else:
		return False

#scan the filesystem in the os with specify eigenvalue
def scanforeigen(path,word):
	json = {}
	pathlist = ""

	for filename in os.listdir(path):
		fp = os.path.join(path,filename)
		if os.path.isfile(fp):
			print fp
			with open(fp) as f:
				for line in f:
					if word in line:
						print "find in the file:" + fp
						pathlist = pathlist + fp + ";"
						break
		'''
		elif os.path.isdir(fp):
			scanforeigen(fp,word)
		'''
	return pathlist

#scan the direct in a list with specify eigenvalue
def scanlist(path,word):
	jsonobj = {}
	findlist = ""

	pathlist = path.split(";")
	for dir in pathlist:
		find = scanforeigen(dir,word)
		findlist = findlist + find

	print "the findlist is :" 
	print findlist
	if findlist is None or len(findlist) == 0:
		jsonobj[u'Result'] = 0
	else:
		print "dddddddddddddddddddddddddddddd"
		jsonobj[u'Result'] = 1
		jsonobj[u'pathlist'] = findlist

	data_string = json.dumps(jsonobj)
	return data_string

#del all file and dir in specify dir
def delete_file_folder(path):
	if os.path.isfile(path):
		try:
			print "the remove path is " + path
			os.remove(path)
		except:
			pass
	elif os.path.isdir(path):
		for item in os.listdir(path):
			itempath = os.path.join(path,item)
			delete_file_folder(itempath)
		try:
			os.rmdir(path)
		except:
			pass

#read the configfile 
def killcore():
	global pidlist
	global viruslist

	configpath = getcfgpath()
	cf = ConfigParser.ConfigParser()

	cf.read(configpath)

	#return all section
	secs = cf.sections()
	print 'sections:',secs

	if 'windows' in secs:
		print "anti-virus in the windows,read the anti-virus info from config"
		winopts = cf.options("windows")
		win_option = cf.get("windows","option")
		if win_option == "scan":
			win_filescan = cf.get("windows","filescan")
			win_sign = cf.get("windows","sign")
			print "the win_sign is: " + win_sign
			result = scanlist(win_filescan,win_sign)
			print "xxooxxoo"
			print result

		if win_option == "kill":
			print "im in kill"
			for winopt in winopts:
				if 'command' == winopt:
					windows_command = cf.get("windows","command")
					print "command:" + windows_command
				if 'filepath' == winopt:
					pass
					'''
					windows_filepath = cf.get("windows","filepath")
					print "filepath :" + windows_filepath
					windelfile(windows_filepath)
					'''
				if 'register' == winopt:
					windows_register = cf.get("windows","register")
					print "register :" + windows_register
					windelregister(windows_register)

				if 'processes' == winopt:
					print "im in processes"
					windows_processes = cf.get("windows","processes")
					print "process :" + windows_processes
					winprocesskiller(windows_processes)

				if 'delpath' == winopt:
					windows_delpath  = cf.get("windows","delpath")
					print "the delfile is :" + windows_delpath
					windelfile(windows_delpath)

					win_filescan = cf.get("windows","filescan")
					win_sign = cf.get("windows","sign")
					result = scanlist(win_filescan,win_sign)
					print "xxooxxoo"
					print result



	elif 'linux' in secs:
		print "anti-virus in the linuxsign,read the anti-virus info from config"
		linopts = cf.options("linux")
		linux_option = cf.get("linux","option")
		if linux_option == "scan":
			linux_filescan = cf.get("linux","filescan")
			linux_sigin = cf.get("linux","sign")
			result = scanlist(linux_filescan,linux_sigin)
			print "xxooxxoo"
			print result
		if linux_option == "kill":
			for linopt in linopts:		
				print "the linoptis :" + linopt
				if 'filepath' == linopt:
					linux_filepath = cf.get("linux","filepath")
					linux_sigin = cf.get("linux","sign")
					print "file path :" + linux_filepath
					#(pidlist,viruslist) = pidhunter(linux_filepath,linux_sigin)
					linpidhunter(linux_filepath,linux_sigin)
					print pidlist
					print viruslist
					
					for item in pidlist:
						print "item is " + item 
						cmd = "kill -STOP " + item
						os.popen(cmd)
						print "going sleeping"
						time.sleep(10)
						
					
				if 'command' == linopt:
					linux_command = cf.get("linux","command")
					print "command :" + linux_command
					linexcutecommand(linux_command)

				if 'initdscan' == linopt:
					linux_initdscan = cf.get("linux","initdscan")
					print "initdscan :" + linux_initdscan
					lininithandler(linux_initdscan,linux_sigin)
					#print "the viruslist is " + viruslist

				if 'delpath' == linopt:
					linux_delpath = cf.get("linux","delpath")	               #int the config,the delpath end with ;
					print "the linxu_delpath is " + linux_delpath
					print "the viruslist is " + viruslist
					linux_delpath = linux_delpath + viruslist
					print "del path :" + linux_delpath
					
					lindelfile(linux_delpath)
					for item in pidlist:
						cmd = "kill -9 " + item
						os.popen(cmd)
					
					linux_filescan = cf.get("linux","filescan")
					linux_sigin = cf.get("linux","sign")
					result = scanlist(linux_filescan,linux_sigin)
					print "xxooxxoo"
					print result
					
					

#############################################################################################################
#window anti-virus                                                                                          #
#############################################################################################################

#delet the register in the config,the del register must accord to the this format blow
#############################################################################################################
#    HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Mytest11\testkeyvaluse            #
#    |                 |                                                           |            |           #
#    +                 +                                                           +            +           #
#############################################################################################################   

def winexcutecommand(command):
	commandlist = command.split(';')
	for cmd in commandlist:
		print "execute the command is :" + cmd
		result = os.popen(cmd).read()
		print "the result of the cmd is :" + result

def windelregister(register):
	registerlist = register.split(';')
	for register in registerlist:
		print register
		#split the register 
		prefix = register.index('\\')
		postfx = register.split('\\')[-1]
		regkey = register[0:prefix]
		regsub = register[prefix+1:]
		valueskeypost  = regsub.rfind('\\')
		valueskey = regsub[valueskeypost + 1:]
		regsubkey = regsub[0:valueskeypost]
		print "regkey is :" + regkey + " regsub is :" + regsub + " valueskey is :" + valueskey + " regsubkey is :" + regsubkey

		
		if regkey == "HKEY_CLASSES_ROOT":
			print "in the root"
			key1 = _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT,regsubkey,0,_winreg.KEY_WRITE)
		if regkey == "HKEY_CURRENT_USER":
			print "in the curren user"
			key1 = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,regsubkey,0,_winreg.KEY_WRITE)
		if regkey == "HKEY_LOCAL_MACHINE":
			print "in the machine"
			key1 = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,regsubkey,0,_winreg.KEY_WRITE)
		if regkey == "HKEY_USERS":
			print "in the user"
			key1 = _winreg.OpenKey(_winreg.HKEY_USERS,regsubkey,0,_winreg.KEY_WRITE)
		if regkey == "HKEY_CURRENT_CONFIG":
			print "config"
			key1 = _winreg.OpenKey(_winreg.HKEY_CURRENT_CONFIG,regsubkey,0,_winreg.KEY_WRITE)
        
        #delete it 
		print key1
		if "moren" in valueskey:
			valueskey = ''
		_winreg.DeleteValue(key1, valueskey)
		#_winreg.DeleteKey(key1,valueskey)

#throught iocode to unload the driver
def winunloaddriver(devicelink,ioclcode):
	kernel32 = windll.LoadLibrary("kernel32.dll")

	GENERIC_READ = 0x80000000
	GENERIC_WRITE = 0x40000000
	OPEN_EXISTING = 0x3

	current_length = 5
	in_buffer = 'A'*current_length
	out_buffer = (c_char * current_length)()
	bytes_returned = c_ulong(current_length)

	driver_handle = kernel32.CreateFileW(devicelink,GENERIC_READ|GENERIC_WRITE,0,None,OPEN_EXISTING,0,None)
	print driver_handle
	if driver_handle:
		print "[*]Success! %s is a vaild device"
		kernel32.DeviceIoControl(driver_handle,ioclcode,in_buffer,current_length,byref(out_buffer),current_length,byref(bytes_returned),None)
	else:
		print "[*]No vaild devices found,exiting"
		
def windelfile(path):
	pathlist = path.split(';')
	for filepath in pathlist:
		delete_file_folder(filepath)

#to kill the process in the config list,specify for the process which was injected code
def winprocesskiller(processes):
	processlist = processes.split(';')
	for processname in processlist:
		result = os.popen('tasklist').read()
		print "the result of tasklist is " + result
		while processname in result:
			killcommand = "taskkill /im " + processname +" /f"
			print "the command is " + killcommand
			os.popen(killcommand).read
			result = os.popen('tasklist').read()

#############################################################################################################
#linux anti-virus                                                                                           #
#############################################################################################################
#def linuxkill

#extc the command from the congif file 
def linexcutecommand(command):
	cmdlist = command.split(';')
	for cmd in cmdlist:
		print "excute the command:" + cmd
		result = os.popen(cmd).read()
		print "the result of the " + cmd + "is:" + result 

#remove the file from the config file 
def lindelfile(path):
	pathlist = path.split(';')
	for filepath in pathlist:
		delete_file_folder(filepath)

#scan all pid throught the file under the specify path 
def linpidhunter(delfilepath,sign):
	global pidlist
	global viruslist
	dirlist = delfilepath.split(';')

	for dirspecify in dirlist:
		scanresult = scanforeigen(dirspecify,sign)
		print "before" + scanresult
		#scanresult = scanresult[0:-1]
		viruslist = viruslist + scanresult

	viruslist = viruslist[0:-1]
	if viruslist is None:
		pass
	else:
		scanresultlist = viruslist.split(';')
		viruslist = viruslist + ";"
		for itemnum in os.listdir("/proc"):
			if itemnum.isdigit():
				path = "/proc/" + itemnum + "/maps"
				print "####################################"
				print path
				for result in scanresultlist:
					mapscontent = readfile(path)
					if result in mapscontent:
						print "in if "
						print "the pid of the " + result + " is " + itemnum
						pidlist.append(itemnum)
					else:
						print "oh my god"
	#return pidlist,viruslist

#throught the processname to get the speacify pid
def pidhunterbyname(processname):
	pass

#get samplepath in a specify init script
def linpathbyinit(initpaht,sign):
	global viruslist
	with open(initpaht) as fp:
		for line in fp:
			m = re.search('(\/([0-9a-zA-Z._-]+))+',line)
			if m and os.path.isfile(m.group(0)):
				print "get the file" + m.group(0)
				if detectfile(m.group(0),sign):
					if m.group(0) in viruslist:
						continue
					else:
						viruslist = viruslist + m.group(0) + ";"
						print "the viruslist is " + viruslist

#handle the init and get the may sample path in the initl
def lininithandler(initpaths,sign):
	confuselist = []
	global viruslist
	initlist = initpaths.split(";")
	for initpath in initlist:
		print "the initpath is" + initpath
		filename = initpath.split('/')[-1]
		filedir = initpath[0:len(initpath)-len(filename)]
		print "the filename is :" + filename
		print "the filedir is :" + filedir

		if filename.endswith("**d"):
			for files in os.listdir(filedir):
				targetname = filename[0:-3]
				if targetname in files:
					path = os.path.join(filedir,files)
					print "get it,target is :" + path
					viruslist = viruslist + path + ";"
					confuselist.append(path)

			if len(confuselist):
				for cfpath in confuselist:
					linpathbyinit(cfpath,sign)
		else:
			linpathbyinit(initpath,sign)

def test():
	list = ""
	list = list + "ddd"
	print list

if __name__ == '__main__':
	#lininithandler(sys.argv[1],sys.argv[2])
	#pathbyinit(sys.argv[1])
    #result = scanforeigen(sys.argv[1],sys.alrgv[2])
    
  

	#checkresult = josnresult["Result"]
    #print checkresult
	killcore()
	#windelfile(sys.argv[1])
	#winregisterdel(sys.argv[1])l
	#winunloaddriver("\\\\.\\SysLinkUsbAminDevice","0x222005")

	'''
    result = scanlist(sys.argv[1],sys.argv[2])
    print 1
    print result
    josnresult = json.loads(result)
    print josnresult
    print josnresult[u'Result']
    print josnresult[u'pathlist']
    '''
