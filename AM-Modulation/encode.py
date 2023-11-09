from module import calcFFT, generateSin
import numpy as np
import sounddevice as sd
from scipy.io import wavfile as sf
import matplotlib.pyplot as plt

def main():
    
    samplerate, signal = sf.read('audios/auau.wav') # Lendo o arquivo WAV signal
    filtrado = []

    a, b, c, d, e = 0.03365, 0.02783, 1, -1.504, 0.5656 # f_corte = 2000 

    filtrado.append(signal[0])
    filtrado.append(signal[1])

    for i in range(2,len(signal)):
        valor = -d*filtrado[i-1] - e*filtrado[i-2] + a*signal[i-1] + b*signal[i-2]
        filtrado.append(valor)


    sf.write('audios/encoded.wav', samplerate, filtrado) # Criando arquivo WAV modulado


if __name__ == "__main__":
    main()