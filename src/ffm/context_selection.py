import csv
import numpy as np
import matplotlib.pyplot as plt
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import HiveContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *


'''
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
'''

conf = SparkConf().setAppName("FFM data engineering").set("spark.executor.memory", "30g").set("saprk.driver.memory", "50g")
sc = SparkContext(conf = conf)
sqlContext = HiveContext(sc)


#rdd_ans = sc.textFile('s3://vpon.data/user/vincent/cvr_prediction/Baseline/cvr/te_imps_pred.csv')
#rdd_ans = sc.parallelize(answer)
ans = []
with open('te_imps_pred.csv', 'rb') as f:
    reader = csv.reader(f, delimiter = ',')
    for row in reader:
        ans.append(row)
rdd = sc.parallelize(ans)
strSchema = "Label,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11"
strFields = [StructField(field_name, StringType(), True) for field_name in strSchema.split(',')]
fields = []
for item in strFields:
    fields.append(item)
schema = StructType(fields)
df_ans = sqlContext.createDataFrame(rdd, schema)
#print df_ans.show()
df_ans.registerTempTable('df_ans')

df = sqlContext.sql('select C1 as imei, C2 as create_at_hr, C9 as app_id, avg(C11) as avg, stddev(C11) as stddev from df_ans group by C1, C2, C9 order by avg desc')
df.registerTempTable('df')

df_098 = sqlContext.sql('select distinct imei from df where avg > 0.98')
#df_60w = sqlContext.sql('select distinct imei from df where avg > 0.95')

#df_87w.coalesce(1).write.format('com.databricks.spark.csv').save('s3://vpon.data/user/vincent/cvr_prediction/Baseline/cvr/seg_context_87w')

df_098.coalesce(1).write.format('com.databricks.spark.csv').save('s3://vpon.data/user/vincent/cvr_prediction/Baseline/cvr/seg_context_098')



