import os 
import sys
import getopt 
import argparse

import uploader
import manager
import vriuscheck

def usage():
	usage = """                          enter --help for some help
+---------------------------------------------------------------+
|        ---  (_)        ---  (_)  _    _    _             (_)  |
|   ____|   ||   |  ____|   ||   || |  | |  | |   _____   |   | |
|  /  __|   ||   | /  __|   ||   || |  | |  | | /  ___  \ |   | |
| |  /  |   ||   ||  /  |   ||   || | _| |_ | ||  /___\ _||   | |
| | (___|   ||   || (___|   ||   | \         / |  | __ _  |   | |  
|  \ ___|___||___| \ ___|___||___|  \ _ ^ _ /   \ ______/ |___| |
|                                                               |       
|                                                     goabout2  |
+---------------------------------------------------------------+
|                     My blog:  http://www.cnblogs.com/goabout2/|
+---------------------------------------------------------------+
	"""
	print usage

if "__main__" == __name__:
	'''
	try:
		opts,args = getopt.getopt(sys.argv[1:],"hu:t:a:",["help","dshow","dinsert=","ddel=","dupdate=","upload=","tools=","analyse="])
		for opt ,arg in opts:
			if opt in ("-h","--help"):
				usage()
				sys.exit(1)
			elif opt in ("--dshow"):                                #for datebase option
				print "show the datebase"
				manager.showdatebase()
			elif opt in ("--dinsert"):
				print arg
			 	manager.insertdatebase(arg)
			elif opt in ("--ddel"):
				manager.deldatebase(arg)
			elif opt in ("--dupdate"):
				print "dupdate"
				print arg
			elif opt in ("-u","--upload"):                          #for upload the killcore
				print "upload the kill "
				print arg
				uploader.readfileandload(arg)

			elif opt in ("-t","--tools"):                           #for tools use in the analyse
				print "tools"
				print arg

			elif opt in ("-a","--analyse"):                         #for analysecore
				print "analyse"
				print arg
	except getopt.GetoptError:
		print("getopt error!")
		usage()
		sys.exit(1)

	'''
	usage()
	currentdir = os.path.split(os.path.realpath(sys.argv[0]))[0]
	parser = argparse.ArgumentParser(description = 'tools to kill an clear virus throught a config script in a specify machine')

	parser.add_argument('--dshow',help = 'show the current datebase(ds/dshow all )')
	parser.add_argument('--dinsert',help = 'insert one sample info into the datebase,in this version ,you need inter data format as follow : id,famalyname,size,hash,md5,sign,time,deparment')
	parser.add_argument('--ddel',help = 'del one sample info from the datebase')
	parser.add_argument('--dupdate',help = 'update one sample info into the datebase')

	parser.add_argument('--upload',help = 'upload the killcore to specify machine and execut kill/scan,you can tell killcore which os is,windows/linux/none,if you do not kenw,inter with none')

	parser.add_argument('--tools',help = 'some tools to use during the analyse')

	parser.add_argument('--analyse',help = 'start the analysecore for a sample')

	parser.add_argument('--search',help = 'has to search for in local repository',nargs = '+')
	parser.add_argument('--update',help = 'updates local hash containing files (--update all/missing/10,11,12/0-20)')
	parser.add_argument('--latest',help = 'sets latest vriusshare file released',default = '220')
	parser.add_argument('--directory',help = 'set working directory',default = currentdir+'/virushash')

	args = parser.parse_args()
	#for vriussearch
	directory = args.directory
	latest = args.latest
	if not os.path.exists(directory):
		os.makedirs(directory)

	if args.update is not None:
		vriuscheck.update(directory,args.update,latest)

	if args.search is not None:
		print "| Hash                      | File                      | Line"
		for t in args.search:
			vriuscheck.search(directory,t)

    #for datebase option
	if args.dshow == 'all':
		manager.showdatebase()

	if args.dinsert is not None:
		manager.insertdatebase(args.dinsert)
		
	if args.ddel is not None:
		manager.deldatebase(args.ddel)

	if args.dupdate is not None:
		manager.updatebase(args.dupdate)

	#for killcore upload
	if args.upload is not None:
		uploader.readfileandload(args.upload)



		