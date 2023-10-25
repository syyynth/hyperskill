import argparse
import math
from typing import Any

from commands import AnnuityPaymentCommand, AnnuityPeriodCommand, AnnuityPrincipalCommand, DifferentiatedPaymentsCommand

parser = argparse.ArgumentParser(
    description='Loan Calculator',
    allow_abbrev=False
)
parser.add_argument('--type', type=str)
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


def exists_and_positive(value):
    return value and value > 0


def all_exists_and_positive(*values):
    return all(exists_and_positive(value) for value in values)


def get_command(calculator, commands) -> Any:
    command_map = {
        'annuity': [(AnnuityPeriodCommand, (calculator.principal, calculator.payment, calculator.interest)),
                    (AnnuityPaymentCommand, (calculator.principal, calculator.periods, calculator.interest)),
                    (AnnuityPrincipalCommand, (calculator.payment, calculator.periods, calculator.interest))],
        'diff': [(DifferentiatedPaymentsCommand, (calculator.principal, calculator.periods, calculator.interest))]
    }

    for command_class, parameters in command_map.get(commands.type, ()):
        if all_exists_and_positive(*parameters):
            return command_class(calculator)


def main() -> None:
    args = parser.parse_args()

    lc = LoanCalculator(args.principal,
                        args.interest,
                        args.periods,
                        args.payment)

    command = get_command(lc, args)
    if command:
        command.execute()
    else:
        print('Incorrect parameters')


if __name__ == '__main__':
    main()
