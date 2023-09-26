import numpy as np
from datetime import datetime
import time


COLORS = {
    '': '00',
    'RED': '91',
    'GREEN': '92',
    'YELLOW': '93',
    'LIGHTPURPLE': '94',
    'PURPLE': '95',
    'CYAN': '96',
    'LIGHTGRAY': '97',
    'BLACK': '98'
}
def color_print(text:str, color:str=''):
    print(f'\033[{COLORS[color.upper()]}m{text}\033[00m')


class Message():
    def __init__(self, type:int=0, server_number:int=0, total:int=0, current:int=0, size_id:int=0, restart:int=0, sucess:int=0, crc:bytearray=b'', payload:bytearray=b'', eop:bytearray=b'', length:int=0) -> None:
        self.type = type
        self.server_number = server_number
        self.current = current
        self.total = total
        self.id = size_id if len(payload) == 0 else 0
        self.size = size_id if len(payload) > 0 else 0
        self.restart = restart
        self.sucess = sucess
        self.crc = crc
        self.payload = payload
        self.eop = eop
        self.length = length

    def __str__(self) -> str:
        text = f'Type: {self.type} | '
        if self.type == 1:
            text += f'Server Number: {self.server_number} | File ID: {self.id} | '
        elif self.type == 3:
            text += f'Size: {self.size} | [{self.current}|{self.total}] | '
        valid = 'Valid' if self.isValid() else 'Invalid'
        text += f'Length: {self.length} | {valid}'
        return text
        
    def isValid(self) -> bool:
        return (1 <= self.type <=6 and self.length > 0 and self.eop == b'\xAA\xBB\xCC\xDD')


def unpack_datagrama(datagrama:bytearray, head_length:int=10) -> tuple[bytearray,bytearray,bytearray]:
    size = datagrama[5] if datagrama[0] == 3 else 0
    return datagrama[:head_length], datagrama[head_length:head_length+size], datagrama[head_length+size:]
    

def read_datagrama(datagrama:bytearray) -> Message:
    head, payload, eop = unpack_datagrama(datagrama)
    type = head[0]
    server_number = head[1]
    total = head[3]
    current = head[4]
    size_id = head[5]
    restart = head[6]
    sucess = head[7]
    crc = head[8:]
    length = len(head)+len(payload)+len(eop)
    return Message(type, server_number, total, current, size_id, restart, sucess, crc, payload, eop, length)


class Timer():
    def __init__(self, cooldown:int) -> None:
        self.cooldown = cooldown
        self.init = time.time()
        self.elapsed = time.time() - self.init

    def __str__(self) -> str:
        self.elapsed = time.time() - self.init
        return f'[{self.elapsed:.2f}|{self.cooldown:.2f}] {(self.elapsed/self.cooldown)*100:.2f}%'
    
    def timeOut(self) -> bool:
        self.elapsed = time.time() - self.init
        return self.elapsed > self.cooldown
    
    def reset(self) -> None:
        self.init = time.time()
        self.elapsed = time.time() - self.init


class Log():
    log, text = None, ''
    def __init__(self, register:str, id:int=0, path:str='log/', decoder:list[str]=[]) -> None:
        self.filename = path+register+'{id}'+'.txt'
        self.register = register
        self.set_id(id)
        self.decoder = decoder

    def set_id(self, id:int) -> None:
        self.id = id
        if id > 0:
            self.filename = self.filename.format(id=id)
            open(self.filename, 'w').close()
            self.log = open(self.filename, 'a')
    
    def write(self, type:str, datagrama:bytearray) -> None:
        message = read_datagrama(datagrama)
        text = f'\n[{datetime.now().strftime("%d/%m/%Y %I:%M:%S:%f")[:-3]}] {type.upper():11} | '+'{type}'+f' | {message.length:03}'
        if message.type == 3:
            text += f' | [{message.current:03}|{message.total:03}]'
        
        self.text += text.format(type=message.type)
        if self.log is not None:
            self.log.write(self.text) 
            self.text = ''
            

    def save(self, filepath:str='', data:list[bytearray]=[]) -> None:
        if filepath != '' and len(data) > 0:
            with open(filepath, 'wb') as file:
                file.write(b''.join(data))
            file.close()
        self.log.close()