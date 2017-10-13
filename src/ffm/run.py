#!/usr/bin/env python3

import subprocess, sys, os, time

NR_THREAD = 3

start = time.time()


start_input_transform_tr = time.time()
print(" ===== Transform tr.csv into tr.ffm  =====")
cmd = 'converters/parallelizer-b.py -s {nr_thread} converters/pre-b.py tr.csv tr.ffm'.format(nr_thread=NR_THREAD)
subprocess.call(cmd, shell = True)
time_step1 = time.time() - start_input_transform_tr
print('Time for tr.csv to tr.ffm: {0:.0f}'.format(time_step1))

start_input_transform_va = time.time()
print(" ===== Transform va.csv into va.ffm  =====")
cmd = 'converters/parallelizer-b.py -s {nr_thread} converters/pre-b.py va.csv va.ffm'.format(nr_thread=NR_THREAD)
subprocess.call(cmd, shell = True) 
time_step2 = time.time() - start_input_transform_va
print('Time for va.csv to va.ffm: {0:.0f}'.format(time_step2))

start_input_transform_te = time.time()
print(" ===== Transform te.csv into te.ffm  =====")
cmd = 'converters/parallelizer-b.py -s {nr_thread} converters/pre-b.py te.csv te.ffm'.format(nr_thread=NR_THREAD)
subprocess.call(cmd, shell = True) 
time_step3 = time.time() - start_input_transform_te
print('Time for te.csv to te.ffm: {0:.0f}'.format(time_step3))



start_train = time.time()
print(" ===== FFM training  =====")
cmd = './ffm-train -k 5 -t 1000 -s {nr_thread} -p va.ffm --auto-stop tr.ffm model'.format(nr_thread=NR_THREAD) 
subprocess.call(cmd, shell = True)
time_step4 = time.time() - start_train
print('Time for FFM training: {0:.0f}'.format(time_step4))


start_pred = time.time()
print(" ===== FFM prediction  =====")
cmd = './ffm-predict te.ffm model out_te'.format(nr_thread=NR_THREAD) 
subprocess.call(cmd, shell = True)
time_step5 = time.time() - start_pred
print('Time for FFM prediction: {0:.0f}'.format(time_step5))

print('Time used overall: {0:.0f}'.format(time.time() - start))

