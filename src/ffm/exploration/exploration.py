import csv

clks = 1
impr_effective = 7

impr_count = 0
clks_count = 0
with open('../test_0701.csv', 'rb') as f:
    reader = csv.reader(f, delimiter = ',')
    for row in reader:
        clk = row[clks]
        impr = row[impr_effective]
        #print 'clk: ', clk
        #print 'impr: ', impr
        if 'Label' not in clk:
            clks_count = clks_count +int(clk)
        if 'I' not in impr:
            impr_count = impr_count + int(impr)


print 'impr_count: ', impr_count
print 'clks_count: ', clks_count
print 'CTR: ', float(clks_count) / impr_count

