import string
import random
from django.conf import settings
from .utils import utils
import collections

class Structure:
    operations = dict([(operation, utils.get_settings('FORMULA_OPERATIONS'))[operation] for operation in collections.OrderedDict(
        sorted(
            dict(
                [(len(operation), operation) for operation, operaton_reference in utils.get_settings('FORMULA_OPERATIONS').items()]
                )
            )
        ).items()])

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
        for formula in self.formulas:
            yield (formula['name'], formula['label_name'])

    def get_correct_formula(self, method):
        for formula in self.__formulas_as_list():
            if formula[1] == method:
                return formula[0]
        return method


    def is_formula(self, token):
        names = [formula[0] for formula in self.__formulas_as_list()]
        label_names = [formula[1] for formula in self.__formulas_as_list()]
        return token in names or token in label_names
    