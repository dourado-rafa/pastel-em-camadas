
#importe as bibliotecas
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftshift
from scipy.io import wavfile

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

number_signals = [[941, 1209], [697, 1209], [697, 1336], [697, 1477], [770, 1209], [770, 1336], [770, 1477], [852, 1209], [852, 1336], [852, 1477]]

def main():
    samplerate = 44100 # taxa de amostragem
    duration = 3 # tempo de reprodução

    #********************************************instruções*********************************************** 
    ### Seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada
    ### Então inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF
    ### Agora, voce tem que gerar, por alguns segundos, suficiente para a outra aplicação gravar o audio, duas senoides com as frequencias 
    # corresposndentes à tecla pressionada, segundo a tabela DTMF
    ### Essas senoides tem que ter taxa de amostragem de 44100 amostras por segundo, entao voce tera que gerar uma lista de tempo correspondente 
    # a isso e entao gerar as senoides
    ### Lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t)
    ### O tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). Construa 
    # com amplitude 1.
    ### Some as senoides. A soma será o sinal a ser emitido.
    ### Utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
    ### Grave o som com seu celular ou qualquer outro microfone. Cuidado, algumas placas de som não gravam sons gerados por elas mesmas. 
    # (Isso evita microfonia).
    ### Construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado. Como as frequencias sao relativamente altas, voce deve
    # plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
    

    print('Inicializando encoder')
    number = int(input('Digite um numero: '))

    print('Gerando Tons base')
    t, signal_low_frequence = generateSin(number_signals[number][0], duration, samplerate)
    t, signal_high_frequence = generateSin(number_signals[number][1], duration, samplerate)

    print(f'Gerando Tom referente ao número: {number} [frequências: {number_signals[number][0]}Hz e {number_signals[number][1]}Hz]')
    signal:np.ndarray = signal_low_frequence + signal_high_frequence

    print('Executando as senoides (emitindo o som)')
    sd.play(signal, samplerate)
    sd.wait() # aguarda fim do audio
    
    plt.figure()
    freqs, ampls = calcFFT(signal, samplerate)
    plt.stem(freqs, np.abs(ampls))
    plt.xlim(0, 1500)

    plt.figure()
    plt.plot(t[0:1000], signal[0:1000], '-')
    plt.show()

    print('Salvando onda gerada')
    wavfile.write(f'ondas/onda{number}.wav', samplerate, signal.astype(np.int16)*1000)

if __name__ == '__main__':
    main()
