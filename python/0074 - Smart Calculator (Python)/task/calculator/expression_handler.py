from constants import MSG_UNKNOWN_VARIABLE, MSG_INVALID_ASSIGNMENT, MSG_INVALID


class ExpressionHandler:
    def __init__(self):
        self.memo = {}

    def assign_variable(self, var, value):
        """
        Assigns a value to a variable.
        The validity of variable and value is checked before the assignment.
        """
        if not var.isalpha() or (value.isalpha() and value not in self.memo):
            return MSG_INVALID_ASSIGNMENT

        try:
            self.memo[var] = eval(value, self.memo)
        except (NameError, SyntaxError):
            return MSG_INVALID_ASSIGNMENT

    def parse_assignment(self, expr):
        """
        Parses a given expression and assigns a value to a variable.
        The expression is expected to have exactly one '=' sign.
        """
        if expr.count('=') != 1:
            return MSG_INVALID_ASSIGNMENT

        var, value = expr.split('=')

        return self.assign_variable(var, value)

    def parse_variable(self, expr):
        """
        Fetches the value of a given variable from the memory.
        If the variable does not exist, returns an unknown variable message.
        """
        return self.memo.get(expr, MSG_UNKNOWN_VARIABLE)

    def parse_expression(self, expr):
        """
        Evaluates a given expression with the known variables.
        """
        try:
            return eval(expr.replace('/', '//'), self.memo)
        except SyntaxError:
            return MSG_INVALID
