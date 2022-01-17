from sqlalchemy import Column, Integer, String
from config.db import Base


class UserModel(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    email = Column(String(100))
    password = Column(String(20))
    name = Column(String(100))
    descrip = Column(String(255))
