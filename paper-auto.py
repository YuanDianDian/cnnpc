import cnnpc_main_T0 as cnnpc_for_acc
import cnnpc_main_A0 as cnnpc_for_t
import os
from src_cnnpc.tools import partitions_init

model = 'resnet' # or 'mobilenet'
partitions_init(model)

def group_for_acc(end, w, Ts):
    '''
    Args:
    * end: a string, end-device's name
    * w: a float, bandwith between edge and cloud
    * Ts: a list, given latency
    '''
    os.system('cp ./R-C-Time/'+model+'/TC-20M-'+str(w)+'M/T_C.npy ./model_profile/T_C.npy')

    cnnpc_for_acc.main(Ts[0])
    os.system('mv ./process.txt ./result/'+model+'/'+end+'-20M-'+str(w)+'M/process-'+str(Ts[0])+'.txt')
    os.system('mv ./result.txt ./result/'+model+'/'+end+'-20M-'+str(w)+'M/result-'+str(Ts[0])+'.txt')

    cnnpc_for_acc.main(Ts[1])
    os.system('mv ./process.txt ./result/'+model+'/'+end+'-20M-'+str(w)+'M/process-'+str(Ts[1])+'.txt')
    os.system('mv ./result.txt ./result/'+model+'/'+end+'-20M-'+str(w)+'M/result-'+str(Ts[1])+'.txt')

    cnnpc_for_acc.main(Ts[2])
    os.system('mv ./process.txt ./result/'+model+'/'+end+'-20M-'+str(w)+'M/process-'+str(Ts[2])+'.txt')
    os.system('mv ./result.txt ./result/'+model+'/'+end+'-20M-'+str(w)+'M/result-'+str(Ts[2])+'.txt')


def group_for_t(end, w, Accs):
    '''
    Args:
    * end: a string, end-device's name
    * w: a float, bandwith between edge and cloud
    * Accs: a list, given accuracy
    '''
    os.system('cp ./R-C-Time/'+model+'/TC-20M-'+str(w)+'M/T_C.npy ./model_profile/T_C.npy')

    cnnpc_for_t.main(Accs[0])
    os.system('mv ./process.txt ./result/'+model+'/'+end+'-20M-'+str(w)+'M/process-'+str(Accs[0])+'.txt')
    os.system('mv ./result.txt ./result/'+model+'/'+end+'-20M-'+str(w)+'M/result-'+str(Accs[0])+'.txt')

    cnnpc_for_t.main(Accs[1])
    os.system('mv ./process.txt ./result/'+model+'/'+end+'-20M-'+str(w)+'M/process-'+str(Accs[1])+'.txt')
    os.system('mv ./result.txt ./result/'+model+'/'+end+'-20M-'+str(w)+'M/result-'+str(Accs[1])+'.txt')
    


if __name__ == '__main__':
    
    ## Mobilenet
    # 44.34555  37.6556  30.96565 Mi 20M 10M 
    # 44.382925 37.73035 31.07775 Mi 20M 5M
    # 44.682    38.3285  31.975   Mi 20M 1M

    # 60.3936  49.3675 38.3414  MiSE 20M 10M
    # 60.431   49.4423 38.4535  MiSE 20M 5M
    # 60.7301  50.0404 39.3508  MiSE 20M 1M

    # resnet

    # MI8 
    os.system('cp ./R-C-Time/'+model+'/TR-MI8/T_R.npy ./model_profile/T_R.npy')

    Ts = [66.133125, 52.18065, 38.228175]
    group_for_acc('MI8', 10, Ts)

    Ts = [66.1750,   52.2554,  38.3403]
    group_for_acc('MI8', 5, Ts)

    Ts = [66.469575, 52.85355, 39.237525]
    group_for_acc('MI8', 1, Ts)

    # MI8SE 
    os.system('cp ./R-C-Time/'+model+'/TR-MI8SE/T_R.npy ./model_profile/T_R.npy')

    Ts = [70.14935,  55.87134, 41.59332]
    group_for_acc('MI8SE', 10, Ts)

    Ts = [70.186735, 55.94609, 41.705445]
    group_for_acc('MI8SE', 5, Ts)

    Ts = [70.485581, 56.54424, 42.60267]
    group_for_acc('MI8SE', 1, Ts)


    # MI8 
    os.system('cp ./R-C-Time/'+model+'/TR-MI8/T_R.npy ./model_profile/T_R.npy')
    # original accuracy 0.906
    Accs = [0.896, 0.856]
    group_for_t('MI8', 10, Accs)
    group_for_t('MI8', 5, Accs)
    group_for_t('MI8', 1, Accs)

    # MI8SE 
    os.system('cp ./R-C-Time/'+model+'/TR-MI8SE/T_R.npy ./model_profile/T_R.npy')
    # original accuracy 0.906
    Accs = [0.896, 0.856]
    group_for_t('MI8SE', 10, Accs)
    group_for_t('MI8SE', 5, Accs)
    group_for_t('MI8SE', 1, Accs)




