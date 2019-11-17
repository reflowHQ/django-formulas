from .exceptions import FormulaException
from .utils.parser import Parser
from .utils.utils import get_settings
from multiprocessing import queues

class Formula:
    def __init__(self, model, expression, *args, **keywords):
        try:
            self.__parser = Parser(model, expression)
        except FormulaException as fe:
            pass

    @property
    def value(self):
        try:
            return self.__parser.parse()
        except AttributeError as ae:
            return get_settings('FORMULA_ERROR_MESSAGE')
        except queues.Empty as empty:
            return get_settings('FORMULA_NUM_MESSAGE')
        except Exception as e:
            return get_settings('FORMULA_NA_MESSAGE')
