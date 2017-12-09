import csv
import operator
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import classification_report
from pqdict import pqdict

def main():
    n = 0
    m = 0
    k = 0
    with open('../model_tmp', 'rb') as f_r:
        with open('inner_product_small.csv', 'w') as f_w:
            lines = f_r.readlines()
            for i in range(0, len(lines)):

                line = lines[i].strip().split(' ')
                if i == 0:
                    n = line[1]
                    print 'n: ', n
                if i == 1:
                    m = line[1]
                    print 'm: ', m
                if i == 2:
                    k = line[1]
                    print 'k: ', k 

                if i > 3:
                    key = line[0]
                    lf = line[1:]
                    
                    for j in range(i + 1, len(lines)):
                        
                        line_other = lines[j].strip().split(' ')
                        key_other = line_other[0]
                        lf_other = line_other[1:]
                        
                        inner_prod = 0
                        for idx in range(5):
                            inner_prod += float(lf[idx])*float(lf_other[idx])
           
                        writer = csv.writer(f_w, delimiter = ',')
                        tmp = [key, key_other, inner_prod]
                        writer.writerow(tmp)
        

if __name__ == '__main__':
    main()
