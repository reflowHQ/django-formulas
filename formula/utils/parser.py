from .lexer import Lexer
from ..tokens import Token
from ..settings import Structure
from ..exceptions import ValidateError
from django.conf import settings
import multiprocessing

class Parser(Structure):
    def __init__(self, expression, model, *args, **kwargs):
        # lexer validates and do most of the formating of the formula
        lexer = Lexer(expression, model)
        self.__model = model
        self.__tokens = lexer.tokens
        self.__expression = self.__pre_parse(lexer.expression)

    def __pre_parse(self, expression):
        """
        This pre_parse function is used to parse the parenthesis.
        if we have a function like `SUM ( token ; COUNT ( token ; token ) )` it needs to
        first calculate the COUNT, then calculate the SUM, the idea here is to get all the
        formulas from the upper level and going down to the lower level.
        We end up getting something like
        `[
            ('COUNT', 'token ; token'),
            ('SUM', 'token ; COUNT ( token ; token )')
        ]`

        it`s important to notice that the SUM there will not have the values substituted with the new value
        we do this in parse, so in the `SUM`, in the parse function we will end up getting something like
        `('SUM', 'token ; newly_generated_token_from_count')`

        for simple formulas like `( 2 * 2 ) + 2` we end up getting (THE VALUES ARE ALL TOKENIZED, I'M WRITTING LIKE
        THIS FOR EASIER REPRESENTATION)
        `[
            ('', '2 * 2'),
            ('', '( 2 * 2 ) + 2')
        ]`

        """
        response = list()
        stack = list()
        for index, content in enumerate(expression):
            if content == '(':
                stack.append(index)
            elif content == ')' and stack:
                start = stack.pop()
                method = expression[start-1] if self.is_formula(expression[start-1].upper()) else None
                extracted_expression =' '.join(expression[start + 1: index]).replace('( ', '').replace(' )', '')
                response.append((method, extracted_expression))
        return response

    def __to_python(self, python_evaluated, result):
        try:
            result.put(eval(python_evaluated, {'__builtins__':None}, {}))
        except OverflowError as oe:
            pass

    def __evaluate(self, method):
        """
        This converts everything to a python-like string and evaluates the value for a single value.
        The tokens here are retrieved, on this retriaval of the value we convert it to the correct value.
        """
        python_evaluated = ''
        complete_expression = []
        for token in method.split(' '):
            complete_expression.append(str(self.__tokens[token].value()))
        python_evaluated = ''.join(complete_expression)

        # this is used so it doesn't overkill our cpu
        result = multiprocessing.Queue()
        process = multiprocessing.Process(target=self.__to_python, args=(python_evaluated, result))
        process.start()
        process.join(0.5)
        if process.is_alive():
            process.terminate()
        result = result.get(timeout=0.5)
        return result

    def __append_token(self, value):
        """
        Read __pre_parse function, values calculated in the upper level of the function are tokenized and 
        substituted on the lower levels
        """
        new_token = self.new_token
        self.tokenized[new_token] = Token(value, 'number')
        return new_token

    def __validate_and_calculate_formulas(self, method, parameters):
        """
        This helper function, it only works for formulas
        since we can have
        `[
            ('COUNT', 'token ; token'),
            ('SUM', 'token ; COUNT ( token ; token )')
        ]` 
        and
        `[
            ('', '2 * 2'),
            ('', '( 2 * 2 ) + 2')
        ]`
        when the FORMULA is set in the tuple (first value of the tuple), this formula is used/

        It is used for retriving formulas as objects, where to find the classes is defined on FORMULA_FORMULAS.
        If we have a keyword defined like `Formula` we will find `FormulaCount` instead of `Count`
        FORMULA_TRIM_SPACES is used since we can have formulas like COUNT.IF, or COUNT_IF, we count '.' or '_' as spaces
        The FORMULA_TILE_STRING means if the method is COUNT it will look for a class named `Count` instead of `COUNT`

        This makes a last validation on the formulas, we can have formulas that accept (boolean; any; any), we can then validate if
        the parameters are correct.
        """
        method = method.replace(settings.FORMULA_TRIM_SPACES, ' ')
        if settings.FORMULA_TITLE_STRING:
            method = method.title()
        method = settings.FORMULA_KEYWORD + method
        module = __import__(settings.FORMULA_FORMULAS, fromlist=[method])
        obj = getattr(module, method)
        handler = obj()
        if handler.validate(tuple(parameters)):
            result = handler.calculate(tuple(parameters))
            return result
        else:
            raise ValidateError(detail=method, code='formula_not_valid')

    def parse(self):
        """
        Effectively parses the formula and retrieves the result for the user. So the user just have to call instantiate the Parser class
        with the formula string and then call the parse in order to retrieve the result.

        The parser is responsible for substituting results from the upper level to the lower level. In the following example
         `[
            ('COUNT', 'token ; token'),
            ('SUM', 'token ; COUNT ( token ; token )')
        ]`
        on the first pass the result from COUNT ( token ; token ) is tokenized and added to a dict, then, on the second pass
        the value is substituted in the lower levels.
        """
        calculated = dict()
        result = 0
        for method, expression in self.__expression:
            for key, value in calculated.items():
                expression = expression.replace(key, value)            
            calculated_key = '{} {}'.format(method, expression) if method else expression
            if method:
                parameters = [self.__evaluate(parameter) for parameter in expression.split(' ; ')]
                result = self.__validate_and_calculate_formulas(method, parameters)
            else:
                result = self.__evaluate(expression)

            token = self.__append_token(result)
            calculated[calculated_key] = token
        return result
