from module import calcFFT, generateSin
import numpy as np
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt

def main():
    
    signal, samplerate = sf.read('audios/signal.wav', dtype='float32') # Lendo o arquivo WAV signal
    filtrado = []

    a = 0.003285
    b = 0.003108
    c = 1
    d = -1.84
    e = 0.8465

    filtrado.append(signal[0])
    filtrado.append(signal[1])

    for i in range(2,len(signal)):
        valor = -d*filtrado[i-1] - e*filtrado[i-2] + a*signal[i-1] + b*signal[i-2]
        filtrado.append(valor)


    sf.write('audios/encoded.wav', filtrado, samplerate) # Criando arquivo WAV modulado


if __name__ == "__main__":
    main()