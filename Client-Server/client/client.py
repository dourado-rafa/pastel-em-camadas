from enlace import *
import time
import numpy as np
import random

serialName = "COM3"                  # Windows(variacao de)

def main():
    print("Iniciou o main")
    try:
        # Ativa comunicacao. Inicia os threads e a comunicação seiral
        com1 = enlace(serialName)

        com1.enable()
        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)
 
        print("Abriu a comunicação\n")

        dic_comandos = {1: b'\x00\x00\x00\x00', 2:b'\x00\x00\xBB\x00', 3: b'\xBB\x00\x00', 4:b'\x00\xBB\x00', 5:b'\x00\x00\xBB', 6:b'\x00\xAA', 7:b'\xBB\x00', 8:b'\x00', 9:b'\xBB'}
        dic_tamanhos = {1: '0001', 2:'0010', 3:'0011', 4:'0100'}
        
        # Escreva o código aqui:
        n = random.randint(10,30)
        print(f"Serão enviados {n} comandos")
        comandos = np.random.randint(1,10, size=(n))
        num_comandos = len(comandos)

        tamanhos = b''
        lista_comandos = b''

        i = 0
        while i <= num_comandos-2:
            concatenado = ''

            comando1_hex = dic_comandos[comandos[i]]
            print(comando1_hex)
            comando2_hex = dic_comandos[comandos[i+1]]
            print(comando2_hex)
            lista_comandos += comando1_hex + comando2_hex

            concatenado = dic_tamanhos[len(comando1_hex)] + dic_tamanhos[len(comando2_hex)]
            tamanhos += int(concatenado,2).to_bytes(1, byteorder = 'big')
            i += 2

        if num_comandos % 2 != 0:
            ultimo_comando = comandos[num_comandos-1]
            ultimo_comando_hex = dic_comandos[ultimo_comando]
            print(ultimo_comando_hex)
            len_ultimo = dic_tamanhos[len(ultimo_comando_hex)]
            tamanhos += int(len_ultimo,2).to_bytes(1, byteorder = 'big')
            

        txBuffer = b'\xFF' + tamanhos + b'\xFF' + lista_comandos + b'\xBD'
        """
        txBuffer = b''
        for numero in comandos:
            txBuffer += b'\xFF' + dic_comandos[numero]
        txBuffer += b'\xFF\xFF'
        print(txBuffer) 
        """

        print("Meu array de bytes tem tamanho {}\n" .format(len(txBuffer)))

        print("Iniciando transmissão")

        com1.sendData(np.asarray(txBuffer))
        time.sleep(1)

        txSize = com1.tx.getStatus()
        print('Enviou {} bytes\n' .format(txSize))

        print("Esperando resposta do server")
        inicio = time.time()

        recebeu = False

        while time.time() - inicio <= 5 and not recebeu:
            rxBuffer_len = com1.rx.getBufferLen()
            if rxBuffer_len > 0:
                recebeu = True
                rxBuffer, nRx = com1.getData(rxBuffer_len)
                int_rxBuffer = int.from_bytes(rxBuffer, byteorder='big')
                print(f"Foram enviados {num_comandos} comandos e o servidor recebeu {int_rxBuffer} comandos")
                if int_rxBuffer == num_comandos:
                    print("Tudo certo!")
                else:
                    print("Algo deu errado")

        if not recebeu:
            print("Time out :(")
        else:
            print(f"Tempo de recepção = {(time.time() - inicio)*1000:.2f} ms")

        # Encerra comunicação.
        print("\nComunicação encerrada")
        com1.disable()
        
    except Exception as erro:
        print(f"ops! :-\n{erro}")
        com1.disable()
        
if __name__ == "__main__":
    main()
