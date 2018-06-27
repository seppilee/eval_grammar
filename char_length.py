
#!/usr/bin/python
#-*- coding: UTF-8 -*-
import sys
import re
import collections

#utf-8 encoding for python2
reload(sys)
sys.setdefaultencoding("UTF-8")


line_num = 0
char_length = 0
sum_char_length = 0
char_lengths = []
threshold = 150

def count_letters(word):
    return len(filter(lambda x: x not in " ", word))

for line in sys.stdin:
    line = re.sub("\r|\n|\uFEFF", "", line)
    char_length = len(line.decode('utf8')) - line.count(' ')
    line_num += 1
    sum_char_length += char_length
    char_lengths.append(char_length)

    if line_num % 10000 == 0 :
        print "processing:", line_num
    #print line, "\t", char_length

c = collections.Counter()
c.update(char_lengths)
#long_sent = [c[el] for el in c.elements() if el >= 100 and el <150]

long_sent1 = len([x for x in char_lengths if x <= 50])
long_sent2 = len([x for x in char_lengths if x > 50 and x <= 100])
long_sent3 = len([x for x in char_lengths if x > 100 and x <= 150])
long_sent4 = len([x for x in char_lengths if x > threshold])

print ''.rjust(10), "***************"
print ''.rjust(10), "Length Summary"
print ''.rjust(10), "***************"

print "total lines:", line_num, "\tmean length:", sum_char_length/line_num, \
      "\tmax length:", max(char_lengths), "\tlong sentence(>",threshold,"):",long_sent4

print ""
print ''.rjust(10), "***************"
print ''.rjust(10), 'Most common(1-5):'
print ''.rjust(10), "***************"
for letter, count in c.most_common(5):
    print 'chars: %s, count: %3d' % (letter, count)

print ""
print ''.rjust(10), "********************"
print ''.rjust(10), "proportion of length"
print ''.rjust(10), "********************"
print "chars( 1 - 50):", long_sent1, "(", 100 * float(long_sent1)/float(line_num), "%)"
print "chars(50 - 100):", long_sent2, "(", 100 * float(long_sent2)/float(line_num), "%)"
print "chars(100- 150):", long_sent3, "(", 100 * float(long_sent3)/float(line_num), "%)"
