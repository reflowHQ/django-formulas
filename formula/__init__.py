from .exceptions import FormulaException
from formula.utils.parser import Parser
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
            return '#ERROR'
        except queues.Empty as empty:
            return '#NUM'
        except Exception as e:
            return '#N/A'
