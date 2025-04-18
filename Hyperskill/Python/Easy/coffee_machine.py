BUY = "buy"
FILL = "fill"
TAKE = "take"
REMAINING = "remaining"
EXIT = "exit"


class CoffeeMachine:

    supplies = {'water': 400, 'milk': 540, 'coffee beans': 120, 'disposable cups': 9, 'money': 550}
    coffee_menu = {
        "1": {"water": 250, "milk": 0, "coffee beans": 16, "disposable cups": 1, "money": -4},
        "2": {"water": 350, "milk": 75, "coffee beans": 20, "disposable cups": 1, "money": -7},
        "3": {"water": 200, "milk": 100, "coffee beans": 12, "disposable cups": 1, "money": -6},
        }

    def buy_coffee(self):
        while True:
            coffee_type = input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu: ")
            if coffee_type in {"1", "2", "3"}:
                for resource in self.coffee_menu[coffee_type]:
                    if self.supplies[resource] - self.coffee_menu[coffee_type][resource] < 0:
                        print(f"Sorry, not enough {resource}!")
                        break
                    else:
                        self.supplies[resource] -= self.coffee_menu[coffee_type][resource]
                print("I have enough resources, making you a coffee!")
                break
            elif coffee_type == "back":
                break
            else:
                print("Choose one of available options only")

    def fill_supplies(self):
        self.supplies['water'] += int(input("Write how many ml of water do you want to add: "))
        self.supplies['milk'] += int(input("Write how many ml of milk do you want to add: "))
        self.supplies['coffee beans'] += int(input("Write how many grams of coffee beans do you want to add: "))
        self.supplies['disposable cups'] += int(input("Write how many disposable cups of coffee do you want to add: "))

    def take_money(self):
        print(f"I gave you {self.supplies['money']}")
        self.supplies['money'] = 0

    def view_supplies(self, supplies):
        print('The coffee machine has: ')
        for value, key in supplies.items():
            print(key, 'of', value)

    def main(self):
        while True:
            action = input("Write action (buy, fill, take, remaining, exit): ")
            if action in {BUY, FILL, TAKE, REMAINING, EXIT}:
                if action == BUY:
                    self.buy_coffee()
                elif action == FILL:
                    self.fill_supplies()
                elif action == TAKE:
                    self.take_money()
                elif action == REMAINING:
                    self.view_supplies(CoffeeMachine.supplies)
                else:
                    break
            else:
                print("Choose one of available options only")


coffee_machine = CoffeeMachine()
coffee_machine.main()
