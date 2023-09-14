from enlace import *
from datagrama import datagrama, read_datagrama, Message
from color import color_print
import time, random
import traceback

serialName = "COM5" # O gerenciador de dispositivos informa a porta
ERROR_CHANCE = 0

def receive_message(com:enlace, head_length:int=12, eop_expected:str='END'.encode()) -> Message:
    head = com.rx.getNData(head_length)
    payload = com.rx.getNData(head[0])
    eop = com.rx.getNData(len(eop_expected))
    if eop == eop_expected:
        return read_datagrama(head, payload, eop)
    print('Pacote invalido! EOP diferente do esperado')
    return Message() # Mensagem vazia com code 204 (No content)

def wait_response(com:enlace, wait:int) -> Message:
    start = time.time()
    wait = 1e10 if wait == 0 else wait
    while (time.time() - start) <= wait:
        if not com.rx.getIsEmpty():
            return receive_message(com)
    return Message() # Mensagem vazia com code 204 (No content)

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
                if response.code == 202:
                    print('Conexão estabelecida!')
                    status = 'TRANSMITTING'
                else:
                    try_connect = input('Servidor inativo. Tentar novamente? (S/N) ').upper() == 'S'
                    if not try_connect:
                        status = 'END-CONNECTION-FAILED'

            elif status == 'TRANSMITTING':
                size = len(fragments[current-1])
                if random.random() < ERROR_CHANCE :
                    color_print('\n-----> Essa menssagem está com erro! <-----', 'red')
                    size = 0

                com1.sendData(datagrama(current, total, code=code, payload=fragments[current-1], size=size))
                time.sleep(.01)
                print(f'\nPacote [{current}/{total}] enviado! Aguardando confirmação de recebimento...')

                response = wait_response(com1, 3)
                if response.code == 200:
                    color_print(f'Pacote [{current}/{total}] recebido com sucesso pelo cliente!\nEnviando próximo pacote...', 'green')
                    code = 100
                    current += 1
                elif response.code in [409, 413]:
                    color_print(f'Houve uma falha no recebimento do pacote [{current}/{total}]!\nReenviando pacote...', 'yellow')
                    if current-1 <= response.current <= current+1:
                        current = response.current
                    code = 205
                elif not response.isValid():
                    color_print(f'Nenhuma resposta recebida!\nReenviando pacote...', 'yellow')
                    code = 205
                else:
                    color_print(f'Pacote tipo {response.code} recebido! Não há ação para esse tipo de pacote\nReenviando pacote...', 'red')
                    code = 205

                if current > total:
                    print(f'\nTodos os {total} pacos foram enviados!')
                    status = 'CONFIRMING'

            elif status == 'CONFIRMING':
                print(f'Aguardando confirmação de recebimento...')

                response = wait_response(com1, 0)
                if response.code == 418:
                    color_print(f'Todos os {total} pacotes foram recebidos com sucesso!', 'green')
                    color_print("\nI'm a Teapot!", 'cyan')
                    status = 'END-TRANSMISSION-SUCESSFUL'
                else:
                    color_print(f'Algo na transmissão falhou, mas não há nada a se fazer... :(', 'red')
                    status = 'END-TRANSMISSION-FAILED'
        
        # Encerra comunicação.
        print("\nComunicação encerrada")
        com1.disable()
        
    except Exception as error:
        print(f"ops! :-{traceback.format_exc()}")
        com1.disable()
        
if __name__ == "__main__": 
    main()
