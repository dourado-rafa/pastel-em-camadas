from enlace import *
from datagrama import datagrama
import time, random
import numpy as np
import traceback

serialName = "COM5" # O gerenciador de dispositivos informa a porta

def receive_package(com:enlace, head_length:int=12, eop_expected:str='END') -> tuple[bytearray, bytearray]:
    head = com.rx.getNData(head_length)
    payload = com.rx.getNData(head[0])
    eop = com.rx.getNData(len(eop_expected)).decode()
    if eop == eop_expected:
        return (head, payload)
    print('Pacote invalido! EOP diferente do esperado')
    return None

def wait_response(com:enlace, wait:int) -> (bool | int):
    start = time.time()
    wait = 1e10 if wait == 0 else wait
    while (time.time() - start) <= wait:
        if not com.rx.getIsEmpty():
            package = receive_package(com)
            if package is not None:
                head, payload = package
                message_recived = int.from_bytes(head[6:8])
                return message_recived
            return None
    return False

def fragment_file(filepath:str, length:int=50) -> list[bytearray]:
    fragments = []
    with open(filepath, 'rb') as file:
        content = file.read()
        for i in range(0, len(content), 50):
            fragment = content[i:i+length] if i+length < len(content) else content[i:]
            fragments.append(fragment)
    file.close()
    return fragments


def main():
    try:
        # Ativa comunicacao. Inicia os threads e a comunicação seiral
        com1 = enlace(serialName)
        com1.enable()
        print("Abriu a comunicação")
        
        # Escreva o código aqui:
        fragments = fragment_file('../img/teapot.png')
        current, total = 1, len(fragments)
        code = 100

        status = 'CONNECTING'
        while 'END' not in status:

            if status == 'CONNECTING':
                print('Verificando se o Servidor está Ativo')
                com1.sendData(datagrama(0, total, code=511))
                time.sleep(.01)

                response = wait_response(com1, 5)
                if response == 202:
                    print('Conexão estabelecida!')
                    status = 'TRANSMITTING'
                else:
                    try_connect = input('Servidor inativo. Tentar novamente? (S/N) ').upper() == 'S'
                    if not try_connect:
                        status = 'END-CONNECTION-FAILED'

            elif status == 'TRANSMITTING':
                com1.sendData(datagrama(current, total, code=code, payload=fragments[current-1]))
                time.sleep(.01)
                print(f'\nPacote [{current}/{total}] enviado! Aguardando confirmação de recebimento...')

                response = wait_response(com1, 3)
                if response == 200:
                    print(f'Pacote [{current}/{total}] recebido com sucesso pelo cliente!\nEnviando próximo pacote...')
                    code = 100
                    current += 1
                elif response in [409, 413]:
                    print(f'Houve uma falha no recebimento do pacote [{current}/{total}]!\nReenviando pacote...')
                    code = 205
                elif not response:
                    print(f'Nenhuma resposta recebida!\nReenviando pacote...')
                    code = 205

                if current > total:
                    print(f'\nTodos os {total} pacos foram enviados!')
                    status = 'CONFIRMING'

            elif status == 'CONFIRMING':
                print(f'Aguardando confirmação de recebimento...')

                response = wait_response(com1, 0)
                if response == 418:
                    print(f'Todos os {total} pacotes foram recebidos com sucesso!')
                    print("I'm a Teapot!")
                    status = 'END-TRANSMISSION-SUCESSFUL'
                else:
                    print(f'Algo na transmissão falhou, mas não há nada a se fazer... :(')
                    status = 'END-TRANSMISSION-FAILED'
        
        # Encerra comunicação.
        print("\nComunicação encerrada")
        com1.disable()
        
    except Exception as error:
        print(f"ops! :-{traceback.format_exc()}")
        com1.disable()
        
if __name__ == "__main__": 
    main()
