#!/usr/bin/env python
# coding: utf-8
# Ce script formate les pages de la Wikiversité :
# 1) Il retire les clés de tri devenues inutiles.
# 2) Il complète les modèles {{Chapitre}} à partir des {{Leçon}}.
# 3) Ajoute {{Bas de page}}.
# Reste à faire :
# 4) Remplir les {{Département}} à remplir à partir des {{Leçon}}.
# 5) Compléter les {{Bas de page}} existants.

from __future__ import absolute_import, unicode_literals
import catlib, codecs, collections, datetime, os, re, socket, sys, urllib
from lib import *
import pywikibot
from pywikibot import *
from pywikibot import pagegenerators

# Global variables
debugLevel = 0
debugAliases = ['-debug', '-d']
for debugAlias in debugAliases:
    if debugAlias in sys.argv:
        debugLevel= 1
        sys.argv.remove(debugAlias)

fileName = __file__
if debugLevel > 0: print fileName
if fileName.rfind('/') != -1: fileName = fileName[fileName.rfind('/')+1:]
siteLanguage = fileName[:2]
if debugLevel > 1: print siteLanguage
siteFamily = fileName[3:]
siteFamily = siteFamily[:siteFamily.find('.')]
if debugLevel > 1: print siteFamily
site = pywikibot.Site(siteLanguage, siteFamily)
username = config.usernames[siteFamily][siteLanguage]

checkURL = False
fixTags = False
fixFiles = True
fixTemplates = False
addCategory = False


oldParameters = []
newParameters = []
oldParameters.append(u'numero')
newParameters.append(u'numéro')

# https://fr.wikiversity.org/wiki/Catégorie:Modèles_de_l'université
categorizingTemplates = []
categorizingTemplates.append(u'Faculté')
categorizingTemplates.append(u'Département')
categorizingTemplates.append(u'Cours')
categorizingTemplates.append(u'Leçon')
categorizingTemplates.append(u'Chapitre')
categorizingTemplates.append(u'Annexe')
categorizingTemplates.append(u'Quiz')

subPages = []
# {{leçon}}
subPages.append(u'Présentation de la leçon')
subPages.append(u'Objectifs')
subPages.append(u'Prérequis conseillés')
subPages.append(u'Référents')
subPages.append(u'Post-notions')
# {{cours}}
subPages.append(u'Présentation du cours')
subPages.append(u'Leçons')
subPages.append(u'Fiche')
subPages.append(u'Feuille d\'exercices')
subPages.append(u'Annexe')
subPages.append(u'Voir aussi')
# {{département}}
subPages.append(u'Présentation du département')
subPages.append(u'Leçons par thèmes')
subPages.append(u'Leçons par niveaux')
subPages.append(u'Contributeurs')

# {{faculté}}
subPages.append(u'Présentation de la faculté')
subPages.append(u'Départements')
subPages.append(u'Transverse')

# {{Chapitre}} parameters
'''
param = []
param.append(u'titre ') # espace pour disambiguiser
param.append(u'titre_leçon')
param.append(u'idfaculté')
param.append(u' leçon')
param.append(u'page')
param.append(u'numero')
param.append(u'précédent')
param.append(u'suivant')
param.append(u'align')
param.append(u'niveau')
'''


def treatPageByName(pageName):
    if debugLevel > 0: print u'------------------------------------'
    print(pageName.encode(config.console_encoding, 'replace'))
    summary = u'Formatage'
    page = Page(site, pageName)
    PageBegin = getContentFromPage(page, 'All')
    PageTemp = PageBegin
    PageEnd = '' # On sauvegarde la partie traitée d'une page provisoire dans une page finale jusqu'à disparition de la première

    PageTemp = globalOperations(PageTemp)
    if fixFiles: PageTemp = replaceFilesErrors(PageTemp)
    if fixTags: PageTemp = replaceDepretacedTags(PageTemp)
    if checkURL: PageTemp = hyperlynx(PageTemp)
        
    PageTemp = PageTemp.replace(u'[[Catégorie:{{PAGENAME}}|{{SUBPAGENAME}}]]', u'{{AutoCat}}')
    PageTemp = PageTemp.replace(u'[[Catégorie:{{BASEPAGENAME}}|{{SUBPAGENAME}}]]', u'{{AutoCat}}')
    PageTemp = PageTemp.replace(u'{{autoCat}}', u'{{AutoCat}}')
    if addCategory and pageName.find(u'/') != -1:
        subPageName = pageName[pageName.rfind(u'/')+1:]
        if debugLevel > 0: print subPageName
        if subPageName in subPages and PageTemp.find(u'[[Catégorie:') == -1 and PageTemp.find(u'{{AutoCat}}') == -1 and PageTemp.find(u'{{imprimable') == -1:
            PageTemp = PageTemp + u'\n\n{{AutoCat}}'
            summary = summary + u', [[Spécial:Pages non catégorisées]]'

    if page.namespace() == 0:
        # Remplacements consensuels (ex : numero -> numéro)
        if debugLevel > 1: print u' Balises désuètes <center>'
        ''' Solution 1 : bug d'inclusion dans les modèles (qui demandent "|1=")
        regex = ur'<div *style *= *"? *text\-align: *center;? *"? *>((?!div).*)</div>'
        if re.search(regex, PageTemp):
            PageTemp = re.sub(regex, ur'{{centrer|1=\1}}', PageTemp)
        regex = ur'<div *style *= *"? *text\-align: *right;? *"? *>((?!div).*)</div>'
        if re.search(regex, PageTemp):
            PageTemp = re.sub(regex, ur'{{droite|1=\1}}', PageTemp)
            Solution 2 : absconse
        regex = ur'<div *style *= *"? *text\-align: *center;? *"? *>({{[Ee]ncadre\|)((?!div).*)</div>'
        if re.search(regex, PageTemp):
            PageTemp = re.sub(regex, ur'\1class=center|\2', PageTemp)
            Solution 3 : modèle connu sur WP
        '''
        regex = ur'<div style *= *"text\-align: *center;">([^<]*(?:<(.*?)>|.)*[^<]*)</div>'
        if re.search(regex, PageTemp):
            summary += ', [[Modèle:centrer]]'
            PageTemp = re.sub(regex, ur'{{centrer|\1}}', PageTemp)

        # Fix parameters
        for p in range(1, len(oldParameters)-1):
            if PageTemp.find(u'{{' + temp[p] + u'|') != -1 or PageTemp.find(u'{{' + oldParameters[p] + u'}}') != -1:
                PageTemp = PageTemp[0:PageTemp.find(temp[p])] + newParameters[p] + PageTemp[PageTemp.find(temp[p])+len(temp[p]):]

        # http://fr.wikiversity.org/wiki/Catégorie:Modèle_mal_utilisé
        if fixTemplates == True:
            if PageTemp.find('{Chapitre') != -1 or PageTemp.find('{chapitre') != -1:
                    ''' Bug du modèle tronqué :
                    if re.compile('{Chapitre').search(PageTemp):
                            if re.compile('{Chapitre[.\n]*(\n.*align.*=.*\n)').search(PageTemp):
                                    i1 = re.search(u'{{Chapitre[.\n]*(\n.*align.*=.*\n)',PageTemp).end()
                                    i2 = re.search(u'(\n.*align.*=.*\n)',PageTemp[:i1]).start()
                                    PageTemp = PageTemp[:i2] + u'\n' + PageTemp[i1:]
                            PageEnd = PageTemp[0:PageTemp.find(u'{{Chapitre')+len(u'{{Chapitre')]
                            PageTemp = PageTemp[PageTemp.find(u'{{Chapitre')+len(u'{{Chapitre'):len(PageTemp)]
                    elif re.compile('{chapitre').search(PageTemp):
                            if re.compile('{chapitre[.\n]*(\n.*align.*=.*\n)').search(PageTemp):
                                    i1 = re.search(u'{{chapitre[.\n]*(\n.*align.*=.*\n)',PageTemp).end()
                                    i2 = re.search(u'(\n.*align.*=.*\n)',PageTemp[:i1]).start()
                                    PageTemp = PageTemp[:i2] + u'\n' + PageTemp[i1:]
                            PageEnd = PageTemp[0:PageTemp.find(u'{{chapitre')+len(u'{{chapitre')]
                            PageTemp = PageTemp[PageTemp.find(u'{{chapitre')+len(u'{{chapitre'):len(PageTemp)]

                            if re.compile('{{Chapitre[\n.]*(\n.*leçon.*=.*\n)').search(PageTemp):
                                    print "leçon1"
                            if re.compile('{{Chapitre.*\n.*\n.*(\n.*leçon.*=.*\n)').search(PageTemp):
                                    print "leçon2"
                            if re.compile('{{Chapitre.*\n.*\n.*\n.*(\n.*leçon.*=.*\n)').search(PageTemp):
                                    print "leçon3"
                            if re.compile('{{Chapitre[.\n]*(\n.*niveau.*=.*\n)').search(PageTemp):
                                    print "niveau"
                                    print re.compile('{{Chapitre[.\n]*(\n.*niveau.*=.*\n)').search(PageTemp)
                            if re.compile('{{Chapitre[.\n]*(\n.*précédent.*=.*\n)').search(PageTemp):
                                    print "précédent"
                            if re.compile('{{Chapitre[.\n]*(\n.*suivant.*=.*\n)').search(PageTemp):
                                    print "suivant"
                    else: # Pas de modèle chapitre
                            print u'Pas de chapitre dans :'
                            print (pageName.encode(config.console_encoding, 'replace'))
                            return
                    raw_input (PageTemp.encode(config.console_encoding, 'replace'))'''

                    Lecon = u''
                    # Majuscule
                    if PageTemp.find(u'Leçon') != -1 and PageTemp.find(u'Leçon') < 100:
                            PageTemp2 = PageTemp[PageTemp.find(u'Leçon'):len(PageTemp)]
                            Lecon = Valeur(u'Leçon',PageTemp)
                    # Minuscule
                    elif PageTemp.find(u'leçon') != -1 and PageTemp.find(u'leçon') < 100:
                            PageTemp2 = PageTemp[PageTemp.find(u'leçon'):len(PageTemp)]
                            Lecon = Valeur(u'leçon',PageTemp)
                    #raw_input (Lecon.encode(config.console_encoding, 'replace'))

                    if Lecon.find(u'|') != -1:
                            Lecon = Lecon[0:Lecon.find(u'|')]
                    while Lecon[0:1] == u'[':
                            Lecon = Lecon[1:len(Lecon)]
                    while Lecon[len(Lecon)-1:len(Lecon)] == u']':
                            Lecon = Lecon[0:len(Lecon)-1]
                    if (Lecon == u'../' or Lecon == u'') and pageName.find(u'/') != -1:
                            Lecon = pageName[0:pageName.rfind(u'/')]
                    #raw_input (Lecon.encode(config.console_encoding, 'replace'))

                    if Lecon != u'' and Lecon.find(u'.') == -1: 
                        page2 = Page(site,Lecon)
                        if page2.exists():
                            if page2.namespace() != 0 and page2.title() != u'User:JackBot/test': 
                                return
                            else:
                                try:
                                    PageLecon = page2.get()
                                except pywikibot.exceptions.NoPage:
                                    print "NoPage"
                                    return
                                except pywikibot.exceptions.IsRedirectPage:
                                    PageLecon = page2.getRedirectTarget().get()
                                except pywikibot.exceptions.LockedPage:
                                    print "Locked/protected page"
                                    return
                            #raw_input (PageLecon.encode(config.console_encoding, 'replace'))

                            # Majuscule
                            if PageLecon.find(u'{{Leçon') != -1:
                                if Valeur(u'Leçon',PageTemp) == u'':
                                    if PageTemp.find(u'Leçon') < PageTemp.find(u'}}') or PageTemp.find(u'Leçon') < PageTemp.find(u'}}'):
                                        if Valeur(u'Leçon',PageTemp) == u'':
                                            PageTemp2 = PageTemp[PageTemp.find(u'Leçon')+len(u'Leçon'):len(PageTemp)]
                                            PageTemp2 = PageTemp2[0:PageTemp2.find(u'\n')]
                                            while PageTemp2[len(PageTemp2)-1:len(PageTemp2)] == u' ' or PageTemp2[len(PageTemp2)-1:len(PageTemp2)] == u'\t':
                                                PageTemp2 = PageTemp2[0:len(PageTemp2)-1]
                                            if PageTemp2[len(PageTemp2)-1:len(PageTemp2)] == u'=':
                                                PageEnd = PageEnd + PageTemp[0:PageTemp.find(u'Leçon')+len(u'Leçon')+PageTemp2.find(u'=')+1] + page2.title()
                                                PageTemp = PageTemp[PageTemp.find(u'Leçon')+len(u'Leçon')+PageTemp2.find(u'=')+1:len(PageTemp)]
                                            else:
                                                print u'Signe égal manquant dans :'
                                                print PageTemp2[len(PageTemp2)-1:len(PageTemp2)]
                                    else:
                                        PageEnd = PageEnd + u'\n|Leçon=' + page2.title()
                                PageEnd = PageEnd + PageTemp
                                if PageLecon.find(u'niveau') != -1:
                                    PageTemp = PageLecon[PageLecon.find(u'niveau'):len(PageLecon)]
                                    if PageTemp.find(u'=') < PageTemp.find(u'\n') and PageTemp.find(u'=') != -1:
                                        if Valeur(u'niveau',PageLecon) != -1:
                                            PageTemp = PageEnd
                                            if PageTemp.find(u'{{Chapitre') != -1:
                                                PageEnd = PageTemp[0:PageTemp.find(u'{{Chapitre')+len(u'{{Chapitre')]
                                                PageTemp = PageTemp[PageTemp.find(u'{{Chapitre')+len(u'{{Chapitre'):len(PageTemp)]
                                            elif PageTemp.find(u'{{chapitre') != -1:
                                                PageEnd = PageTemp[0:PageTemp.find(u'{{chapitre')+len(u'{{chapitre')]
                                                PageTemp = PageTemp[PageTemp.find(u'{{chapitre')+len(u'{{chapitre'):len(PageTemp)]
                                            else: return
                                            if PageTemp.find(u'niveau') < PageTemp.find(u'}}') and PageTemp.find(u'niveau') != -1:
                                                PageTemp2 = PageTemp[PageTemp.find(u'niveau')+len(u'niveau'):len(PageTemp)]
                                                while PageTemp2[0:1] == " " or PageTemp2[0:1] == "=":
                                                    PageTemp2 = PageTemp2[1:len(PageTemp2)]
                                                if PageTemp2[0:PageTemp2.find(u'\n')] == u'':
                                                    PageEnd = PageEnd + PageTemp[0:PageTemp.find(u'niveau')+len(u'niveau')] + "=" + Valeur(u'niveau',PageLecon)
                                                    PageTemp = PageTemp2
                                                elif Valeur(u'niveau',PageLecon) != PageTemp2[0:PageTemp2.find(u'\n')]:
                                                    if debugLevel > 0:
                                                        print u'Différence de niveau dans ' + pageName.encode(config.console_encoding, 'replace') + u' : '
                                                        print Valeur(u'niveau',PageLecon)
                                                        print PageTemp2[0:PageTemp2.find(u'\n')].encode(config.console_encoding, 'replace')
                                            else:
                                                PageEnd = PageEnd + u'\n  | niveau      = ' + Valeur(u'niveau',PageLecon)
                                            #print (PageEnd.encode(config.console_encoding, 'replace'))
                                            #raw_input (PageTemp.encode(config.console_encoding, 'replace'))
                            # Minuscule
                            elif PageLecon.find(u'{{leçon') != -1:
                                if Valeur(u'leçon',PageTemp) == u'':
                                    if PageTemp.find(u'leçon') < PageTemp.find(u'}}') or PageTemp.find(u'leçon') < PageTemp.find(u'}}'):
                                        if Valeur(u'leçon',PageTemp) == u'':
                                            PageTemp2 = PageTemp[PageTemp.find(u'leçon')+len(u'leçon'):len(PageTemp)]
                                            PageTemp2 = PageTemp2[0:PageTemp2.find(u'\n')]
                                            while PageTemp2[len(PageTemp2)-1:len(PageTemp2)] == u' ' or PageTemp2[len(PageTemp2)-1:len(PageTemp2)] == u'\t':
                                                PageTemp2 = PageTemp2[0:len(PageTemp2)-1]
                                            if PageTemp2[len(PageTemp2)-1:len(PageTemp2)] == u'=':
                                                PageEnd = PageEnd + PageTemp[0:PageTemp.find(u'leçon')+len(u'leçon')+PageTemp2.find(u'=')+1] + page2.title()
                                                PageTemp = PageTemp[PageTemp.find(u'leçon')+len(u'leçon')+PageTemp2.find(u'=')+1:len(PageTemp)]
                                            else:
                                                print u'Signe égal manquant dans :'
                                                print PageTemp2[len(PageTemp2)-1:len(PageTemp2)]
                                    else:
                                        PageEnd = PageEnd + u'\n|leçon=' + page2.title()
                                PageEnd = PageEnd + PageTemp
                                PageTemp = u''
                                if PageLecon.find(u'niveau') != -1:
                                    niveauLecon = Valeur(u'niveau',PageLecon)
                                    print niveauLecon
                                    PageTemp = PageLecon[PageLecon.find(u'niveau'):len(PageLecon)]
                                    if PageTemp.find(u'=') < PageTemp.find(u'\n') and PageTemp.find(u'=') != -1:
                                        if niveauLecon != -1:
                                            PageTemp = PageEnd
                                            if PageTemp.find(u'{{Chapitre') != -1:
                                                PageEnd = PageTemp[0:PageTemp.find(u'{{Chapitre')+len(u'{{Chapitre')]
                                                PageTemp = PageTemp[PageTemp.find(u'{{Chapitre')+len(u'{{Chapitre'):len(PageTemp)]
                                            elif PageTemp.find(u'{{chapitre') != -1:
                                                PageEnd = PageTemp[0:PageTemp.find(u'{{chapitre')+len(u'{{chapitre')]
                                                PageTemp = PageTemp[PageTemp.find(u'{{chapitre')+len(u'{{chapitre'):len(PageTemp)]
                                            else: return
                                            if PageTemp.find(u'niveau') < PageTemp.find(u'}}') and PageTemp.find(u'niveau') != -1:
                                                PageTemp2 = PageTemp[PageTemp.find(u'niveau')+len(u'niveau'):len(PageTemp)]
                                                while PageTemp2[0:1] == " " or PageTemp2[0:1] == "=":
                                                    PageTemp2 = PageTemp2[1:len(PageTemp2)]
                                                niveauChapitre = PageTemp2[0:PageTemp2.find(u'\n')]
                                                if niveauChapitre == u'':
                                                    PageEnd = PageEnd + PageTemp[0:PageTemp.find(u'niveau')+len(u'niveau')] + "=" + niveauLecon
                                                    PageTemp = PageTemp2
                                                elif niveauChapitre != niveauLecon:
                                                    print u'Niveau du chapitre différent de celui de la leçon dans ' + pageName.encode(config.console_encoding, 'replace')
                                            else:
                                                PageEnd = PageEnd + u'\n|niveau=' + niveauLecon

                            PageEnd = PageEnd + PageTemp
                            PageTemp = u''
                            #raw_input (PageEnd.encode(config.console_encoding, 'replace'))

                            '''print Valeur(u'niveau',PageEnd)
                            print u'********************************************'
                            print Valeur(u'numéro',PageEnd)
                            print u'********************************************'
                            print Valeur(u'précédent',PageEnd)
                            print u'********************************************'
                            print Valeur(u'suivant',PageEnd)
                            raw_input(u'Fin de paramètres')'''
                            NumLecon = u''
                            PageTemp2 = u''
                            if Valeur(u'numéro',PageEnd) == u'' or Valeur(u'précédent',PageEnd) == u'' or Valeur(u'suivant',PageEnd) == u'':
                                if PageLecon.find(pageName) != -1:
                                        PageTemp2 = PageLecon[0:PageLecon.find(pageName)]    # Nécessite que le département ait un nom déifférent et que les leçons soient bien nommées différemment
                                elif PageLecon.find(pageName[pageName.rfind(u'/')+1:len(pageName)]) != -1:
                                        PageTemp2 = PageLecon[0:PageLecon.find(pageName[pageName.rfind(u'/')+1:len(pageName)])]
                                if PageTemp2 != u'':
                                        while PageTemp2[len(PageTemp2)-1:len(PageTemp2)] == " " or PageTemp2[len(PageTemp2)-1:len(PageTemp2)] == "=" or PageTemp2[len(PageTemp2)-1:len(PageTemp2)] == "[" or PageTemp2[len(PageTemp2)-1:len(PageTemp2)] == "{" or PageTemp2[len(PageTemp2)-1:len(PageTemp2)] == "|" or PageTemp2[len(PageTemp2)-2:len(PageTemp2)] == "{C" or PageTemp2[len(PageTemp2)-2:len(PageTemp2)] == "{c" or PageTemp2[len(PageTemp2)-2:len(PageTemp2)] == "{L" or PageTemp2[len(PageTemp2)-2:len(PageTemp2)] == "{l":
                                                PageTemp2 = PageTemp2[0:len(PageTemp2)-1]
                                        if PageTemp2.rfind(u' ') > PageTemp2.rfind(u'|'):
                                                NumLecon = PageTemp2[PageTemp2.rfind(u' ')+1:len(PageTemp2)]
                                        else:
                                                NumLecon = PageTemp2[PageTemp2.rfind(u'|')+1:len(PageTemp2)]
                                        #print (PageTemp2.encode(config.console_encoding, 'replace'))                
                                        if NumLecon != u'' and NumLecon != u'département':
                                            # Le numéro de la leçon permet de remplir les champs : |numéro=, |précédent=, |suivant=
                                            if Valeur(u'numéro',PageEnd) == u'':
                                                if PageEnd.find(u'numéro') == -1:
                                                    PageTemp = PageEnd
                                                    PageEnd = PageTemp[0:PageTemp.find(u'{{Chapitre')+len(u'{{Chapitre')]
                                                    PageTemp = PageTemp[PageTemp.find(u'{{Chapitre')+len(u'{{Chapitre'):len(PageTemp)]
                                                    if PageTemp.find(u'numéro') < PageTemp.find(u'}}') and PageTemp.find(u'numéro') != -1:
                                                        PageTemp2 = PageTemp[PageTemp.find(u'numéro')+len(u'numéro'):len(PageTemp)]
                                                        while PageTemp2[0:1] == " " or PageTemp2[0:1] == "=":
                                                            PageTemp2 = PageTemp2[1:len(PageTemp2)]
                                                        PageEnd = PageEnd + PageTemp[0:PageTemp.find(u'numéro')+len(u'numéro')] + "=" + NumLecon
                                                        PageTemp = PageTemp2
                                                    else:
                                                        PageEnd = PageEnd + u'\n|numéro=' + NumLecon
                                                    PageEnd = PageEnd + PageTemp
                                                    PageTemp = u''
                                            if Valeur(u'précédent',PageEnd) == u'' and NumLecon    == 1:
                                                PageTemp = PageEnd
                                                PageEnd = PageTemp[0:PageTemp.find(u'{{Chapitre')+len(u'{{Chapitre')]
                                                PageTemp = PageTemp[PageTemp.find(u'{{Chapitre')+len(u'{{Chapitre'):len(PageTemp)]
                                                if PageTemp.find(u'précédent') < PageTemp.find(u'}}') and PageTemp.find(u'précédent') != -1:
                                                    PageTemp2 = PageTemp[PageTemp.find(u'précédent')+len(u'précédent'):len(PageTemp)]
                                                    while PageTemp2[0:1] == " " or PageTemp2[0:1] == "=":
                                                        PageTemp2 = PageTemp2[1:len(PageTemp2)]
                                                    PageEnd = PageEnd + PageTemp[0:PageTemp.find(u'précédent')+len(u'précédent')] + "=" + NumLecon
                                                    PageTemp = PageTemp2
                                                else:
                                                    PageEnd = PageEnd + u'\n|précédent=' + NumLecon
                                                PageEnd = PageEnd + PageTemp
                                                PageTemp = u''                                
                                            elif Valeur(u'précédent',PageEnd) == u'' and Valeur(str(int(NumLecon)-1),PageLecon) != u'':
                                                PageTemp = PageEnd
                                                PageEnd = PageTemp[0:PageTemp.find(u'{{Chapitre')+len(u'{{Chapitre')]
                                                PageTemp = PageTemp[PageTemp.find(u'{{Chapitre')+len(u'{{Chapitre'):len(PageTemp)]
                                                if PageTemp.find(u'précédent') < PageTemp.find(u'}}') and PageTemp.find(u'précédent') != -1:
                                                    PageTemp2 = PageTemp[PageTemp.find(u'précédent')+len(u'précédent'):len(PageTemp)]
                                                    while PageTemp2[0:1] == " " or PageTemp2[0:1] == "=":
                                                        PageTemp2 = PageTemp2[1:len(PageTemp2)]
                                                    PageEnd = PageEnd + PageTemp[0:PageTemp.find(u'précédent')+len(u'précédent')] + "=" + Valeur(str(int(NumLecon)-1),PageLecon)
                                                    PageTemp = PageTemp2
                                                else:
                                                    PageEnd = PageEnd + u'\n|précédent=' + Valeur(str(int(NumLecon)-1),PageLecon)
                                                PageEnd = PageEnd + PageTemp
                                                PageTemp = u''
                                            if Valeur(u'suivant',PageEnd) == u'' and Valeur(str(int(NumLecon)+1),PageLecon) != u'':                    
                                                PageTemp = PageEnd
                                                PageEnd = PageTemp[0:PageTemp.find(u'{{Chapitre')+len(u'{{Chapitre')]
                                                PageTemp = PageTemp[PageTemp.find(u'{{Chapitre')+len(u'{{Chapitre'):len(PageTemp)]
                                                if PageTemp.find(u'suivant') < PageTemp.find(u'}}') and PageTemp.find(u'suivant') != -1:
                                                    PageTemp2 = PageTemp[PageTemp.find(u'suivant')+len(u'suivant'):len(PageTemp)]
                                                    while PageTemp2[0:1] == " " or PageTemp2[0:1] == "=":
                                                        PageTemp2 = PageTemp2[1:len(PageTemp2)]
                                                    PageEnd = PageEnd + PageTemp[0:PageTemp.find(u'suivant')+len(u'suivant')] + "=" + Valeur(str(int(NumLecon)+1),PageLecon)
                                                    PageTemp = PageTemp2
                                                else:
                                                    if PageTemp.find(u'précédent') != -1:
                                                        PageTemp2 = PageTemp[PageTemp.find(u'précédent'):len(PageTemp)]
                                                        PageEnd = PageEnd + PageTemp[0:PageTemp.find(u'précédent')+PageTemp2.find(u'\n')] + u'\n|suivant=' + Valeur(str(int(NumLecon)+1),PageLecon)
                                                        PageTemp = PageTemp[PageTemp.find(u'précédent')+PageTemp2.find(u'\n'):len(PageTemp)]
                                                    else:
                                                        PageEnd = PageEnd + u'\n|suivant=' + Valeur(str(int(NumLecon)+1),PageLecon)
                                                PageEnd = PageEnd + PageTemp
                                                PageTemp = u''
                        else: # Pas de leçon
                            print u'Pas de leçon : '
                            print (Lecon.encode(config.console_encoding, 'replace'))
                            print u'dans : '
                            print (pageName.encode(config.console_encoding, 'replace'))
                            #raw_input ('Attente')
                        PageEnd = PageEnd + PageTemp
                        PageTemp = u''
            elif PageTemp.find(u'{Leçon') != -1 or PageTemp.find(u'{leçon') != -1:
                # Evaluations
                page2 = Page(site,u'Discussion:' + pageName)
                if page2.exists():
                    try:
                        PageDisc = page2.get()
                    except pywikibot.exceptions.NoPage:
                        print "NoPage"
                        return
                    except pywikibot.exceptions.IsRedirectPage:
                        print "Redirect page"
                        return
                    except pywikibot.exceptions.LockedPage:
                        print "Locked/protected page"
                        return
                else: 
                    PageDisc = u''
                if PageDisc.find(u'{{Évaluation') == -1 and PageDisc.find(u'{{évaluation') == -1: savePage(page2, u'{{Évaluation|idfaculté=' + Valeur(u'idfaculté',PageTemp) + u'|avancement=?}}\n' + PageDisc, u'Ajout d\'évaluation inconnue')    

                # Synchronisations avec les niveaux des départements, et les évaluations des onglets Discussion:
                #...
            PageEnd = PageEnd + PageTemp

            # Bas de page
            if (PageEnd.find(u'{{Chapitre') != -1 or PageEnd.find(u'{{chapitre') != -1) and PageEnd.find(u'{{Bas de page') == -1 and PageEnd.find(u'{{bas de page') == -1:
                idfaculte = u''
                precedent = u''
                suivant = u''
                if PageEnd.find(u'idfaculté') != -1:
                    PageTemp = PageEnd[PageEnd.find(u'idfaculté'):len(PageEnd)]
                    idfaculte = PageTemp[0:PageTemp.find(u'\n')]    # pb si tout sur la même ligne, faire max(0,min(PageTemp.find(u'\n'),?))
                    if PageEnd.find(u'précédent') != -1:
                        PageTemp = PageEnd[PageEnd.find(u'précédent'):len(PageEnd)]
                        precedent = PageTemp[0:PageTemp.find(u'\n')]
                    if PageEnd.find(u'suivant') != -1:
                        PageTemp = PageEnd[PageEnd.find(u'suivant'):len(PageEnd)]
                        suivant = PageTemp[0:PageTemp.find(u'\n')]
                    PageEnd = PageEnd + u'\n\n{{Bas de page|' + idfaculte + u'\n|' + precedent + u'\n|' + suivant + u'}}'

            # Exercices (pb http://fr.wikiversity.org/w/index.php?title=Allemand%2FVocabulaire%2FFormes_et_couleurs&diff=354352&oldid=354343)
            '''PageTemp = PageEnd
            PageEnd = u''
            while PageEnd.find(u'{{CfExo') != -1 or PageEnd.find(u'{{cfExo') != -1:
                PageTemp = PageEnd[
                if 
                |exercice=[[
                /Exercices/
                /quiz/
            PageEnd = PageEnd + PageTemp'''

    PageEnd = PageEnd + PageTemp
    PageTemp = u''

    if debugLevel > 1: raw_input (u'--------------------------------------------------------------------------------------------')
    if PageBegin != PageEnd: savePage(page, PageEnd, summary)


#*** Wikiversity functions ***
def Valeur(Mot, Page):
    #raw_input(u'Bug http://fr.wikiversity.org/w/index.php?title=Initiation_%C3%A0_l%27arithm%C3%A9tique/PGCD&diff=prev&oldid=386685')
    if re.search(u'\n *' + Mot + u' *=', Page):
        niveau = re.sub(u'\n *' + Mot + u' *=()[\n|\||}|{]', ur'$1', Page)
        if debugLevel > 0: raw_input(niveau)
        #return
    '''
    if Page.find(u' ' + Mot) != Page.find(Mot)-1 and Page.find(u'|' + Mot) != Page.find(Mot)-1: # Pb du titre_leçon
        PageTemp2 = Page[Page.find(Mot)+len(Mot):len(Page)]
    else:
        PageTemp2 = Page
    if PageTemp2.find(Mot) == -1:
        return u''
    else:
        PageTemp2 = PageTemp2[PageTemp2.find(Mot)+len(Mot):len(PageTemp2)]
        PageTemp2 = PageTemp2[0:PageTemp2.find(u'\n')]
        if PageTemp2.find (u'{{C|') != -1:        
            PageTemp2 = PageTemp2[PageTemp2.find (u'{{C|')+4:len(PageTemp2)]
            PageTemp2 = u'[[../' + PageTemp2[0:PageTemp2.find (u'|')] + u'/]]'
        while PageTemp2[0:1] == u' ' or PageTemp2[0:1] == u'\t' or PageTemp2[0:1] == u'=':
            PageTemp2 = PageTemp2[1:len(PageTemp2)]
        if PageTemp2[0:3] == u'[[/':        
            PageTemp2 = u'[[..' + PageTemp2[2:len(PageTemp2)]
        return PageTemp2
    '''


p = PageProvider(treatPageByName, site, debugLevel)
setGlobals(debugLevel, site, username)
def main(*args):
    if len(sys.argv) > 1:
        if debugLevel > 1: print sys.argv
        if sys.argv[1] == u'-test':
            treatPageByName(u'User:' + username + u'/test')
        elif sys.argv[1] == u'-test2':
            treatPageByName(u'User:' + username + u'/test2')
        elif sys.argv[1] == u'-page' or sys.argv[1] == u'-p':
            treatPageByName(u"Fonctions_d'une_variable_réelle/Continuité")
        elif sys.argv[1] == u'-file' or sys.argv[1] == u'-txt':
            p.pagesByFile(u'src/lists/articles_' + siteLanguage + u'_' + siteFamily + u'.txt')
        elif sys.argv[1] == u'-dump' or sys.argv[1] == u'-xml':
            #regex = u'{{[Ee]ncadre *\|[^}]*text-align: center'
            regex = u'text-align'
            if len(sys.argv) > 2: regex = sys.argv[2]
            p.pagesByXML(siteLanguage + siteFamily + '\-.*xml', regex)
        elif sys.argv[1] == u'-u':
            p.pagesByUser(u'User:' + username)
        elif sys.argv[1] == u'-search' or sys.argv[1] == u'-s' or sys.argv[1] == u'-r':
            if len(sys.argv) > 2:
                p.pagesBySearch(sys.argv[2])
            else:
                p.pagesBySearch(u'insource:text-align: center', namespaces = [0])
        elif sys.argv[1] == u'-link' or sys.argv[1] == u'-l' or sys.argv[1] == u'-template' or sys.argv[1] == u'-m':
            p.pagesByLink(u'Modèle:Encadre')
        elif sys.argv[1] == u'-category' or sys.argv[1] == u'-cat':
            afterPage = u''
            if len(sys.argv) > 2: afterPage = sys.argv[2]
            p.pagesByCat(u'Catégorie:Pages utilisant des liens magiques ISBN', namespaces = None, afterPage = afterPage)
            p.pagesByCat(u'Catégorie:Pages avec ISBN invalide', namespaces = None, afterPage = afterPage)
        elif sys.argv[1] == u'-redirects':
            p.pagesByRedirects()
        elif sys.argv[1] == u'-all':
           p.pagesByAll()
        elif sys.argv[1] == u'-RC':
            while 1:
                p.pagesByRCLastDay()
        elif sys.argv[1] == u'-nocat':
            global addCategory
            addCategory = True
            p.pagesBySpecialNotCategorized()
        elif sys.argv[1] == u'-lint':
            p.pagesBySpecialLint()
        elif sys.argv[1] == u'-extlinks':
            p. pagesBySpecialLinkSearch('www.dmoz.org')
        else:
            # Format: http://tools.wmflabs.org/jackbot/xtools/public_html/unicode-HTML.php
            treatPageByName(sys.argv[1])
    else:
        while 1:
            p.pagesByRC()

if __name__ == "__main__":
    main(sys.argv)
