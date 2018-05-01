# AS410712_FinalProject
Final Project for Advanced Practical Computing Concepts

ABOUT

This program is called the Restriction Enzyme Mapper. Full source code can be found here:

https://github.com/seann27/AS410712_FinalProject/tree/master/Restriction%20Enzyme%20Mapper

A demo of the web application can be currently accessed by going to:

bfx.eng.jhu.edu/sblack22/Restriction_Enzyme_Mapper/index.cgi

This web application takes an accession number input by the user and maps all sites of digestion from the restriction
sites stored in the database assuming the user has queried a plasmid. The application has the ability to show a table
of genes that the organism has (from the GenBank file) as well as the ability to analyze the organism's genome for
optimal sites of digestion and the enzymes involved in the digestion process.

REQUIREMENTS

Uses the Entrez module from the Biopython library

http://biopython.org/DIST/docs/api/Bio.Entrez-module.html

The Entrez module is used to grab FASTA and GenBank files, as well as the GI number from a user entered accession number

Other Modules:

sys

re

mysql.connector

jinja2

cgi

cgitb

Version: Python3

Database: MySQL

The database has been optimized to run ~40 restriction sites against plasmids of size 2.5 million base pairs. A gateway timeout
error might occur if the user increases the amount of enzymes or the plasmid size or the loading time takes more than the 
default 60 seconds before this error is thrown.

INSTRUCTIONS - USING THE APPLICATION

The user will need to input a valid plasmid accession number in the text field next to the upload button. Valid accession numbers refer to organisms which have FASTA and GenBank entries in NCBI's nucleotide database. This will add the organism to the
list of organisms currently in the database. This list will be displayed on the index.html page. Each organism entry will have a radio
button next to it. If the user wishes to view the table of annotated genes, or perform an analysis and view a table of compatible
restriction sites (sites which do not interfere with coding regions), the user has the ability to select either or. The user will be
able to upload an accession number on any page during the application. If an invalid accession number is entered, the application will not upload the accession and will notify the user that their input is invalid.

INSTRUCTIONS - GENERATING ENZYMES IN DB

A key component to this web application utilizes a list of restriction enzymes stored in the database. The current database
uses enzymes marked with an asterisk from the current web page from addgene:
https://www.addgene.org/mol-bio-reference/restriction-enzymes/

The database currently has 39 enzymes stored in the database. If the user wants to add/change enzymes, please follow the next set of instructions:

The user must format a text file with the name of the enzyme, followed by a tab, followed by a sequence. An example is:

"EcoRI *	G AATTC"

(taken from addgene)

The user needs to use the same SNP notation (Nucleotide codes) as addgene if they wish to specify nucleotides which can be
multiple residues.

K	(Keto) - G or T

M	(Amino) - A or C

R	(Purine) - A or G

Y	(Pyrimidine) - C or T

One sequence per line is a requirement. Once the file has been formatted, the script utilities/cleanup.py must be ran with
the file as an argument.

./utilities/cleanup.py myfile.txt

This will generate a file, newenzymes.txt, with all the formatted enzymes (and generate all possible sequences if nucleotide codes are used for SNPs). Once this is generated, the user will need to run the script:

./utilities/uploadEnzymes.py

Which will upload the enzymes to the database.

INSTRUCTIONS - RESETTING THE DATABASE

If the user wishes to delete all entries in the database, simply run the script:

./utilities/deleteOrg.py

This will remove all entries and their genes from the database. This is mainly used for testing/debugging purposes.




