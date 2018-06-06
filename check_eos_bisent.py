#!/usr/bin/python
#-*- coding: UTF-8 -*-
import sys
import string
import re

reload(sys)
sys.setdefaultencoding("UTF-8")

def main(strRefFile):
    hangul = re.compile('[^a-zA-Z0-9�꽦-�뀭媛�-�옡]+')
    nLineNum = 0
    lstRef = {}
    
  # read reference file
    fref = open(strRefFile, 'r')
    while 1:
        nLineNum = nLineNum + 1
        strLine = fref.readline()
        if not strLine:
            break
        strLine = strLine.strip('\r\n')
	nTab = strLine.find('\t')
        if nTab < 0:
            continue
        strSrc = strLine[0:nTab].strip()
        strTgt = strLine[nTab+1:].strip()
        strKey = hangul.sub('',strTgt) #?
        if len(strSrc) <= 0 or len(strTgt) <= 0 or len(strKey) <= 0:
            continue
        print strKey
        lstRef[strKey] = strTgt  #?
       
# read working file for recovery of special character  
    nLineNum = 0
    while 1:
        try:
            strLine = raw_input("")
        except Exception:
            break
        if not strLine:
            break
        nLineNum = nLineNum + 1
        if (nLineNum % 100) == 0:
            sys.stderr.write("\r{0} lines progressed...".format(nLineNum))
        line = strLine
        nTab = line.find("\t")
        if nTab < 0:
            sys.stderr.write("{0} Line Error : [{1}]\n".format(nLineNum, line))
            continue
        strSrc2 = line[0:nTab].strip()
        strTgt2 = line[nTab+1:].strip()
        if len(strSrc2) <= 0 or len(strTgt2) <= 0:
            sys.stderr.write("{0} Line Error : [{1}]\n".format(nLineNum, line))
            #continue
        strKey = hangul.sub('',strTgt2)
        
# starting  recovery processing 
        strDiff="FALSE"
        if len(strSrc2) <= 0:
            strDiff="TRUE"
        #print ">>",lstRef[strKey][-1],"<<" 
        if (strKey in lstRef) == True:
            #not found end of sentence symbol and add  EOS symbol 
            if strTgt2[-1] != lstRef[strKey][-1] and (lstRef[strKey][-1] == "." or lstRef[strKey][-1] == "?" or lstRef[strKey][-1] == "!"):
               strTgt2 += lstRef[strKey][-1]
               print  ">>", strTgt2, "<<" 
            if strTgt2 != lstRef[strKey]:
                strDiff="TRUE" # not same with original
            strTgt2 = lstRef[strKey]
            if len(strSrc2) > 0 and strSrc2[-1] != lstRef[strKey][-1] and strSrc2[-1] != "." and strSrc2[-1] != "?" and strSrc2[-1] != "!" and (lstRef[strKey][-1] == "." or lstRef[strKey][-1] == "?" or lstRef[strKey][-1] == "!"):
                strSrc2 += lstRef[strKey][-1]
        
# print out the recovered file.
        sys.stdout.write("{0}\t{1}\t{2}\n".format(strSrc2, strTgt2, strDiff))
    sys.stderr.write("\n")
    fref.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Example : python copy-period.py reference-file < input-file > output-file"
    else:
        main(sys.argv[1])
