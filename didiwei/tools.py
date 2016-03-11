import os
import sys
import time
import hashlib
import binascii

class tools(object):
	def __init__(self,filepath,sigin):
		self.filepath = filepath
		self.sigin = sigin
		pass
    
    #get the sha1 of the file 
	def CalcSha1(self):
		with open(filepath,'rb') as f:
			sha1obj = hashlib.sha1()
			sha1obj.update(f.read())
			hash = sha1obj.hexdigest()
			print "the hash is :" + hash
			return hash

	#get the md5 of the file 
	def CalcMd5(self):
		with open(filepath,'rb') as f:
			md5obj = hashlib.md5();
			md5obj.update(f.read())
			md5 = md5obj.hexdigest()
			print "the md5 is :" + md5
			return md5

    #get the size of the file 
	def CalcSize(self):
		size = os.path.getsize(filepath)
		print "the size is :%d" %size
		return size

	#get the time of the collect
	def GetTime(self):
		currenttime = time.strftime("%Y-%m-%d-%H:%M",time.localtime(time.time()))
		print "the time is :" + currenttime
		return currenttime

	#string transfer to hex
	def StringToHex(self):
		hex = binascii.b2a_hex(sigin)
		print "the hex of the sigin is :" + hex
		return hex


if __name__ == "__main__":
	if len(sys.argv) == 3:
		filepath = sys.argv[1]
		sigin = sys.argv[2]
		print filepath
		littertool = tools(filepath,sigin)
		#littertool.GetBaseInfo()
		
		littertool.CalcMd5()
		littertool.CalcSha1()
		littertool.CalcSize()
		littertool.GetTime()
		littertool.StringToHex()




