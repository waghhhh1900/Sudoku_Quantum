import numpy as np
import pandas as pd 



# 1.0建立棋盘 row_num

def creat_table(sudoku_df):
    """creat 9x9 sudo table_df,
    columns=[row_num,col_num,group_key,num_list,real_num]
    """

    
    
    # creat col:row_num,col_num
    row_list=[]
    for i in range(1,10):
        row_list+=range(1,10)
        
    col_list=[]
    for i in range(1,10):
        col_list+=[i,i,i,i,i,i,i,i,i]
        
    sudoku_df['row_num']=row_list
    sudoku_df['col_num']=col_list

    
   
    #creat  col :group_key
    group_keys=['a','a','a','b','b','b','c','c','c',
            'a','a','a','b','b','b','c','c','c',
            'a','a','a','b','b','b','c','c','c',
            'd','d','d','e','e','e','f','f','f',
            'd','d','d','e','e','e','f','f','f',
            'd','d','d','e','e','e','f','f','f',
            'g','g','g','h','h','h','i','i','i',
            'g','g','g','h','h','h','i','i','i',
            'g','g','g','h','h','h','i','i','i',]

    sudoku_df['group_key']=group_keys
    
    #creat col:num_list
    nums=[]
    for i in range(1,82):
        nums.append(list(range(1,10)))
        
    sudoku_df['num_list']=nums
    
    #creat col:num_real
    sudoku_df['num_real']=0
    

# 2.0录入数独信息
# 2.1录入单个点的信息
def change_num_list(row,col,num):
    index_num=sudoku_df[(sudoku_df['row_num']==row)&(sudoku_df['col_num']==col)].index    
    sudoku_df.loc[index_num,'num_real']=num
    
    print(sudoku_df.loc[index_num])

# 2.2录入列表类所有信息
def input_table(start_nums):
    st_num=0
    while st_num<len(start_nums):
        change_num_list(start_nums[st_num],start_nums[st_num+1],start_nums[st_num+2])
        st_num+=3
        
# 3.0 更新棋盘

# 3.1 检查同一row、col、group的是否有相同的数

def check_num(sudoku_df,index_num,num):
    #检查每一row/col/group
    row_num=sudoku_df.loc[index_num,'row_num']
    col_num=sudoku_df.loc[index_num,'col_num']
    group_key=sudoku_df.loc[index_num,'group_key']
    index_list=sudoku_df[(sudoku_df['row_num']==row_num)|
                         (sudoku_df['col_num']==col_num)|
                         (sudoku_df['group_key']==group_key)].index
    index_list=index_list.tolist()
    print('以下要提取index为：')
    print(index_list)
    
    #检查详细的每个区块
    for blog_index in index_list:
        print('以下为检查index:')
        print(blog_index)
        blog_num_list=sudoku_df.loc[blog_index,'num_list']
       
        print('num_list 列表为：')
        print(blog_num_list)
        #判断blog——list是否为int
        if len(blog_num_list)==1:
            print('pass')
            
        else:
            if num in blog_num_list:
                sudoku_df.loc[blog_index,'num_list'].remove(num)
            
        print('-'*10)
#     sudoku_df.loc[index_num,'num_list']=[]
#     sudoku_df.loc[index_num,'num_list'].append(num)
            
#更新num——list
def rebuilt_df(sudoku_df):
    check_indexs=sudoku_df[sudoku_df['num_real']!=0].index
    
    for index_num in check_indexs:
        print('检查index_num:'+str(index_num))
        num=sudoku_df.loc[index_num,'num_real']
        check_num(index_num,num)
        print('*'*20)

#将num——list中已为单个的提取出来
for index_num in sudoku_df.index:
    k=len(sudoku_df.loc[index_num,'num_list'])
    if k==1:
        print('index:'+str(index_num))
        print(sudoku_df.loc[index_num,])        
        print('-'*10)
        
