import numpy as np
import time, datetime


def fragment_file(filepath:str, length:int=114) -> list[bytearray]:
    fragments = []
    with open(filepath, 'rb') as file:
        content = file.read()
        for i in range(0, len(content), length):
            fragment = content[i:i+length] if i+length < len(content) else content[i:]
            fragments.append(bytearray(fragment))
    file.close()
    return fragments


def head(type:int=0, server_number:int=0, total:int=0, current:int=0, id:int=0, restart:int=0, sucess:int=0) -> bytearray:
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


def datagrama(type:int=0, server_number:int=0, total:int=0, current:int=0, id:int=0, restart:int=0, sucess:int=0, 
              payload:bytearray=b'', eop:str=b'\xAA\xBB\xCC\xDD') -> bytearray:
    size_id = len(payload) if id == 0 else id
    return bytearray(head(type, server_number, total, current, size_id, restart, sucess) + payload + eop)

def localTime(time_msg):
    return datetime.fromtimestamp(time_msg)

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
        
    def isValid(self) -> bool:
        return (self.type != 0 and self.length > 0 and self.eop == b'\xAA\xBB\xCC\xDD')


def unpack_datagrama(datagrama:bytearray, head_length:int=10) -> tuple[bytearray,bytearray,bytearray]:
    size = datagrama[5] if datagrama[0] == 3 else 0
    return datagrama[:head_length], datagrama[head_length:size], datagrama[head_length+size:]
    

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
    
    def timeOut(self) -> bool:
        self.elapsed = time.time() - self.init
        return self.elapsed > self.cooldown
    
    def reset(self) -> None:
        self.init = time.time()
        self.elapsed = time.time() - self.init


class Log():
    def __init__(self, register:str, id:int, path:str='log/', decoder:list[str]=[]) -> None:
        self.id = id
        self.log_name = register+str(id)
        self.decoder = decoder
        open(path+self.log_name+'.txt', 'w').close()
        self.log = open(path+self.log_name+'.txt', 'a')
    
    def write(self, type:str, datagrama:bytearray) -> None:
        message = read_datagrama(datagrama)
        text = f'\n[{datetime.datetime.now().strftime("%d/%m/%Y %I:%M:%S:%f")[:-3]}] {type.upper():11} | '+'{type}'+f' | {message.length:03}'
        if message.type == 3:
            text += f' | [{message.current:03}|{message.total:03}]'
        self.log.write(text.format(type=message.type))

        if len(self.decoder) > 0:
            print(text.format(type=f'{self.decoder[message.type]:20}'))

    def save(self, filepath:str='', data:bytearray=b'') -> None:
        if filepath == '' or data == b'':
            with open(filepath, 'wb') as file:
                file.write(data)
            file.close()
        self.log.close()