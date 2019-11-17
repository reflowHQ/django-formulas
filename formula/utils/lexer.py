from ..settings import Structure
from ..exceptions import FormulaException
from ..tokens import Token
import re

class Lexer(Structure):
    def __init__(self, expression, model, *args, **kwargs):
        self.__model = model
        self.__expression = '({})'.format(expression)
        self.__tokenized = dict()
        for to_tokenize in self.to_tokenize:
            matches = re.findall(to_tokenize[1], self.__expression)
            self.__tokenize(matches, to_tokenize[0])
        self.__format_and_validate()

    @property
    def expression(self):
        """
        Returns the lexed expression, the lexed expression is tokenized values ignoring formulas, 
        and special characters as (, ) and ;
        """
        
        return self.__expression

    @property
    def tokens(self):
        """
        Returns a dict of tokenized objects, each token is on this dict, we need this to pass it to every step on the pipeline
        from lexing to parsing the values.
        """

        return self.tokenized

    def __tokenize(self, matches, token_type):
        """
        Creates a Token object based on regex expressions, each token holds the type on which type the string is,
        and the value. The tokens are saved in a variable called tokenized, it is a dict that holds all the tokens as keys
        And Token objects as value. The keys are then replaced in the expression.

        :param: matches -> List of regular expression matches from the regex
        :param: token_type -> Check types in Structure inside settings.py
        """

        for match in matches:
            key = self.new_token
            self.tokenized[key] = Token(match, token_type, self.__model)
            self.__expression = self.__expression.replace(match, ' {} '.format(key), 1)

    def __format_and_validate(self):
        """
        Runs format and validate functions
        """

        return self.__format()

    def __format(self):
        """
        Removes all the extra spaces from the formula and adds exactly one space per item, do if the formula is as
        'SUM     ( 1; 2; 3)' we first tokenize the numbers in the __tokenize() function so we end up with 
        'SUM     ( token; token; token)' and then in this function we format and end up with
        'SUM ( token ; token ; token )' with exactly one space per item.

        Based on that we also get the correct formula, so if, in pt-br the formula is `SOMA` we end up getting `SUM`
        """

        for character in self.valid_characters:
            self.__expression = self.__expression.replace(character, ' {} '.format(character))
        self.__expression = list(filter(None, self.__expression.split(' ')))
        for index, item in enumerate(self.__expression):
            self.__expression[index] = self.get_correct_formula(item)
        print(self.__expression)

        return self.__validate()
    
    def __validate(self):
        """
        Validates if the formula is valid, only formulas, valid characters or and tokens are valid, if it is not any of 
        them the formula is invalid. We also check for the number of parenthesis so a formula like
        `SUM (1;2;3))` will fail because of the extra parenthesis.
        """

        validate_parenthesis = [0, 0]
        for token in self.__expression:
            if token != '':
                if token in self.tokenized.keys():
                    pass
                elif self.is_formula(token.upper()): 
                    pass
                elif token in self.valid_characters:
                    if token == '(':
                        validate_parenthesis[0] += 1
                    elif token == ')':
                        validate_parenthesis[1] += 1
                else:
                    raise FormulaException('Formula not valid')
        if validate_parenthesis[0] != validate_parenthesis[1]:
            raise FormulaException('Formula not valid')
        