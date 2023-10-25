from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker


class Base(DeclarativeBase):
    pass


db_path = '/events.db'
engine = create_engine(f'sqlite://{db_path}', echo=True)
Session = sessionmaker(bind=engine)
