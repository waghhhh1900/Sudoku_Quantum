#coding=utf-8
import numpy as np
import sys  # 导入sys模块
sys.setrecursionlimit(3000)


def creat_new_table():
    # 每一纬度依次为 num_stage,group，row，col, 可能、不可能、确定 依次为 1，0，10
    table = np.ones((9, 9, 9, 9)).astype(np.int32)
    # 对与grop 进行定义
    group_list = [
        1, 1, 1, 2, 2, 2, 3, 3, 3,
        1, 1, 1, 2, 2, 2, 3, 3, 3,
        1, 1, 1, 2, 2, 2, 3, 3, 3,
        4, 4, 4, 5, 5, 5, 6, 6, 6,
        4, 4, 4, 5, 5, 5, 6, 6, 6,
        4, 4, 4, 5, 5, 5, 6, 6, 6,
        7, 7, 7, 8, 8, 8, 9, 9, 9,
        7, 7, 7, 8, 8, 8, 9, 9, 9,
        7, 7, 7, 8, 8, 8, 9, 9, 9,
    ]

    group_np = np.array(group_list).reshape(9, 9)

    # 每一个num_stage
    for num_stage in range(0, 9):

        # 每一个group
        for group in range(0, 9):
            table[num_stage, group] = np.where(group_np != group + 1, 0, table[num_stage, group])

    return table


# 知道row,col,求group
def get_group(row, col):
    group_list = [
        1, 1, 1, 2, 2, 2, 3, 3, 3,
        1, 1, 1, 2, 2, 2, 3, 3, 3,
        1, 1, 1, 2, 2, 2, 3, 3, 3,
        4, 4, 4, 5, 5, 5, 6, 6, 6,
        4, 4, 4, 5, 5, 5, 6, 6, 6,
        4, 4, 4, 5, 5, 5, 6, 6, 6,
        7, 7, 7, 8, 8, 8, 9, 9, 9,
        7, 7, 7, 8, 8, 8, 9, 9, 9,
        7, 7, 7, 8, 8, 8, 9, 9, 9,
    ]

    group_np = np.array(group_list).reshape(9, 9)
    group = group_np[row, col] - 1
    return group


# 根据提供的数据更新table
def input_table(table, start_np):
    the_index = np.argwhere(start_np != 0)
    for index in the_index:
        row, col = index
        num_stage = start_np[row, col] - 1
        table = rebuilt_table_by_blog(table, num_stage, row, col)

    return table

# 更新每个确定了的相关num_stage,group,row,col 的数据

def table_1_to_0(table,index):
    row,col=index
    num_stage,group=np.argwhere(table[:,:,row,col]==10)[0]
    table[:,:,row,col]=0
    table[num_stage,group,:,:]=0
    table[num_stage,:,row,:]=0
    table[num_stage,:,:,col]=0
    return table


def input_the_num(table,index):
    row,col=index
    num_stage,group=np.argwhere(table[:,:,row,col]==10)[0]
    table[num_stage,group,row,col]=10
    return table


def input_table_1_to_10(table,num_stage,group,row,col):
    table[num_stage,group,row,col]=10
    return table


# table_sum 里有1 将这块改为10
def sum_1_to_10(table):
    # 如果一个blog只有1种num_stage 就替换为10
    table_sum = np.sum(table, axis=(0, 1))
    if 1 in table_sum:
        the_index = np.argwhere(table_sum == 1)
        for index in the_index:
            row, col = index
            group = get_group(row, col)
            num_stage = np.argwhere(table[:, group, row, col] == 1)[0, 0]
            table = rebuilt_table_by_blog(table, num_stage, row, col)

    return table


# 已确定blog的num_stage，更新相关数据
def rebuilt_table_by_blog(table, num_stage, row, col):
    # 将同一group的更新0
    group = get_group(row, col)

    print('更新row%d,col%d,group%d 为%d' % (row, col, group, num_stage + 1))
    table[num_stage, group, :, :] = 0
    table[num_stage, :, :, col] = 0
    table[num_stage, :, row, :] = 0
    table[:, :, row, col] = 0
    table[num_stage, group, row, col] = 10

    return table


# 根据已有信息重塑table
def rebuilt_table(table):
    while (np.sum(table, axis=(0, 1)) == 1).any():
        table = sum_1_to_10(table)

    return table


def get_bignum(table, index):
    row, col = index

    num_list = np.sum(table[:, :, row, col], axis=1)

    numstage_list = np.argwhere(num_list == 1)
    numstage_list = (numstage_list + 1)[:, 0].tolist()

    big_num = 0
    plush_num = 1
    i = len(numstage_list) - 1
    while i > -1:
        big_num += numstage_list[i] * plush_num
        plush_num *= 10
        i -= 1

    return big_num


# show 解数进展
def show_table(table):
    the_index = np.argwhere(table == 10)
    show_table = np.zeros((9, 9)).astype(np.int32)
    for index in the_index:
        num_stage, group, row, col = index
        show_table[row, col] = num_stage + 1
    # 未确定num—stage的数
    table_sum = np.sum(table, axis=(0, 1))
    the_index = np.argwhere(table_sum != 10)
    for index in the_index:
        big_num = get_bignum(table, index)
        row, col = index
        show_table[row, col] = big_num

    return show_table


def get_blog_numstage(table, num_tag, group, row, col):
    return np.argwhere(table[:, group, row, col] == num_tag).T[0].tolist()

# 判断是否求出正确解，用于递归
def recheck_answer(table):
    # 校核是否满足要求
    # 每个位置是否只有一个确定
    if all(
        [
            (np.sum(table,axis=(0,1))==10).all(),
           (np.sum(table,axis=(1,2))==10).all(),
           (np.sum(table,axis=(1,3))==10).all(),
           (np.sum(table,axis=(2,3))==10).all()
        ]
    ):
        print('yes ,fond it!!!')
        return True
    else:
        print('sorry ,not it!!!')
        return False

# 判断是否求出正确解
def recheck_table(table):
    # 校核是否满足要求
    # 每个位置是否只有一个确定
    if all(
        [
            (np.sum(table,axis=(1,2))==0).any(),
         (np.sum(table,axis=(1,3))==0).any(),
         (np.sum(table,axis=(2,3))==0).any()

        ]
    ):
        print('Warning ,it is not !!!')
        return False
    else:
        print('yeah ,go on!!!')
        return True


# 使用递归来尝试找到正确答案

#使用递归方案
def test_answer(table):
    # 如果np.sum 都为10
    if (np.sum(table, axis=(0, 1)) == 10).all():
        if recheck_answer(table):
            answer.append(table)
    else:

        # 找到table里只有2个可能性的，给一个赋值
        table_sum = np.sum(table, axis=(0, 1))
        the_2_index = np.argwhere(table_sum == 2)

        if the_2_index.any():

            row, col = the_2_index[0]
            change_index = np.argwhere(table[:, :, row, col] == 1)

            for i in change_index:
                row, col = i
                group = get_group(row, col)
                num_list = get_blog_numstage(table, 1, group, row, col)

                for num_stage in num_list:
                    new_table=table.copy()
                    new_table = rebuilt_table_by_blog(new_table, num_stage, row, col)
                    if recheck_table(new_table):
                        new_table = rebuilt_table(new_table)
                        test_answer(new_table)