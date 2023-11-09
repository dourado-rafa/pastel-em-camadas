from module import calcFFT, generateSin
import numpy as np
import sounddevice as sd
from scipy.io import wavfile as sf
import matplotlib.pyplot as plt

def low_pass_filter(signal:np.ndarray) -> list: 
    a, b, c, d, e = 0.03365, 0.02783, 1, -1.504, 0.5656 # f_corte = 2000 

    filtered_signal = [0, 0]
    for i in range(2, len(signal)):
        filtered_signal.append(-d*filtered_signal[i-1] -e*filtered_signal[i-2] + a*signal[i-1] + b*signal[i-2])
    return np.array(filtered_signal)

f_carrier = 14e3 # Hz
band = 4e3 # Hz
duration = 5 # s

def main():
    
    samplerate, signal = sf.read('audios/encoded.wav') # Lendo o arquivo WAV modulado
    _, carrier_signal = generateSin(f_carrier, duration, samplerate)
    time = np.linspace(0, duration, samplerate*duration)
    
    demoduled_signal = carrier_signal*signal
    freqs, ampls = calcFFT(demoduled_signal, samplerate)
    plt.figure('Fourier - Sinal Demodulado')
    plt.plot(freqs, np.abs(ampls))
    plt.xlim(0, 20e3)

    plt.figure('Sinal Demodulado')
    plt.plot(time, demoduled_signal)
    plt.xlim(0, 5)

    filtered_signal = low_pass_filter(demoduled_signal)
    freqs, ampls = calcFFT(filtered_signal, samplerate)
    plt.figure('Fourier - Sinal Demodulado e Filtrado')
    plt.plot(freqs, np.abs(ampls))
    plt.xlim(0, 20e3)

    sd.play(filtered_signal, samplerate)
    
    plt.show()
    sd.wait()

    sf.write('audios/decoded.wav', samplerate, filtered_signal) # Criando arquivo WAV demodulado

if __name__ == "__main__":
    main()