from model import * 
from database import *

class resource():

	def distribute(self,origin_tablename,tableName):
		#
		#tableName = 'movie'
		(db,cursor) = connectdb()
		sql = "DROP TABLE IF EXISTS %s;"%tableName
		cursor.execute(sql)
		sql ="CREATE TABLE %s( resource_id char(20) NOT NULL, user_id char(20) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8"%tableName
		cursor.execute(sql)

		sql = 'select id from '+origin_tablename
		cursor.execute(sql)
		data = cursor.fetchall()
		print (data )
		closedb(db,cursor)
		pass 
if __name__ == '__main__':
	resource().distribute('movie','movie_rsdrite')