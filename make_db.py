import MySQLdb

conn = MySQLdb.connect(host='127.0.0.1', user='root', password='0921Nknkn', db='another_user')
cursor = conn.cursor()
# cursor.execute(
#                 'CREATE TABLE users('
#                 'id int NOT NULL AUTO_INCREMENT,'
#                 'user_name text(20) NOT NULL,'
#                 'password text(20) NOT NULL,'
#                 'PRIMARY KEY(id))')
conn.commit()
cursor.close()
conn.close()