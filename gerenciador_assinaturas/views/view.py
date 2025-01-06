import __init__
from sqlmodel import Session, select
from models.database import engine
from models.model import Subscription
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

subservice = SubscriptionService(engine)

#subscription = Subscription(company='Amazon', site='primevideo.com', sub_date=date.today(), value=19)

#subservice.create(subscription)

print(subservice.list_all())