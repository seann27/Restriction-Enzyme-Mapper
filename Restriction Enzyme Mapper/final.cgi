#!/usr/local/bin/python3

import mysql.connector
import re
import parseFasta
import parseGb
import returnInfo
import analyzeResults4
import errChk
from Bio import Entrez
import jinja2
import cgi, cgitb
cgitb.enable()

### This is the driver module which executes and handles all user submissions. This includes uploading new organisms to the database, analyzing and
# displaying digestion sites for that organism, and displaying gene information for that organism. ###

Entrez.email = "sblack22@jhu.edu"

# print html header #
print("Content-type: text/html\n")
print()

# grab submitted form information #
form = cgi.FieldStorage(keep_blank_values=1)

# if user uploads a new accession number #
if "upload" in form:
	term = form["acc"].value
	term = term.strip()
	accession = term.upper()
	
	# validate user input #
	gi = errChk.validate(accession)
	errorMsg = ""
	msg = ""

	# if valid #
	if int(gi) > 0:
		# Perform SQL Query on accession number #
		conn = mysql.connector.connect(user='sblack22',password='278zTsV^',host='localhost',database='sblack22', use_unicode=False)
		curs = conn.cursor()

		qry = "select * from final_organism where gi = %s"
		curs.execute(qry,(gi,))
		all_results = curs.fetchall()

		# if new accession number, populate database #
		if len(all_results) == 0:
			parseFasta.run(accession,gi)
			parseGb.run(accession)

		conn.commit()
		curs.close()
		conn.close()
		msg = '"'+accession+'"'+" successfully uploaded."
	else:
		errorMsg = '"'+accession+'"'+" is an invalid accession number"

	# grab list of organisms in database #
	organisms = returnInfo.organism("ALL")

	# initialize template loader #
	templateLoader = jinja2.FileSystemLoader( searchpath="./templates" )
	env = jinja2.Environment(loader=templateLoader)
	template = env.get_template('index.html')

	# load index html page #
	print(template.render(organisms=organisms,msg=msg,errorMsg=errorMsg))

# if user wants to analyze existing organism for digestion sites #
elif "analyze" in form:
	gi = form["accession"].value

	# analyze data #
	comSites,optSites = analyzeResults4.analyze(gi)
	lengthCom = len(comSites)	
	lengthOpt = len(optSites)

	# initialize template loader
	templateLoader = jinja2.FileSystemLoader( searchpath="./templates" )
	env = jinja2.Environment(loader=templateLoader)
	template = env.get_template('siteTable.html')

	# load siteTable html page #
	print(template.render(comSites=comSites,optSites=optSites,lengthCom=lengthCom,lengthOpt=lengthOpt,gi=gi))

# if user wants to display gene information #
else:
	gi = form["accession"].value	
	# analyze data #
	genes = returnInfo.genes(gi)
	numGenes = len(genes)

	# initialize template loader
	templateLoader = jinja2.FileSystemLoader( searchpath="./templates" )
	env = jinja2.Environment(loader=templateLoader)
	template = env.get_template('genes.html')

	# load genes html page #
	print(template.render(genes=genes,numGenes=numGenes))
