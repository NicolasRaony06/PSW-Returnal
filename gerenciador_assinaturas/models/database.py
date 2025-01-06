from sqlmodel import SQLModel, create_engine
from .model import *

SQL_FILE_NAME = 'database.db'
SQL_URL = f'sqlite:///{SQL_FILE_NAME}'

engine = create_engine(SQL_URL, echo=True)

if __name__ == '__main__':
    SQLModel.metadata.create_all(engine)