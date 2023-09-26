from enlace_server.enlace import enlace
from support import *
from datagrama import *
import traceback

serialName = "COM5" # O gerenciador de dispositivos informa a porta

SERVER_NUMBER = 13
MESSAGE_TYPES = ['[MENSAGEM INVALIDA]', '[PEDIDO DE CONEXÃO]', '[SERVER PRONTO]', '[ENVIANDO PACOTE DE DADOS]', '[PACOTE DE DADOS RECEBIDO]', '[TIME OUT]', '[ERROR]']


def receive_message(com:enlace, log:Log, head_length:int=10, eop_expected:bytearray=b'\xAA\xBB\xCC\xDD') -> Message:
    if com.rx.getBufferLen() >= head_length+len(eop_expected):
        head = com.rx.getNData(head_length)
        size = head[5] if head[0] == 3 else 0
        if com.rx.getBufferLen() > size:
            payload = com.rx.getNData(size)
            eop = com.rx.getNData(len(eop_expected))
            if eop == eop_expected:
                datagrama = head+payload+eop
                log.write('RECEBIMENTO', datagrama)
                return read_datagrama(datagrama)
    com.rx.clearBuffer()
    return Message()

def send_message(com:enlace, log:Log, datagrama:bytearray) -> None:
    com.sendData(datagrama)
    log.write('ENVIO', datagrama)
    while com.tx.getStatus() == 0:
        time.sleep(.01)


def main():
    try:
        # Ativa comunicacao. Inicia os threads e a comunicação seiral
        com1 = enlace(serialName)
        com1.enable()
        print("Abriu a comunicação")
        
        # Escreva o código aqui:
        status = 'IDLE'
        global total, current
        global ressend_timer, wait_timer
        global log, data

        log = Log('Server', decoder=MESSAGE_TYPES)
        
        print('Servidor Iniciado!\n')
        while status != 'OFFLINE':
            
            if status == 'IDLE':
                message = receive_message(com1, log)
                if message.isValid() and message.type == 1 and message.server_number == SERVER_NUMBER:
                    log.set_id(message.id)
                    data = []
                    total, current = message.total, 1
                    ressend_timer = Timer(2)
                    wait_timer = Timer(20)
                    send_message(com1, log, datagrama(type=2))
                    status = 'RECIVING'
                time.sleep(1)
            
            elif status == 'RECIVING':
                if total >= current:
                    message = receive_message(com1, log)
                    if message.type == 3:
                        if message.isValid() and message.current == current:
                            color_print(f'Pacote [{current}|{total}] recebido com sucesso!', 'green')
                            send_message(com1, log, datagrama(type=4, sucess=current))
                            data.append(message.payload)
                            current += 1
                        else:
                            color_print(f'Erro! Pacote [{message.current}|{total}] enviado, mas era esperado o pacote [{current}|{total}]', 'red')
                            com1.rx.clearBuffer()
                            send_message(com1, log, datagrama(type=6, restart=current))
                        ressend_timer.reset()
                        wait_timer.reset()

                    else:
                        time.sleep(1)
                        if wait_timer.timeOut():
                            send_message(com1, log, datagrama(type=5))
                            status = 'OFFLINE'
                        elif ressend_timer.timeOut():
                            send_message(com1, log, datagrama(type=4, sucess=current))
                            ressend_timer.reset()

                else:
                    print('Sucesso na Transmissão!')
                    log.save(f'img/teapot{log.id}.png', data)
                    status = 'OFFLINE'

        print('\nServidor Encerrado')

        # Encerra comunicação.
        print("\nComunicação encerrada")
        com1.disable()
        
    except Exception as error:
        print(f"ops! :-{traceback.format_exc()}")
        com1.disable()
        
if __name__ == "__main__":
    main()