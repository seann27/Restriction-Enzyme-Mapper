#!/usr/local/bin/python3

import mysql.connector
import re
from Bio import Entrez

### This module parses a GenBank file for gene and organism information of the input accession number ###

def run(accNum):
	Entrez.email = "sblack22@jhu.edu"

	file = Entrez.efetch(db="nucleotide", id=accNum, rettype="gbwithparts", retmode="text")
	contents = file.readlines()

	# initialize parsing regex, variables, and lists #
	CDS = "\s+CDS(\s)\s+"
	id = "\s+/protein_id="
	gb = []

	org_name = ""
	accession = ""
	size = 0
	
	number_CDS = 0
	
	# Define a parsing class #
	class gene_obj:
		def __init__(self,start,stop,product,name,strand):
			self.start = start
			self.stop = stop
			self.product = product
			self.name = name
			self.strand = strand
		def set_protein(self,id):
			self.name = id
		def set_product(self,prod):
			self.product = prod
	
	class org_obj:
		def __init__(self,gi,accession,name,size,genes):
			self.gi = gi
			self.accession = accession
			self.name = name
			self.size = size
			self.genes = genes
	
	# Parse GenBank file #
	atGenes = 0
	for line in contents:
		if re.match(r"LOCUS(\s+)(\S+)(\s+)(\S+)(.+)",line):
			m = re.match(r"LOCUS(\s+)(\S+)(\s+)(\S+)(.+)",line)
			size = m.group(4)
		elif re.match(r"VERSION(\s+)(\S+)",line):
			m = re.match(r"VERSION(\s+)(\S+)",line)
			accession = m.group(2)
		elif re.match("FEATURES",line):
			atGenes = 1
		elif re.match(CDS,line) and atGenes == 1:
			number_CDS = number_CDS+1
			num_match = 4
			strand = 1
			if re.match(r".+join.+",line):
				m = re.match(r"(\D+)(\d+)(\D+)(\d+),1..(\d+)",line)
				num_match = 5
			else:			
				m = re.match(r"(\D+)(\d+)(\D+)(\d+)",line)
			if re.search(r"complement",line):
				strand = -1

			gb.append(gene_obj(m.group(2),m.group(num_match),"no product description","",strand))
		elif re.match(r"(\s+)(.)(product=)(.+)",line):
			prod = re.match(r"(\s+)(.)(product=)(.+)",line)
			product = str(prod.group(4))
			product = product.strip('\"')
			gb[number_CDS-1].set_product(product)	
		elif re.match(id,line):
			info = re.split('"',line)
			gb[number_CDS-1].set_protein(info[1])
	
	handle = Entrez.esummary(db="nucleotide", id=accession)
	record = Entrez.read(handle)
	handle.close()
	org_name= (record[0]["Title"])
	org_name = str(org_name)
	gi = (record[0]["Gi"])
	gi = str(gi)
	organism = org_obj(gi,accession,org_name,size,number_CDS)
	
	# connect and upload gene and organism information to database #
	conn = mysql.connector.connect(user='sblack22',password='278zTsV^',host='localhost',database='sblack22', use_unicode=False)
	curs = conn.cursor()
	
	qry = "INSERT INTO final_organism (gi,accession,name,size,num_genes) VALUES (%s,%s,%s,%s,%s)"
	curs.execute(qry,(organism.gi,organism.accession,organism.name,organism.size,organism.genes))
	
	for gene in gb:
		if gene.name == "":
			gene.name = "unnamed gene"
		geneAcc = organism.accession+" - ["+gene.start+":"+gene.stop+"]"	
		qry = "INSERT INTO final_genes (org_acc,geneNum,product,protein_id,strand,gstart,gstop) VALUES (%s,%s,%s,%s,%s,%s,%s)"
		curs.execute(qry,(organism.gi,geneAcc,gene.product,gene.name,gene.strand,gene.start,gene.stop))
	
	conn.commit()
	curs.close()
	conn.close()
