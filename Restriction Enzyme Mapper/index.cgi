#!/usr/local/bin/python3

import re
import returnInfo
import jinja2
import cgi, cgitb
cgitb.enable()

### Populates the index HTML page with a list of organisms in the database which have been mapped and uploaded ###

# html processing #
print("Content-type: text/html\n")
print()

# grab list of organisms in database #
organisms = returnInfo.organism("ALL")

# initialize template loader #
templateLoader = jinja2.FileSystemLoader( searchpath="./templates" )
env = jinja2.Environment(loader=templateLoader)
template = env.get_template('index.html')

# load html with organisms #
print(template.render(organisms=organisms))
