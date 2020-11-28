import numpy as np

from scipy import signal
from matplotlib import pyplot as plt


def bits_to_wave(bits, fs=48000, baud=50):
    sample_bit = int(fs / baud)
    wave = np.repeat(bits, sample_bit)
    print(wave)
    wave = 2.0 * wave - 1.0
    return wave


def modulate(bitwave, fs=48000, f0=1400, df=500):
    time_end = len(bitwave) / fs
    t = np.linspace(0.0, time_end, len(bitwave))
    fsk = np.sin(2.0 * np.pi * (f0 + df * bitwave) * t)
    # plt.figure()
    # plt.plot(fsk)
    # plt.show()
    return fsk


def demodulate(wave, fs=48000, f0=1400, df=500):
    low_freq = f0 - df
    high_freq = f0 + df
    filter_order = 5
    dev = 100
    sos_low = signal.butter(filter_order, [(
        low_freq - dev), (low_freq + dev)], btype='band', fs=fs, output='sos')
    sos_high = signal.butter(filter_order, [(
        high_freq - dev), (high_freq + dev)], btype='band', fs=fs, output='sos')

    low_wave = signal.sosfilt(sos_low, wave)
    high_wave = signal.sosfilt(sos_high, wave)

    # plt.subplot(211)
    # plt.plot(low_wave)
    # plt.subplot(212)
    # plt.plot(high_wave)
    # plt.show()

    low_wave = np.abs(signal.hilbert(low_wave))
    high_wave = np.abs(signal.hilbert(high_wave))

    bitwave = high_wave / max(high_wave) - low_wave / max(low_wave)
    # plt.plot(bitwave)
    # plt.show()
    bitwave[bitwave > 0.0] = 1.0
    bitwave[bitwave <= 0.0] = 0.0
    return bitwave


if __name__ == "__main__":
    x = np.array([1, 0, 1, 1, 0, 0])
    baud = 10
    fsk = modulate(bits_to_wave(x, baud=baud))
    res = demodulate(fsk)
    _r = []
    offset = int(48000 / (baud * 2))
    for i in range(len(x)):
        _r.append((int)(res[int(i*48000/baud)+offset]))
    print(_r)
# print(res)
