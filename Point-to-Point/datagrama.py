import numpy as np

def head(type:int=0, server_number:int=0, current:int=0, total:int=0, id:int=0, restart:int=0, sucess:int=0) -> bytearray:
    head = b''
    head += type.to_bytes(1)
    head += server_number.to_bytes(1)
    head += b'\x00'
    head += current.to_bytes(1)
    head += total.to_bytes(1)
    head += id.to_bytes(1)
    head += restart.to_bytes(1)
    head += sucess.to_bytes(1)
    head += 3*b'\x00'
    return head

def datagrama(type:int=0, server_number:int=0, current:int=0, total:int=0, id:int=0, restart:int=0, sucess:int=0, 
              payload:bytearray=b'', eop:str=b'\xAA\xBB\xCC\xDD') -> bytearray:
    size_id = len(payload) if id != 0 else id
    return np.asarray(head(type, server_number, current, total, size_id, restart) + payload + eop)

def fragment_file(filepath:str, length:int=114) -> list[bytearray]:
    fragments = []
    with open(filepath, 'rb') as file:
        content = file.read()
        for i in range(0, len(content), length):
            fragment = content[i:i+length] if i+length < len(content) else content[i:]
            fragments.append(fragment)
    file.close()
    return fragments
