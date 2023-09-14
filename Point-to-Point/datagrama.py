import numpy as np
from enlace_server.enlace import enlace

def fragment_file(filepath:str, length:int=114) -> list[bytearray]:
    fragments = []
    with open(filepath, 'rb') as file:
        content = file.read()
        for i in range(0, len(content), length):
            fragment = content[i:i+length] if i+length < len(content) else content[i:]
            fragments.append(fragment)
    file.close()
    return fragments

def head(type:int=0, server_number:int=0, current:int=0, total:int=0, id:int=0, restart:int=0, sucess:int=0) -> bytearray:
    head = b''
    head += type.to_bytes(1)
    head += server_number.to_bytes(1)
    head += b'\x00'
    head += total.to_bytes(1)
    head += current.to_bytes(1)
    head += id.to_bytes(1)
    head += restart.to_bytes(1)
    head += sucess.to_bytes(1)
    head += 2*b'\x00'
    return head

def datagrama(type:int=0, server_number:int=0, current:int=0, total:int=0, id:int=0, restart:int=0, sucess:int=0, 
              payload:bytearray=b'', eop:str=b'\xAA\xBB\xCC\xDD') -> bytearray:
    size_id = len(payload) if id == 0 else id
    return np.asarray(head(type, server_number, total, current, size_id, restart, sucess) + payload + eop)

class Message():
    def __init__(self, type:int=0, server_number:int=0, current:int=0, total:int=0, size_id:int=0, restart:int=0, sucess:int=0, payload:bytearray=b'', eop:bytearray=b'') -> None:
        self.type = type
        self.server_number = server_number
        self.current = current
        self.total = total
        self.id = size_id if len(payload) == 0 else 0
        self.size = size_id if len(payload) > 0 else 0
        self.restart = restart
        self.sucess = sucess
        self.payload = payload
        self.eop = eop
        
    def isValid(self) -> bool:
        return (self.type != 0 and self.eop == b'\xAA\xBB\xCC\xDD')
    
def read_datagrama(head:bytearray, payload:bytearray, eop:bytearray) -> Message:
    type = head[0]
    server_number = head[1]
    total = head[3]
    current = head[4]
    size_id = head[5]
    restart = head[6]
    sucess = head[7]
    return Message(type, server_number, total, current, size_id, restart, sucess, payload, eop)