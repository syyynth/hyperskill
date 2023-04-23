import argparse
import math

args = argparse.ArgumentParser(
    description='Loan Calculator',
    allow_abbrev=False
)
args.add_argument('--type', choices=['annuity', 'diff'])
args.add_argument('--payment', type=float)
args.add_argument('--principal', type=float)
args.add_argument('--interest', type=float)
args.add_argument('--periods', type=float)

commands = args.parse_args()
payment = commands.payment
principal = commands.principal
interest = commands.interest
periods = commands.periods


def fmonths(months):
    y, m = divmod(months, 12)
    out = ''
    if y:
        out += f'{y} year{(y > 1) * "s"}'
    if m:
        out += f' and {m} month{(m > 1) * "s"}'
    return out


def get_months(lp, mp, li):
    months = math.log(mp / (mp - li / 1200 * lp), 1 + li / 1200)
    print(f'It will take {fmonths(math.ceil(months))} to repay loan!')
    print(f'Overpayment = {mp * math.ceil(months) - lp}')


def get_monthly_payment(lp, np, li):
    tmp = (1 + li / 1200) ** np
    mp = math.ceil(lp * ((li / 1200 * tmp) / (tmp - 1)))
    print(f'Your monthly payment = {mp}!')

def get_loan_principal(ap, np, li):
    tmp = (1 + li / 1200) ** np
    lp = ap / (li / 1200 * tmp / (tmp - 1))

    print(f'Your loan principal = {math.ceil(lp)}!')


def get_diff_payment():
    total = 0
    for n in range(1, int(periods) + 1):
        di = math.ceil(
            principal / periods + (interest / 1200) * (principal - principal * (n - 1) / periods)
        )
        total += di
        print(f'Month {n}: payment is {di}')
    print(f'Overpayment = {total - principal}')


if commands.type == 'annuity':
    if payment and principal and interest and periods:
        print('Incorrect parameters')
    elif principal and payment and interest:
        get_months(principal, payment, interest)
    elif principal and periods and interest:
        get_monthly_payment(principal, periods, interest)
    elif payment and periods and interest:
        get_loan_principal(payment, periods, interest)
    else:
        print('Incorrect parameters')
elif commands.type == 'diff':
    if principal and periods and interest:
        get_diff_payment()
    else:
        print('Incorrect parameters')
else:
    print('Incorrect parameters')
