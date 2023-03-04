import mysql.connector
cnx = mysql.connector.connect(user='root' , password='',
                              host='127.0.0.1' ,
                              )
cursor=cnx.cursor()
cursor.execute('USE Advanced;')
cursor.execute('SELECT * FROM dataset;')
res=cursor.fetchall()
for item in res:
    print(item)
cursor.execute('Drop TABLE dataset;')
print('Deleted!!!')