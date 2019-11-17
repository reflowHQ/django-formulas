import string
import random
from .utils import utils
import collections

class Structure:
    operations = dict([(operation, utils.get_settings('FORMULA_OPERATIONS')[operation]) for __, operation in
        reversed(
            sorted(
                [(len(operation), operation) for operation, operaton_reference in utils.get_settings('FORMULA_OPERATIONS').items()]
                )
            )
        ])
    print(operations)
    types = ['string', 'field', 'number', 'operation']

    formulas =  utils.get_settings('FORMULA_FORMULAS')

    to_tokenize = [
        ('string', r'"[^"]*"'),
        ('field', r'{{[^{{]*}}'),
        ('number', r'[\d_-]+\.[\d-]+|[\d_-]+,[\d-]+|[\d_-]+'),
        ('operation', '|'.join(['\\' + operator for operator in operations.keys()]))
    ]

    valid_characters = [
        '(', ')', ';'
    ]
 
    tokenized = dict()
    
    @property
    def new_token(self):
        random_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(30))
        while random_key in self.tokenized:
            random_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(30))
        return random_key

    def __formulas_as_list(self):
        for key, values_list in self.formulas.items():
            yield [key] + values_list

    def get_correct_formula(self, method):
        if self.formulas.get(method, None):
            return method
        else:
            for formula in self.__formulas_as_list():
                if method in formula:
                    return formula[0]
        return method

    def is_formula(self, token):
        for formula in self.__formulas_as_list():
            if token in formula:
                return True
        return False
    