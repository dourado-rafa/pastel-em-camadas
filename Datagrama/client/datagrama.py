class Datagrama():
    def __init__(self) -> None:
        pass

    def head(n:int=0, current:int=0, total:int=0, type:str='', message:str='') -> bytearray:
        head = b''
        head += n.to_bytes(1)
        head += current.to_bytes(2)
        head += total.to_bytes(2)
        head += type.upper().encode() if type != '' else b'\x00'
        message_bytes = message.upper().encode()
        while len(message_bytes) < 6:
            message_bytes += b'\x00'
        head += message_bytes
        return head
    
    def datagrama(current:int=0, total:int=0, type:str='', message:str='', payload:bytearray=b'', eop:str='END') -> bytearray:
        return Datagrama.head(len(payload), current, total, type, message) + payload + eop.upper().encode()

