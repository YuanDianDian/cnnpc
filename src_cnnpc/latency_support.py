import numpy as np

def min_profile_T_():
    '''find the minimum latency when only use one device

    Returns:
    * Latency: the minimum latency when only use one device
    ''' 
    T_R = np.load("./model_profile/T_R.npy") # running time of each layer on every device 
    T_C = np.load("./model_profile/T_C.npy") #transmittion time of each layer between every two devices 
    T_end= sum(T_R[:,0])+0.53+1.127
    T_edge= sum(T_R[:,1])+T_C[0,0]+0.53+1.13
    T_cloud= sum(T_R[:,2])+T_C[0,1]+0.53+1.13
    return min(T_end, T_cloud, T_edge)

def min_profile_T():
    '''find the minimum latency with Neurosurgeon

    Returns:
    * Latency: the minimum latency when only use one device
    ''' 
    a = np.load("./model_profile/partitions.npy")
    num = a.shape[1]
    T = 1000.0
    parts = []
    rates = []
    for i in range(num):
        p = [i]
        r = [0.0]
        t = get_T(p, r)
        if t < T:
            T = t
            parts = p
            rates = r
        for j in range(i, num):
            p = [i, j]
            r = [0.0, 0.0]
            t = get_T(p, r)
            if t < T:
                T = t
                parts = p
                rates = r

    return T


def min_cnnpc_T(for_minT=False):
    '''find the minimum time by algorithm

    Args:
    * for_minT: if True, return a float number only

    Returns:
    * T: the minimum latency when using CNNPC algorithm
    '''
    a = np.load("./model_profile/partitions.npy")
    num = a.shape[1]
    T = 1000.0
    parts = []
    rates = []
    for i in range(num):
        p = [i]
        r = [1 - 1.0 / a[1][i]]
        t = get_T(p, r)
        if t < T:
            T = t
            parts = p
            rates = r
        for j in range(i, num):
            p = [i, j]
            r = [1 - 1.0 / a[1][i], 1 - 1.0 / a[1][j]]
            t = get_T(p, r)
            if t < T:
                T = t
                parts = p
                rates = r
    if for_minT:
        return T
    else:
        return str(T)+str(parts)+str(rates)


def cnnpc_latency_range():
    '''return the latency range when using CNNPC algorithm

    Returns:
    * T: [min-latency, max-latency]
    '''
    T = [min_cnnpc_T(for_minT=True), min_profile_T()]
    return T


def get_T(com, rate, for_minT=True):
    '''get the latency of given strategy

    Args:
    * com: denotes the compression layer
    * rate: denotes the compression rate
    * for_minT: if True, return a float number only
    
    Return:
    * T: the latency of given strategy
    * temp: all kinds of the deployment ways and their latency
    * best_deploy: the best deployment way
    '''
    T_R = np.load("./model_profile/T_R.npy")
    T_C = np.load("./model_profile/T_C.npy") 
    
    temp = 'EEC result'
    best_deploy = 'end-edge-cloud'
    if len(com)==2 and com[0]!=com[1]:
        T = sum(T_R[0:com[0] + 1, 0]) + sum(T_R[com[0] + 1:com[1] + 1, 1]) + sum(T_R[com[1] + 1:len(T_R) + 1, 2]) + T_C[
            com[0] + 1, 0] * (1 - rate[0]) + T_C[com[1] + 1, 1] * (1 - rate[1])+0.53+1.13
        temp = 'end-edge-cloud: ' + str(T)
        best_deploy = 'end-edge-cloud'
    else:
        T1 = sum(T_R[0:com[0] + 1, 0]) + sum(T_R[com[0] + 1:len(T_R) + 1, 1]) + T_C[com[0] + 1, 0] * (
                    1 - rate[0])+0.53+1.13  # end-edge inference time
        T2 = sum(T_R[0:com[0] + 1, 0]) + sum(T_R[com[0] + 1:len(T_R) + 1, 2]) + (
                    T_C[com[0] + 1, 0] + T_C[com[0] + 1, 1]) * (1 - rate[0])+0.53+1.13  # end-cloud inference time
        T3 = sum(T_R[0:com[0] + 1, 1]) + sum(T_R[com[0] + 1:len(T_R) + 1, 2]) + T_C[com[0] + 1, 1] * (1 - rate[0]) + \
             T_C[0, 0]+0.53+1.13  # edge-cloud inference time
        T= min(T1,T2,T3)

        if not for_minT:
            temp = 'end-edge: ' + str(T1) + '\n' + 'end-cloud: ' + str(T2) + '\n' + 'edge-cloud: ' + str(T3)
            if T1 <= T2 and T1 <= T3:
                best_deploy = 'end-edge' 
            elif T2 <= T1 and T2 <= T3:
                best_deploy = 'end-cloud' 
            else:
                best_deploy = 'edge-cloud' 

    if for_minT:        
        return T
    else:
        return temp, best_deploy


if __name__ == '__main__':
    '''test content'''
    cnnpc_latency_range()
    pass
    parts = [0, 4]
    rates = [1 - 0.09375, 1-0.453125]
    print(get_T(parts, rates))
