#!/usr/local/bin/python3

import sys
from Bio import Entrez

Entrez.email = "sblack22@jhu.edu"

### This module (short for error check) checks the user input against the Entrez module. If the user input is invalid, the module catches the
# exception and returns a value for the gi number which is interpreted by the final.cgi driver and handled accordingly. ###

def validate(accession):
	try:
		handle = Entrez.esummary(db="nucleotide", id=accession)
		record = Entrez.read(handle)
		handle.close()
		gi = (record[0]["Gi"])
		gi = str(gi)
	except RuntimeError:
		gi = 0
		return (gi)
	return gi
