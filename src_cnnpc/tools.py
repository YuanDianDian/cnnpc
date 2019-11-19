import numpy as np

def add_logs(lines):
    '''add logs to file
    
    Args:
    * lines: the content will be recorded in process.txt
    '''
    with open('process.txt', 'a+') as f:
        f.write(lines)
    print(lines)


def partitions_init(model):

    resnet_partitions = [[1,  6,  11,  16],
                         [64, 64, 128, 256],
                         [3,  13, 23,  33]]

    mobilenet_partitions = [[0,  1,  3,  6,  10, 13,  16],
                            [32, 16, 24, 32, 64, 96, 160],
                            [1,  2,  6,  12, 20, 26,  32]]

    # ssd_partitions = [[],
    #                   [],
    #                   []]

    if model == 'resnet':
        np.save('./model_profile/partitions.npy', np.asarray(resnet_partitions))

    if model == 'mobilenet':
        np.save('./model_profile/partitions.npy', np.asarray(resnet_partitions))