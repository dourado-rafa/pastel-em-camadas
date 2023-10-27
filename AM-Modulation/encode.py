from module import calcFFT, generateSin
import numpy as np
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt

def main():
    
    signal, samplerate = sf.read('audios/original.wav', dtype='float32') # Lendo o arquivo WAV original


    sf.write('audios/encoded.wav', signal, samplerate) # Criando arquivo WAV modulado

if __name__ == "__main__":
    main()