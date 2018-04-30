#!/usr/local/bin/python3

import mysql.connector
import sys

### This script is used to clear the database of all organism information. This is used to reset the database when testing parsing modules ###

# connect to database #
conn = mysql.connector.connect(user='sblack22',password='278zTsV^',host='localhost',database='sblack22', use_unicode=False)
curs = conn.cursor()

qry = "select * from final_organism"
curs.execute(qry)
orgs = curs.fetchall()

tables = []

# delete all organism information from database for all organisms #
for (gi,accession,name,size,num_genes) in orgs:
	accNum = gi.decode('utf-8')

	qry = "delete from final_genes where org_acc = %s"
	curs.execute(qry,(accNum,))

	qry = "delete from final_organism where gi = %s"
	curs.execute(qry,(accNum,))
	
	tables.append(accNum)

for table in tables:
	curs.execute("DROP TABLE final_sites_{tab}".format(tab=table))

conn.commit()
curs.close()
conn.close()
