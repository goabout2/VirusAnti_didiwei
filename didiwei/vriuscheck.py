import argparse
import os
import time

import urllib2

def downloader(directory,iteration):
	url = 'https://virusshare.com/hashes/VirusShare_%05d.md5' % iteration
	print "Downloading {0} into {1}..." .format(url,directory)
	file_path = os.path.join(directory,os.path.basename(url))
	print "in the downloader,the file_path is: " + file_path
	contents = urllib2.urlopen(url).read()
	print "the contents is:" + contents
	
	file_output = open(file_path,'wb')
	file_output.write(contents)
	file_output.close()
	time.sleep(1)
	

def find_missing(directory,latest):
	to_find = list(range(0,latest+1))
	for i in os.listdir(directory):
		to_find.remove(int(''.join(c for c in i if c.isdigit())[:5]))
	return to_find

def parse_amount(amount):
	to_find = []
	try:
		if ',' in amount:
			temp = amount.split(',')
			for i in temp:
				to_find.append(int(i))
			return to_find

		elif '-' in amount:
			temp = amount.split('-')
			for i in range(int(temp[0]),int(temp[1]) + 1):
				to_find.append(i)
			return to_find

		else:
			to_find.append(int(amount))
			return to_find
	except ValueError:
		print "ERROR: incorrect value given for update range."
		exit()

def update(directory,amount,latest):
	try:
		l = int(latest)
	except ValueError:
		print "ERROR:incorrect value given for update range."
		exit()

	print "in the update,the directory is :" + directory

	if amount == "all":
		for i in range(0,l):
			downloader(directory,i)

	elif amount == "missing":
		for i in range(0,l):
			to_find = find_missing(directory,l)
			for i in to_find:
				downloader(directory,i)

	else:
		to_find = parse_amount(amount)
		for i in to_find:
			downloader(directory,i)

def search(directory,term):
	counter = 1
	for file_to_search in os.listdir(directory):
		full_file_path = os.path.join(directory,file_to_search)
		if os.path.isfile(full_file_path):
			with open(full_file_path) as f:
				for line in f:
					if term in line:
						print('FOUND|{0}|{1}|{2}'.format(term,file_to_search,counter))
						return
					counter += 1
		counter = 1
	print('     |{0}|{1}|{2}'.format(term,"None                ", -1))

def main():
	parser = argparse.ArgumentParser(description = 'tool to download VirusShare hash files and search them for specified hashes')
	parser.add_argument('-s','--search',help = 'has to search for in local repository',nargs = "+")
	parser.add_argument('-u','--update',help = 'updates local hash containing files')
	parser.add_argument('-l','--latest',help = 'sets latest virusshare file released',default ='220')
	parser.add_argument('-d','--directory',help = 'set working directory',default = 'VirusShare_Hashes')

	args = parser.parse_args()
	directory = args.directory
	print "the directory is :" + directory
	latest = args.latest

	if not os.path.exists(directory):
		print "im in not existst"
		os.makedirs(directory)
		

	if args.update is not None:
		update(directory,args.update,latest)
		print "im in update"

	if args.search is not None:
		print "      | Hash  | File               | Line"
		for t in args.search:
			search(directory,t)

	if args.search is None and args.update is None:
		parser.print_help()

if __name__ == "__main__":
	main()