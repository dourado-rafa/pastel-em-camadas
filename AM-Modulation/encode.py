from module import calcFFT, generateSin
import numpy as np
import sounddevice as sd
from scipy.io import wavfile as sf
import matplotlib.pyplot as plt

def main():
    
    samplerate, signal = sf.read('audios/auau.wav') # Lendo o arquivo WAV channel1
    channel1 = signal[:,0]

    xf, yf = calcFFT(channel1, samplerate)
    plt.plot(xf, np.abs(yf))

    filtrado = []

    a, b, c, d, e = 0.03365, 0.02783, 1, -1.504, 0.5656 # f_corte = 2000 

    filtrado.append(channel1[0])
    filtrado.append(channel1[1])

    for i in range(2,len(channel1)):
        valor = -d*filtrado[i-1] - e*filtrado[i-2] + a*channel1[i-1] + b*channel1[i-2]
        filtrado.append(valor)

    xf, yf = calcFFT(filtrado, samplerate)
    plt.plot(xf, np.abs(yf))
    plt.show()

    tempo, portadora = generateSin(14000, 5, samplerate)
    S = []
    for i in range(len(portadora)):
        valor = (1+filtrado[i])*portadora[i]
        S.append(valor)

    plt.plot(tempo, S)
    plt.show()

    xf, yf = calcFFT(S, samplerate)
    plt.plot(xf, np.abs(yf))
    plt.show()

    sinal_norm = []
    maximo = max(S)
    for valor in S:
        sinal_norm.append(valor/maximo)

    plt.plot(tempo, sinal_norm)
    plt.show()

    sf.write('audios/encoded.wav', samplerate, np.array(sinal_norm)) # Criando arquivo WAV modulado

if __name__ == "__main__":
    main()