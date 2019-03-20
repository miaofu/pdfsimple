import pymysql
from config import *

def connectdb():
	db = pymysql.connect(host=HOST, user=USER, passwd=PASSWORD, db=DATABASE, port=PORT, charset=CHARSET)
	db.autocommit(True)
	cursor = db.cursor()
	return (db,cursor)

def getCols(cursor):
	col = cursor.description
	dd = []
	for i in range(len(col)):
		dd.append(col[i][0])
	return dd 

# 关闭数据库
def closedb(db,cursor):
	db.close()
	cursor.close()