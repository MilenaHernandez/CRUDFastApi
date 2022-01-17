from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

connect_args = {
    'user': 'mhernandez',
    'password': '1234',
    'database': 'crudfastapi',
    'host': 'localhost',
    'port': 5432
}
engine = create_engine('postgresql://', connect_args=connect_args)
conn = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
