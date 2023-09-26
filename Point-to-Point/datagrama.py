import numpy as np
from datetime import datetime
from crc import Crc16, Calculator

CRC = Calculator(Crc16.CCITT)

def fragment_file(filepath:str, length:int=114) -> list[bytearray]:
    fragments = []
    with open(filepath, 'rb') as file:
        content = file.read()
        for i in range(0, len(content), length):
            fragment = content[i:i+length] if i+length < len(content) else content[i:]
            fragments.append(bytearray(fragment))
    file.close()
    return fragments


def datagrama(type:int=0, server_number:int=0, total:int=0, current:int=0, id:int=0, restart:int=0, sucess:int=0, 
              payload:bytearray=b'', eop:str=b'\xAA\xBB\xCC\xDD') -> bytearray:
    
    size_id = len(payload) if id == 0 else id
    crc = CRC.checksum(payload) if type == 3 else 0
    head = b''

    head += type.to_bytes(1)
    head += server_number.to_bytes(1)
    head += b'\x00'
    head += total.to_bytes(1)
    head += current.to_bytes(1)
    head += size_id.to_bytes(1)
    head += restart.to_bytes(1)
    head += sucess.to_bytes(1)
    head += crc.to_bytes(2)

    return bytearray(head + payload + eop)


def write_line(arq, time:float, env_reb:str, tipo:int, tamanho:int, current:int=0, total:int=0):
    line = ""
    line += datetime.fromtimestamp(time).strftime("%m/%d/%Y, %H:%M:%S")
    line += f" {env_reb}"
    if current != 0:
        line += f" {tipo}/ {tamanho} / {current} / {total}"
    else:
        line += f" {tipo}/ {tamanho}"
    line += "\n"
    arq.write(line)
