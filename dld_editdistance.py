#!/usr/bin/python
#-*- coding: UTF-8 -*-

import sys
import re

reload(sys)
sys.setdefaultencoding("UTF-8")

def ksyl_split(s):
	
	o = ""
	
	sI = [u"ㄱ", u"ㄲ", u"ㄴ", u"ㄷ", u"ㄸ", u"ㄹ", u"ㅁ", u"ㅂ", u"ㅃ", u"ㅅ", u"ㅆ", u"ㅇ", u"ㅈ", u"ㅉ", u"ㅊ", u"ㅋ", u"ㅌ", u"ㅍ", u"ㅎ"]
	sV = [u"ㅏ", u"ㅐ", u"ㅑ", u"ㅒ", u"ㅓ", u"ㅔ", u"ㅕ", u"ㅖ", u"ㅗ", u"ㅘ", u"ㅙ", u"ㅚ", u"ㅛ", u"ㅜ", u"ㅝ", u"ㅞ", u"ㅟ", u"ㅠ", u"ㅡ", u"ㅢ", u"ㅣ"]
	sF = [u"", u"ㄱ", u"ㄲ", u"ㄳ", u"ㄴ", u"ㄵ", u"ㄶ", u"ㄷ", u"ㄹ", u"ㄺ", u"ㄻ", u"ㄼ", u"ㄽ", u"ㄾ", u"ㄿ", u"ㅀ", u"ㅁ", u"ㅂ", u"ㅄ", u"ㅅ", u"ㅆ", u"ㅇ", u"ㅈ", u"ㅊ", u"ㅋ", u"ㅌ", u"ㅍ", u"ㅎ"]
     
    #german
	"""
	sI  = ['g', 'gg', 'n', 'd', 'dd', 'r', 'm', 'b', 'bb', 's', 'ss', '', 'j', 'jj', 'c', 'k', 't', 'p', 'h']
	sV = ['a', 'ae', 'ya', 'yae', 'eo', 'e', 'yeo', 'ye', 'o', 'wa', 'wae', 'oe', 'yo', 'u', 'weo', 'we', 'wi', 'yu', 'eu', 'yi', 'i']
	sF  = ['', 'g', 'gg', 'gs', 'n', 'nj', 'nh', 'd', 'l', 'lg', 'lm', 'lb', 'ls', 'lt', 'lp', 'lh', 'm', 'b', 'bs', 's', 'ss', 'ng', 'j', 'c', 'k', 't', 'p', 'h']
	"""


	for c in s:
		u = ord(c)
		if u < 0xAC00 or u > 0xD7A3:
			o += c
			continue
		u -= 0xAC00
		f = u % 28
		v = (u - f) / 28 % 21
		i = ((u - f) / 28 - v) / 21
		o += sI[i]
		if v != 18:
			o += sV[v]
		if f > 0:
			o += sF[f]
	return o

def dld(a, b, wI = 1, wD = 1, wS = 1): # weighted Damerau–Levenshtein distance with backtrace
	d = [[0 for i in range(len(b) + 1)] for j in range(len(a) + 1)]
	for i in range(len(a) + 1):
		d[i][0] = i
	for j in range(len(b) + 1):
		d[0][j] = j

	for i in range(1, len(a) + 1):
		for j in range(1, len(b) + 1):
			d[i][j] = min(
				d[i][j - 1] + 1, # insertion
				d[i - 1][j] + 1, # deletion
				d[i - 1][j - 1] + (a[i - 1] != b[j - 1])) # substitution
			if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]: # swap
				d[i][j] = min(d[i][j], d[i - 2][j - 2] + 1)

	x, y, z = 0, 0, 0
	while x < len(a) or y < len(b): # backtrace and weighting
		i, j = -1, 0
		if x < len(a) and (i < 0 or j >= d[x + 1][y]):
			i, j = 0, d[x + 1][y]
		if y < len(b) and (i < 0 or j >= d[x][y + 1]):
			i, j = 1, d[x][y + 1]
		if x < len(a) and y < len(b) and (i < 0 or j >= d[x + 1][y + 1]):
			i, j = 2, d[x + 1][y + 1]
		if i == 0:
			z += (j - d[x][y]) * wD
			x += 1
		elif i == 1:
			z += (j - d[x][y]) * wI
			y += 1
		elif i == 2:
			z += (j - d[x][y]) * wS
			x, y = x + 1, y + 1
		#sys.stderr.write("(%d, %d) : %d\n" % (x, y, z))
	
	sys.stderr.write("dld(%s, %s) = %d\n" % (a, b, z))
	for i in range(len(a) + 1):
		if i == 0:
			sys.stderr.write("       ")
			for j in range(len(b)):
				sys.stderr.write("%s " % b[j])
			sys.stderr.write("\n   ")
		for j in range(len(b) + 1):
			if i > 0 and j == 0:
				sys.stderr.write("%s " % a[i - 1])
			sys.stderr.write("%2d " % d[i][j])
		sys.stderr.write("\n")
	
	return z
	# return d[len(a) - 1][len(b) - 1] # without weight

for line in sys.stdin:
	line = line.decode(encoding = "UTF-8")
	line = re.sub(" |\r|\n|\uFEFF", "", line)
	tkn = line.split("\t")
	#sys.stdout.write("%s\t%s\t" % (tkn[0], tkn[1]))
	# sys.stdout.write("\n")
	a = re.sub("\(.+?\)", "", tkn[0])
	x = ""
	y = 100
	for i in range(len(tkn[1])):
		for j in range(i + 1, len(tkn[1]) + 1):
			b = tkn[1][i:j]
			print ksyl_split(a)
			z = dld(a, b, 1, 1, 1)
			# sys.stdout.write("%s\t%d\n" % (b, z))
			if y > z or y == z and len(b) > len(x):
				x = b
				y = z
	sys.stdout.write("%s\t%d\n" % (x, y))
