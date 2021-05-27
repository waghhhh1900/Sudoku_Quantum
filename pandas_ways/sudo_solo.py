import numpy as np
import pandas as pd 



# 1.0建立棋盘 row_num

def creat_table():
    """creat 9x9 sudo table_df,
    columns=[row_num,col_num,group_key,num_list,real_num]
    """

    
    sudoku_df=pd.DataFrame()
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
    nums_ls='123456789'
    sudoku_df['num_list']=nums_ls    
    #creat col:num_real
    sudoku_df['num_real']=0
    
    return sudoku_df
    

# 2.0录入数独信息
# 将信息录入到棋盘df中
def input_blog(table,row,col,num):
    index_num=table[(table['row_num']==row)&(table['col_num']==col)].index    
    table.loc[index_num,'num_real']=num
    table.loc[index_num,'num_list']=str(num) 

def start_table(table,start_nums):
    st_num=0
    while st_num<len(start_nums):
        input_blog(table,start_nums[st_num],start_nums[st_num+1],start_nums[st_num+2])
        st_num+=3

# 3.0 更新棋盘

# 3.1 检查同一row、col、group的是否有相同的数

# 根据已经确定的blog更新相关row、col、group信息

def update_associated_blog(sudoku_df,index_num,num):
    #检查每一row/col/group
    row_num=sudoku_df.loc[index_num,'row_num']
    col_num=sudoku_df.loc[index_num,'col_num']
    group_key=sudoku_df.loc[index_num,'group_key']
    index_list=sudoku_df[(sudoku_df['row_num']==row_num)|
                         (sudoku_df['col_num']==col_num)|
                         (sudoku_df['group_key']==group_key)].index
    index_list=index_list.tolist()
    
    
    #检查详细的每个区块
    for blog_index in index_list:      
        blog_num_list=sudoku_df.loc[blog_index,'num_list']   
        #判断blog——list是否为int
        if len(blog_num_list)==1:
            continue
            
        else:
            if str(num) in blog_num_list:
                sudoku_df.loc[blog_index,'num_list']=blog_num_list.replace(str(num),'')
        
    return sudoku_df
        
#更新num——list
def update_table(sudoku_df):
    check_indexs=sudoku_df[sudoku_df['num_real']!=0].index
    print('start to check if there has num_real to update')
    #检查每一个确定了数字的格子blog
    for index_num in check_indexs:
        
        num=sudoku_df.loc[index_num,'num_real']
        update_associated_blog(sudoku_df,index_num,num)
        
    return sudoku_df
        
    

# 生成棋盘求解视图
def show_table(sudoku_df):
    mid_table=pd.pivot(sudoku_df,values='num_list',index=['row_num','group_key'],columns=['col_num'])
    return mid_table.fillna('')