import math
import sys
from argparse import ArgumentParser
from sunau import Au_read


def input_arguments_handler():
    # Creating the parser object
    parser = ArgumentParser(description="Incorrect parameters")

    # Adding the optional command line arguments
    parser.add_argument("--type", type=str)
    parser.add_argument("--payment", type=float)
    parser.add_argument("--principal", type=float)
    parser.add_argument("--periods", type=int)
    parser.add_argument("--interest", type=float)

    args = parser.parse_args()
    #return args
    return args

def calculate_annuity_payment(principal, interest, periods): # Calculates a annuity payment
    return math.ceil(principal * ((interest * ((1 + interest) ** periods)) / (((1 + interest) ** periods) - 1)))

def calculate_loan_principal(payment, periods, interest): # Calculates loan principle
    return payment / ((interest * (1 + interest) ** periods) / ((1 + interest) ** periods - 1))

def calculate_interest_rate(interest): # Calculates nominal (monthly) interest rate
    return interest / (12 * 100)

def calculate_periods(payment, interest, principal): # Calculate number of payments / periods
    return math.ceil((math.log(payment / (payment - interest * principal)) / (math.log(1 + interest))))

def calculate_differentiated_payment(principal, interest, periods):
    all_payments = []
    for m in range(1, periods + 1, 1):
        all_payments.append(math.ceil((principal / periods) + interest * (principal - (principal * (m - 1)) / periods)))

    #overpayment = sum(all_payments) - principal
    return all_payments

def calculate_overpayment(all_payments, principal):
    return all_payments - principal

def month_to_years_convertor(months):
    if (months % 12) == 0:
        years = months // 12
        return f"{years} years"
    elif months > 12:
        years = months // 12
        months = months - (years * 12)
        return f"{years} years and {months} months"
    else:
        return f"{months}"

def output_handler():
    if args.type=="annuity" and args.principal and args.periods and args.interest: # Annuity payment
        if args.principal < 0 or args.periods < 0 or args.interest < 0:
            print("Incorrect parameters")
        else:
            interest = calculate_interest_rate(args.interest)
            result = calculate_annuity_payment(args.principal, interest, args.periods)
            print(f"Your monthly payment = {result}")
            print(f"Overpayment = {calculate_overpayment((result * args.periods), args.principal)}")
    elif args.type=="diff" and args.principal and args.periods and args.interest: # Differentiated payment
        if args.principal < 0 or args.periods < 0 or args.interest < 0:
            print("Incorrect parameters")
        else:
            interest = calculate_interest_rate(args.interest)
            result = calculate_differentiated_payment(args.principal, interest, args.periods)
            for payment in result:
                print(f"Month {result.index(payment) + 1}: payment is {payment}")
            print(f"Overpayment = {calculate_overpayment((sum(result)), args.principal)}")
    elif args.type=="annuity" and args.principal and args.payment and args.interest: # number of monthly payments
        if args.principal < 0 or args.payment < 0 or args.interest < 0:
            print("Incorrect parameters")
        else:
            interest = calculate_interest_rate(args.interest)
            number_of_months = calculate_periods(args.payment, interest, args.principal)
            num_of_months_int = month_to_years_convertor(number_of_months)
            print(f"It will take {num_of_months_int} to repay this loan!")
            print(f"Overpayment = {calculate_overpayment((number_of_months * args.payment), args.principal)}")
    elif args.type=="annuity" and args.payment and args.periods and args.interest: # Loan principal
        if args.payment < 0 or args.periods < 0 or args.interest < 0:
            print("Incorrect parameters")
        else:
            interest = calculate_interest_rate(args.interest)
            loan_principal = calculate_loan_principal(args.payment, args.periods, interest)
            print(f"Your loan principal = {loan_principal}!")
            print(f"Overpayment = {calculate_overpayment((args.payment * args.periods), loan_principal)}")
    else:
       print("Incorrect parameters")

args = input_arguments_handler()
output_handler()