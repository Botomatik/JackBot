﻿#!/usr/bin/env python
# coding: utf-8	

def HTMLUnicode(PageHS):
	PageHS = PageHS.replace(u'&#32;', u'&nbsp;')
	PageHS = PageHS.replace(u'&#224;', u'à')
	PageHS = PageHS.replace(u'&#225;', u'á')
	PageHS = PageHS.replace(u'&#226;', u'â')
	PageHS = PageHS.replace(u'&#259;', u'ă')
	PageHS = PageHS.replace(u'&#228;', u'ä')
	PageHS = PageHS.replace(u'&#261;', u'ą')
	PageHS = PageHS.replace(u'&#261;&#769;', u'ą́ ')
	PageHS = PageHS.replace(u'&#231;', u'ç')
	PageHS = PageHS.replace(u'&#269;', u'č')
	PageHS = PageHS.replace(u'&#240;', u'ð')
	PageHS = PageHS.replace(u'&#233;', u'é')
	PageHS = PageHS.replace(u'&#232;', u'è')
	PageHS = PageHS.replace(u'&#234;', u'ê')
	PageHS = PageHS.replace(u'&#235;', u'ë')
	PageHS = PageHS.replace(u'&#235;', u'ë')
	PageHS = PageHS.replace(u'&#817;', u'e̱')
	PageHS = PageHS.replace(u'&#281;', u'ę')
	PageHS = PageHS.replace(u'&#287;', u'ğ')
	PageHS = PageHS.replace(u'&#688;', u'ʰ')
	PageHS = PageHS.replace(u'&#238;', u'î')
	PageHS = PageHS.replace(u'&#237;', u'í')
	PageHS = PageHS.replace(u'&#239;', u'ï')
	PageHS = PageHS.replace(u'&#299;', u'ī')
	PageHS = PageHS.replace(u'&#305;', u'ı')
	PageHS = PageHS.replace(u'&#303;', u'į')
	PageHS = PageHS.replace(u'&#241;', u'ñ')
	PageHS = PageHS.replace(u'&#242;', u'ò')
	PageHS = PageHS.replace(u'&#243;', u'ó')
	PageHS = PageHS.replace(u'&#244;', u'ô')
	PageHS = PageHS.replace(u'&#246;', u'ö')
	PageHS = PageHS.replace(u'&#353;', u'š')
	PageHS = PageHS.replace(u'&#351;', u'ş')
	PageHS = PageHS.replace(u'&#249;', u'ù')
	PageHS = PageHS.replace(u'&#250;', u'ú')
	PageHS = PageHS.replace(u'&#7913;', u'ứ')
	PageHS = PageHS.replace(u'&#251;', u'û')
	PageHS = PageHS.replace(u'&#252;', u'ü')
	PageHS = PageHS.replace(u'&#365;', u'ŭ')
	PageHS = PageHS.replace(u'&#223;', u'ß')
	PageHS = PageHS.replace(u'&#380;', u'ż')
	PageHS = PageHS.replace(u'&#700;', u'\'')
	PageHS = PageHS.replace(u'&#35;', u'#')
	# grec
	PageHS = PageHS.replace(u'&#973;', u'ύ')
	PageHS = PageHS.replace(u'&#954;', u'κ')
	PageHS = PageHS.replace(u'&#955;', u'λ')
	PageHS = PageHS.replace(u'&#969;', u'ω')
	PageHS = PageHS.replace(u'&#968;', u'ψ')
	return PageHS
	  