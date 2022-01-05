from random import choice

guest_dict = {}

try:
    guest_num = int(input('Enter the number of friends joining (including you):\n'))
except:
    print('You must enter a single number')

if guest_num < 1:
    print('No one is joining for the party')
else:
    i = 0
    print("Enter the name of every friend (including you), each on a new line:")
    while i < guest_num:
        try:
            guest = str(input())  
        except:
            print('You must enter a name, dumbo')
        else:
            guest_dict[guest] = 0
            i += 1
    total_bill = int(input('Enter the total bill value:\n'))
    
    lucky_prompt = input('Do you want to use the "Who is lucky?" feature? Write Yes/No:\n')
    if lucky_prompt == 'Yes':
        lucky_one = choice(list(guest_dict.keys()))
        print(f'{lucky_one} is the lucky one!')
        per_person_bill = round(total_bill / (guest_num - 1), 2)
        guest_dict = {key: per_person_bill for key in guest_dict}
        guest_dict[lucky_one] = 0
    else:
        print('No one is going to be lucky')
        per_person_bill = round(total_bill / guest_num, 2)
        guest_dict = {key: per_person_bill for key in guest_dict}   
    print(guest_dict)