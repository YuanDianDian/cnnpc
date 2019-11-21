import numpy as np
import src_cnnpc.CRS as CRS
from src_cnnpc.R_support import create_R, update_R, nextPoint_R, get_R
from src_cnnpc.latency_support import min_profile_T, get_T
from src_cnnpc.tools import add_logs, turn_r_L

def main(input_A, is_warmup=False):
    '''main function

    Args:
    * input_A: the accuracy requirement
    '''
    A0 = input_A  
    L_partition = np.load("./model_profile/partitions.npy")  # load the partition points and their channel amount in model：[[1, 11, ...],[64, 64, ...],[2,22,...]]
    num_partition = L_partition.shape[1]
    rate_temp = [0.0, 0.0]  # current optimal compression rates
    L_temp = [0, 0]  # current optimal partition points
    T = min_profile_T()  # find the minimum latency among single device inference
    add_logs('original T is:' + str(T))
    add_logs('A0 is:' + str(A0))

    warmup = is_warmup  # whether create the solution space afresh
    if not warmup:
        create_R()

    for i in range(num_partition):
        for j in range(i + 1, num_partition):
            update_R(i, 1.0, T, j, 0)

    for i in range(num_partition):
        # start to single device search
        add_logs("------Partition Layer " + str(i) + " Search Begin------\n")
        R = np.zeros((L_partition[1][i]), dtype=np.float32)  # create solution space R for single layer compression
        for m in range(L_partition[1][i]): # update R
            R[m] = m / L_partition[1][i]
            if get_T([i], [R[m]]) > T or CRS.CAE(i, R[m], i, R[m]) < A0:
                R[m] = -10
        add_logs("------For CRS：------\n")

        res = CRS.search_rate1_acc(R, A0, i)  # search the maximum compression rate r1 with given com1 and A0
        if res == []:
            continue
        rate_1 = res[0]

        t = get_T([i], [rate_1])
        if t < T: # update the optimal solution
            L_temp = [i, 0]
            rate_temp = [rate_1, 0.0]
            T = t
            logs = "------Best point changed!------\n"
            logs += "New Best Partitions: " + str(turn_r_L(L_temp)) + "\n"
            logs += "New Best Compression Rate: " + str(rate_temp) + "\n"
            logs += "New Best Latency: " + str(T) + "\n"
            add_logs(logs)

        add_logs('start to two devices search\n')
        for j in range(i + 1, num_partition):
            add_logs("For partition Layer " + str(j) + " Search\n")
            update_R(i, rate_temp[0], T, j, 0) # update solution space R 
            while True:
                next_point = nextPoint_R(i,j)
                if not next_point:
                    break
                rate_1 = next_point[0]
                rate_2 = next_point[1]
                add_logs('next_point :' + str(next_point) + "\n")
                add_logs("------For judgment：------" + "\n")
                print('the result of CAE is:',CRS.CAE(i, rate_1, j, rate_2))
                if CRS.CAE(i, rate_1, j, rate_2) > A0 and CRS.CAE(j, rate_2, j, rate_2) > A0 and CRS.A(j, rate_2) > A0 and CRS.A(j, rate_2, i, rate_1) > A0:
                    R = get_R(i, rate_1, j)
                    add_logs("------For CRS：------" + "\n")
                    res = CRS.search_rate2_acc(R, A0, i, rate_1, j)
                    rate_2 = res[0]

                    # update the optimal solution
                    rate_temp = [rate_1, rate_2]
                    L_temp = [i, j]
                    T = get_T([i, j], [rate_1, rate_2])
                    logs = "------Best point changed!------\n"
                    logs += "New Best Partitions: " + str(turn_r_L(L_temp)) + "\n"
                    logs += "New Best Compression Rate: " + str(rate_temp) + "\n"
                    logs += "New Best Latency: " + str(T) + "\n"
                    add_logs(logs)
                update_R(i, rate_1, T, j, 1) # update solution space R 

    add_logs("Best ponit:" + str(turn_r_L(L_temp)) + " " + str(rate_temp) + " " + str(T) + "\n")
    if L_temp[0] >= L_temp[1] and rate_temp[0] >= rate_temp[1]: # get the number of compression layer
        all_latency, best_deploy = get_T([turn_r_L(L_temp)[0]], [rate_temp[0]], for_minT=False)
    else:
        all_latency, best_deploy = get_T(turn_r_L(L_temp), rate_temp, for_minT=False)
    add_logs(all_latency)

    result = "When A0 is " + str(A) + "\n"
    result += "Best point:" + str(turn_r_L(L_temp)) + " " + str(rate_temp) + " " +str(T) + "\n"
    result += "The deployment way:" + best_deploy
    with open('result.txt', 'w+') as f:
        f.write(result)

if __name__ == '__main__':   
    pass
