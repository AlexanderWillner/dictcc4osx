#!/usr/bin/python
# -*- coding: utf-8 -*-
#  Warning:
#  This is my first dive into Python. There is much room for improvement. :)

import re
import string
import codecs

# initialize dictionary
dictionary = {}

# adds a term to the dictionary
def addTerm(key, term, definition):
	global dictionary

	# remove incompatible characters
	term = term.replace("<", "&lt;").replace(">", "&gt;")
	definition = definition.replace("<", "&lt;").replace(">", "&gt;")
		
	translation = {"de" : term, "en" : definition}
	
	if dictionary.has_key(key):
		entry = dictionary[key]
		entry.append(translation)
	else:
		entry = [translation]  # an entry is a list of translations
	
	dictionary[key] = entry;

# "huhu(m)" ->  huhu
# removes braces
# TODO: doesn't work with: "hallo welt) l (hallo)"
# TODO: there must be a simpler solution to this :)
def removeBraces(term, left, right):
	while 1:
		start = term.find(left)
		end = term.find(right)
		if (start!=-1)and(end!=-1)and(start<end):
			newTerm = term[:start] + term[end+1:]
			term = newTerm
		else:
			break
	return term		

# normalizes an entry so that insignificant variations of the same
# word fit into the same directory entry
# TODO: Apfel == Äpfel would be great :)
def normalize(term):
	term = removeBraces(term, "{", "}");
	term = removeBraces(term, "[", "]");
	term = term.lower()
	return term

def readFile(fileName):
	global dictionary
	lines=0
	comments=0
	errors=0
	warnings=0
	
	# prepare regular expressions for comments
	p_comment = re.compile('#', re.IGNORECASE)
	
	try:
		input = codecs.open(fileName, encoding='utf-8')
		print 'Processing "'+fileName+'"'
	except IOError:
		print '*** File "' + fileName + '" not found.' 
	else: 
		for line in input:
			lines=lines+1
			# trow away comments
			if (p_comment.match(line)) or (len(line)<=2):
				comments=comments+1
				continue

			# split entry into english and german part
			data = line.split("\t", 1);

			if len(data)!=2:
				errors = errors+1
				continue
		
			left = data[0].strip();
			right = data[1].strip();
			dictEntry = normalize(left);
	
			if len(dictEntry)<2:
				# some weird translations are completely enclosed in []
				warnings = warnings+1
				print("Warning: '%s' normalization is empty! (Line %s)" % (left.encode('utf-8'), lines))
				continue;
				
			# ok... add to dictionary
			# additional string processing is done while writing
			addTerm(dictEntry, left, right);

		input.close
		print("Read %s lines with %s comments. Warnings: %s Errors: %s" % ( lines, comments, warnings, errors) )
		print("%s entries in dictionary. " % len(dictionary))


# {m} -> ", der"
# {n} -> ", das"
# {f} -> ", die"
# TODO: Aachen {n} -> der Aachen looks strange
def reformatString(data):
	if data.find("{m}")>0:
		data = data.replace("{m}","")
		data = "der "+data
	if data.find("{n}")>0:
		data = data.replace("{n}","")
		data = "das "+data
	if data.find("{f}")>0:
		data = data.replace("{f}","")
		data = "die "+data
	if data.find("{pl}")>0:
		data = data.replace("{pl}","{plural}")
	return data


def makeEntry(ID, translations):
	# unique entry id
	ID = unicode("id"+str(ID))

	title = unicode(translations[0]["de"])
	index = unicode(removeBraces(translations[0]["de"],"{", "}").replace('"', "'"));

	# get translations
	translation_de = []
	translation_en = []
	for translation in translations:
		#translation_de.append(stringEncode(translation["de"]))
		#translation_en.append(stringEncode(translation["en"]))
		translation_de.append(translation["de"])
		translation_en.append(translation["en"])
			
	# create html entry
	s =   '<d:entry id="' + ID + '" d:title="' + title +'" >\n'
	s = s+'<d:index d:value="' + index +'"/>\n'
	s = s+'<h1>'+reformatString(title)+'</h1>\n'
	
	# add english translations
	for word in translation_en:
		s = s + word+"<br />\n"
	s = s+'</d:entry>\n'

	s = unicode(s)
	return s.encode('utf-8')

# Generate XML output
def writeFile(fileName):
	global dictionary
	output = file(fileName, "w")
	print 'Generating XML output. This may take some time...'
	output.write(u'''<?xml version="1.0" encoding="UTF-8"?>
<d:dictionary xmlns="http://www.w3.org/1999/xhtml" xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng">\n''')
	
	# front matter
	output.write(u'''<d:entry id="front_back_matter" d:title="Vorwort">
	<h1>dict.cc - Dictionary</h1>
	<h2>Front/Back Matter</h2>
	<div>
		This is a front matter page of the sample dictionary.<br/><br/>
	</div>
	</d:entry>\n''')
	
	# process each dictionary term
	count = 0
	for term in dictionary.keys():
		output.write(makeEntry(count, dictionary[term]))
		count = count + 1
	
	output.write(u'''</d:dictionary>\n''');
	output.close
	print ("Wrote %s entries to '%s'" % (count, fileName) )

# main()
print("dict.cc to Dictionary.app XML Converter")
print("input2xml.py dict.cc to Apple Dictionary Plugin Script")
print("by Philipp Brauner/Lipflip 2008, licensed under the GLP")
print("   lipflip@lipflip.org")
print("   http://lipflip.org/blog/2008/02/dictcc-plugin-os-xs-dictionaryapp")

# add a personal entry
addTerm ("Lipflip" , "Lipflip", "lipflip.org");
addTerm ("dict.cc" , "dict.cc", "dict.cc");

readFile("de-en.txt");
readFile("en-de.txt");

# a bit dump
if len(dictionary)<10:
	print 'Error: No data to process. You need to get at least one translation database'
	print 'from "http://www1.dict.cc/translation_file_request.php".'
	print 'Rename the file(s) to "de-en.txt" or "en-de.txt" and start over.'
else:
	writeFile("MyDictionary.xml");
