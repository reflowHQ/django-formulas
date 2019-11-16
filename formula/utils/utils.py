from django.conf import settings

DEFAULTS = {
    'FORMULA_OPERATIONS': {
        '>=': '>=',
        '<=': '<=',
        '<>': '!=',
        '<': '<',
        '>': '>',
        '/':'/', 
        '&':'+',
        '%':'%', 
        '-':'-', 
        '+':'+',
        '*':'*',
        '^':'**', 
        '=': '=='
    },
    'FORMULA_TYPES': [
        ('field', r'{{[^{{]*}}')
    ],
    'FORMULA_FORMULAS': {
        'SUM': ['SOMA', 'SUM', 'ADD'],
        'COUNT': ['CONTA'],
        'AVERAGE': ['MEDIA']
    },
    'FORMULA_FORMULAS_PATH': 'formula.formulas',
    'FORMULA_KEYWORD': 'Formula',
    'FORMULA_TRIM_SPACES': '_',
    'FORMULA_TITLE_STRING': True

}

def get_settings(name):
    return getattr(settings, name, DEFAULTS[name])