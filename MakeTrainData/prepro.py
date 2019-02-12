from scipy import signal

def Denoise(ECG):
    fs = 250
    sig = ECG['sig']
    win_size = int(0.2 * 250 + 1)
    tmp_sig = signal.medfilt(sig , kernel_size = win_size)
    win_size = int(0.6 * 250 + 1)
    tmp_sig = signal.medfilt(tmp_sig , kernel_size = win_size)
    sig = sig - tmp_sig

    b , a = signal.butter(2 , Wn = [50 * 2 / fs] , btype = 'low')
    sig = signal.filtfilt(b , a , sig)
    ECG['sig'] = sig



    return ECG