import numpy as np
from scipy.fftpack import fft, fftshift

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
