from enlace import *
import time
import numpy as np

serialName = "COM5" # O gerenciador de dispositivos informa a porta

def main():
    print("Iniciou o main")
    try:
        # Ativa comunicacao. Inicia os threads e a comunicação seiral
        com1 = enlace(serialName)
        com1.enable() 
        print("Abriu a comunicação")
        
        # Escreva o código aqui:
        transmission = True
        data = b""
        # recived_data = b'\xff\x00\xaa\xff\x00\xbb\x00\xff\xbb\x00\x00\xff\xbb\xff\x00\xaa\xff\x00\x00\xbb\xff\x00\x00\xbb\xff\xbb\x00\x00\xff\x00\x00\xbb\x00\xff\x00\xff\x00\xaa\xff\xbb\xff\x00\x00\x00\x00\xff\x00\xaa\xff\x00\x00\xbb\xff\x00\xff\xbb\xff\x00\xaa\xff\x00\xaa\xff\x00\xbb\x00\xff\xbb\xff\x00\x00\x00\x00\xff\xbb\x00\xff\x00\x00\xbb\x00\xff\x00\x00\x00\x00\xff\xbb\x00\x00\xff\x00\x00\xbb\xff\xbb\x00\x00\xff\xbb\xff\xff'
        while transmission:
            recived_data = com1.rx.getAllBuffer(0)
            if recived_data != b'':
                print(f'{recived_data} recebido')
            data = data + recived_data
            if  b'\xFF\xFF' in data:
                transmission = False

        commands = [ command for command in data.split(b'\xff') if command != b'' ]

        txBuffer = (len(commands)).to_bytes()
        com1.sendData(np.asarray(txBuffer))

        print(f'{len(commands)} comandos recebidos')
        for command in commands:
            print(command)
    
        # Encerra comunicação.
        print("\nComunicação encerrada")
        com1.disable()
        
    except Exception as erro:
        print(f"ops! :-\n{erro}")
        com1.disable()
        
if __name__ == "__main__":
    main()
