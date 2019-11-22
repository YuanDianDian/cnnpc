## An Introduction of Code：
### Auto.py:
Search the best strategy according to the given model, accuracy, latency, device and bandwith. This file calls 'cnnpc_main_A0.py' and 'cnnpc_main_T0.py'.

### cnnpc_main_A0/T0：
A0, T0 分别对应于给定精度约束求最低时延和给定时延约束求最高精度两种情景。
该文件给出了对应算法的基本框架，其基本思路是对两个分割层选择的嵌套遍历循环，并在循环过程中，逐步加强约束条件，缩小解空间范围，直至剩唯一符合要求的解。
流程说明：
首先进行解空间以及部分变量的初始化；之后开始第一个分割点i的循环遍历，在固定i的情况下，求得单分割情况下的最优方案；以该分割方案为出发点，进行第二个点j的循环遍历，求得对应分割层选取下的最优方案，并进行约束条件和解空间范围的更新。

### ./src_cnnpc/
该文件夹主要存放了需要在主函数中直接调用的一些模块，包括精度估计与搜索模块CRS.py，模型推理延时刻画模块latency_support.py，解空间操作模块R_support.py, execute_compression.py和pocketflow.py提供基于PocketFlow的压缩功能,mysql_support.py提供MySQL数据库功能。
1.	CRS.py的两个核心函数为CAE()和CRS_serach()，其作用分别是对给定方案进行精度估计，搜索给定精度和压缩层条件下的最大压缩率。在实现过程中，它们又会调用获得最近点get_descrete_point()，获得精度get_acc()等子函数模块（详细说明可参见末尾的函数列表）。需要注意的是，CRS_search()自身主要充当一个接口的作用，其主体循环是在CRS_next()中完成的。
2.	latency_support.py文件对模型的延时进行了刻画。其中，min_profile_T()给出了模型在纯端、纯边、纯云三种情况下，推理延时最低的一种；get_T()则会给出对应方案的推理延时，当给定方案为单层压缩的时候，它给出的是端边、边云、端云中推理延时最低的那一种。
3.	R_support.py文件包含了一些对解空间的操作方式，主要用途是在搜索过程中对解空间进行限制和更新。
4.	Mysql_support.py通过定义类MySQL中的各种操作函数，为整个搜索过程中的数据和模型文件的存储、修改、检索提供了技术支持，使得工程在多次运行的情形下可以更加有效的利用历史数据以及结果。
5.	POCKETFLOW_ACC.py和EXECUTE_COMPRESSION.py共同实现了模型压缩功能，前者侧重于为我们的工程提供接口并提供一些转换服务，使得我们的工程可以更好的与PocketFlow进行对接。而EXECUTE_COMPRESSION.py则侧重于对PocketFlow的调用，它使得PocketFlow工程对用户透明化，减少了使用时所需要考虑的因素，降低了使用难度。

### Model_profile:
该文件夹下主要存储由上一环节model profiling得到的一些模型特性，如模型各层通信量的传输时间T_C.npy，模型各层在各设备上的运行时间T_R.npy，以及模型的可选分割层以及其对应通道数partitions.npy等。

## 附：函数列表
#### CRS.py:
1.	get_descrete_point(input_rate, r) 
将理论压缩率转化为实际的离散的压缩率, 返回索引
2.	get_acc(com1, rate1, com2 = 0, rate2 = -1.0)
得到需要压缩的点的精确度，数据库中搜索得到或者训练得到 A()
3.	CRS_next(r, A0, com1, com2, rate_input, wh, index1, index2, acc1, acc2)
核心迭代搜索算法
4.	CRS_search(r, A0, com1, com2, rate_input, wh)
wh 为1 表示输入rate1，为0 表示输入为rate2
5.	search_rate2_acc(R, A0, com1, rate1, com2)
已知 rate1 搜寻 rate2
6.	search_rate1_acc(R, A0, com1, com2 = 1, rate2 = -1.0)
已知 rate2 搜寻 rate1
7.	CAE(com1, rate1, com2, rate2)
用直线拟合估计精度
8.	get_r1_r2(res, rate)
从一系列已有点中找出，在 rate 同一侧的两个点，没有就返回 []
9.	get_mininest_r1(res, rate)
从一系列已有点中找出，比rate大最少的那个点，没有就返回 []
10.	A(com2, rate2, com1 = 1, rate1 = -1.0)
查询或者实测精度
11.	get_r_range(r)
获得解空间的范围
12.	get_r1_r2_special(res, rate)
为CAE中的单层压缩情况专用


#### Profile_support.py:
1.	min_profile_T()
寻找单端最短延迟
2.	get_T(com, rate)
此种情况下的(最佳延时)

#### R_support.py：
1.	update_R(com1, rate1, T, com2)
对此个解空间对应的 .npy 文件进行更新
2.	update_R_CAE(com1, com2, rate2, A)
第二种 Latency Search 中的第二种解空间的压缩
3.	nextPoint_R(com1, com2)
将当前解空间下按下边规则对应的 a1, a2 给出
4.	get_R(com1, rate1, com2)
为了CRS rate2，得到当前搜索位置下的局部解空间

#### POCKETFLOW_ACC.py:
1.	turn_to_r_rate(com1, rate1, com2, rate2)
压缩率转换
2.	get_nearest_point(input_rate, tuple_res)
获得最近点
3.	get_nearest_point_TD(input_rate1, input_rate2, tuple_res)
二维平面寻找最近的点
4.	is_proper_point(com_1, rate_1, com_2, rate_2, acc)
判断该点精度是否合理
5.	PocketFlow_acc(com1, rate1, com2, rate2)
用PocketFlow基于已有结果得出所要点的精度结果
6.	create_txt_of_ratio(com1, rate1, com2, rate2, nearest, number_of_channel)
生成PocketFlow所需的ratio.txt文件
7.	choose_interval(rate, w1, w2, w3)
步长区间选择

#### EXECUTE_COMPRESSION.py:
1.	run_cmd2file(cmd, listname)
将推理结果输出至文件
2.	create_ratio_list()
生成当次的压缩列表
3.	execute_inference(com1,com2,nearest)
执行压缩
4.	save_result_to_sql()
将结果保存至数据库

#### Mysql_support.py:
1.	__init__(self)
初始化
2.	SQL_connect(self)
连接服务器
3.	save_result(self, com_1, rate_1, com_2, rate_2, accuracy=0.0, res_dir='NO_DIR_INPUT')
向数据库增添结果
4.	delete_acc(self, com_1, rate_1, com_2, rate_2)
从数据库删除一条结果
5.	search_acc(self, com_1, rate_1, com_2, rate_2)
搜寻对应精度（两点压缩）
6.	search_acc_onePar(self, com_1, rate_1)
搜寻对应精度（单点压缩）
7.	search_rate2_acc(self, com_1, rate_1, com_2)
找到对应要求下的A2压缩率、对应的精度和地址
8.	search_rate1_acc(self, com_1, com_2, rate_2)
找到对应要求下的A1压缩率、对应的精度和地址
9.	search_rate1_acc_onePar(self, com_1, com_2)
找到对应要求下的所有 A1压缩率、 A1压缩率、 对应的精度和地址（单点压缩）
10.	search_rate1_rate2_acc(self, com_1, com_2)
找到对应要求下的所有 A1压缩率、 A1压缩率、 对应的精度和地址
11.	change_acc(self, com_1, rate_1, com_2, rate_2, accuracy)
修改对应实验的结果
12.	get_all_to_excel(self)
将数据库中的所有内容保存在本地一个Excel中
13.	search_pureacc(self, com_1, rate_1, com_2, rate_2)
查找对应点的精度
14.	search_puredir(self, com_1, rate_1, com_2, rate_2)
查找对应点的结果存放位置
15.	DELETE_ALL(self)
清空数据库
16.	get_row_numbers(self)
得到此时数据库的总行数








