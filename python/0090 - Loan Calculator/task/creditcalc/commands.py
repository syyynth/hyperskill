from abc import ABC, abstractmethod


class OverpaymentCommandMixin:
    def print_overpayment(self):
        print(f'Overpayment = {self.calculator.payment * self.calculator.periods - self.calculator.principal}')


class Command(ABC):
    def __init__(self, calculator):
        self.calculator = calculator

    @abstractmethod
    def execute(self):
        pass


class AnnuityPeriodCommand(Command, OverpaymentCommandMixin):
    def execute(self):
        self.calculator.calc_periods()
        print(f'It will take {self.calculator.format_months(self.calculator.periods)} to repay loan!')
        self.print_overpayment()


class AnnuityPaymentCommand(Command, OverpaymentCommandMixin):
    def execute(self):
        self.calculator.calc_payment()
        print(f'Your monthly payment = {self.calculator.payment}!')
        self.print_overpayment()


class AnnuityPrincipalCommand(Command, OverpaymentCommandMixin):
    def execute(self):
        self.calculator.calc_principle()
        print(f'Your loan principal = {self.calculator.principal}!')
        self.print_overpayment()


class DifferentiatedPaymentsCommand(Command):
    def execute(self):
        diff_payments = self.calculator.calc_payments()
        for idx, month in enumerate(diff_payments, start=1):
            print(f'Month {idx}: payment is {month}')
        print(f'Overpayment = {sum(diff_payments) - self.calculator.principal}')
