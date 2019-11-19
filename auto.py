import cnnpc_main_T0 as cnnpc_for_acc
import cnnpc_main_A0 as cnnpc_for_t
from src_cnnpc.tools import partitions_init

from options import args_parser
import os

def set_model(model):
    with open('set.txt', 'w+') as f:
        f.write(model)
    
if __name__ == '__main__':
    
    args = args_parser()

    model = args.model
    end_device = args.end_device
    args.bandwith = args.bandwidth

    set_model(model) # create set.txt
    partitions_init(model)
    os.system('cp ./R-C-Time/'+model+'/TR-'+end_device+'/T_R.npy ./model_profile/T_R.npy')
    os.system('cp ./R-C-Time/'+model+'/TC-20M-'+bandwidth+'M/T_C.npy ./model_profile/T_C.npy')

    if args.Accuracy:
        cnnpc_for_t.main(float(args.Accuracy))
        os.system('mv ./process.txt ./result/'+model+'/'+end_device+'-20M-'+bandwidth+'M/process-'+args.Accuracy+'.txt')
        os.system('mv ./result.txt ./result/'+model+'/'+end_device+'-20M-'+bandwidth+'M/result-'+args.Accuracy+'.txt')        

    if args.Latency:
        cnnpc_for_t.main(float(args.Latency))
        os.system('mv ./process.txt ./result/'+model+'/'+end_device+'-20M-'+bandwidth+'M/process-'+args.Latency+'.txt')
        os.system('mv ./result.txt ./result/'+model+'/'+end_device+'-20M-'+bandwidth+'M/result-'+args.Latency+'.txt')        




