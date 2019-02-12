import wfdb
import numpy as np
from scipy import signal
import csv


def _resample_ann(resampled_t, ann_sample):
    tmp = np.zeros(len(resampled_t), dtype='int16')
    j = 0
    tprec = resampled_t[j]
    for i, v in enumerate(ann_sample):
        while True:
            d = False
            if v < tprec:
                j -= 1
                tprec = resampled_t[j]

            if j + 1 == len(resampled_t):
                tmp[j] += 1
                break

            tnow = resampled_t[j + 1]
            if tprec <= v and v <= tnow:
                if v - tprec < tnow - v:
                    tmp[j] += 1
                else:
                    tmp[j + 1] += 1
                d = True
            j += 1
            tprec = tnow
            if d:
                break

    idx = np.where(tmp > 0)[0].astype('int64')
    res = []
    for i in idx:
        for j in range(tmp[i]):
            res.append(i)
    assert len(res) == len(ann_sample)

    return np.asarray(res, dtype='int64')


def _resample_sig(x, fs, fs_target):
    t = np.arange(x.shape[0]).astype('float64')

    if fs == fs_target:
        return x, t

    new_length = int(x.shape[0] * fs_target / fs)
    resampled_x, resampled_t = signal.resample(x, num=new_length, t=t)
    assert resampled_x.shape == resampled_t.shape and resampled_x.shape[0] == new_length
    assert np.all(np.diff(resampled_t) > 0)
    return resampled_x, resampled_t


def OpenECGFile(path, type, batch_size = 10000, batch_num=0):
    if type not in ['wfdb', 'txt']:
        return ValueError('File Open Type Error')

    if type == 'txt':
        sig = np.loadtxt(path, delimiter=',')
        return sig

    tmp1, tmp2 = wfdb.rdsamp(record_name=path, channels=[0, 1])

    if len(tmp1) == 0 or len(tmp1) < (batch_num + 1) * batch_size:
        print('No data , thank for use !')
        return 0

    sig = tmp1[batch_num * batch_size: (batch_num + 1) * batch_size, 0]

    ann = wfdb.rdann(path, 'atr', sampfrom=batch_num * batch_size, sampto=(batch_num + 1) * batch_size)

    sample = ann.sample - batch_num * batch_size

    sig, resampled_t = _resample_sig(sig, fs=360, fs_target=250)

    sample = _resample_ann(resampled_t, sample)

    label = ann.symbol

    return {'sig':sig , 'sample':sample , 'label':label}
    # return sig, sample, label


