from enlace import *
import time, random
import numpy as np

serialName = "COM3" # O gerenciador de dispositivos informa a porta

def main():
    try:
        # Ativa comunicacao. Inicia os threads e a comunicação seiral
        com1 = enlace(serialName)
        com1.enable()
        print("Abriu a comunicação")
        
        # Escreva o código aqui:

        # Encerra comunicação.
        print("\nComunicação encerrada")
        com1.disable()
        
    except Exception as erro:
        print(f"ops! :-\n{erro}")
        com1.disable()
        
if __name__ == "__main__":
    main()
