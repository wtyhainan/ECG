import numpy as np
import ecg
import csv
import prepro as pp
import  matplotlib.pyplot as plt
import os

fs = 250

set1 = ['101' , '106' , '108' , '109' , '112' , '114' , '115' , '116' , '118' , '119' , '122' , '124' , '201' , '203' , '205' , '207' , '208' , '209' , '215' , '220' , '223' , '230']
set2 = ['100' , '103' , '105' , '111' , '113' , '117' , '121' , '123' , '200' , '202' , '210' , '212' , '213' , '214' , '219' , '221' , '222' , '228' , '231' , '232' , '233' , '234']

set1 = ['115']
set2 = ['202']


all_label_type = ['N' , 'L' , 'R' , 'V' , 'A' , '+' , 'F' , '~' , '!' , '"' ,
              'j' , 'x' , 'a' , '|' , 'E' , 'J' , 'e' , 'Q' , '[' , ']' , 'S']

valid_label_type = ['N' , 'L' , 'R' , 'B' , 'V' , 'E' , 'a' , 'J' ,
                    'A' , 'S' , 'j' , 'e' , 'n' , 'F' , '|' , 'f' , 'Q']
#这个分类标准依据论文
#《Heartbeat classification using abstract features from the abductive interpretation of the ECG》
N_type = ['N' , 'L' , 'R' , 'B']
V_type = ['V' , 'E']
A_type = ['a' , 'J' , 'A' , 'S' , 'j' , 'e' , 'n']
F_type = ['F']
Q_type = ['|' , 'f' , 'Q']


def filter_bad_label(ECG):
    sig = ECG['sig']
    sample = ECG['sample']
    label = ECG['label']

    real_label = []
    real_sample = []

    for i in range(0 , len(label)):
        tmp_label = label[i]
        if tmp_label in valid_label_type:
            real_sample.append(sample[i])
            if tmp_label in N_type:
                real_label.append(0)    #-->N
            elif tmp_label in V_type:
                real_label.append(1)    #-->V
            elif tmp_label in A_type:
                real_label.append(2)    #-->A
            elif tmp_label in F_type:
                real_label.append(3)    #-->F
            elif tmp_label in Q_type:
                real_label.append(4)    #-->Q

    ECG['sample'] = np.array(real_sample)
    ECG['label'] = np.array(real_label)
    return ECG


def get_train_data(ECG):

    sig = ECG['sig']
    label = ECG['label']
    sample = ECG['sample']
    rand = np.random.randint(-3 , 3 , len(sample))
    sample += rand


    x = []
    y = []
    for i in range(2 , len(sample) - 2):
        pos = sample[i]
        tmp_sig = sig[int(pos - 0.25 * fs) : int(pos + 0.25 * fs)]
        tmp_label = label[i]
        x.append(tmp_sig)
        y.append(tmp_label)

    return {'x':np.array(x) , 'y':np.array(y)}


def write_to_csv(data , num , str):

    root = '/home/wty/桌面/ECG/' + str
    path = os.path.join(root , num) + '.csv'

    hfile = open(path , 'a' , newline = '')
    csvwriter = csv.writer(hfile)

    first_row = np.arange(0 , data['x'].shape[1] , 1)
    first_row = np.reshape(first_row , [1 , -1])

    x = data['x']
    x = np.concatenate((first_row , x) , axis = 0)


    y = np.concatenate((['label'] , data['y']))
    y = np.reshape(y , [-1 , 1])

    dat = np.concatenate((x , y) , axis = 1)

    csvwriter.writerows(dat)
    print('write finished')

    hfile.close()


def main():

    # root = '/home/wty/MyDataDir/MIT-BIH'
    #
    # for i in [set1 , set2]:
    #     for j in i:
    #         path = os.path.join(root , j)
    #         ECG = ecg.OpenECGFile(path , type = 'wfdb' , batch_size=650000 , batch_num = 0)
    #         ECG = filter_bad_label(ECG)
    #         ECG = pp.Denoise(ECG)
    #         data = get_train_data(ECG)
    #         write_to_csv(data , j , 'Train')


    import  pandas as pd
    dat = np.array(pd.read_csv('/home/wty/桌面/ECG/Train/115.csv'))

    x = dat[: , 0:dat.shape[1] - 1]
    y = dat[: , dat.shape[1] - 1 : ]


    # x = ECG['sample']
    # y = ECG['sig'][x]
    # s = np.array(ECG['label'])
    # fig , ax = plt.subplots(2)
    # ax[0].scatter(x = x , y = y , c = 'r')
    # for i in range(0, len(x)):
    #     ax[0].text(x = x[i] , y = y[i] + 0.1 , s = s[i])
    #
    #
    # plt.show()




if __name__ == '__main__':
    main()










