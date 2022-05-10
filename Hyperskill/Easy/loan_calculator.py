from argparse import ArgumentParser
import math


PER_MONTH_PAYMENT = 'Month {month}: payment is {diff}'
MONTHLY_PAYMENT = 'Your monthly payment = {annuity}!'
OVERPAYMENT = 'Overpayment = {overpayment}'
LOAN_PRINCIPAL = 'Your loan principal = {principal}!'
PERIODS = "It will take {periods} to repay this loan!"


parser = ArgumentParser(description='Enter all necessary arguments '
                        'for calculations')

parser.add_argument('-t', '--type', choices=['diff', 'annuity'],
                    help='Choose one type of repayment out of the provided '
                    'options diff for differentiated payments or '
                    'annuity for annuity payments')
parser.add_argument('-li', '--interest', type=float,
                    help='Enter the loan interest')
parser.add_argument('-lp', '--principal', type=int,
                    help='Enter the loan principal')
parser.add_argument('-ap', '--payment', type=int,
                    help='Enter the montly payment (do not use with '
                    'differentiated repayment type)')
parser.add_argument('-np', '--periods', type=int,
                    help='Enter the number of monthly payments')


def quantifier(*args):
    """Prepare correct string representation of periods."""
    if isinstance(args[0], str):
        prefix = 's' if args[1] > 1 else ''
        return f"{args[1]} {args[0]}{prefix}"
    return f"{quantifier('year', args[0])} and {quantifier('month', args[1])}"


def calc_periods(_lp, _ap, _li):
    """Calculate the number of periods you gonna be slaving."""
    return math.log((_ap / (_ap - _li * _lp)), 1 + _li)


def calc_annuity(_lp, _np, _li):
    """Calculate the annual payment for the period."""
    return math.ceil(_lp * (_li * (1 + _li) ** _np / ((1 + _li) ** _np - 1)))


def calc_diff(_lp, _np, _li, _m):
    """Calculate the differentiate payment for the current month."""
    return math.ceil(_lp / _np + _li * (_lp - _lp * (_m - 1) / _np))


def calc_overpay(_lp, _ps):
    """Calculate how much of a fool you are."""
    return _ps - _lp


def calc_principal(_ap, _np, _li):
    """Calculate the loan principal."""
    return math.ceil(_ap / (_li * (1 + _li) ** _np / ((1 + _li) ** _np - 1)))


def diff_overpayment(interest, principal, periods):
    pay_sum = 0
    for month in range(1, periods + 1):
        diff = calc_diff(principal, periods, interest / 1200, month)
        pay_sum += diff
        print(PER_MONTH_PAYMENT.format(month=month, diff=diff))
    return calc_overpay(principal, pay_sum)


def annuity_overpayment(interest, principal, periods):
    annuity = calc_annuity(principal, periods, interest / 1200)
    print(MONTHLY_PAYMENT.format(annuity=annuity))
    return calc_overpay(principal, annuity * periods)


def principal(interest, payment, periods):
    principal = calc_principal(payment, periods, interest / 1200)
    print(LOAN_PRINCIPAL.format(principal=principal))
    return calc_overpay(principal, payment * periods)


def periods(interest, payment, principal):
    periods = math.ceil(
        calc_periods(principal, payment, interest / 1200)
        )
    if periods < 12:
        periods_string = quantifier('month', periods)
    elif periods % 12 == 0:
        periods_string = quantifier('year', periods // 12)
    else:
        periods_string = quantifier(periods // 12, periods % 12)
    print(PERIODS.format(periods=periods_string))
    return calc_overpay(principal, payment * periods)


OPERATIONS = {
    'diff': {
        hash(('interest', 'principal', 'periods')): diff_overpayment
    },
    'annuity': {
        hash(('interest', 'principal', 'periods')): annuity_overpayment,
        hash(('interest', 'payment', 'periods')): principal,
        hash(('interest', 'principal', 'payment')): periods
    },
}


def loan_calculator(type=None, interest=None, principal=None, payment=None, periods=None):
    """
    Program's entry point

    Processes keyword arguments:

    @param type: type of payment
    @param principal: string the pattern is searched in
    @param payment: string the pattern is searched in
    @param periods: string the pattern is searched in
    @param interest: string the pattern is searched in
    @return: none

    >>> loan_calculator(**{
    ...    'type': 'annuity',
    ...    'payment': 8722,
    ...    'periods': 120,
    ...    'interest': 5.6
    ... })
    Your loan principal = 800019!
    Overpayment = 246621
    >>> loan_calculator(**{
    ...    'type': 'annuity',
    ...    'principal': 500000,
    ...    'payment': 23000,
    ...    'interest': 7.8
    ... })
    It will take 2 years to repay this loan!
    Overpayment = 52000
    >>> loan_calculator(**{
    ...    'type': 'diff',
    ...    'principal': 1000000,
    ...    'payment': 104000
    ... })
    Incorrect parameters
    """

    passed_args = {
        arg: value for arg, value in locals().items() if value != None and arg != 'type'
    }
    signature = hash(tuple(passed_args.keys()))
    try:
        func = OPERATIONS[type][signature]
    except KeyError:
        print('Incorrect parameters')
    else:
        overpayment = func(**passed_args)
        print(OVERPAYMENT.format(overpayment=overpayment))


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL)
    loan_calculator(**vars(parser.parse_args()))
