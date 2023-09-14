from enlace import *
import time
import numpy as np
import traceback
import sys,os
from datagrama import datagrama

serialName = "COM3" # O gerenciador de dispositivos informa a porta
# 100: Continue
# 200: OK
# 511: Conexão com a network
# 409: Conflito (Número do Pacote)
# 413: Erro no tamanho do payload
# 205: Reset content

def clearBuffer(com:enlace) -> None:
    com.rx.threadPause()
    com.rx.clearBuffer()
    time.sleep(.02)
    com.rx.threadResume()

def main():
    try:
        # Ativa comunicacao. Inicia os threads e a comunicação seiral
        com1 = enlace(serialName)
        com1.enable()
        print("Abriu a comunicação")
        
        # Escreva o código aqui:
        handshake = False
        stop = False
        package_received = b''
        i=1

        while not stop:

            print("Esperando mensagem")

            head = com1.rx.getNData(12)
            size = head[0]
            current = int.from_bytes(head[1:3], byteorder='big')
            total = int.from_bytes(head[3:5], byteorder='big')
            code = int.from_bytes(head[6:8])
            payload = com1.rx.getNData(size)
            eop = com1.rx.getNData(3)

            if code == 511:
                print("Pacote tipo STATUS recebido")
                if eop == "END".encode():
                    print("Respondendo status")

                    txBuffer = datagrama(code=202)
                    com1.sendData(np.asarray(txBuffer))
                    time.sleep(0.01)

                    handshake = True
                    print("Esperando pacote\n")
                else:
                    print("Erro na mensagem de status\n")

                    txBuffer = datagrama(code=413)
                    com1.sendData(np.asarray(txBuffer))
                    time.sleep(0.01)

            elif handshake:
                if code == 100:
                    print("Pacote tipo SEND recebido")
                    if i != current:
                        print(f"Erro no numero do pacote, recebido: {current}, esperado: {i}\n")

                        txBuffer = datagrama(current = i, total = total, code = 409)
                        com1.sendData(np.asarray(txBuffer))
                        time.sleep(0.01)
                        package_status = False
                    elif eop != "END".encode():
                        print(f"Erro no tamanho do pacote {current}\n")

                        clearBuffer(com1)
                        print(com1.rx.buffer)

                        txBuffer = datagrama(current = current, total = total, code = 413)
                        com1.sendData(np.asarray(txBuffer))
                        time.sleep(0.02)
                        package_status = False
                    else:
                        print(f"Pacote {current} OK\n")
                        txBuffer = datagrama(current = current, total = total, code = 200)
                        com1.sendData(np.asarray(txBuffer))
                        time.sleep(0.01)
                        package_status = True
                        package_received += payload
                        i += 1

                elif code == 205: 
                    print("Pacote tipo RESEND recebido")
                    if current == i-1 or current == i:
                        if eop != "END".encode():
                            print(f"Erro no RESEND: Tamanho do pacote {current}\n")
                            clearBuffer(com1)
                            print(com1.rx.buffer)
                            txBuffer = datagrama(current = current, total = total, code = 413)
                            com1.sendData(np.asarray(txBuffer))
                            time.sleep(0.02)
                            package_status = False
                        else:
                            print(f"RESEND: Pacote {current} OK\n")
                            txBuffer = datagrama(current = current, total = total, code = 200)
                            com1.sendData(np.asarray(txBuffer))
                            time.sleep(0.01)
                            if not package_status or current == i:
                                package_status = True
                                package_received += payload
                                i += 1
                    else:
                        print(f"Erro no RESEND: Numero do pacote recebido: {current}, esperado: {i}\n")

                        clearBuffer(com1)
                        print(com1.rx.buffer)
                        txBuffer = datagrama(current = i, total = total, code = 409)
                        com1.sendData(np.asarray(txBuffer))
                        time.sleep(0.01)
                        package_status = False

                else:
                    print(f"Erro: Pacote tipo {code} recebido")
                    print(f"Numero do pacote recebido: {current}, esperado {i}\n")

                    clearBuffer(com1)
                    print(com1.rx.buffer)
                    txBuffer = datagrama(current = i, total = total, code = 409)
                    com1.sendData(np.asarray(txBuffer))
                    time.sleep(0.01)
                    package_status = False

                if current == total and i == total+1:
                    print("Transmissão feita com sucesso")
                    print("I'm a teapot")
                    txBuffer = datagrama(code=418)
                    com1.sendData(np.asarray(txBuffer))
                    time.sleep(0.01)

                    copia = open("../img/teapot.png", "wb")
                    copia.write(package_received)
                    copia.close()

                    handshake = False
                    stop = True
            
            else:
                print("Não houve confirmação de status\n")
    
        # Encerra comunicação.
        print("\nComunicação encerrada")
        com1.disable()
        
    except Exception as erro:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        
if __name__ == "__main__":
    main()