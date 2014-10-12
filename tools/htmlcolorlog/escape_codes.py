"""
Generates a dictionary of ANSI escape codes

http://en.wikipedia.org/wiki/ANSI_escape_code

Uses colorama as an optional dependancy to support color on Windows
"""

try:
    import colorama
except ImportError:
    pass
else:
    colorama.init()

__all__ = ['escape_codes']


# The initial list of escape codes
escape_codes = {
    'black'     : '<span style="color:black">',
    'red'       : '<span style="color:red">',
    'green'     : '<span style="color:green">',
    'yellow'     : '<span style="color:yellow">',
    'purple'     : '<span style="color:purple">',
    'cyan'     : '<span style="color:cyan">',
    'white'     : '<span style="color:white">',
    'blue'      : '<span style="color:blue">',
    'orange'    : '<span style="color:orange">',
    'bold'      : '<b>',
    'ebold'     : '</b>',
    'br'        : '<br/>',
    'reset'     : '</span>'
}

# The color names
COLORS = [
    'black',
    'red',
    'green',
    'yellow',
    'blue',
    'purple',
    'cyan',
    'white',
    'underline'
]




