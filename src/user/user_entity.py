from src.database.mysql.mysql_config import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cpf = Column(String(14), nullable=False)
    nome = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(300), nullable=False)
    role = Column(String(50), nullable=False, default='user')