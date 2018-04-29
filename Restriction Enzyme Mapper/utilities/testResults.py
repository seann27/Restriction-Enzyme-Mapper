#!/usr/local/bin/python3

import mysql.connector
import sys

gi = sys.argv[1]
	
comEnz = []
optEnz = []

class enzyme:
	def __init__(self,name,seq,start,stop):
		self.name = name		
		self.seq = seq
		self.start = start
		self.stop = stop	

class comSite:
	def __init__(self,enz,enzname,estart,estop,gene3,gene5):
		self.enz = enz
		self.enzname = enzname
		self.estart = estart
		self.estop = estop
		self.gene3 = gene3
		self.gene5 = gene5

# initialze connection #
conn = mysql.connector.connect(user='sblack22',password='278zTsV^',host='localhost',database='sblack22', use_unicode=False)
curs = conn.cursor()
# initialze connection #

qry = "select * from final_enzymes"
curs.execute(qry)
enzymes = curs.fetchall()
enzDict = {}
enzCounter = {}
for (seq,name) in enzymes:
	seq = seq.decode('utf-8')
	name = name.decode('utf-8')
	enzDict.update({seq:name})
	enzCounter.update({seq:0})

qry = "select * from final_genes where org_acc = %s order by gstop asc"
curs.execute(qry,(gi,))
all_results = curs.fetchall()
idx = 1
tidx = 0
gstop = 0

geneList = []

for (org_acc,geneNum,product,protein_id,strand,gstart,gstop) in all_results:
	geneNum = str(geneNum.decode('utf-8'))
	geneList.append(geneNum)
	if tidx > 0:
		print(geneList[tidx-1]+"\t"+geneList[tidx]+"\t"+str(gstop))
	tidx += 1

for (org_acc,geneNum,product,protein_id,strand,gstart,gstop) in all_results:
	if idx == 1:
		currentstop = gstop
	elif idx > 1 and idx <= len(all_results):
		qry = "select * from final_sites_{name} where org_acc = %s and start > %s and stop < %s"
		curs.execute(qry.format(name=gi),(org_acc,currentstop,gstart))
		results = curs.fetchall()
		if len(results) > 0:
			for (siteNum,org_acc,seq,start,stop) in results:
				seq = seq.decode('utf-8')
				ename = enzDict[seq]
				val = enzCounter[seq]
				val+=1
				enzCounter.update({seq:val})
				comEnz.append(comSite(seq,ename,start,stop,gstop,gstart))
		currentstop = gstop		
	else:
		continue		
	idx = idx+1

if len(comEnz) > 0:
	for site in comEnz:		
		qryTotal = "select count(*) from final_sites_{name} where org_acc = %s and seq = %s".format(name=gi)
		curs.execute(qryTotal,(org_acc,site.enz))
		total = curs.fetchone()
		total = total[0]
		local = enzCounter[site.enz]
		if total == local:
			optEnz.append(site)
conn.commit()
curs.close()
conn.close()
