#!/usr/bin/env python

import re
import sys

### This module takes a text file of restriction enzymes formatted from addgene.org/mol-bio-reference/restriction-enzymes/ and configures them into
# a readable list that can be uploaded to the database. K stands for 'keto', M stands for 'amino', R stands for 'purine', and Y stands for
# 'pyrimidine'. This method is designed to create a list of all possible digestion sequences for enzymes with multiple sequence entries
# (sequences with K, M, R, or Y) ###

enzymes = {}

filename = sys.argv[1]

file = open(filename,'r')
idx = 0
for line in file:
	line = line.strip()
	print line
	line = line.replace("*"," ")
	print ("step 1: "+line)
	words = re.split('\s+',line,1)
	print ("step 2: "+words[0]+" - "+words[1])
	seq = words[1].replace(" ","")
	print ("step 3: "+words[0]+" - "+seq+"\n")
	idx = idx+1
	enzymes.update({seq:words[0]})

file.close()

newfile = open('newenzymes.txt','w')

temp = enzymes
	
for key in list(enzymes):
	print "iter"
	if "K" in key:
		newkey = key
		newkey = newkey.replace("K","G")
		enzymes.update({newkey:enzymes[key]})
		newkey = key
		newkey = newkey.replace("K","T")
		enzymes.update({newkey:enzymes[key]})
		enzymes.pop(key)

for key in list(enzymes):
	print "iter"
	if "M" in key:
		newkey = key
		newkey = newkey.replace("M","A")
		enzymes.update({newkey:enzymes[key]})
		newkey = key
		newkey = newkey.replace("M","C")
		enzymes.update({newkey:enzymes[key]})
		enzymes.pop(key)

for key in list(enzymes):
	print "iter"
	if "R" in key:
		newkey = key
		newkey = newkey.replace("R","A")
		enzymes.update({newkey:enzymes[key]})
		newkey = key
		newkey = newkey.replace("R","G")
		enzymes.update({newkey:enzymes[key]})
		enzymes.pop(key)

for key in list(enzymes):
	print "iter"
	if "Y" in key:
		newkey = key
		newkey = newkey.replace("Y","C")
		enzymes.update({newkey:enzymes[key]})
		newkey = key
		newkey = newkey.replace("Y","T")
		enzymes.update({newkey:enzymes[key]})
		enzymes.pop(key)

for key in enzymes:
	print "val: "+enzymes[key]
	print "key: "+key
	newfile.write(enzymes[key]+"\t"+key+"\n")

newfile.close()
