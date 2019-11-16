from .settings import Structure
import random

class Token(Structure):
    def __init__(self, value, token_type, model=None, *args, **kwargs):
        self.__model = model
        if token_type not in self.types:
            raise ValueError("Must be one of the valid token types")
        if token_type in 'fields':
            value = value.replace('{{', '').replace('}}', '').replace(' ', '')
        self.__raw_value = value
        self.type = token_type

    def value(self):
        """
        When we tokenize the value we tokenize the value `as is`, so the values are not changed, when we retrieve the
        value on the other hand the values are retrieved the `right way`, so a way that python can read and evaluate.
        """
        value = str(self.__raw_value)
        if self.type == 'number':
            value = str(float(value.replace('_', '').replace(',','.')))

        if self.type == 'operation':
            value = self.operations[value]

        if self.type == 'field':
            if self.__model:
                # gets value if it exsits in model, otherwise get 0
                value = self.__model.__dict__.get(value,  0)
            
        return value
