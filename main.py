import numpy as np
import ecg

import  matplotlib.pyplot as plt

set1 = ['101' , '106' , '108' , '109' , '112' , '114' , '115' , '116' , '118' , '119' , '122' , '124' , '201' , '203' , '205' , '207' , '208' , '209' , '215' , '220' , '223' , '230']
set2 = ['100' , '103' , '105' , '111' , '113' , '117' , '121' , '123' , '200' , '202' , '210' , '212' , '213' , '214' , '219' , '221' , '222' , '228' , '231' , '232' , '233' , '234']

label_type = ['N' , 'L' , 'R' , 'V' , 'A' , '+' , 'F' , '~' , '!' , '"' ,
              'j' , 'x' , 'a' , '|' , 'E' , 'J' , 'e' , 'Q' , '[' , ']' , 'S']

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
    for i in label:
        if i not in ['N' , 'V' , 'A' , 'F' , 'Q']:
            pass


def main():
    import os
    root = '/home/wty/MyDataDir/MIT-BIH'
    # path = os.path.join(path , '101')
    # print(path)
    # ECG = ecg.OpenECGFile(path = path , type = 'wfdb' ,batch_size = 60000 , batch_num = 0)

    labels = np.array([])
    for i in [set1 , set2]:
        for j in i:
            path = os.path.join(root , j)
            ECG = ecg.OpenECGFile(path , type = 'wfdb' , batch_size=650000 , batch_num=0)
            # labels.append(ECG['label'])

            labels = np.append(labels , np.array(ECG['label']))

    labels = np.reshape(labels , [-1])


    from collections import Counter
    print(Counter(labels))
    labels = Counter(labels)
    N_num = 0
    V_num = 0
    A_num = 0
    for i in labels:
        if i in N_type:
            N_num += labels[i]
        elif i in A_type:
            A_num += labels[i]
        elif i in V_type:
            V_num += labels[i]
    print(N_num , V_num , A_num)





    # x = sample
    # y = sig[x]
    # s = np.array(label)
    # fig , ax = plt.subplots(2)
    # ax[0].plot(sig)
    # ax[0].scatter(x = sample , y = sig[sample] , c = 'r')
    # for i in range(0, len(x)):
    #     ax[0].text(x = x[i] , y = y[i] + 0.1 , s = s[i])
    #
    #
    # plt.show()




if __name__ == '__main__':
    main()











