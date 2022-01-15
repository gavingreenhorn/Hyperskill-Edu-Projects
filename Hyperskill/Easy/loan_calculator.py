import math
import argparse

parser = argparse.ArgumentParser(description="Enter all necessary arguments for calculations")

parser.add_argument('-t', '--type', choices=['diff', 'annuity'],
                    help='Choose one type of repayment out of the provided options diff for differentiated payments or annuity for annuity payments')
parser.add_argument('-lp', '--principal', type=int,
                    help='Enter the loan principal')
parser.add_argument('-ap', '--payment', type=int,
                   help='Enther the montly payment (do not use with differentiated repayment type)')
parser.add_argument('-np', '--periods', type=int,
                   help='Enter the number of monthly payments')
parser.add_argument('-li', '--interest', type=float,
                   help='Enter the loan interest')

args = parser.parse_args()


def calc_periods(_lp, _ap, _li):
    '''Calculate the number of months you gonna be slaving'''
    return math.log((_ap / (_ap - _li * _lp)), 1 + _li)
    
    
def calc_annuity(_lp, _np, _li):
    '''Calculate the annual payment for the period'''
    return math.ceil(_lp * (_li * (1 + _li) ** _np / ((1 + _li) ** _np - 1)))


def calc_diff(_lp, _np, _li, _m):
    '''Calculate the differentiate payment for the current month'''
    return math.ceil(_lp / _np + _li * ( _lp - _lp * (_m - 1) / _np ))


def calc_overpay(_lp, _ps):
    '''Calculate how much of a fool you are'''
    return _ps - _lp
   
    
def calc_principal(_ap, _np, _li):
    '''Calculate the loan principal'''
    return math.ceil(_ap / (_li * (1 + _li) ** _np / ((1 + _li) ** _np - 1)))

passed_args = [arg for arg in vars(args).values() if arg is not None]

if len(passed_args) == 4 and 0 <= min([x for x in passed_args if isinstance(x, int) or isinstance(x, float)]):
    print([x for x in vars(args) if x is not None])
    if args.type == 'diff' and not args.payment:
        pay_sum = 0
        for month in range(1, args.periods + 1):
            diff = calc_diff(args.principal, args.periods, args.interest / 1200, month)
            pay_sum += diff
            print(f'Month {month}: payment is {diff}')
        print(f'\nOverpayment = {calc_overpay(args.principal, pay_sum)}')
    elif args.type == 'annuity' and not args.payment:
        annuity = calc_annuity(args.principal, args.periods, args.interest / 1200)
        print(f'Your monthly payment = {annuity}!')
        print(f'Overpayment = {calc_overpay(args.principal, annuity * args.periods)}')
    elif args.type == 'annuity' and args.interest and args.payment and args.periods:
        principal = calc_principal(args.payment, args.periods, args.interest / 1200)
        print(f'Your loan principal = {principal}!')
        print(f'Overpayment = {calc_overpay(principal, args.payment * args.periods)}')
    elif args.type == 'annuity' and args.principal and args.payment and args.interest:
        periods = math.ceil(calc_periods(args.principal, args.payment, args.interest / 1200))
        if periods < 12:
            print(f"It will take {periods} month{'s' if periods > 1 else ''} to repay this loan")
        elif periods % 12 == 0:
            print(f"It will take {periods // 12} year{'s' if periods >= 24 else ''} to repay this loan")
        else:
            months = periods % 12
            qtr = 's' if periods > 1 else ''
            print(f"It will take {periods // 12} year{'s' if periods > 1 else ''} and {months} month{qtr} to repay this loan")
        print(f'Overpayment = {calc_overpay(args.principal, args.payment * periods)}')
else:
    print('Incorrect parameters')