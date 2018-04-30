#!/usr/local/bin/python3

import mysql.connector

### This module analyzes all digestion sites for a given accession number and returns a list of sites which do not occur within a coding region
# and a list of optimal sites in which the enzyme itself only digests at these sites. ###

def analyze(gi):	
	
	comEnz = []
	optEnz = []	

	# define compatible site object #
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

	# create enzyme dictionaries #
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

	# grab list of genes for accession number #
	qry = "select * from final_genes where org_acc = %s order by gstop asc"
	curs.execute(qry,(gi,))
	all_results = curs.fetchall()
	idx = 1
	temp = 0
	products = []
	startList = []
	stopList = []
	strandList = []
	gstop = 0

	# parse introns (regions between coding sequences) for digestion sites #
	for (org_acc,geneNum,product,protein_id,strand,gstart,gstop) in all_results:
		geneProduct = product.decode('utf-8')
		products.append(geneProduct)
		strandList.append(strand)
		startList.append(gstart)
		stopList.append(gstop)
		if temp > 0:
			gene3 = products[temp-1]+" - ["+str(startList[temp-1])+":"+str(stopList[temp-1])+"] --> strand ("+str(strandList[temp-1])+")"
			gene5 = products[temp]+" - ["+str(startList[temp])+":"+str(stopList[temp])+"] --> strand ("+str(strandList[temp])+")"

		if idx == 1:
			currentstop = gstop
		else:
			qry = "select * from final_sites_{name} where org_acc = %s and start > %s and stop < %s"
			curs.execute(qry.format(name=gi),(org_acc,currentstop,gstart))
			results = curs.fetchall()
			if len(results) > 0:
				# update enzyme counts for intron cutting sites #
				for (siteNum,org_acc,seq,start,stop) in results:
					seq = seq.decode('utf-8')
					ename = enzDict[seq]
					val = enzCounter[seq]
					val+=1
					enzCounter.update({seq:val})
					comEnz.append(comSite(seq,ename,start,stop,gene3,gene5))
			currentstop = gstop			
		idx += 1
		temp += 1

	# compare the amount of total sites versus sites at introns for all enzymes and return optimal and compatible lists #
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

	return comEnz,optEnz
