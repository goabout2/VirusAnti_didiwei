import os 
import sys 
import sqlite3

#the path of the db
DB_FILE_PATH = ''
#table name
TABLE_NAME = ''
#flag sql paint or not 
SHOW_SQL = True

#get the object of the database
def get_conn(path):
	conn = sqlite3.connect(path)
	if os.path.exists(path) and os.path.isfile(path):
		print('on the hardcard:[{}]'.format(path))
		return conn
	else:
		conn = None
		print('on the memory:[:memory:]')
		return sqlite3.connect(':memory:')

#get_conn("D:\\tool\\python_script\\samplescan\\test.db")

#get cursor
def get_cursor(conn):
	if conn is not None:
		return conn.cursor()
	else:
		return get_conn('').cursor()

#############################################################################################################
#for the table create and drop                                                                              #
#############################################################################################################
#test the table exist or not, if exist ,del it
def drop_table(conn,table):
	if table is not None and table !='':
		sql = 'DROP TABLE IF EXISTS ' + table
		if SHOW_SQL:
			print('the execute sql'.format(sql))
		cu = get_cursor(conn)
		cu.execute(sql)
		conn.commit()
		print('del table success'.format(table))
		close_all(conn,cu)
	else:
		print('the [{}] is empty or equal None'.format(sql))

#create a table 
def create_table(conn,sql):
	if sql is not None and sql != '':
		cu = get_cursor(conn)
		if SHOW_SQL:
			print('execute sql[{}]'.format(sql))
		cu.execute(sql)
		conn.commit()
		print('create the table success')
		close_all(conn,cu)
	else:
		print('the [{}] is empty or equal None'.format(sql))

#############################################################################################################
#release the object and cursor                                                                              #
#############################################################################################################
def close_all(conn,cu):
	try:
		if cu is not None:
			cu.close()
	finally:
		if conn is not None:
			conn.close()

#############################################################################################################
#option for database                                                                                        #
#############################################################################################################
#save the database
def save(conn, sql, data):
    if sql is not None and sql != '':
        if data is not None:
            cu = get_cursor(conn)
            for d in data:
                if SHOW_SQL:
                    print('excute sql:[{}],param:[{}]'.format(sql, d))
                cu.execute(sql, d)
                conn.commit()
            close_all(conn, cu)
    else:
        print('the [{}] is empty or equal None!'.format(sql))

#requary the all data 
def fetchall(conn,sql):
	if sql is not None and sql != '':
		cu = get_cursor(conn)
		if SHOW_SQL:
			print('execute sql:[{}]')
		cu.execute(sql)
		r = cu.fetchall()
		if len(r) > 0:
			for e in range(len(r)):
				print(r[e])
	else:
		print('the [{}] is empty or equal None'.format(sql))

#requary one data
def fetchone(conn,sql,data):
	if sql is not None and sql != '':
		if data is not None:
			d = (data,)
			cu = get_cursor(conn)
			if SHOW_SQL:
				print('execute sql:[{}],para:[{}]'.format(sql,data))
			cu.execute(sql,d)
			r = cu.fetchall()
			if len(r) > 0:
				for e in range(len(r)):
					print(r[e])
		else:
			print('the [{}] equal None'.format(data))
	else:
		print('the [{}] is empty or equal None'.format(sql))

#update
def update(conn,sql,data):
	if sql is not None and sql != '':
		if data is not None:
			cu = get_cursor(conn)
			for d in data:
				if SHOW_SQL:
					print('execute sql:[{}]'.format(sql,d))
				cu.execute(sql,d)
				conn.commit()
			close_all(conn,cu)
	else:
		print('the [{}]is empty or equal None'.format(sql))

#delete
def delete(conn,sql,data):
	if sql is not None and sql != '':
		if data is not None:
			cu = get_cursor(conn)
			for d in data:
				if SHOW_SQL:
					print('execute sql:[{}],para:[{}]'.format(sql,d))
				cu.execute(sql,d)
				conn.commit()
			close_all(conn,cu)
	else:
		print('the [{}]is empty or equal None!'.format(sql))

#############################################################################################################
#option for database test                                                                                   #
#############################################################################################################
def drop_table_test():
	print('del db test')
	conn = get_conn(DB_FILE_PATH)
	drop_table(conn,TABLE_NAME)

#create the init table
def create_table_test():
	print('create table test')
	create_table_sql = '''CREATE TABLE 'virus'(
						'id' int(11) NOT NULL,
						'family' varchar(30) DEFAULT NULL,
						'size'   int(20)  DEFAULT NULL,
						'md5'    varchar(100) DEFAULT NULL,
						'hash'   varchar(100) DEFAULT NULL,
						'sigin'  varchar(100) DEFAULT NULL,
						'time' varchar(100) DEFAULT NULL,
						'departmetn' varchar(150) DEFAULT NULL,
						PRIMARY KEY ('id')
		)'''
	conn = get_conn(DB_FILE_PATH)
	create_table(conn,create_table_sql)

#save the data
def save_test():
	print('save the init virus info')
	save_sql = '''INSERT INTO virus values (?,?,?,?,?,?,?,?)'''
	data = [(1,'linux.trojan.gates',11546,'4137a7010cdbd50ce20a0ef68eaec9ad8e6861f8','0cdbd50ce20a0ef68eaec9ad','siginfdadfa','2016-1-18','dizhengju'),
			(2,'linux.trojan.xor',9062,'bd50ce20a0ef68eaec9ad8e6861f8','010cdbd50ce20a0ef68eaec','siginfdhthta','2016-1-18','shanghai'),
			(3,'linux.trojan.gates',8062,'bd50ce20a0ef68eaec9ad8e6861f8','010cdbd50ce20a0ef68eaec','siginfdafdserbdfa','2016-1-14','chongqin'),
			(4,'linux.trojan.xor',3452,'bd50ce20a0ef68eaec9ad8e6861f8','010cdbd50ce20a0ef68eaec','siginfdapommdfa','2016-1-1','beijing'),
			(5,'linux.trojan.gates',8763,'bd50ce20a0ef68eaec9ad8e6861f8','010cdbd50ce20a0ef68eaec','siginfpmfeddadfa','2016-1-18','dizhengju')]
	conn = get_conn(DB_FILE_PATH)
	save(conn,save_sql,data)



#requary all data 
def fetchall_test():
	print('requary all data.....')
	fetchall_sql = '''SELECT * FROM virus'''
	conn = get_conn(DB_FILE_PATH)
	fetchall(conn,fetchall_sql)

#requary one data
def fetchone_test():
	print('requary one data')
	fetchone_sql = 'SELECT * FROM virus WHERE ID = ?'
	data = 1
	conn = get_conn(DB_FILE_PATH)
	fetchone(conn,fetchone_sql,data)

#update
def update_test():
	print('update the data')
	update_sql = 'UPDATE virus SET md5 = ? WHERE ID = ?'
	data = [('1a1a1a1a1a1a1a1a',1),
			('3e3e3e3e3e3e3e3e',2),
	]
	conn = get_conn(DB_FILE_PATH)
	update(conn,update_sql,data)

#delete
def delete_test():
	print('del data')
	delete_sql = 'DELETE FROM virus WHERE family = ? AND ID = ?'
	data = [('linux.trogan.gates',10),
	]
	conn = get_conn(DB_FILE_PATH)
	delete(conn,delete_sql,data)


def init():
	#the path of database file
	global DB_FILE_PATH
	DB_FILE_PATH = "D:\\tool\\python_script\\samplescan\\test.db"
	#table name
	global TABLE_NAME
	TABLE_NAME = 'virus'
	#paint sql or not
	global SHOW_SQL
	SHOW_SQL = True
	print('show_sql:{}'.format(SHOW_SQL))
	#if the table exit,del it
	drop_table_test()
	#create the table
	create_table_test()
	#insert into the table 
	save_test()

'''

#creat a new datebase
def initdatabase(dbpath,tablename,createtablesql):
	#the path of datebase file 
	global DB_FILE_PATH
	DB_FILE_PATH = dbpath
	#table name 
	global TABLE_NAME
	TABLE_NAME = tablename
	#paint sql or not 
	global SHOW_SQL
	SHOW_SQL = True
	print ('show_sql:{}'.format(SHOW_SQL))
	conn = get_conn(DB_FILE_PATH)
	create_table(conn,createtablesql)

'''

def initglobal(path):
	global DB_FILE_PATH
	DB_FILE_PATH = path
	global TABLE_NAME
	TABLE_NAME = 'virus'

def showdatebase():
	path = os.getcwd()
	scriptpath = os.path.split(os.path.realpath(sys.argv[0]))[0]
	path = os.path.join(scriptpath,"test.db")

	initglobal(path)

	print "im in the showdatebase"
	print('show_sql:{}'.format(SHOW_SQL))
	print DB_FILE_PATH
	fetchall_sql = '''SELECT * FROM virus'''
	conn = get_conn(DB_FILE_PATH)
	fetchall(conn,fetchall_sql)

def insertdatebase(insertdate):
	insertdate = datatransfer(insertdate)
	path = os.getcwd()
	scriptpath = os.path.split(os.path.realpath(sys.argv[0]))[0]
	path = os.path.join(scriptpath,"test.db")

	initglobal(path)

	print('show_sql:{}'.format(SHOW_SQL))
	save_sql = '''INSERT INTO virus values (?,?,?,?,?,?,?,?)'''
	conn = get_conn(DB_FILE_PATH)
	print "the insertdate is"
	print insertdate
	save(conn,save_sql,insertdate)

def deldatebaseyuan(deldate):
	deldate = datatransfer(deldate)
	print "the deldate is :"
	print deldate
	path = os.getcwd()
	scriptpath = os.path.split(os.path.realpath(sys.argv[0]))[0]
	path = os.path.join(scriptpath,"test.db")

	initglobal(path)

	print('show_sql:{}'.format(SHOW_SQL))
	del_sql = '''DELETE FROM virus WHERE family = ? AND ID = ?'''
	data = [('linux.trojan.gates',6),
	]
	conn = get_conn(DB_FILE_PATH)
	delete(conn,del_sql,deldate)

def deldatebase(deldate):
	deldate = datatransfer(deldate)
	print "the deldate is :"
	print deldate
	path = os.getcwd()
	scriptpath = os.path.split(os.path.realpath(sys.argv[0]))[0]
	path = os.path.join(scriptpath,"test.db")

	initglobal(path)

	print('show_sql:{}'.format(SHOW_SQL))
	del_sql = '''DELETE FROM virus WHERE ID = ?'''
	data = [('linux.trojan.gates',6),
	]
	conn = get_conn(DB_FILE_PATH)
	delete(conn,del_sql,deldate)

def updatebase(update):
	templist = update.split(',')
	print "the templist[1]"
	print templist[1]
	print "the templist[0]"
	print templist[0]
	deldate = templist[0]
	print deldate
	deldatebase(deldate)
	insertdatebase(update)



def main():
	init()
	'''
	fetchall_test()
	print('#' * 50)
	fetchone_test()
	print('#' * 50)
	update_test()
	fetchall_test
	print('#' * 50)
	fetchone_test()
	print('#' * 50)
	delete_test()
	fetchall_test()

	'''

def datatransfer(datainter):
	data = []
	datalist = datainter.split(',')
	data.append(datalist)
	return data


if __name__ == '__main__':
	#main()


	
	print 1
	#data = [('linux.trojan.gates',5),]
	#deldatebase(data)
	#delete_test()
	print 2
	#showdatebase()
	

	print 3
	
	'''
	data = [(9,'linux.trojan.gates',11546,'4137a7010cdbd50ce20a0ef68eaec9ad8e6861f8','0cdbd50ce20a0ef68eaec9ad','siginfdadfa','2016-1-18','dizhengju'),
			]
	'''

	#insertdatebase(sys.argv[1])
	#deldatebase(sys.argv[1])
	#datatransfer(sys.argv[1])
	updatebase(sys.argv[1])
'''
	data = [('linux.trojan.xor',6),
	]
	print "the data is "
	print data
	deldatebase(data)
	showdatebase()
'''
	
	

	
    

    
    
	


