from enlace import *
import time
import numpy as np
from datagrama import Datagrama

serialName = "COM3" # O gerenciador de dispositivos informa a porta
# 100: Continue
# 200: OK
# 511: Conexão com a network
# 409: Conflito (Número do Pacote)
# 413: Erro no tamanho do payload
# 205: Reset content

def main():
    try:
        # Ativa comunicacao. Inicia os threads e a comunicação seiral
        com1 = enlace(serialName)
        com1.enable()
        print("Abriu a comunicação")
        
        # Escreva o código aqui:
        print("Esperando mensagem")
        stop = False
        package_received = b''

        while not stop:

            head = com1.rx.getNData(12)
            size = head[0]
            current = int.from_bytes(head[1:3], byteorder='big')
            total = int.from_bytes(head[3:5], byteorder='big')
            type = head[5].to_bytes(1, byteorder = 'big').decode()
            msg = int.from_bytes(head[6:8])
            payload = com1.rx.getNData(size)
            eop = com1.rx.getNData(3)

            if type == "S":
                if eop == "END".encode():
                    print("Respondendo status")
                    txBuffer = Datagrama.datagrama(type = "S", message="OK")
                    com1.sendData(np.asarray(txBuffer))
                    time.sleep(0.01)
                    
                    print("Esperando pacote")
                    i = 1
                    while i <= total:

                        head = com1.rx.getNData(12)
                        size = head[0]
                        current = int.from_bytes(head[1:3])
                        total = int.from_bytes(head[3:5])
                        type = head[5].to_bytes(1, byteorder = 'big').decode()
                        msg = head[6:].decode()
                        print(msg) 
                        payload = com1.rx.getNData(size)
                        eop = com1.rx.getNData(3)

                        print(head, payload, eop)

                        if msg == "RESEND" and (current == i-1 or current == i):
                            if eop != "END".encode():
                                print("Erro: Tamanho do payload resend")
                                com1.rx.clearBuffer()
                                time.sleep(0.02)
                                print(com1.rx.buffer)
                                txBuffer = Datagrama.datagrama(current = current, total = total, type = "P", message="ERROR")
                                com1.sendData(np.asarray(txBuffer))
                                time.sleep(0.02)
                            else:
                                print(f"Pacote {current} resend OK")
                                txBuffer = Datagrama.datagrama(current = current, total = total, type = "P", message="OK")
                                com1.sendData(np.asarray(txBuffer))
                                time.sleep(0.01)
                                if not package_status or current == i:
                                    package_status = True
                                    package_received += payload
                                    i += 1

                        elif i != current:
                            print(f"Erro: Numero do pacote, recebido: {current}, esperado: {i}")
                            txBuffer = Datagrama.datagrama(current = current, total = total, type = "P", message="ERROR")
                            com1.sendData(np.asarray(txBuffer))
                            time.sleep(0.01)
                            package_status = False

                        elif eop != "END".encode():
                            print(f"Erro: Tamanho do payload do pacote {current}")
                            com1.rx.clearBuffer()
                            time.sleep(0.05)
                            print(com1.rx.buffer)
                            txBuffer = Datagrama.datagrama(current = current, total = total, type = "P", message="ERROR")
                            com1.sendData(np.asarray(txBuffer))
                            time.sleep(0.05)
                            package_status = False

                        else:
                            print(f"Pacote {current} OK")
                            txBuffer = Datagrama.datagrama(current = current, total = total, type = "P", message="OK")
                            com1.sendData(np.asarray(txBuffer))
                            time.sleep(0.01)
                            package_status = True
                            package_received += payload
                            i += 1

                    # Fim do while de pacotes

                    print("Transmissão feita com sucesso")
                    txBuffer = Datagrama.datagrama(type = "S", message="END")
                    com1.sendData(np.asarray(txBuffer))
                    time.sleep(0.01)

                    copia = open("./imagem_recebida.png", "wb")
                    copia.write(package_received)
                    copia.close()

                    stop = True
                else:
                    print("Erro no status")
                    txBuffer = Datagrama.datagrama(type = "S", message="ERROR")
                    com1.sendData(np.asarray(txBuffer))
                    time.sleep(0.01)
    
        # Encerra comunicação.
        print("\nComunicação encerrada")
        com1.disable()
        
    except Exception as erro:
        print(f"ops! :-\n{erro}")
        com1.disable()
        
if __name__ == "__main__":
    main()
