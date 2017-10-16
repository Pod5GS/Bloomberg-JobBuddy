#!/usr/bin/env python3

import argparse, csv, sys

from common import *

if len(sys.argv) == 1:
    sys.argv.append('-h')

from common import *

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--nr_bins', type=int, default=int(100))
parser.add_argument('-t', '--threshold', type=int, default=int(10))
parser.add_argument('csv_path', type=str)
#parser.add_argument('gbdt_path', type=str)
parser.add_argument('out_path', type=str)
args = vars(parser.parse_args())

def gen_hashed_fm_feats(feats, nr_bins):
    feats = ['{0}:{1}:1'.format(field-1, hashstr(feat, nr_bins)) for (field, feat) in feats]
    return feats


frequent_feats = []#read_freqent_feats(args['threshold'])

with open(args['out_path'], 'w') as f:
    
    count = 0    

    for row in csv.DictReader(open(args['csv_path'])):
        #print('!!!!!!!!!!!!!!! row: ', row)
        feats = []

        for feat in gen_feats(row):
            #print('     @@@@@@@@@@@@@@@ feat: ', feat)
            field = feat.split('-')[0]
            type, field = field[0], int(field[1:])
            '''
            if type == 'C' and feat not in frequent_feats:
                feat = feat.split('-')[0]
            

            
            print('           ################# feat2: ', feat)
            print('                 field + feat: ', (field, feat))
 
            if type == 'C':
                field += 8
            '''

            feats.append((field, feat))

        '''
        for i, feat in enumerate(line_gbdt.strip().split()[1:], start=1):
            field = i + 39
            feats.append((field, str(i)+":"+feat))
        '''
        #print('feats before hash: ', feats)
        feats = gen_hashed_fm_feats(feats, args['nr_bins'])
        #print('feats after hash: ', feats)
        f.write(row['Label'] + ' ' + ' '.join(feats) + '\n')

