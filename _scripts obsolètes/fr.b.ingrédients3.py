﻿#!/usr/bin/env python
# coding: utf-8
# Ce script ajoute les ingrédients dans leurs catégories

# Importation des modules
import catlib, pagegenerators, os, codecs, urllib
from wikipedia import *

# Déclaration
mynick = "JackBot"
language = "fr"
family = "wikibooks"
site = getSite(language,family)
summary = u'[[Discussion:Recettes de cuisine|Ajout des catégories des ingrédients sans hyperlien]]'

# Modification du wiki
def modification(PageHS):
	page = Page(site,PageHS)
	if page.namespace() != 0: return
	try:
		PageTemp = page.get()
	except wikipedia.NoPage:
		print "NoPage"
		return
	except wikipedia.IsRedirectPage:
		print "Redirect page"
		return
	while PageTemp.find(u'oeuf') != -1:
		PageTemp = PageTemp[0:PageTemp.find(u'oeuf')] + u'œuf' + PageTemp[PageTemp.find(u'oeuf')+len(u'oeuf'):len(PageTemp)]
	PagesIngr = open(u'articles_listed.txt', 'r')
	while 1:
		PageIngr = PagesIngr.readline()
		fin = PageIngr.find("\t")
		PageIngr = PageIngr[0:fin]
		if PageIngr == '': break
		if PageTemp.find(PageIngr) != -1:
			if PageTemp.find(u'[[' + PageIngr) != -1:
				PageTemp2 = PageTemp[PageTemp.find(u'[[' + PageIngr):len(PageTemp)]
				PageTemp = PageTemp[0:PageTemp.find(u'[[' + PageIngr)] + u'{{i|' + PageTemp[PageTemp.find(u'[[' + PageIngr)+2:PageTemp.find(u'[[' + PageIngr)+PageTemp2.find(u']]')] + u'}}' + PageTemp[PageTemp.find(u'[[' + PageIngr)+PageTemp2.find(u']]')+2:len(PageTemp)]
			elif PageTemp.find(u'[[w:' + PageIngr) != -1:
				PageTemp2 = PageTemp[PageTemp.find(u'[[w:' + PageIngr):len(PageTemp)]
				PageTemp = PageTemp[0:PageTemp.find(u'[[w:' + PageIngr)] + u'{{i|' + PageTemp[PageTemp.find(u'[[w:' + PageIngr)+4:PageTemp.find(u'[[w:' + PageIngr)+PageTemp2.find(u']]')] + u'}}' + PageTemp[PageTemp.find(u'[[w:' + PageIngr)+PageTemp2.find(u']]')+2:len(PageTemp)]
			elif PageTemp.find(u'[[wikt:' + PageIngr) != -1:
				PageTemp2 = PageTemp[PageTemp.find(u'[[wikt:' + PageIngr):len(PageTemp)]
				PageTemp = PageTemp[0:PageTemp.find(u'[[wikt:' + PageIngr)] + u'{{i|' + PageTemp[PageTemp.find(u'[[wikt:' + PageIngr)+7:PageTemp.find(u'[[wikt:' + PageIngr)+PageTemp2.find(u']]')] + u'}}' + PageTemp[PageTemp.find(u'[[wikt:' + PageIngr)+PageTemp2.find(u']]')+2:len(PageTemp)]
			elif PageTemp.find(u' ' + PageIngr + u'\n') != -1:
				PageTemp = PageTemp[0:PageTemp.find(u' ' + PageIngr + u'\n')+1] + u'{{i|' + PageIngr + u'}}' + PageTemp[PageTemp.find(u' ' + PageIngr + u'\n')+len(u' ' + PageIngr + u'\n')-1:len(PageTemp)]				
			elif PageTemp.find(u' ' + PageIngr + u' ') != -1:
				PageTemp = PageTemp[0:PageTemp.find(u' ' + PageIngr + u' ')+1] + u'{{i|' + PageIngr + u'}}' + PageTemp[PageTemp.find(u' ' + PageIngr + u' ')+len(u' ' + PageIngr + u' ')-1:len(PageTemp)]
			elif PageTemp.find(PageIngr + u's') != -1:
				if PageTemp.find(u' ' + PageIngr + u's\n') != -1:
					PageTemp = PageTemp[0:PageTemp.find(u' ' + PageIngr + u's\n')+1] + u'{{i|' + PageIngr + u'}}s' + PageTemp[PageTemp.find(u' ' + PageIngr + u's\n')+len(u' ' + PageIngr + u's\n')-1:len(PageTemp)]				
				elif PageTemp.find(u' ' + PageIngr + u's ') != -1:
					PageTemp = PageTemp[0:PageTemp.find(u' ' + PageIngr + u's ')+1] + u'{{i|' + PageIngr + u'}}s' + PageTemp[PageTemp.find(u' ' + PageIngr + u's ')+len(u' ' + PageIngr + u's ')-1:len(PageTemp)]
	PagesIngr.close()

	PageEnd = PageTemp
	while PageEnd.find(u'[[../Ingrédients/') != -1:
		PageTemp = PageEnd[PageEnd.find(u'[[../Ingrédients/'):len(PageEnd)]
		PageEnd = PageEnd[0:PageEnd.find(u'[[../Ingrédients/')] + u'{{i|' + PageEnd[PageEnd.find(u'[[../Ingrédients/')+PageTemp.find(u'|')+1:PageEnd.find(u'[[../Ingrédients/')+PageTemp.find(u']')] + u'}}' + PageEnd[PageEnd.find(u'[[../Ingrédients/')+PageTemp.find(u']')+2:len(PageEnd)]
	while PageEnd.find(u'[[Livre_de_cuisine/Ingrédients/') != -1:
		PageTemp = PageEnd[PageEnd.find(u'[[Livre_de_cuisine/Ingrédients/'):len(PageEnd)]
		PageEnd = PageEnd[0:PageEnd.find(u'[[Livre_de_cuisine/Ingrédients/')] + u'{{i|' + PageEnd[PageEnd.find(u'[[Livre_de_cuisine/Ingrédients/')+PageTemp.find(u'|')+1:PageEnd.find(u'[[Livre_de_cuisine/Ingrédients/')+PageTemp.find(u']')] + u'}}' + PageEnd[PageEnd.find(u'[[Livre_de_cuisine/Ingrédients/')+PageTemp.find(u']')+2:len(PageEnd)]
	while PageEnd.find(u'[[Livre de cuisine/Ingrédients/') != -1:
		PageTemp = PageEnd[PageEnd.find(u'[[Livre de cuisine/Ingrédients/'):len(PageEnd)]
		PageEnd = PageEnd[0:PageEnd.find(u'[[Livre de cuisine/Ingrédients/')] + u'{{i|' + PageEnd[PageEnd.find(u'[[Livre de cuisine/Ingrédients/')+PageTemp.find(u'|')+1:PageEnd.find(u'[[Livre de cuisine/Ingrédients/')+PageTemp.find(u']')] + u'}}' + PageEnd[PageEnd.find(u'[[Livre de cuisine/Ingrédients/')+PageTemp.find(u']')+2:len(PageEnd)]

	# Majuscules, parenthèses, et doublons
	if PageEnd.find(u'{{i|') == -1: return
	PageTemp = PageEnd[PageEnd.find(u'{{i|'):len(PageEnd)]
	PageEnd = PageEnd[0:PageEnd.find(u'{{i|')]
	while PageTemp.find(u'{{i|') != -1:
		PageTemp = PageTemp[4:len(PageTemp)]
		if PageTemp.find(u'|') < PageTemp.find(u'}') and PageTemp.find(u'|') != -1:
			mot = PageTemp[0:PageTemp.find(u'|')]
			if mot.find(u' (') != -1: mot = mot[0:mot.find(u' (')]
			PageTemp = mot.lower() + PageTemp[PageTemp.find(u'|'):len(PageTemp)]
		else:
			mot = PageTemp[0:PageTemp.find(u'}')]
			if mot.find(u' (') != -1: mot = mot[0:mot.find(u' (')]
			PageTemp = mot.lower() + PageTemp[PageTemp.find(u'}'):len(PageTemp)]
		if PageTemp.find(u'|') == -1: break
		if PageTemp[0:PageTemp.find(u'|')] == PageTemp[PageTemp.find(u'|')+1:PageTemp.find(u'}}')]:
			PageTemp = PageTemp[0:PageTemp.find(u'|')] + PageTemp[PageTemp.find(u'}}'):len(PageTemp)]
		if PageTemp.find(u'{{i|') != -1:
			PageEnd = PageEnd + u'{{i|' + PageTemp[0:PageTemp.find(u'{{i|')]
			PageTemp = PageTemp[PageTemp.find(u'{{i|'):len(PageTemp)]
	PageEnd = PageEnd + u'{{i|' + PageTemp
	
	# Elisions
	while PageEnd.find(u'{{i|eau}}') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|eau}}')] + u'eau' + PageEnd[PageEnd.find(u'{{i|eau}}')+len(u'{{i|eau}}'):len(PageEnd)] 
	while PageEnd.find(u'{{i|huile d’olive') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|huile d’olive')] + u'{{i|huile d\'olive' + PageEnd[PageEnd.find(u'{{i|huile d’olive')+len(u'{{i|huile d’olive'):len(PageEnd)] 
	while PageEnd.find(u'{{i|sel}}') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|sel}}')] + u'sel' + PageEnd[PageEnd.find(u'{{i|sel}}')+len(u'{{i|sel}}'):len(PageEnd)] 
	while PageEnd.find(u'{{i|Sel}}') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|Sel}}')] + u'Sel' + PageEnd[PageEnd.find(u'{{i|Sel}}')+len(u'{{i|Sel}}'):len(PageEnd)] 
	while PageEnd.find(u'{{i|sel alimentaire|sel}}') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|sel alimentaire|sel}}')] + u'sel' + PageEnd[PageEnd.find(u'{{i|sel alimentaire|sel}}')+len(u'{{i|sel alimentaire|sel}}'):len(PageEnd)] 
	while PageEnd.find(u'{{i|Sel alimentaire|Sel}}') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|Sel alimentaire|Sel}}')] + u'Sel' + PageEnd[PageEnd.find(u'{{i|Sel alimentaire|Sel}}')+len(u'{{i|Sel alimentaire|Sel}}'):len(PageEnd)] 
	while PageEnd.find(u'{{i|Sel alimentaire|salé}}') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|Sel alimentaire|salé}}')] + u'salé' + PageEnd[PageEnd.find(u'{{i|Sel alimentaire|salé}}')+len(u'{{i|Sel alimentaire|salé}}'):len(PageEnd)] 
	while PageEnd.find(u'{{i|Sel alimentaire|salée}}') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|Sel alimentaire|salée}}')] + u'salée' + PageEnd[PageEnd.find(u'{{i|Sel alimentaire|salée}}')+len(u'{{i|Sel alimentaire|salée}}'):len(PageEnd)] 
	while PageEnd.find(u'{{i|Œuf (cuisine)') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|Œuf (cuisine)')+4] + u'œuf' + PageEnd[PageEnd.find(u'{{i|Œuf (cuisine)')+len(u'{{i|Œuf (cuisine)'):len(PageEnd)] 
	while PageEnd.find(u'{{i|huile}} d\'{{i|olive}}') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|huile}} d\'{{i|olive}}')+4] + u'huile d\'olive' + PageEnd[PageEnd.find(u'{{i|huile}} d\'{{i|olive}}')+len(u'{{i|huile}} d\'{{i|olive}}')-2:len(PageEnd)] 
	while PageEnd.find(u'{{i|hu') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|hu')+4] + u'\'=oui|' + PageEnd[PageEnd.find(u'{{i|hu')+4:len(PageEnd)]
	while PageEnd.find(u'{{i|a') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|a')+4] + u'\'=oui|' + PageEnd[PageEnd.find(u'{{i|a')+4:len(PageEnd)]
	while PageEnd.find(u'{{i|A') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|A')+4] + u'\'=oui|' + PageEnd[PageEnd.find(u'{{i|A')+4:len(PageEnd)]
	while PageEnd.find(u'{{i|e') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|e')+4] + u'\'=oui|' + PageEnd[PageEnd.find(u'{{i|e')+4:len(PageEnd)]
	while PageEnd.find(u'{{i|E') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|E')+4] + u'\'=oui|' + PageEnd[PageEnd.find(u'{{i|E')+4:len(PageEnd)]
	while PageEnd.find(u'{{i|i') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|i')+4] + u'\'=oui|' + PageEnd[PageEnd.find(u'{{i|i')+4:len(PageEnd)]
	while PageEnd.find(u'{{i|I') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|I')+4] + u'\'=oui|' + PageEnd[PageEnd.find(u'{{i|I')+4:len(PageEnd)]
	while PageEnd.find(u'{{i|o') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|o')+4] + u'\'=oui|' + PageEnd[PageEnd.find(u'{{i|o')+4:len(PageEnd)]
	while PageEnd.find(u'{{i|O') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|O')+4] + u'\'=oui|' + PageEnd[PageEnd.find(u'{{i|O')+4:len(PageEnd)]
	while PageEnd.find(u'{{i|u') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|u')+4] + u'\'=oui|' + PageEnd[PageEnd.find(u'{{i|u')+4:len(PageEnd)]
	while PageEnd.find(u'{{i|U') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|U')+4] + u'\'=oui|' + PageEnd[PageEnd.find(u'{{i|U')+4:len(PageEnd)]
	while PageEnd.find(u'{{i|y') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|y')+4] + u'\'=oui|' + PageEnd[PageEnd.find(u'{{i|y')+4:len(PageEnd)]
	while PageEnd.find(u'{{i|Y') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|Y')+4] + u'\'=oui|' + PageEnd[PageEnd.find(u'{{i|Y')+4:len(PageEnd)]
	while PageEnd.find(u'{{i|œ') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|œ')+4] + u'\'=oui|' + PageEnd[PageEnd.find(u'{{i|œ')+4:len(PageEnd)]
	while PageEnd.find(u'{{i|Œ') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|Œ')+4] + u'\'=oui|' + PageEnd[PageEnd.find(u'{{i|Œ')+4:len(PageEnd)]
	while PageEnd.find(u'{{i|à') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|à')+4] + u'\'=oui|' + PageEnd[PageEnd.find(u'{{i|à')+4:len(PageEnd)]
	while PageEnd.find(u'{{i|À') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|À')+4] + u'\'=oui|' + PageEnd[PageEnd.find(u'{{i|À')+4:len(PageEnd)]
	while PageEnd.find(u'{{i|â') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|â')+4] + u'\'=oui|' + PageEnd[PageEnd.find(u'{{i|â')+4:len(PageEnd)]
	while PageEnd.find(u'{{i|Â') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|Â')+4] + u'\'=oui|' + PageEnd[PageEnd.find(u'{{i|Â')+4:len(PageEnd)]
	while PageEnd.find(u'{{i|é') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|é')+4] + u'\'=oui|' + PageEnd[PageEnd.find(u'{{i|é')+4:len(PageEnd)]
	while PageEnd.find(u'{{i|É') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|É')+4] + u'\'=oui|' + PageEnd[PageEnd.find(u'{{i|É')+4:len(PageEnd)]
	while PageEnd.find(u'{{i|è') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|è')+4] + u'\'=oui|' + PageEnd[PageEnd.find(u'{{i|è')+4:len(PageEnd)]
	while PageEnd.find(u'{{i|È') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|È')+4] + u'\'=oui|' + PageEnd[PageEnd.find(u'{{i|È')+4:len(PageEnd)]
	while PageEnd.find(u'{{i|ê') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|ê')+4] + u'\'=oui|' + PageEnd[PageEnd.find(u'{{i|ê')+4:len(PageEnd)]
	while PageEnd.find(u'{{i|Ê') != -1:
		PageEnd = PageEnd[0:PageEnd.find(u'{{i|Ê')+4] + u'\'=oui|' + PageEnd[PageEnd.find(u'{{i|Ê')+4:len(PageEnd)]
	# Conclusion
	if PageEnd != page.get():
		#print (PageEnd.encode(config.console_encoding, 'replace'))
		#if raw_input("Sauver (o/n)") == u'n' or raw_input("Sauver (o/n)") == u'no' or raw_input("Sauver (o/n)") == u'non': return
		try:
			page.put(PageEnd, summary)
		except pywikibot.EditConflict:
			print "Conflict"
			return
		except wikipedia.NoPage:
			print "NoPage"
			return
		except wikipedia.IsRedirectPage:
			print "Redirect page"
			return
		except wikipedia.LockedPage:
			print "Locked/protected page"
			return	

# Traitement d'un fichier
def crawlerFile(source):
	if source:
		PagesHS = open(source, 'r')
		while 1:
			PageHS = PagesHS.readline()
			fin = PageHS.find("\t")
			PageHS = PageHS[0:fin]
			if PageHS == '': break
			print (PageHS)
			modification(PageHS)
		PagesHS.close()
		
# Traitement d'une catégorie
def crawlerCat(category):
	cat = catlib.Category(site, category)
	pages = cat.articlesList(False)
	for Page in pagegenerators.PreloadingGenerator(pages,100):
		modification(Page.title())
	subcat = cat.subcategories(recurse = True)
	for subcategory in subcat:
		pages = subcategory.articlesList(False)
		for Page in pagegenerators.PreloadingGenerator(pages,100):
			modification(Page.title())
	
# Traitement des modifications récentes
def crawlerRC():
	RC = pagegenerators.RecentchangesPageGenerator()
	for Page in pagegenerators.PreloadingGenerator(RC,100):
		modification(Page.title())

# Traitement des pages liées
def crawlerLink(pagename):
	#pagename = unicode(arg[len('-links:'):], 'utf-8')
	page = wikipedia.Page(site, pagename)
	gen = pagegenerators.ReferringPageGenerator(page)
	#gen =  pagegenerators.NamespaceFilterPageGenerator(gen, namespaces)
	for Page in pagegenerators.PreloadingGenerator(gen,100):
		modification(Page.title())

# Lancement
TraitementFile = crawlerFile('articles_list.txt')
#TraitementCategory = crawlerCat(u'Catégorie:Recettes de cuisine')
#TraitementLink = crawlerLink(u'Livre de cuisine/Ingrédients/Lait')
#while 1:
#	TraitementRC = crawlerRC()
#raw_input("Jackpot")

'''
cd "C:\Program Files\wamp\www\Personnel\mybot\pywikipedia"
python fr.b.ingrédients3.py
'''
