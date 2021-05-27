#coding=utf-8
import numpy as np
import sys
sys.setrecursionlimit(3000)

import shudu_in_numpy

# 开局信息
table=shudu_in_numpy.creat_new_table()
from shudu_in_numpy import rebuilt_table,show_table,test_answer

start_list=[
    0,8,0,0,0,7,0,0,6,
    0,3,9,2,0,8,0,0,0,
    4,0,0,1,3,0,0,0,0,
    9,0,5,0,0,0,0,0,4,
    0,0,3,0,0,0,0,0,0,
    6,2,0,0,0,5,0,0,0,
    8,0,1,0,0,6,2,0,0,
    0,0,0,5,0,0,0,0,0,
    0,6,0,3,0,0,8,0,0
]
#转为 numpy格式
start_np=np.array(start_list).reshape((9,9))

# 信息更新进table
table=shudu_in_numpy.input_table(table,start_np)

table=rebuilt_table(table)

show=show_table(table)
print (show)

answer=[]
test_answer(table)

print len(answer)