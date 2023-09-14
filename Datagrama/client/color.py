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
