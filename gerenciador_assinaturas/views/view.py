import __init__
from sqlmodel import Session, select
from models.database import engine
from models.model import Subscription, Payment
from datetime import date

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

subservice = SubscriptionService(engine)

print(subservice.total_value()) # via de teste

