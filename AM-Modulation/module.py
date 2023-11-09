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

def low_pass_filter(signal:np.ndarray) -> np.ndarray: 
    a, b, c, d, e = 0.03365, 0.02783, 1, -1.504, 0.5656 # f_corte = 2000 

    filtered_signal = [signal[0], signal[1]]
    for i in range(2, len(signal)):
        filtered_signal.append(-d*filtered_signal[i-1] -e*filtered_signal[i-2] + a*signal[i-1] + b*signal[i-2])
    return np.array(filtered_signal)


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
    