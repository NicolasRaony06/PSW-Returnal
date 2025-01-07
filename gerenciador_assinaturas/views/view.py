from sqlmodel import Session, select
from models.database import engine
from models.model import Subscription, Payment
from datetime import date, datetime

class SubscriptionService:
    def __init__(self, engine):
        self.engine = engine

    def create(self, subscription: Subscription):
        with Session(self.engine) as session:
            session.add(subscription)
            session.commit()
            return subscription
    
    def list_all(self):
        with Session(self.engine) as session:
            statement = select(Subscription)
            results = session.exec(statement).all()
        return results
    
    def delete(self, id):
        with Session(self.engine) as session:
            statement = select(Subscription).where(Subscription.id==id)
            result = session.exec(statement).one()

            pay_statement = select(Payment).where(Payment.subscription_id == id)

            results = session.exec(pay_statement).all()

            for pay_result in results:
                session.delete(pay_result)

            session.delete(result)
            session.commit()
    
    def _has_paid(self, results):
        for result in results:
            if result.date.month == date.today().month:
                return True
        return False

    def pay(self, subscription: Subscription):
        with Session(self.engine) as session:
            statement = select(Payment).join(Subscription).where(Subscription.company==subscription.company)
            results = session.exec(statement).all()

            if self._has_paid(results):
                question = input('This subscription has been paid for this month. Do you wish to repay it? Y or N: ')

                if question.upper() == 'Y':
                    return

            pay = Payment(subscription_id=subscription.id, date=date.today())
            session.add(pay)
            session.commit()

    def total_value(self):
        with Session(self.engine) as session:
            statement = select(Subscription)
            results = session.exec(statement).all()

        total = 0
        for result in results:
            total += result.value

        return float(total)
    
    def _get_last_12_months(self):
        today = datetime.now()  
        year = today.year
        month = today.month

        last_12_months = []
        for _ in range(12):
            last_12_months.append((month, year))
            month -= 1
            if month == 0:
                month = 12
                year -= 1

        return last_12_months[::-1]
    
    def _get_values_for_month(self, last_12_months):
        with Session(self.engine) as session:
            statement = select(Payment)
            results = session.exec(statement).all()

            value_for_month = []
            for i in last_12_months:
                month_value = 0
                for result in results:
                    if result.date.month == i[0] and result.date.year == i[1]:
                        month_value += float(result.subscription.value)

                value_for_month.append(month_value)

        return value_for_month
    
    def generate_chart(self):
        last_12_months = self._get_last_12_months()
        value_for_month = self._get_values_for_month(last_12_months)

        last_12_months = list(map(lambda x: x[0],self._get_last_12_months()))

        import matplotlib.pyplot as plt
        
        plt.plot(last_12_months, value_for_month)
        plt.show()
