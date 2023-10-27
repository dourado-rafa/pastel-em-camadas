from module import calcFFT, generateSin
import numpy as np
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt

def main():
    
    signal, samplerate = sf.read('audios/encoded.wav', dtype='float32') # Lendo o arquivo WAV modulado


    sf.write('audios/decoded.wav', signal, samplerate) # Criando arquivo WAV demodulado

if __name__ == "__main__":
    main()