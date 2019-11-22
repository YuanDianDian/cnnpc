# Collaborative CNN Inference with Joint Model Partition and Compression in End-Edge-Cloud Systems

We proposed CNNPC, a distributed collaborative system based on the model compression and on-device deployment methods, to inference CNN with high accuracy and low latency. CNNPC achieves this goal by three parts: the distributed nature, a model compression method and a search algorthim. The distributed nature of CNNPC ensures the data privacy, the model compression method driven by communication reduce transmission latency significantly and the search algorthim finds the best compression and deployment strategy which gets the largest latency reduction with least accuracy loss. In our experiments, comprared with single-end and state-of-the-art collaborative approaches, collaborative inference latency is up to 6.1x and 4.1x faster, and communication requirements are reduced by a factor of 45.6x and 16.5x respectively in CNNPC.

## Structure

## Dependencies
* tensorflow = 1.12.0
* pandas >= 0.25.3 
* sklearn >= 0.0 
* pymysql >=  0.9.3 
* openpyxl >= 3.0.0 
* mysql >= 15.6+

## Data Resource
* Experiments are running on the dataset ImageNet
* You may follow the data preparation guide [here](https://pocketflow.github.io/tutorial/).

## Running the experiments
#### Prepare
* Copy [CNNPC](https://github.com/YuanDianDian/cnnpc.git) to local
```
git clone https://github.com/YuanDianDian/cnnpc.git
```
* Copy [PocketFlow](https://github.com/YuanDianDian/PocketFlow) to CNNPC file:
```
git clone https://github.com/YuanDianDian/PocketFlow.git CNNPC
cd CNNPC
```
* Open the file './path.conf' and change the value of 'data_dir_local_ilsvrc12' to the local path of ImageNet.(Line 25)
* Creat a new database 'cnnpc' in MySQL and excute the following command to load the prepared data table
```
cd SQL-file
mysql -u'user' -p'123456' cnnpc < cnnpc.sql;
```
    Attention: replace 'user' and '123456' with you own account and password
* Edit the serverIP and password to yours in ./src_cnnpc/mysql_support.py (line 18)
* Execute follow command to change the access permissions of files.
```
chmod 777 ./scripts/run_local.sh
```
#### Run
According to your needs to modify auto.py, you can execute like this:
```
python auto.py --model=mobilenet --end_device=MI8 --bandwidth=10 --A0=0.896
```
#### Result
You can find the best result and the pilot process of all situations in ./result

## Self-defined Process
Self-defined processes (including the neural network and inference environment) are also supported by CNNPC. 

If you would like to change the type of neural network, you should create the model in [Pocketflow](https://pocketflow.github.io/self_defined_models/#self-defined-models) first. 
Then, create a new './model_profile/partitions.npy' which is a 3xN numpy array, where N is the total number of possible compression layers. Its first line indicates the block index (e.g. the inception block). Its second line indicates the channel's number of every kernel in this block. And the last line includes the real layer index and this information will be uesd to guide the model compression process. 
Additionally, change the './model_profile/T_C.npy' and './model_profile/T_R.npy' to the actual transmission and running latency according to the profiling results with given environment. 

If you would like to change the inference environment setting, only recreate the './model_profile/T_C.npy' and './model_profile/T_R.npy' according to the profiling results with given environment.
