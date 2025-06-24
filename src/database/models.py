from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, BigInteger, Date, func, TEXT, ForeignKey, DateTime


class Base(DeclarativeBase):
    pass


class Client(Base):
    __tablename__ = "clients"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    username = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    date_create = Column(DateTime)

    def __str__(self):
        return f"Клиент: {self.username} | {self.id} | {self.is_paid}"


class Messages(Base):
    __tablename__ = "messages"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    message = Column(TEXT)
    from_user = Column(ForeignKey("clients.id"))
    to_user = Column(ForeignKey("clients.id"))
    date_create = Column(DateTime)
