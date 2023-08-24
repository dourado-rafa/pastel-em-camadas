from client.enlace import *
import time
import numpy as np

serialName = "COM5"                  # Windows(variacao de)

def main():
    print("Iniciou o main")
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
