import os
import numpy as np
import copy
from src_cnnpc import CRS 
from src_cnnpc import execute_compression
from src_cnnpc.mysql_support import MySQL

def turn_to_r_rate(com1, rate1, com2, rate2):
    '''get the possible rate space and change rate1, rate2 to the form used in Pocketflow

    Args:
    * com1, com2: the index of compression layer
    * rate1, rate2: the value of two compression rates

    Returns:
    * R1, R2: the possible rate space of com1 and com2 compression layer
    * r_rate1, r_rate2: another form of rate1 and rate2 which used in Pocketflow  
    '''
    number_of_channel = np.load("./model_profile/partitions.npy")

    num_com1 = number_of_channel[1][com1]
    num_com2 = number_of_channel[1][com2]
    R1 = np.zeros((num_com1+1), dtype=np.float32)
    for m in range(num_com1+1):
        R1[m] = m / num_com1

    R2 = np.zeros((num_com2+1), dtype=np.float32)
    for m in range(num_com2+1):
        R2[m] = m / num_com2
    index1 = CRS.get_descrete_point(rate1, R1)
    index2 = CRS.get_descrete_point(rate2, R2)

    r_rate1 = R1[index1]
    r_rate2 = R2[index2]

    return R1, R2, r_rate1, r_rate2

def get_nearest_point(input_rate, tuple_res, in_line=True):
    '''find the nearest result from MySQL

    Args:
    * input_rate: the given compression rate 
    * tuple_res: the set of related results in MySQL database
    * in_line: If True, search in 1 dimensionality

    Returns:
    * output_point: a list recording the nearest point
    '''
    output_point = [] # record the nearest point： [rate2, acc, dir]
    if tuple_res :
        k = 0 # record the best location
        num = 0
        best_dis = 1 # record the shortest distance
        for point in tuple_res: 
            if in_line:
                distance = abs(input_rate - point[0])
            else:
                distance = abs(input_rate[0] - point[0]) + abs(input_rate[1] - point[1])
            if(distance < best_dis):
                k = num
                best_dis = distance
            num += 1
        output_point = list(tuple_res[k])
    return output_point

def get_nearest_point_TD(input_rate1, input_rate2, tuple_res):
    '''find the nearest point in 2 dimensionalities

    Args:
    * input_rate1, input_rate2: the given compression rate 
    * tuple_res: the set of related results in MySQL database 

    Returns:
    * output_point: a list recording the nearest point
    '''
    output_point = [] # record the nearest point： [rate1, rate2, acc, dir]

    output_point = get_nearest_point([input_rate1, input_rate2], tuple_res, in_line=False)

    return output_point

def PocketFlow_acc(com1, rate1, com2, rate2, multistep=False):
    '''get the accuracy with given strategy

    Args:
    * com1, com2: the index of compression layer
    * rate1, rate2: the value of two compression rates
    * multistep: this arg denotes which compression method is choosed. 
                 If multistep is True, the algorithm will use a method that achieve the target strategy step by step, 
                 and every time it starts from the model whose strategy is the nearest one to target. For example, if 
                 now we have two models, whose strategy are [0,0,0,0] and [1,0.5,1,0.5], and the target strategy we want
                 is [1,0.8,1,0.8], the algorithm will choose the model with strategy of [1,0.5,1,0.5] as the start point 
                 because it is closer to [1,0.8,1,0.8] compared with [0,0,0,0]. And the algorithm may choose the [1,0.6,1,0.6] 
                 and [1,0.7,1,0.7] as the intermediate strategy so as to achieve a better accuracy and shorter retraining time.

    Returns:
    * acc: the accuracy of given strategy
    '''
    sql = MySQL()
    if rate1==rate2 and rate1==0:
        return sql.search_acc(0,0.0,0,0.0)

    # number_of_channel is the list of channel of all available  compression layers.
    number_of_channel = np.load("./model_profile/partitions.npy")

    # change index to real number of layer
    r_com1 = number_of_channel[0,com1]
    r_com2 = number_of_channel[0,com2]

    nearest=[]
    if multistep:
        tuple_rate1_rate2_acc = sql.search_rate1_rate2_acc(r_com1, r_com2)
        nearest = get_nearest_point_TD(rate1, rate2, tuple_rate1_rate2_acc)

    if nearest==[]:
        nearest=[0,0,0,0]    
    if nearest[0]!= nearest[1] or nearest[0] !=0 : # whether OnEEC has compressed the model under these partition point situation.
        # create ratio.txt
        protect_nearest = copy.deepcopy(nearest)
        ratio_list=create_txt_of_ratio(com1, rate1, com2, rate2, protect_nearest, number_of_channel)
    else:
        ratio_list=[['2-'+str(r_com1)+'-'+str(1-rate1)+'-'+str(r_com2)+'-'+str(1-rate2)]]
        nearest=[0,0,0,0]
    print('ratio_list is :',ratio_list)
    f= open('ratio.txt','w')
    for i in ratio_list:  
        if type(i)==list:
            i=i[0]
        temp=i.split('-')
        temp3=turn_to_r_rate(int(com1),temp[2],int(com2),temp[4])
        h=temp[0]+'-'+temp[1]+'-'+str(temp3[2])+'-'+temp[3]+'-'+str(temp3[3])
        f.writelines(h+'\n')
    f.close()

    execute_compression.create_ratio_list() # create ratio.list from ratio.txt
    if sql.search_acc(r_com1,rate1,r_com2,rate2)==[] or sql.search_acc(r_com1,rate1,r_com2,rate2)==None or sql.search_acc(r_com1,rate1,r_com2,rate2)==(): # execute inference according ratio.list
        execute_compression.execute_inference(r_com1,r_com2,nearest)
        execute_compression.save_result_to_sql() # save the result of this loop to sql
       
    acc= sql.search_acc(r_com1, rate1, r_com2, rate2)
    return acc

def create_txt_of_ratio(com1, rate1, com2, rate2, nearest, number_of_channel): 
    '''create the ratio.txt to guide compression process

    Args:
    * com1, com2: the index of compression layer
    * rate1, rate2: the value of two compression rates
    * nearest: the start point to compress
    * number_of_channel: a vector of available channel in com1 and com2 
    '''    
    # define interval space w1, w2, w3 and step s
    w1= 0.65  
    w2= 0.88  
    w3= 0.95  
    s=[4,3,2,1]

    # change index to real number of layer
    r_com1 = number_of_channel[0][com1]
    r_com2 = number_of_channel[0][com2]

    ratio_list=[]
    if com1 != com2:
        while rate1 != nearest[0] or rate2 != nearest[1]:
            if rate1 != nearest[0]:
                signal1 = (rate1 - nearest[0]) / abs(rate1 - nearest[0])  # denote the add or minus
                temp_interval = choose_interval(nearest[0], w1, w2, w3) # select the interval
                nearest[0]= nearest[0]+signal1*s[temp_interval]/number_of_channel[1][com1]        # determine the next point
                if rate1 == nearest[0]:
                    ratio_list.append('2-' + str(r_com1) + '-' + str(1 - nearest[0]) + '-' + str(r_com2) + '-' + str(1 - nearest[1]))
                elif (rate1-nearest[0])/abs(rate1-nearest[0]) == signal1: # creat a new line of the ratio.txt
                    ratio_list.append('2-'+ str(r_com1) +'-'+str(1-nearest[0])+'-'+str(r_com2)+'-'+str(1-nearest[1]))
                else:
                    nearest[0]=rate1
                    ratio_list.append('2-'+ str(r_com1) +'-'+str(1-nearest[0])+'-'+str(r_com2)+'-'+str(1-nearest[1]))
            if rate2 != nearest[1]:
                signal2 = (rate2 - nearest[1]) / abs(rate2 - nearest[1])
                temp_interval = choose_interval(nearest[1], w1, w2, w3)
                nearest[1]= nearest[1]+signal2*s[temp_interval]/number_of_channel[1][com2]
                if rate2 == nearest[1]:
                    ratio_list.append('2-' + str(r_com1) + '-' + str(1 - nearest[0]) + '-' + str(r_com2) + '-' + str(1 - nearest[1]))
                if (rate1-nearest[1])/abs(rate1-nearest[1]) == signal2:
                    ratio_list.append('2-'+ str(r_com1) +'-'+str(1-nearest[0])+'-'+str(r_com2)+'-'+str(1-nearest[1]))
                else:
                    nearest[1]=rate2
                    ratio_list.append('2-'+ str(r_com1) +'-'+str(1-nearest[0])+'-'+str(r_com2)+'-'+str(1-nearest[1]))
    else: # the situation that only compression one layer
        while rate1 != nearest[0]: 
            signal1=(rate1-nearest[0])/abs(rate1-nearest[0])
            temp_interval = choose_interval(nearest[0], w1, w2, w3)
            nearest[0]= nearest[0]+signal1*s[temp_interval]/number_of_channel[1][com1]
            nearest[1]= nearest[0]
            if rate1 == nearest[0]:
                ratio_list.append('2-' + str(r_com1) + '-' + str(1 - nearest[0]) + '-' + str(r_com2) + '-' + str(1 - nearest[1]))
                break
            if (rate1-nearest[0])/abs(rate1-nearest[0]) == signal1: # creat a new line of the ratio.txt
                ratio_list.append('2-'+ str(r_com1) +'-'+str(1-nearest[0])+'-'+str(r_com2)+'-'+str(1-nearest[1]))
            else:
                nearest[0]= rate1
                nearest[1]= nearest[0]
                ratio_list.append('2-'+ str(r_com1) +'-'+str(1-nearest[0])+'-'+str(r_com2)+'-'+str(1-nearest[1]))
    return ratio_list

def choose_interval(rate, w1, w2, w3): 
    '''choose the step interval
    
    Args:
    * rate: input compression rate
    * w1, w2, w3: interval space 
    '''
    if rate<w1:
        return 0
    elif rate<w2:
        return 1
    elif rate<w3:
        return 2
    else:
        return 3


if __name__ == '__main__':
    '''test content'''
    sql = MySQL()

    print("Totally " + str(sql.get_row_numbers()) + " groups of result")
    tuple_rate2_acc = sql.search_rate2_acc(1, 0.9, 2)
    list_nearest = get_nearest_point(0.71, tuple_rate2_acc)
    print('the nearest point is '+ str(list_nearest))
    tuple_rate1_rate2_acc = sql.search_rate1_rate2_acc(1, 2)
    list_nearest = get_nearest_point_TD(0.68, 0.71, tuple_rate1_rate2_acc)
    print('the nearest point is '+ str(list_nearest))