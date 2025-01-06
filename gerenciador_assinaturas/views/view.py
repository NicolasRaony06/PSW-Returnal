import __init__
from models.database import engine

class SubscriptionService:
    def __init__(self, engine):
        self.engine = engine

subservice = SubscriptionService(engine)