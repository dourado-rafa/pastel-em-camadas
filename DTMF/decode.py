
#Importe todas as bibliotecas
from SignalLib import *
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time


#funcao para transformas intensidade acustica em dB, caso queira usar
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():

    #*****************************instruções********************************
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)   
    # algo como:
    signal = MySignal() 
       
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    sd.default.samplerate = 44100 # taxa de amostragem
    sd.default.channels = 2 #numCanais # o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas
    duration = 2 #tempo # tempo em segundos que ira aquisitar o sinal acustico captado pelo mic
    
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes) durante a gracação. Para esse cálculo você deverá utilizar a taxa de amostragem e o tempo de gravação
    numAmostras = sd.default.samplerate*duration
    freqDeAmostragem = sd.default.samplerate

    #faca um print na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera
    print("A captação do áudio iniciará em 1 segundos")
    time.sleep(1)
   
    #Ao seguir, faca um print informando que a gravacao foi inicializada
    print("Gravação iniciada")

    #para gravar, utilize
    audio = sd.rec(numAmostras, freqDeAmostragem, channels=2)
    sd.wait()
    print("...     FIM")


    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista, isso dependerá so seu sistema, drivers etc...
    #extraia a parte que interessa da gravação (as amostras) gravando em uma variável "dados". Isso porque a variável audio pode conter dois canais e outas informações).
    dados = audio[:,0]
    
    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    # plot do áudio gravado (dados) vs tempo! Não plote todos os pontos, pois verá apenas uma mancha (freq altas) .

    tempo = np.linspace(0,duration, num=len(dados))
    plt.figure("Som")
    plt.plot(tempo, dados)
       
    ## Calcule e plote o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(dados, freqDeAmostragem)
    plt.figure("Fourier Audio")
    plt.stem(xf, np.abs(yf))
    plt.grid()
    plt.title('Amplitude x Frequência')
    plt.xlim(600,1500)

    #agora, voce tem os picos da transformada, que te informam quais sao as frequencias mais presentes no sinal. Alguns dos picos devem ser correspondentes às frequencias do DTMF!
    #Para descobrir a tecla pressionada, voce deve extrair os picos e compara-los à tabela DTMF
    #Provavelmente, se tudo deu certo, 2 picos serao PRÓXIMOS aos valores da tabela. Os demais serão picos de ruídos.

    # para extrair os picos, voce deve utilizar a funcao peakutils.indexes(,,)
    # Essa funcao possui como argumentos dois parâmetros importantes: "thres" e "min_dist".
    # "thres" determina a sensibilidade da funcao, ou seja, quao elevado tem que ser o valor do pico para de fato ser considerado um pico
    #"min_dist" é relatico tolerancia. Ele determina quao próximos 2 picos identificados podem estar, ou seja, se a funcao indentificar um pico na posicao 200, por exemplo, só identificara outro a partir do 200+min_dis. Isso evita que varios picos sejam identificados em torno do 200, uma vez que todos sejam provavelmente resultado de pequenas variações de uma unica frequencia a ser identificada.   
    # Comece com os valores:
    index = peakutils.indexes(yf, thres=0.2, min_dist=40)
    #print("index de picos {}" .format(index)) #yf é o resultado da transformada de fourier

    #printe os picos encontrados! 
    # Aqui você deverá tomar o seguinte cuidado: A funcao  peakutils.indexes retorna as POSICOES dos picos. Não os valores das frequências onde ocorrem! Pense a respeito
    frequencias_id = [xf[i] for i in index]
    print(f"todas as frequencias: {frequencias_id}")

    f_intervalo = []
    for valor in index:
        if xf[valor] > 600 and xf[valor] < 1500:
            f_intervalo.append(xf[valor])
    
    print(f"frequências identificadas no intervalo: {f_intervalo}")

    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    
    #print o valor tecla!!!
    #Se acertou, parabens! Voce construiu um sistema DTMF

    f_numeros = [[941, 1209], [697, 1209], [697, 1336], [697, 1477], [770, 1209], [770, 1336], [770, 1477], [852, 1209], [852, 1336], [852, 1477]]

    baixas = [frequencia[0] for frequencia in f_numeros]
    print(baixas)
    menor_dif = 100
    f_baixa = 0
    for frequencia_id in f_intervalo:
        for frequencia in baixas:
            if abs(frequencia - frequencia_id) < menor_dif:
                menor_dif = abs(frequencia - frequencia_id)
                f_baixa = frequencia
    
    print(f_baixa)

    provaveis = [numero for numero in f_numeros if numero[0]==f_baixa]
    print(provaveis)
    altas = [frequencia[1] for frequencia in provaveis]

    menor_dif = 100
    f_alta = 0
    for frequencia_id in f_intervalo:
        for frequencia in altas:
            if abs(frequencia - frequencia_id) < menor_dif:
                menor_dif = abs(frequencia - frequencia_id)
                f_alta = frequencia
     
    if [f_baixa,f_alta] in f_numeros:
        print(f"Número identificado: {f_numeros.index([f_baixa,f_alta])}")
    else:
        print("Nenhuma identificada")

    plt.show()

    #Você pode tentar também identificar a tecla de um telefone real! Basta gravar o som emitido pelo seu celular ao pressionar uma tecla. 

      
    ## Exiba gráficos do fourier do som gravados 
    plt.show()

if __name__ == "__main__":
    main()


    # for frequencias in f_numeros:

    #     tem1 = False
    #     tem2 = False
    #     primeira = frequencias[0]
    #     segunda = frequencias[1]
    #     for valor in frequencias_id:
    #         if primeira-erro<valor<primeira+erro:
    #             tem1 = True
    #         if segunda-erro<valor<segunda+erro:
    #             tem2 = True
    #     if tem1 and tem2:
    #         print("Pelo peakutils:")
    #         print(f"Número identificado: {numeros.index(frequencias)}")
