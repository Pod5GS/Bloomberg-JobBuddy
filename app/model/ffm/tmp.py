import csv
import numpy as np
import matplotlib.pyplot as plt
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import HiveContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *



# Get raw prediction label and calculate avg & iq
pred = []
with open('output_imps', 'rb') as f:
    for line in f:
        pred.append(float(line)) 


answer = []
# Check with the answer
with open('te_imps.csv', 'rb') as f:
    lines = f.readlines()
    for idx in range(len(lines)):
        line = lines[idx]
        row = line.strip().split(',')
        if idx == 0:
            row.append('C11')
        else:
            row.append(pred[idx - 1])
            answer.append(row)
    
#print answer[0]
#print answer[1]


with open('te_imps_pred.csv', 'w') as f:
    writer = csv.writer(f, delimiter = ',')
    for item in answer:
	writer.writerow(item)


conf = SparkConf().setAppName("FFM data engineering").set("spark.executor.memory", "30g").set("saprk.driver.memory", "50g")
sc = SparkContext(conf = conf)
sqlContext = HiveContext(sc)


#rdd_ans = sc.textFile('te_imps_pred.csv')
rdd_ans = sc.parallelize(answer)
strSchema = "Label,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11"
strFields = [StructField(field_name, StringType(), True) for field_name in strSchema.split(',')]
fields = []
for item in strFields:
    fields.append(item)
schema = StructType(fields)
df_ans = sqlContext.createDataFrame(rdd_ans, schema)
print df_ans.show()
