import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import classification_report

# Get raw prediction label and calculate avg & iq
pred = []
with open('../output', 'rb') as f:
    for line in f:
        pred.append(float(line)) 
'''
iq = np.percentile(pred, [90, 05, 99])
avg = np.average(pred)
print 'iq: ', iq
print 'avg: ', avg
'''
print 'pred[0]', pred[0]
print 'len of pred: ', len(pred)


answer = []
# Check with the answer
with open('../te.ffm', 'rb') as f:
    for line in f:
	ans = int(line.split(' ')[0].strip())
        if ans > 1:
            ans = 1
	answer.append(ans)
print 'answer[0]: ', answer[0]
print 'len of answer: ', len(answer)




def confusion(threshold):
    pr_pred = []
    for item in pred:
        if item > threshold:
            item = 1
        else:
            item = 0
        pr_pred.append(item)

    tp = 0
    tn = 0
    fp = 0
    fn = 0

    for idx in range(len(pr_pred)):
        ans = answer[idx]
        predicted = pr_pred[idx]
        if ans == 1:
            if predicted == 1:
                tp = tp + 1
            else:
                fn = fn + 1
        else:
            if predicted == 1:
                fp = fp + 1
            else:
                tn = tn + 1
    #print 'tp: ', tp
    #print 'tn: ', tn
    #print 'fp: ', fp
    #print 'fn: ', fn
    #print '==========================='

    return tp, tn, fp, fn



# PR curve
precision, recall, threshold = precision_recall_curve(answer, pred)
average_precision = average_precision_score(answer, pred)

#count = 0
thr_pred_recall_group = []
for idx in range(len(threshold)):
    #if count > 2:
	#break
    tmp = []
    thr = threshold[idx]
    pre = precision[idx]
    
    rec = recall[idx]
    print 'threshold: ', thr
    print 'precision: ', precision[idx]
    print 'recall: ', recall[idx]
    tp, tn, fp, fn = confusion(thr)
    tmp.append(thr)
    tmp.append(pre) 
    tmp.append(rec) 
    tmp.append(tp) 
    tmp.append(tn) 
    tmp.append(fp) 
    tmp.append(fn)
    thr_pred_recall_group.append(tmp)
   
    #count = count + 1
  
with open('thr_prec_recall_group.csv', 'w') as f:
    for item in thr_pred_recall_group:
	writer = csv.writer(f, delimiter = ',')
	writer.writerow(item)



plt.clf()
plt.plot(recall, precision, label='Avg precision = %0.2f'% average_precision)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0.0, 1.05])
plt.xlim([0.0, 1.0])
plt.title('Precision-Recall curve')
plt.legend(loc="lower right")
plt.show()


