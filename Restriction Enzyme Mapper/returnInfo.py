#!/usr/local/bin/python3

import mysql.connector

### This is a database retrieval module. This grabs all information from the organism and genes tables in the database and returns a list of objects ###

def organism(gi):

	# Define organism object to fit the database schema #
	class organism:
		def __init__(self,gi,accession,name,size,num_genes):
			self.gi = gi
			self.accession = accession
			self.name = name
			self.size = size
			self.num_genes = num_genes

	org = []

	conn = mysql.connector.connect(user='sblack22',password='278zTsV^',host='localhost',database='sblack22', use_unicode=False)
	curs = conn.cursor()
	if gi == "ALL":
		qry = "select * from final_organism"
		curs.execute(qry)
	else:
		qry = "select * from final_organism where gi = %s"
		curs.execute(qry,(gi,))
	
	all_results = curs.fetchall()

	conn.commit()
	curs.close()
	conn.close()

	for(gi,accession,name,size,num_genes) in all_results:
		gi = gi.decode('utf-8')
		accession = accession.decode('utf-8')
		name = name.decode('utf')
		org.append(organism(gi,accession,name,size,num_genes))

	return org

def genes(gi):

	# Define gene object to fit the database schema #
	class gene:
		def __init__(self,org_acc,geneNum,product,protein_id,strand,gstart,gstop):
			self.org_acc = org_acc
			self.geneNum = geneNum
			self.product = product
			self.protein_id = protein_id
			self.strand = strand
			self.gstart = gstart
			self.gstop = gstop

	genes = []

	conn = mysql.connector.connect(user='sblack22',password='278zTsV^',host='localhost',database='sblack22', use_unicode=False)
	curs = conn.cursor()

	qry = "select * from final_genes where org_acc = %s order by gstop asc"
	curs.execute(qry,(gi,))
	all_results = curs.fetchall()

	conn.commit()
	curs.close()
	conn.close()

	for(org_acc,geneNum,product,protein_id,strand,gstart,gstop) in all_results:
		org_acc = org_acc.decode('utf-8')
		geneNum = geneNum.decode('utf-8')
		product = product.decode('utf-8')
		protein_id = protein_id.decode('utf-8')
		strand = strand
		gstart = gstart
		gstop = gstop
		genes.append(gene(org_acc,geneNum,product,protein_id,strand,gstart,gstop))

	return genes
