from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import HiveContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.sql.functions import col
import math
import itertools
import hashlib
import csv
from math import sqrt
from operator import add
from time import time
from compiler.ast import flatten




# ========== Constants ==========
FFM_TE_RAW = "s3://vpon.data/user/vincent/cvr_prediction/Baseline/cvr/ffm_te_happymail_07010710_2morefeat/part-00000"
MODEL = "s3://vpon.data/user/vincent/cvr_prediction/Baseline/ctr/model.tar.bz2"
# ===============================


# Spark configuration
conf = SparkConf().setAppName("FFM model correlation").set("spark.executor.memory", "100g").set("saprk.driver.memory", "100g").set("spark.core.max", 10).set("spark.driver.maxResultSize", "20g")
sc = SparkContext(conf = conf)
sqlContext = HiveContext(sc)



def hash(string):
    nr_bins = 1e+7
    return int(hashlib.md5(string.encode('utf8')).hexdigest(), 16)%(nr_bins-1)+1

def field_mapping(field):
    # create_at_hr, ad_unit, campaign_id, campaign_offer_category_tag, email_advertiser, advertiser_region, user_id_publisher
    if field == 'C1':
        return 'create_at_hour'
    if field == 'C2':
        return 'ad_unit'
    if field == 'C3':
        return 'campaign_id'
    if field == 'C4':
        return 'user_id_publisher'
    if field == 'C5':
        return 'campaign_offer_category_tag'
    if field == 'C6':
        return 'email_advertiser'
    if field == 'C7':
        return 'advertiser_region'
    if field == 'C8':
        return 'app_id'
    if field == 'C9':
        return 'banner_id'

def main():

    # Construct data frame for ffm_raw_te
    raw = sc.textFile(FFM_TE_RAW).map(lambda x: x.strip().encode('utf-8').split(','))
    first = raw.first()
    data = raw.filter(lambda x: x != first)
    print data.take(5)

    strSchema = "Label,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10"
    strFields = [StructField(field_name, StringType(), True) for field_name in strSchema.split(',')]

    fields = []
    for item in strFields:
        fields.append(item)
    schema = StructType(fields)
    df_raw = sqlContext.createDataFrame(data, schema)#.fillna({'Label':0})
    df_raw.printSchema()
    print df_raw.show()
    # =====================================

    col_distinct_feats = []
    print 'df_raw.columns: ', df_raw.columns
    for col in df_raw.columns:
        if col != 'Label' and col != 'C1': # Label & imei not included
            distinct_feats = df_raw.select(col).distinct().map(lambda x: x[0]).collect()
            col_distinct_feats.append(distinct_feats)
            #print len(distinct_feats)   

    
    #model_raw = sc.textFile(MODEL).map(lambda x: x.encode('utf-8').strip()).filter(lambda x: x != 'model\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x000000664\x000000764\x000000764\x00\xef\xbf\xbd\x00\x00\x00\x00\x00\x00').filter(lambda x: x != '\xef\xbf\xbd\x12\x7f{12761453225\x00012123\x00 0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00ustar  \x00ec2-user\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00ec2-user\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00n 99999999').filter(lambda x: x != 'm 8' and x != 'k 5' and x != 'normalization 1')
    
    #model = model_raw.map(lambda x: x.split(' ')).map(lambda x: (x[0], x[1:]))
    #print model.take(3)


    with open('../model_cvr_0101_2morefeat', 'rb') as f_r:
        lines = f_r.readlines()
        print len(lines)
        
        m = int(lines[1].strip().split(' ')[1])
        k = int(lines[2].strip().split(' ')[1])
        
        '''
        field = 5
        key_test = int(hash('C3-mb'))
        print key_test
        print lines[key_test * m + 4]
        print lines[key_test * m + 4 + (field - 1)].split(' ')[1:]
        #print lines[key_test * m + 4 + 7]
        #print lines[key_test * m + 4 + 8]
        '''

        result = []
        for idx1 in range(len(col_distinct_feats)):
            field1 = 'C' + str(idx1 + 1)
            for feat1 in col_distinct_feats[idx1]:
                print 'feat1: ', feat1
                key1 = int(hash(field1 + '-' + feat1))
                print 'key1: ', key1
                #matchingAndSave(field1, key1)
                for idx2 in range(len(col_distinct_feats)):
                
                    if idx2 == idx1:
                        continue

                    field2 = 'C' + str(idx2 + 1)
                    for feat2 in col_distinct_feats[idx2]:
                    
                        tmp = []
                        key2 = int(hash(field2 + '-' + feat2))
                        print 'key2', key2
                    
                        #lf1 = model.lookup('w' + str(key1) + ',' + str(idx2))[0]
                        lf1 = lines[key1 * m + 4 + (idx2 - 1)].strip().split(' ')[1:]
                        print lf1
                        print 'lf1lf1lf1lf1lf1lf1lf1lf1lf1lf1lf1lf1lf1lf1lf1lf1lf1lf1lf1lf1lf1lf1lf1lf1lf1lf1lf1lf1lf1'

                        #lf2 = model.lookup('w' + str(key2) + ',' + str(idx1))[0]
                        lf2 = lines[key2 * m + 4 + (idx1 - 1)].strip().split(' ')[1:]
                        print lf2
                        print 'lf2lf2lf2lf2lf2lf2lf2lf2lf2lf2lf2lf2lf2lf2lf2lf2lf2lf2lf2lf2lf2lf2lf2lf2lf2lf2lf2lf2lf2'
    
                        if not lf1:
                            lf1 = [0, 0, 0, 0, 0]
                        if not lf2:
                            lf2 = [0, 0, 0, 0, 0]
                    
                        inner_prod = 0
                        for i in range(5):
                            inner_prod += float(lf1[i])*float(lf2[i])
                     
                        print 'inner_prod: ', inner_prod
                        tmp.append(field_mapping(field1))
                        tmp.append(feat1)
                        tmp.append(field_mapping(field2))
                        tmp.append(feat2)
                        tmp.append(inner_prod)
                        tmp = tmp + lf1 + lf2
                        result.append(tmp)

        rdd_result = sc.parallelize(result).map(lambda x: ','.join(str(d) for d in x))
        rdd_result.coalesce(1).saveAsTextFile("s3://vpon.data/user/vincent/cvr_prediction/Baseline/ctr/result1")



if __name__ == '__main__':
    main()
