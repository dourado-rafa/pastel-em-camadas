import numpy as np
from scipy.fftpack import fft, fftshift
import matplotlib.pyplot as plt
import sounddevice as sd
import soundfile as sf

def generateSin(freq:int, time:int, samplerate:int) -> tuple[np.ndarray, np.ndarray]:
    N = time*samplerate # numero de pontos
    t = np.linspace(0, time, N) # eixo do tempo
    signal = np.sin(freq*t*2*np.pi)
    return (t, signal)

def calcFFT(signal:np.ndarray, samplerate:int) -> tuple[np.ndarray, np.ndarray]:
    N  = len(signal) # numero de pontos
    T  = 1/samplerate # Periodo da onda
    freqs = np.linspace(-1/(2*T), 1/(2*T), N)
    ampls = fft(signal)
    return(freqs, fftshift(ampls))


if __name__ == "__main__":
    samplerate = 44100
    duration = 5 # duração do audio em segundos

    print(f'Gravando Audio por {duration} segundos')
    audio = sd.rec(duration*samplerate, samplerate, channels=2) # Gravando audio
    sd.wait()
    audio = audio[:,0]
    print('Gravação finalizada')

    freqs, ampls = calcFFT(audio, samplerate)
    plt.stem(freqs, np.abs(ampls))
    plt.xlim(0, 20e3)
    plt.show()

    sf.write('audios/audio.wav', audio, samplerate) # Criando arquivo WAV
    