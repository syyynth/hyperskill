from command_handler import CommandHandler
from expression_handler import ExpressionHandler


class Calculator:
    def __init__(self):
        self.command_handler = CommandHandler()
        self.expression_handler = ExpressionHandler()
        self.expr_type_handlers = {
            'command': self.command_handler.parse_command,
            'assignment': self.expression_handler.parse_assignment,
            'variable': self.expression_handler.parse_variable,
            'expression': self.expression_handler.parse_expression,
        }

    @staticmethod
    def preprocess(expr):
        return expr.strip().replace(' ', '')

    @staticmethod
    def determine_expr_type(expr):
        if expr.startswith('/'):
            return 'command'
        if '=' in expr:
            return 'assignment'
        if expr.isalpha():
            return 'variable'
        return 'expression'

    def evaluate(self, expr):
        expr = self.preprocess(expr)
        if len(expr) < 1:
            return

        expr_type = self.determine_expr_type(expr)
        handler = self.expr_type_handlers.get(expr_type)
        if handler:
            return handler(expr)
