import os
import subprocess
import re
import numpy as np
from src_cnnpc.mysql_support import MySQL
from src_cnnpc import pocketflow_acc

def run_cmd2file(cmd, listname):
    '''Save the inference output to file

    Args:
    * cmd: indicate which program should run
    * listname: the file path where you save
    '''
    fdout = open((listname.rstrip('.list\n')+"/file_out.log") , 'w')
    fderr = open((listname.rstrip('.list\n')+"/file_err.log") , 'w')
    p = subprocess.Popen(cmd, stdout=fdout, stderr=fderr, shell=True)
    if p.poll():
        return
    p.wait()
    return 0

def create_ratio_list():
    '''create ratio lists from the file: ratio.txt'''
    number_of_channel = np.load('./model_profile/partitions.npy')
    os.system('rm -r list')
    os.system('mkdir list')
    f=open('ratio.txt','r')
    rlist=f.readlines()
    f.close()
    net_name = get_net_name()
    count=0

    for i in rlist: # the form of i is a-b. a is the amount of partition point. b includes the number of partition point and compress ratio,                     which has a form: number-ratio
        temp=i.split('-')
        amount=int(temp[0]) # amount of partition point
        number=[] # number of partition point
        ratio=[] # correspond compression ratio of partition point
        name='./list/'+net_name+'_'+i.rstrip('\n')+'.list'
        real_number_list = []
        for j in range(amount): 
            number.append(temp[1+j*2])
            ratio.append(temp[2+j*2].rstrip('\n'))
        for j in number:
            temp1 = np.argwhere(number_of_channel[0]==int(j))[0][0]
            real_number_list.append(number_of_channel[2][temp1])
        f=open(name,'w')
        for j in range(int(temp[-2])*2+2):
            real_number=j
            if int(real_number) in real_number_list :
                f.writelines(ratio[real_number_list.index(int(real_number))])
            else:
                f.writelines('1')
            f.writelines('\n')
        f.close()
        count += 1
    return 0

def execute_inference(com1,com2,nearest):
    '''execute CNN compression and inference according the file ratio.txt

    Args:
    * com1, com2: the number of compression layer
    * nearest: choose the start point to compress
    '''
    # init count
    count=1
    net_name = get_net_name()
    # find the ratio.list in this loop
    rootdir=os.getcwd()
    listnames= os.listdir(rootdir+'/list')

    f=open('./ratio.txt','r')
    listnames=f.readlines()
    f.close()
    number_of_channel = np.load("./model_profile/partitions.npy")
    print('number_of_channel :',number_of_channel)
    print('nearest is :', nearest)

    # the model file you want to start from
    if nearest[0]==nearest[1] and nearest[0]==0: 
        start_point_name = net_name+'_2-'+str(0)+'-'+str(0.0)+'-'+str(0)+'-'+str(0.0) # from the original model
    else:
        temp_index1=np.argwhere(number_of_channel[0]==com1)[0][0]
        temp_index2 = np.argwhere(number_of_channel[0] == com2)[0][0]
        temp1= pocketflow_acc.turn_to_r_rate(temp_index1,float(1-nearest[0]), temp_index2,float(1 - nearest[1]))
        start_point_name= net_name+'_2-'+str(com1)+'-'+str(temp1[2])+'-'+str(com2)+'-'+str(temp1[3])

    print('prune from the model in '+start_point_name)

    for listname in listnames:
        # copy the target ratio.list to file 
        listname = net_name+'_'+listname.rstrip('\n')+'.list'
        print('start to prune '+listname.rstrip('.list\n'))
        os.system('cp list/'+listname +' ./ratio.list')
        print('finish '+listname+'.txt copy')
        
        # copy the target model to /models
        os.system('rm -r models')
        os.system('mkdir models')

        if count==1:
            os.system('cp ./'+start_point_name+'/models/bes* ./models/')
            os.system('cp ./'+start_point_name+'/models/checkpoint ./models/')
            print('now count is '+ str(count))
        else:
            print('now count is '+ temp2.rstrip('.list'))
            os.system('cp '+temp2.rstrip('.list')+'/models/bes* ./models')
            os.system('cp '+temp2.rstrip('.list')+'/models/checkpoint ./models')
        temp2 = listname
        count=count+1
        
        # start to prune
        os.system('./scripts/run_local.sh nets/'+ net_name +'_at_ilsvrc12_run.py  \ --learner channel \ --cp_prune_option list \ --cp_prune_list_file ./ratio.list \ --save_step 1000  \ --enbl_warm_start True') # 4000
        
        # save the training result, including models and logs
        os.system('mkdir '+listname.rstrip('.list\n'))
        os.system('cp -r ./models '+listname.rstrip('.list\n')+'/')
        os.system('cp -r ./logs '  +listname.rstrip('.list\n') + '/')
        
        # start to inference the model and save the accuracy
        print('start to inference '+listname.rstrip('.list\n'))
        run_cmd2file("./scripts/run_local.sh nets/"+ net_name +"_at_ilsvrc12_run.py  --exec_mode eval", listname)   
    return 0

def save_result_to_sql():
    '''save new results to sql'''
    sql = MySQL()
    number_of_channel = np.load("./model_profile/partitions.npy")
    # find the accuracy according to the ratio.txt
    f=open('ratio.txt','r')
    count=0
    f_name=f.readlines()
    f.close()
    net_name = get_net_name()
    pattern=re.compile(net_name)
    cp=os.path.abspath('.')
    name_list=os.listdir(cp)
    for j in f_name:
        temp_pattern=re.compile(j.strip('\n'))
        for i in name_list:
            if not re.match(pattern,i)==None:
                if not re.search(temp_pattern,i)==None:
                    # find the content including accuracy
                    f = open(i+'/file_err.log','r')
                    temp = f.readlines()
                    f.close()
                    temp1 = i.split('-')
                    temp2= temp[-2].split('=')[-1] # this is the accuracy of top 1 
                    temp2= temp[-1].split('=')[-1] # this is the accuracy of top 5 
                    temp2= temp2.rstrip('\n')                    
                    model_dir= cp+'/'+i+'/models' # define the model's directory
                    print('temp1 is: ',temp1)
                    print('temp2 is: ',temp2)
                    temp_index1 = np.argwhere(number_of_channel[0]==int(temp1[1]))[0][0]
                    temp_index2 = np.argwhere(number_of_channel[0] == int(temp1[3]))[0][0]
                    temp3= pocketflow_acc.turn_to_r_rate(temp_index1,1-float(temp1[2]),temp_index2,1-float(temp1[4]))
                    check_exist= sql.search_acc(int(temp1[1]),float(temp3[2]),int(temp1[3]),float(temp3[3]))
                    if not not check_exist:
                        continue
                    sql.save_result(int(temp1[1]),float(temp3[2]),int(temp1[3]),float(temp3[3]),float(temp2),model_dir) # here, the compression rate is the number of pruning channel
                    with open('process.txt', 'a+') as f:
                        f.write("PocketFlow-get: %d %.6f %d %.6f" % (int(temp1[1]),float(temp1[2]),int(temp1[3]),float(temp1[4])) + "\n")
    return 0

def get_net_name():
    f = open('set.txt','r')
    init_set = f.readline()
    f.close()
    net_name = init_set.rstrip('\n')
    return  net_name
