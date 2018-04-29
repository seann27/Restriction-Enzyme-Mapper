#!/usr/local/bin/python3

import mysql.connector
import re
from Bio import Entrez

### This module parses a fasta file for all restriction sites (from enzymes in database) found in the nucleotide sequence of the given accession number. ###

def run(accNum,gi):
	Entrez.email = "sblack22@jhu.edu"
	
	# store restriction enzymes in dict #
	f = open('utilities/newenzymes.txt','r')
	
	b = {}
	
	for i in f:
		i = i.strip()
		r = i.split('\t')
		b.update({r[1]:r[0]})

	f.close()

	fas = Entrez.efetch(db="nucleotide", id=accNum, rettype="fasta", retmode="text")

	first = fas.readline()

	# grab gi #
	m = re.search(r">(\S+)(\s+).*",first)
	accession = gi

	first = fas.readlines()
	fasta = ""

	idx = 0
	sites = {}
	temp = ''
	location = 0
	stop = 0

	# build sequence for regex parsing #
	for line in first:
		line = line.strip()
		fasta = fasta+line
		idx = idx+1
	
	# search for all occurrences of every enzyme #
	for key in b:
		hasMatch = re.search(key,fasta)
		numMatches = 0
		if hasMatch:
			matches = re.finditer(key,fasta)
			for match in matches:
				location = match.start()+1
				stop = len(key)+location
				sites.update({str(location):key})
				numMatches = numMatches+1
	fas.close()

	# connect database and upload site information #
	conn = mysql.connector.connect(user='sblack22',password='278zTsV^',host='localhost',database='sblack22', use_unicode=False)
	curs = conn.cursor()

	curs.execute("CREATE TABLE final_sites_{name} (siteKey varchar(255) PRIMARY KEY, org_acc varchar(255), seq varchar(255), start int, stop int)".format(name=gi))

	siteIdx = 0
	siteAcc = ""
	if len(sites) > 0:
		for key in sites:
			siteIdx = siteIdx+1
			stop = len(sites[key])+int(key)
			siteAcc = accession+" - site: "+key
			qry = "INSERT INTO final_sites_{name} (siteKey, org_acc, seq, start, stop) VALUES (%s,%s,%s,%s,%s)".format(name=gi)
			curs.execute(qry,(siteAcc,accession,sites[key],int(key),stop))

	conn.commit()
	curs.close()
	conn.close()
