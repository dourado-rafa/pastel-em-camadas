from enlace import *
from datagrama import Datagrama as Dt
import time, random
import numpy as np

serialName = "COM5" # O gerenciador de dispositivos informa a porta

OK = ('OK'.encode()+b'\x00\x00\x00\x00').decode()
END = ('END'.encode()+b'\x00\x00\x00').decode()
ERROR = ('ERROR'.encode()+b'\x00').decode()

def receive_package(com:enlace, head_length:int=12, eop_expected:str='END') -> tuple[bytearray, bytearray]:
    head = com.rx.getNData(head_length)
    payload = com.rx.getNData(head[0])
    eop = com.rx.getNData(len(eop_expected)).decode()
    if eop == eop_expected:
        return (head, payload)
    print('Pacote invalido! EOP diferente do esperado')
    return None

def wait_response(com:enlace, type_expected:str, wait:int) -> (bool | str):
    start = time.time()
    wait = 1e10 if wait == 0 else wait
    while (time.time() - start) <= wait:
        if not com.rx.getIsEmpty():
            package = receive_package(com)
            if package is not None:
                head, payload = package
                type_recived = head[5].to_bytes().decode()
                message_recived = head[6:].decode()
                if type_expected == type_recived:
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
        fragments = fragment_file('../img/star.png')
        current, total = 1, len(fragments)
        message = 'SEND'    

        status = 'CONNECTING'
        while 'END' not in status:

            if status == 'CONNECTING':
                print('Verificando se o Servidor está Ativo')
                com1.sendData(Dt.datagrama(0, total, 'S', 'ONLINE'))
                time.sleep(.01)

                response = wait_response(com1, 'S', 5)
                if response == OK:
                    print('Conexão estabelecida!')
                    status = 'TRANSMITTING'
                else:
                    try_connect = input('Servidor inativo. Tentar novamente? (S/N) ').upper() == 'S'
                    if not try_connect:
                        status = 'END-CONNECTION-FAILED'

            elif status == 'TRANSMITTING':
                com1.sendData(Dt.datagrama(current, total, 'P', message, fragments[current-1]))
                time.sleep(.01)
                print(f'\nPacote [{current}/{total}] enviado! Aguardando confirmação de recebimento...')

                response = wait_response(com1, 'P', 3)
                if response == OK:
                    print(f'Pacote [{current}/{total}] recebido com sucesso pelo cliente!\nEnviando próximo pacote...')
                    message = 'SEND'
                    current += 1
                elif response == ERROR:
                    print(f'Houve uma falha no recebimento do pacote [{current}/{total}]!\nReenviando pacote...')
                    message = 'RESEND'
                elif not response:
                    print(f'Nenhuma resposta recebida!\nReenviando pacote...')
                    message = 'RESEND'

                if current > total:
                    print(f'\nTodos os {total} pacos foram enviados!')
                    status = 'CONFIRMING'

            elif status == 'CONFIRMING':
                print(f'Aguardando confirmação de recebimento...')

                response = wait_response(com1, 'S', 0)
                if response == END:
                    print(f'Todos os {total} pacotes foram recebidos com sucesso!')
                    status = 'END-TRANSMISSION-SUCESSFUL'
                else:
                    print(f'Algo na transmissão falhou, mas não há nada a se fazer... :(')
                    status = 'END-TRANSMISSION-FAILED'
        
        # Encerra comunicação.
        print("\nComunicação encerrada")
        com1.disable()
        
    except Exception as erro:
        print(f"ops! :-\n{erro}")
        com1.disable()
        
if __name__ == "__main__": 
    main()
