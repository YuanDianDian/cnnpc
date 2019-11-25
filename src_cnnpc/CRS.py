import numpy as np
from src_cnnpc.mysql_support import MySQL 
from src_cnnpc import pocketflow_acc
from src_cnnpc.latency_support import get_T
from src_cnnpc.tools import add_logs


def get_descrete_point(input_rate, r):
    """Change the theoretical compression value to descrete value.

    Args:
    * imput_rate:the theoretical compression value get by calulation.
    * r: the set of descrete value

    Returns:
    * index: output the index which indicates the location of the input_rate in r
    """

    index = 0 # record the best location in r
    num = 0
    best_dis = 1 # record the minimum distance between the point and the given compression
    for point in r: 
        distance = abs(float(input_rate) - float(point))
        if(distance < best_dis ):
            index = num
            best_dis = distance
        num += 1
    return index


def get_acc(com1, rate1, com2 = 0, rate2 = -1.0):  
    '''Get the accuracy of given strategy.

    Args:
    * com1, com2: the number of compression layer
    * rate1, rate2: the compression rate

    Returns:
    * acc: the accuracy of given strategy
    '''
    sql = MySQL()
    # the situation of single layer compression
    if(rate2 == -1.0):
        com2 = com1
        rate2  = rate1
    print('the target strategy is：', com1, rate1, com2, rate2)
    number_of_channel = np.load("./model_profile/partitions.npy")
    # change index to real number of layer
    r_com1 = number_of_channel[0][com1]
    r_com2 = number_of_channel[0][com2]
    # the situation of double layer compression
    res = sql.search_acc(r_com1, rate1, r_com2, rate2)
    if res!=[] and res != None and res !=():
        acc= res        
        add_logs("Find out acc: %d %.6f %d %.6f %.6f" % (com1, rate1, com2, rate2, acc[0][0]) + "\n")        
    else:
        acc = pocketflow_acc.PocketFlow_acc(com1, rate1, com2, rate2)        
        add_logs("PocketFlow-acc: %d %.6f %d %.6f %.6f" % (com1, rate1, com2, rate2, acc[0][0]) + "\n")   
    acc=acc[0][0]
    return acc



def CRS_next(r, A0, com1, com2, rate_input, wh, index1, index2, acc1, acc2): 
    '''the iteration funtion of CRS_search(), which finds the maximum compression rate under a given accuracy A0.

    Args:
    * r: the set of possible strategy solution.
    * A0: the given accuracy which the final strategy should fit. 
    * com1, com2: the number of compression layer
    * rate_input: the compression rate of one layer
    * wh: indicates the compression layer on which we search the maximum compression rate. When wh is 1, it means we search on the com1 layer,
    and when wh is 0, it means we search on the com2 layer.
    * index1, index2: the index in r which corresponds to the two nearest points' compression rate
    * acc1, acc2: the accuracy of index1 and index2

    Returns:
    * [rate, acc]: the maximum compression and its accuracy
    '''
    sql = MySQL()
    print(index1, index2, acc1, acc2)
    k = (A0 - acc1) * (r[index2] - r[index1]) / (acc2 - acc1) + r[index1] # get a new rate by linear estimation
    num = len(r)
    index = get_descrete_point(k, r)   
    # if the new rate exceeds the range of r, we get a new rate by dichotomy
    [bound1, bound2]= get_r_range(r)
    if k <= r[bound1] or k >= r[bound2]:
        k = (r[bound1]+r[bound2]) / 2.0

    index = get_descrete_point(k, r)
    print('compression rate k of the next point is:', r[index])

    # get the accuracy of target strategy [com1, rate_input, com2, r[index]]
    if wh==1:
        acc = get_acc(com1, rate_input, com2, r[index])
    else:
        acc = get_acc(com1, r[index], com2, rate_input)

    # update the two nearest point based on distance of accuracy
    if (abs(acc2-A0)>=abs(acc1-A0)): 
        acc2 = acc
        index2 = index
    else:
        acc1 = acc
        index1 = index

    # update the solution space r
    if acc >A0:
        for i in range(num):
            if i<index:
                r[i]=-10
    else:
        for i in range(num):
            if i>index:
                r[i]=-10

    [bound1,bound2]=get_r_range(r)
    print('the bound of solution space are：', bound1, bound2)
    # judge whether continues to iterate
    if abs(acc - A0) < 0.0001:
        print('Achieve the target accuracy')
        return [r[index], acc]
    # elif(index2 - index1 <= 1):
    elif bound2 - bound1 <= 1:
        print('there is no residual solution under current compression layers')
        return [r[index], acc]
    elif index1==index2:
        if acc1>A0:
            return [r[index1], acc1]
        else:
            if wh == 1:
                # acc_bound1 = get_acc(com1, rate_input, com2, r[bound1])
                index=index2-1
                acc = get_acc(com1, rate_input, com2, r[index])
            else:
                # acc_bound1 = get_acc(com1, r[bound1], com2, rate_input)
                index = index2 - 1
                acc = get_acc(com1, r[index], com2, rate_input)
            return [r[index], acc]
    else:
        [temp1, temp2] = CRS_next(r, A0, com1, com2, rate_input, wh, index1, index2, acc1, acc2)
        return [temp1, temp2]


def CRS_search(r, A0, com1, com2, rate_input, wh):  
    ''' search the maximum rate under a given condition 

    Args:
    * r: the set of possible strategy solution.
    * A0: the given accuracy which the final strategy should fit. 
    * com1, com2: the number of compression layer
    * rate_input: the compression rate of one layer
    * wh: indicates the compression layer on which we search the maximum compression rate. When wh is 1, it means we search on the com1 layer,
    and when wh is 0, it means we search on the com2 layer.

    Returns:
    * [rate, acc]: the maximum compression and its accuracy
    '''
    print('r is:',r)
    r_return=[]  # the current optimal solution
    if not get_r_range(r):
        return []
    [index1, index2] = get_r_range(r)  # get the rate index (index1, index2) of the solution bound 

    print(wh==1,wh)
    print('index1,index2', index1, index2)
    print('com1, com2:', com1, com2)

    if wh==1:
        acc1 = get_acc(com1, rate_input, com2, r[index1])
        if acc1<A0:
            return []
        acc2 = get_acc(com1, rate_input, com2, r[index2])
        if acc2>A0:
            return [r[index2],acc2]
    else:
        acc1 = get_acc(com1, r[index1], com2, rate_input)
        if acc1<A0:
            return []
        acc2 = get_acc(com1, r[index2], com2, rate_input)
        if acc2>A0:
            return [r[index2],acc2]

    # update current optimal solution
    if wh == 1:
        if acc1>A0:
            r_return= [r[index1],acc1]
            if acc2>A0 and get_T([com1,com2],[rate_input,r[index2]])<get_T([com1,com2],[rate_input,r[index1]]):
                r_return = [r[index2], acc2]
        else:
            if acc2 > A0:
                r_return = [r[index2], acc2]
    else:
        if acc1>A0:
            r_return= [r[index1],acc1]
            if acc2>A0 and get_T([com2,com1],[r[index2],rate_input])<get_T([com2,com1],[r[index1],rate_input]):
                r_return = [r[index2], acc2]
        else:
            if acc2 > A0:
                r_return = [r[index2], acc2]

    # judge whether to return
    if(abs(index2 - index1) <= 1):
        return r_return

    # begin to iteration
    output = CRS_next(r, A0, com1, com2, rate_input, wh, index1, index2, acc1, acc2)  
    return output  # the form of output is [rate, accuracy]



def search_rate2_acc(R, A0, com1, rate1, com2):
    ''' search the maximum rate2 under a given condition including rate1

    Args:
    * R: the set of possible strategy solution.
    * A0: the given accuracy which the final strategy should fit. 
    * com1, com2: the number of compression layer
    * rate1: the compression rate

    Returns:
    * [rate, acc]: the maximum compression and its accuracy
    '''

    return CRS_search(R, A0, com1, com2, rate1, 1)


def search_rate1_acc(R, A0, com1, com2 = 1, rate2 = -1.0):
    ''' search the maximum rate1 under a given condition including rate2

    Args:
    * R: the set of possible strategy solution.
    * A0: the given accuracy which the final strategy should fit. 
    * com1, com2: the number of compression layer
    * rate2: the compression rate

    Returns:
    * [rate, acc]: the maximum compression and its accuracy
    '''

    if(rate2 == -1.0):
        com2 = com1

    return CRS_search(R, A0, com1, com2, rate2, 0)



def CAE(com1, rate1, com2, rate2):
    ''' estimate the accuracy of given strategy by linear function based on rate1 and rate2

    Args:
    * com1, com2: the number of compression layer
    * rate1, rate2: the compression rate

    Returns:
    * [rate, acc]: the maximum compression and its accuracy
    '''    

    acc = 1.0
    cae1 = 999  # the accuracy estimated by rate1
    cae2 = 999  # the accuracy estimated by rate1
    temp1 = 999  # accuracy of the point whose rate1 is cloest and less than the given rate1 
    temp2 = 999  # accuracy of the point whose rate2 is cloest and less than the given rate2 

    sql = MySQL()
    number_of_channel = np.load("./model_profile/partitions.npy")
    # change index to real number of layer
    r_com1 = number_of_channel[0][com1]
    r_com2 = number_of_channel[0][com2]

    # situation of single layer compression
    if(r_com1 == r_com2):
        res = sql.search_rate1_rate2_acc(r_com1, r_com2)
        if not res:
            return acc
        local = 0
        distance = 1.0
        for i in range(len(res)):
            dis = rate1 - res[i][0]
            if dis > 0 and dis < distance:
                local = i
                distance = dis
        cae = 1.0
        r1_r2 = get_r1_r2(res, rate1, in_single_layer=True)
        if r1_r2 != [] and r1_r2[0][0] != r1_r2[1][0]:
            cae = (r1_r2[0][1] - r1_r2[1][1]) * (rate1 - r1_r2[0][0]) / (r1_r2[0][0] - r1_r2[1][0]) + r1_r2[0][1]
        if distance == 1.0:
            return min(acc, cae)
        else:
            return min(res[local][2], cae)


    # situation of double layer compression
    # estimate based on rate1
    res = sql.search_rate1_acc(r_com1, r_com2, rate2)
    if res != ():
        r1_r2 = get_r1_r2(res, rate1)
        temp = get_mininest_r1(res, rate1)
        if r1_r2 != []:
            cae1 = (r1_r2[0][1] - r1_r2[1][1]) * (rate1 - r1_r2[0][0]) / (r1_r2[0][0] - r1_r2[1][0]) + r1_r2[0][1]
        if temp != []:
            temp1= temp[0][1]

    # estimate based on rate2
    res = sql.search_rate2_acc(r_com1, rate1, r_com2)
    if res != ():
        r1_r2 = get_r1_r2(res, rate2)  # r1_r2 has the form [[r1, A1], [r2, A2]]
        temp = get_mininest_r1(res, rate2)
        if r1_r2 != []:
            cae2 = (r1_r2[0][1] - r1_r2[1][1]) * (rate2 - r1_r2[0][0]) / (r1_r2[0][0] - r1_r2[1][0]) + r1_r2[0][1]
        if temp != []:
            temp2 = temp[0][1]
    acc = min(cae1, cae2, acc, temp1, temp2)
    return acc


def get_r1_r2(res, rate, in_single_layer=False):
    ''' find two points whose rate are both at the same side of the given rate. If there is no such point, return []

    Args:
    * res: a set of points
    * rate: a compression rate
    * in_single_layer: default False. if True, using for the situation of single layer compression

    Returns:
    * r1_r2: a tuple of two points [[r1, A1], [r2, A2]] or []
    '''
    r1_r2 = []
    num = len(res)
    rates = np.zeros((num, 2), dtype=np.float32)
    for i in range(num):
        rates[i][0] = res[i][0]
        if in_single_layer:
            rates[i][1] = res[i][2]
        else:
            rates[i][1] = res[i][1]

    rates = rates[rates[:,0].argsort()]  # order by the rate in first compression layer

    # record the location of every item
    location = 0
    for i in range(num):
        if(rates[i][0] < rate):
            location = i
        else:
            location = i
            break

    if(location > 1): # there are two points on the left side of given rate
        r1_r2 = [[rates[location-2][0], rates[location-2][1]], [rates[location-1][0], rates[location-1][1]]]
    elif(num - location > 1): # there are two points on the right side of given rate
        r1_r2 = [[rates[location][0], rates[location][1]], [rates[location+1][0], rates[location+1][1]]]
    return r1_r2


def get_mininest_r1(res, rate):
    ''' find the point whose rate are cloest and bigger than the given rate. If there is no such point, return []

    Args:
    * res: a set of points
    * rate: a compression rate

    Returns:
    * r1: a point rate
    '''    
    num = len(res)
    rates = np.zeros((num, 2), dtype=np.float32)
    for i in range(num):
        rates[i][0] = res[i][0]
        rates[i][1] = res[i][1]

    rates = rates[rates[:,0].argsort()]  # order by the rate in first compression layer

    # record the location of every item
    location = 0
    for i in range(num):
        if(rates[i][0] <= rate):
            location = i
        else:
            location = i-1
            break

    if location<0:
        return []

    r1= [[rates[location][0],rates[location][1]]]
    return r1


def A(com2, rate2, com1 = 1, rate1 = -1.0): 
    ''' get the accuracy of given strategy

    Args:
    * com1, com2: the number of compression layer
    * rate1, rate2: the compression rate

    Returns:
    * acc: the accuracy of given strategy
    ''' 
    if(rate1 == -1.0):
        acc = get_acc(com2, rate2)
    else:
        acc = get_acc(com1, rate1, com2, rate2)
    return acc

def get_r_range(r):
    ''' get the range of r

    Args:
    * r: a set of possible solution

    Returns:
    * [index1,index2]: the range of r
    '''     
    num = len(r)
    index1 = num-1 # denote the minimum index of r
    index2 = 0 #  denote the maximum index of r
    for temp in range(num):
        if r[temp]>0:
            if temp<index1:
                index1=temp
            if temp>index2:
                index2=temp
    if index2<index1:
        return []
    else:
        return [index1,index2]


if __name__ == '__main__':


    print("For test!")