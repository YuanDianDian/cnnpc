# CNNPC

...introduction...

## Requirments
Install all the packages from requirment.txt
* Python3 tensorflow pandas sklearn pymysql openpyxl
* mysql5.6+

## Data
* Experiments are run on ImageNet-1000
* You may follow the data preparation guide [here](https://pocketflow.github.io/tutorial/).

## Running the experiments
#### Prepare
1. Copy all PocketFlow [contents](https://github.com/YuanDianDian/PocketFlow) to the current directory
2. If a data directory path exists, then replace 'None' with the actual path.
3. Creat a new dataset in MySQL and excute the following command to load the prepared data table
```
cd SQL-file
mysql -u'user' -p'123456' cnnpc < db.sql;
```
    Attention: replace user and 123456 with you own account and password
4. Edit the account and password to yours in ./src_cnnpc/mysql_support.py (line 17)
5. Execute:
```
chmod 777 ./scripts/run_local.sh
```
#### Run
According to your needs to modify auto.py, you can execute like this:
```
python auto.py --model=mobilenet --end_device=MI8 --bandwidth=10 --A0=0.896
```

## Result
Then you can find the best result and the pilot process of all situations in ./result
