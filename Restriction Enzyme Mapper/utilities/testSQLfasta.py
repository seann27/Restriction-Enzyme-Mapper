#!/usr/local/bin/python3

import mysql.connector
import re
import sys
from Bio import Entrez

### This module tests, prints, and writes debugging information to file for purposes of debugging the fasta parsing script ###

accNum = sys.argv[1]

Entrez.email = "sblack22@jhu.edu"

# store restriction enzymes in dict
f = open('newenzymes.txt','r')
debug = open('debug.txt','w')

b = {}

for i in f:
	i = i.strip()
	r = i.split('\t')
	b.update({r[0]:r[1]})

f.close()

fas = Entrez.efetch(db="nucleotide", id=accNum, rettype="fasta", retmode="text")

#fas = open('sequence.fasta','r')

first = fas.readline()

m = re.search(r">(\S+)(\s+).*",first)
accession = m.group(1)

first = fas.readlines()
fasta = ""

idx = 0
sites = {}
temp = ''
location = 0
stop = 0

for line in first:
	line = line.strip()
	fasta = fasta+line
	idx = idx+1

for key in b:
	hasMatch = re.search(b[key],fasta)
	numMatches = 0
	if hasMatch:
		matches = re.finditer(b[key],fasta)
		for match in matches:
			location = match.start()+1
			stop = len(b[key])+location
			sites.update({str(location):key})
			debug.write("Name: "+key+", Seq: "+b[key]+", Location: "+str(location)+":"+str(stop)+"\n")
			numMatches = numMatches+1
		debug.write("\n")

print ("\nRun Complete. "+str(idx)+" lines processed.")

debug.close()
fas.close()

#sql stuff#
conn = mysql.connector.connect(user='sblack22',password='278zTsV^',host='localhost',database='sblack22', use_unicode=False)
curs = conn.cursor()
#sql stuff#

sitesFile = open('all_sites.txt','w')
siteIdx = 0
siteAcc = ""
if len(sites) > 0:
	print ("Matches found: "+str(len(sites)))
	for key in sites:
		siteIdx = siteIdx+1
		stop = len(b[sites[key]])+int(key)
		sitesFile.write(sites[key]+" - "+b[sites[key]]+" ["+key+":"+str(stop)+"]\n")
		siteAcc = accession+" - site: "+str(key)
		qry = "INSERT INTO final_sites (siteKey, org_acc, seq, start, stop) VALUES (%s,%s,%s,%s,%s)"
		curs.execute(qry,(siteAcc,accession,b[sites[key]],int(key),stop))

conn.commit()
curs.close()
conn.close()

sitesFile.close()
