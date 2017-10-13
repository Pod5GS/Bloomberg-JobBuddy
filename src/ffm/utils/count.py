#!/usr/bin/env python3

import argparse, csv, sys, collections

from common import *

if len(sys.argv) == 1:
    sys.argv.append('-h')

parser = argparse.ArgumentParser()
parser.add_argument('csv_path', type=str)
args = vars(parser.parse_args())

counts = collections.defaultdict(lambda : [0, 0, 0])

for i, row in enumerate(csv.DictReader(open(args['csv_path'])), start=1):
    label = row['Label']
    for j in range(1, 8):
        field = 'C{0}'.format(j)
        value = row[field]
        if label == '0':
            counts[field+','+value][0] += 1
        else:
            counts[field+','+value][1] += 1
        counts[field+','+value][2] += 1
    if i % 1000000 == 0:
        sys.stderr.write('{0}m\n'.format(int(i/1000000)))
#print(counts)
#print "**********************************"
print('Field,Value,Neg,Pos,Total,Ratio')
#print sorted(counts.items(), key=lambda x: x[1][2])
for key, (neg, pos, total) in sorted(counts.items(), key=lambda x: x[1][2]):
    #print "key: ", key
    #print "neg: ", neg
    #print "total: ", total
    #print "pos: ", pos
    if total < 0:
        continue
    ratio = round(float(pos)/total, 5)
    print(key+','+str(neg)+','+str(pos)+','+str(total)+','+str(ratio))
