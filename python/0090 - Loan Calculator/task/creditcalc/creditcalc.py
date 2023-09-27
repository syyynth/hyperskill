import argparse
import math
from typing import Any

from commands import AnnuityPeriodCommand, AnnuityPaymentCommand, AnnuityPrincipalCommand, \
    DifferentiatedPaymentsCommand

parser = argparse.ArgumentParser(
    description='Loan Calculator',
    allow_abbrev=False
)
parser.add_argument('--type', choices=['annuity', 'diff'])
parser.add_argument('--payment', type=float)
parser.add_argument('--principal', type=float)
parser.add_argument('--interest', type=float)
parser.add_argument('--periods', type=float)


class LoanCalculator:
    def __init__(self,
                 principal=None,
                 interest=None,
                 periods=None,
                 payment=None) -> None:
        self.payment = payment
        self.principal = principal
        self.interest = interest
        self.periods = periods
        self.monthly_interest = self.interest / 1200 if self.interest else None

    def calc_periods(self) -> None:
        self.periods = math.ceil(
            math.log(self.payment / (self.payment - self.monthly_interest * self.principal),
                     1 + self.monthly_interest)
        )

    def _annuity_coefficient(self) -> float:
        return (self.monthly_interest * (1 + self.monthly_interest) ** self.periods /
                ((1 + self.monthly_interest) ** self.periods - 1))

    def calc_payment(self) -> None:
        self.payment = math.ceil(self.principal * self._annuity_coefficient())

    def calc_principle(self) -> None:
        self.principal = math.floor(self.payment / self._annuity_coefficient())

    @staticmethod
    def format_months(months: int) -> str:
        years, months = divmod(months, 12)

        years_output = f'{years} year{"s" if years > 1 else ""}' if years else ''
        months_output = f'{months} month{"s" if months > 1 else ""}' if months else ''

        return ' and '.join(filter(None, (years_output, months_output)))

    def calc_payments(self) -> list[int]:
        return [
            math.ceil(self.principal / self.periods + self.monthly_interest *
                      (self.principal - self.principal * (n - 1) / self.periods))
            for n in range(1, int(self.periods) + 1)
        ]


def get_command(calculator, commands) -> Any:
    if commands.type == 'annuity':
        if calculator.principal and calculator.payment and calculator.interest:
            return AnnuityPeriodCommand(calculator)
        elif calculator.principal and calculator.periods and calculator.interest:
            return AnnuityPaymentCommand(calculator)
        elif calculator.payment and calculator.periods and calculator.interest:
            return AnnuityPrincipalCommand(calculator)
    elif commands.type == 'diff' and calculator.principal and calculator.periods and calculator.interest:
        return DifferentiatedPaymentsCommand(calculator)


def main() -> None:
    args = parser.parse_args()

    lc = LoanCalculator(args.principal,
                        args.interest,
                        args.periods,
                        args.payment)

    command = get_command(lc, args)
    command and command.execute() or print('Incorrect parameters')


if __name__ == '__main__':
    main()
