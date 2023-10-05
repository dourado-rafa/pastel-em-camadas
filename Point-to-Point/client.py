from enlace_client.enlace import enlace
from datagrama import *
import time, random
import traceback

serialName = "COM3" # O gerenciador de dispositivos informa a porta
# tipo 1: chamado do cliente ao servidor (handshake) - h0 = 1, h1 = 13
# tipo 2: servidor para o cliente (confirmação handshake) - h0 = 2
# tipo 3: mensagem de dados - h0 = 3
# tipo 4: confirmação de recebimento de dados - h0 = 4
# tipo 5: time out - h0 = 5
# tipo 6: pacote com erro, deve ser reenviado - h0 = 6, h6 = pacote de recomeço

def main():
    id = 5
    arq = open(f"./client{id}.txt", "w")
    arq.close()
    arq = open(f"./client{id}.txt", "a")

    try:
        # Ativa comunicacao. Inicia os threads e a comunicação seiral
        com1 = enlace(serialName)
        com1.enable()
        print("Abriu a comunicação")

        inicia = False
        packages = fragment_file("img/teapot.png")
        numPack = len(packages)
        print(numPack)
        
        # Escreva o código aqui:
        while not inicia:
            print("Enviando chamado")
            msg = datagrama(type=1, server_number=13, total=numPack, id=id)
            write_line(arq, time=time.time(), env_reb="envio", tipo=1)
            com1.sendData(np.asarray(msg))
            time.sleep(5)

            if com1.rx.getBufferLen() == 0:
                print("Não recebeu confirmação\n")
            else:
                head = com1.rx.getNData(10)
                eop = com1.rx.getNData(4)
                write_line(arq, time=time.time(), env_reb="receb", tipo=head[0])
                if eop != b'\xAA\xBB\xCC\xDD':
                    print("Eop incorreto, limpando buffer")
                    com1.rx.clearBuffer()
                    time.sleep(0.02)
                if head[0] == 2:
                    print("Recebeu confirmação\nIniciando transmissão")
                    com1.rx.clearBuffer()
                    inicia = True
                else:
                    print("Mensagem com tipo errado recebida")

        cont = 1
        time_out = False
        while cont <= numPack and not time_out:

            print(f"Enviando pacote {cont}")
            payload = packages[cont-1]
            msg = datagrama(type=3, total=numPack, current=cont, payload=payload)
            write_line(arq, time=time.time(), env_reb="envio", tipo=3, tamanho=len(payload)+14, current = cont, total=numPack)
            com1.sendData(np.asarray(msg))
            time.sleep(0.03)
            print("Esperando confirmação de recebimento")

            inicio = time.time()
            response = False
            
            while time.time() - inicio <= 20 and not response:
                inicio2 = time.time()
                while time.time() - inicio2 <= 5 and not response:
                    rxBuffer_len = com1.rx.getBufferLen()
                    if rxBuffer_len > 0:
                        response = True

                if response:
                    head = com1.rx.getNData(10)
                    eop = com1.rx.getNData(4)
                    com1.rx.clearBuffer()
                    write_line(arq, time=time.time(), env_reb="receb", tipo=head[0])
                    if head[0] == 4 and head[7] == cont:
                        cont += 1
                        print("Confirmação recebida")
                    elif head[0] == 4 and head[7] != cont:
                        print(f"Confirmação recebida, mas do pacote {head[7]}")
                    elif head[0] == 6:
                        print("Mensagem de erro recebida")
                        print(head[6])
                        cont = head[6]
                        print(f"Pacote {cont} será reenviado")
                else:
                    print("Reenviando pacote")
                    payload = packages[cont-1]
                    msg = datagrama(type=3, total=numPack, current=cont, payload=payload)
                    write_line(arq, time=time.time(), env_reb="envio", tipo=3, tamanho=len(payload)+14, current = cont, total=numPack)
                    com1.sendData(np.asarray(msg))
                    time.sleep(0.02)
                    print("Esperando confirmação de recebimento")

            if not response:
                print("Time out")
                write_line(arq, time=time.time(), env_reb="envio", tipo=5)
                arq.close()
                msg = datagrama(type=5)
                com1.sendData(np.asarray(msg))
                time.sleep(0.02)
                time_out = True

        if cont == numPack + 1:
            arq.close()
            print("Transmissão feita com sucesso")
            print("I'm a teapot")

        # Encerra comunicação.
        print("\nComunicação encerrada")
        com1.disable()
        
    except Exception as error:
        print(f"ops! :-{traceback.format_exc()}")
        com1.disable()
        
if __name__ == "__main__": 
    main()
