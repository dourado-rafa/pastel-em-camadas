from enlace import *
import time
import numpy as np

serialName = "COM5" # O gerenciador de dispositivos informa a porta

def main():
    try:
        # Ativa comunicacao. Inicia os threads e a comunicação seiral
        com1 = enlace(serialName)
        com1.enable() 
        print("Abriu a comunicação")
        print("Esperando byte de sacrifício...\n")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)
        
        # Escreva o código aqui:
            
            # Recebendo os dados 
        receiving = True
        data = b""
        print('Aguardando o client enviar os comandos')
        while receiving:
            recived_data = com1.rx.getAllBuffer(0)
            data += recived_data
            if recived_data != b'':
                print(f'\nRecebido {len(recived_data)} bytes:\n{recived_data}\n')
            time.sleep(0.1)
            if  b'\xBD' in data:
                receiving = False

            # Limpando ruidos do recebimento
        while data[0].to_bytes() != b'\xff':
            data = data[1:]
        while data[-1].to_bytes() != b'\xBD':
            data = data[:len(data)-1]

            # Separando comandos
        data_instructions, data_commands = [ part for part in data.split(b'\xff') if part != b'' ]
        instructions = []
        for byte in data_instructions:
            binary = bin(byte)
            instructions.append(int('0b'+binary[2:-4], 2))
            instructions.append(int('0b'+binary[-4:], 2))
        instructions = [command_len for command_len in instructions if command_len != 0]
        commands = []
        for end in instructions:
            commands.append(data_commands[:end])
            data_commands = data_commands[end:]

        print(f'{len(commands)} comandos recebidos')
        for command in commands:
            print(command)

            # Enviando a resposta para o client
        txBuffer = (len(commands)).to_bytes()
        com1.sendData(np.asarray(txBuffer))
        print(f'Byte de resposta enviado')
    
        # Encerra comunicação.
        print("\nComunicação encerrada")
        com1.disable()
        
    except Exception as erro:
        print(f"ops! :-\n{erro}")
        com1.disable()
        
if __name__ == "__main__":
    main()
