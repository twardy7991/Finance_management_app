from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, VARCHAR, Text, DATE, NUMERIC
from datetime import date
from typing import List
from app.db import SQLconnection

connection = SQLconnection()
Base = connection.Base

class User(Base):

    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] =  mapped_column(VARCHAR(100), nullable=False)
    surname: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    telephone: Mapped[str] = mapped_column(VARCHAR(20), nullable=True)
    address: Mapped[str] = mapped_column(Text(), nullable=True)
    
    credential: Mapped['Credential'] = relationship(back_populates="user")
    operations: Mapped[List['Operation']] = relationship(back_populates="user")
    
    def __init__(self, name, surname, telephone, address):

        self.name = name
        self.surname = surname
        self.telephone = telephone
        self.address = address

class Credential(Base):
    
    __tablename__ = 'credentials'
    credential_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    username: Mapped[str] = mapped_column(VARCHAR(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(VARCHAR(50), unique=True, nullable=False)
    
    user: Mapped['User'] = relationship(back_populates="credential")

    def __init__(self, user_id, username, password):

        self.user_id = user_id
        self.username = username
        self.password = password

class Operation(Base):
    
    __tablename__ = 'financial_operations'
    operation_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    operation_date: Mapped[date] = mapped_column(DATE, nullable=False)
    category: Mapped[str] = mapped_column(VARCHAR(50), nullable=True)
    description: Mapped[str] = mapped_column(Text(), nullable=True)
    value: Mapped[int] = mapped_column(NUMERIC(12,2), nullable=False)
    currency: Mapped[str] = mapped_column(VARCHAR(10), nullable=False)  
    
    user: Mapped['User'] = relationship(back_populates="operations")
    
    def __init__(self, user_id, operation_date, category, description, value, currency):

        self.user_id = user_id
        self.operation_date = operation_date
        self.category = category
        self.description = description
        self.value = value
        self.currency = currency