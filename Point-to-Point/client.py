from enlace_client.enlace import enlace
from datagrama import *
from color import color_print
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
    arq = open("./arq_client.txt", "a")

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
            msg = datagrama(type=1, server_number=13, total=numPack, id=1)
            write_line(arq, time=time.time(), env_reb="envio", tipo=1, tamanho=14)
            com1.sendData(np.asarray(msg))
            time.sleep(5)

            if com1.rx.getBufferLen() == 0:
                print("Não recebeu confirmação\n")
            else:
                head = com1.rx.getNData(10)
                eop = com1.rx.getNData(4)
                write_line(arq, time=time.time(), env_reb="receb", tipo=head[0],tamanho=14)
                if eop != b'\xAA\xBB\xCC\xDD':
                    print("Eop incorreto, limpando buffer")
                    com1.rx.clearBuffer()
                    time.sleep(0.02)
                if head[0] == 2:
                    print("Recebeu confirmação\nIniciando transmissão")
                    inicia = True
                else:
                    print("Mensagem com tipo errado recebida")

        cont = 1
        time_out = False
        while cont <= numPack and not time_out:

            print(f"Enviando pacote {cont}")
            msg = datagrama(type=3, total=numPack, current=cont, payload=packages[cont-1])
            com1.sendData(np.asarray(msg))
            time.sleep(0.03)
            write_line(arq, time=time.time(), env_reb="receb", tipo=6, tamanho=len(packages[cont-1])+14, current = cont, total=numPack)
            print("Esperando confirmação de recebimento")

            inicio = time.time()
            confirmed = False
            
            while time.time() - inicio <= 20 and not confirmed:
                inicio2 = time.time()
                response = False
                while time.time() - inicio2 <= 5 and not response:
                    rxBuffer_len = com1.rx.getBufferLen()
                    if rxBuffer_len > 0:
                        response = True

                if response:
                    head = com1.rx.getNData(10)
                    eop = com1.rx.getNData(4)
                    if head[0] == 4 and head[7] == cont:
                        cont += 1
                        confirmed = True
                        print("Confirmação recebida")
                        write_line(arq, time=time.time(), env_reb="receb", tipo=4, tamanho=14)
                    elif head[0] == 4 and head[7] != cont:
                        write_line(arq, time=time.time(), env_reb="receb", tipo=4, tamanho=14)
                        print("Confirmação recebida, mas de outro pacote")
                    elif head[0] == 6:
                        write_line(arq, time=time.time(), env_reb="receb", tipo=6, tamanho=14, current = cont, total=numPack)
                        print("Mensagem de erro recebida")
                        cont = head[6]
                        print(f"Reenviando pacote {cont}")
                        msg = datagrama(type=3, total=numPack, current=cont, payload=packages[cont-1])
                        com1.sendData(np.asarray(msg))
                        time.sleep(0.02)
                        print("Esperando confirmação de recebimento")
                        write_line(arq, time=time.time(), env_reb="envio", tipo=3, tamanho=len(packages[cont-1])+14, current = cont, total=numPack)
                else:
                    print("Reenviando pacote")
                    write_line(arq, time=time.time(), env_reb="envio", tipo=3, tamanho=len(packages[cont-1])+14, current = cont, total=numPack)
                    msg = datagrama(type=3, total=numPack, current=cont, payload=packages[cont-1])
                    com1.sendData(np.asarray(msg))
                    time.sleep(0.02)
                    print("Esperando confirmação de recebimento")

            if not confirmed:
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
