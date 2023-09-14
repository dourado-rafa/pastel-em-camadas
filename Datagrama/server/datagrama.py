def head(n:int=0, current:int=0, total:int=0, origin:str='', code:int=0) -> bytearray:
    head = b''
    head += n.to_bytes(1)
    head += current.to_bytes(2)
    head += total.to_bytes(2)
    head += origin.upper().encode() if origin != '' else b'\x00'
    head += code.to_bytes(2)
    head += 4*b'\x00'
    return head

def datagrama(current:int=0, total:int=0, origin:str='S', code:int=0, payload:bytearray=b'', eop:str='END') -> bytearray:
    return head(len(payload), current, total, origin, code) + payload + eop.upper().encode()

DECODER = {
    100: "Continue", # Continue mandando os pacotes
    101: "Switching Protocols",
    200: "OK", # OK
    201: "Created",
    202: "Accepted", # Conexão aceita
    203: "Non-Authoritative Information",
    204: "No Content",
    205: "Reset Content", # Reenviando Pacote
    206: "Partial Content",
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Found",
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",
    307: "Temporary Redirect",
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Timeout",
    409: "Conflict", # Erro no número do pacote
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed",
    413: "Payload Too Large", # Erro no tamanho do Payload
    414: "URI Too Long",
    415: "Unsupported Media Type",
    416: "Range Not Satisfiable",
    417: "Expectation Failed",
    418: "I'm a Teapot",
    421: "Misdirected Request",
    422: "Unprocessable Entity",
    423: "Locked",
    424: "Failed Dependency",
    425: "Too Early",
    426: "Upgrade Required",
    428: "Precondition Required",
    429: "Too Many Requests",
    431: "Request Header Fields Too Large",
    451: "Unavailable For Legal Reasons",
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
    505: "HTTP Version Not Supported",
    506: "Variant Also Negotiates",
    507: "Insufficient Storage",
    508: "Loop Detected",
    510: "Not Extended",
    511: "Network Authentication Required" # Tentando conectar
}