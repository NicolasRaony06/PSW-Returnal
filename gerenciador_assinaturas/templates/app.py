import __init__
from views.view import SubscriptionService
from models.database import engine, Subscription
from datetime import datetime
from decimal import Decimal

class UI:
    def __init__(self):
        self.subservice = SubscriptionService(engine)

    def add_sub(self):
        company = input('Company: ')
        site = input('Site: ')
        sub_date = datetime.strptime(input('Subscription Date: '), '%d/%m/%Y')
        value = Decimal(input('Value: '))

        subscription = Subscription(company=company, site=site, sub_date=sub_date, value=value)
        self.subservice.create(subscription)
        print('Done!')

    def remove_sub(self):
        options = self.subservice.list_all()
        for index, option in enumerate(options):
            print(f'[{index}] -> {option.company}')

        choice = int(input('Choose an option: '))
        self.subservice.delete(options[choice].id)
        print('Done!')

    def pay(self):
        options = self.subservice.list_all()
        for index, option in enumerate(options):
            print(f'[{index}] -> {option.company}')

        choice = int(input('Choose an option: '))
        self.subservice.pay(options[choice])
        print('Done!')

    def total_value(self):
        print(f"Your subscriptions total value is {self.subservice.total_value()}")

    def last_12_exp(self):
        self.subservice.generate_chart()

    def start(self):
        while True:
            print('''
                [1] -> Add Subscription
                [2] -> Remove Subscription
                [3] -> Pay Subcription
                [4] -> Total Value
                [5] -> Last 12 Expenses
                [6] -> Quit
            ''')

            choice = int(input('Choose an option: '))

            if choice == 1:
                self.add_sub()
            elif choice == 2:
                self.remove_sub()
            elif choice == 3:
                self.pay()
            elif choice == 4:
                self.total_value()
            elif choice == 5:
                self.subservice.generate_chart()
            else:
                break

if __name__ == '__main__':
    UI().start()