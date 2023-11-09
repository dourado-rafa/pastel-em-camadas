from module import calcFFT, generateSin
import numpy as np
import sounddevice as sd
from scipy.io import wavfile as sf
import matplotlib.pyplot as plt

def low_pass_filter(signal:np.ndarray) -> list:
    # a, b, c, d, e = 0.1121, 0.07663, 1, -1.131, 0.33199 # f_corte = 4000 
    # a, b, c, d, e = 0.05021, 0.03959, 1, -1.401, 0.4905 # f_corte = 2500 
    a, b, c, d, e = 0.03365, 0.02783, 1, -1.504, 0.5656 # f_corte = 2000 

    filtered_signal = [0, 0]
    for i in range(2, len(signal)):
        filtered_signal.append(-d*filtered_signal[i-1] -e*filtered_signal[i-2] + a*signal[i-1] + b*signal[i-2])
    return filtered_signal
        

def main():
    
    samplerate, signal = sf.read('audios/encoded.wav') # Lendo o arquivo WAV modulado
    channel1 = signal[:, 0]
    
    channel1 = channel1/np.max(np.abs(channel1))
    # sd.play(channel1, samplerate)
    # sd.wait

    freqs, ampls = calcFFT(channel1, samplerate)
    # plt.figure()
    plt.plot(freqs, np.abs(ampls))
    plt.xlim(0, 15e3)

    filtered_signal = low_pass_filter(channel1)
    freqs, ampls = calcFFT(filtered_signal, samplerate)
    # plt.figure()
    plt.plot(freqs, np.abs(ampls))
    plt.xlim(0, 15e3)

    plt.show()

    sf.write('audios/decoded.wav', samplerate, channel1) # Criando arquivo WAV demodulado

if __name__ == "__main__":
    main()