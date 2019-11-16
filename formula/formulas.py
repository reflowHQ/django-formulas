from .settings import Formula

class FormulaSum(Formula):
    def validate(self, parameters):
        return all([type(parameter) == float for parameter in parameters])

    def calculate(self, parameters):
        result = 0
        for parameter in parameters:
            result += parameter
        return result

class FormulaCount(Formula):
    def calculate(self, parameters):    
        return len(parameters)


class FormulaAvarege(Formula):
    def validate(self, parameters):
        return all([type(parameter) == float for parameter in parameters])

    def calculate(self, parameters):
        result = 0
        for parameter in parameters:
            result += parameter
        result = result/len(parameters)
        return result
