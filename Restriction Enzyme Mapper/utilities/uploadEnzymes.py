#!/usr/local/bin/python3

import mysql.connector

### This module uploads all enzyme information from the generated text file 'newenzymes.txt' into the database ###

f = open('newenzymes.txt','r')

b = {}

for i in f:
	i = i.strip()
	r = i.split('\t')
	b.update({r[1]:r[0]})

f.close()

# connect to database #
conn = mysql.connector.connect(user='sblack22',password='278zTsV^',host='localhost',database='sblack22', use_unicode=False)
curs = conn.cursor()

qry = "DROP TABLE final_enzymes"
curs.execute(qry)

qry = "CREATE TABLE final_enzymes (seq varchar(255) PRIMARY KEY, name varchar(255))"
curs.execute(qry)

for key in b:
	qry = "INSERT INTO final_enzymes (seq,name) VALUES (%s,%s)"
	curs.execute(qry,(key,b[key]))

conn.commit()
curs.close()
conn.close()
