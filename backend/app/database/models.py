from app.db import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, VARCHAR, Text, DATE, NUMERIC
from datetime import date
from typing import List
from decimal import Decimal

class User(Base):

    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] =  mapped_column(VARCHAR(100), nullable=False)
    surname: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    telephone: Mapped[str] = mapped_column(VARCHAR(20), nullable=True)
    address: Mapped[str] = mapped_column(Text(), nullable=True)
    
    credential: Mapped['Credential'] = relationship(back_populates="user")
    operations: Mapped[List['Operation']] = relationship(back_populates="user")
        
    def __repr__(self):
        
        return f'''User(id={self.id})" 
                    name={self.name}
                    surname={self.surname}
                    telephone={self.telephone}
                    address={self.address}
            '''
            
class Credential(Base):
    
    __tablename__ = 'credentials'
    credential_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    username: Mapped[str] = mapped_column(VARCHAR(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(VARCHAR(50), unique=True, nullable=False)
    
    user: Mapped['User'] = relationship(back_populates="credential")
        
    def __repr__(self):
        return f'''Credential(credential_id={self.credential_id}, 
                    user_id={self.user_id}, 
                    username='{self.username}')"'''

class Operation(Base):
    
    __tablename__ = 'financial_operations'
    operation_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    operation_date: Mapped[date] = mapped_column(DATE, nullable=False)
    category: Mapped[str] = mapped_column(VARCHAR(50), nullable=True)
    description: Mapped[str] = mapped_column(Text(), nullable=True)
    value: Mapped[Decimal] = mapped_column(NUMERIC(12,2, asdecimal=True), nullable=False)
    currency: Mapped[str] = mapped_column(VARCHAR(10), nullable=False)  
    
    user: Mapped['User'] = relationship(back_populates="operations")
    
    # needed for testing, to ignore the operation_id
    def is_equal(self, other) -> bool:
        return (
            self.user_id == other.user_id and
            self.operation_date == other.operation_date and
            self.category == other.category and
            self.description == other.description and
            self.value == other.value and
            self.currency == other.currency
        )    
        
    def __repr__(self):
        return f'''Operation(operation_id={self.operation_id}, 
                    user_id={self.user_id}, 
                    operation_date='{self.operation_date}', 
                    category='{self.category}', 
                    description='{self.description}', 
                    value={self.value}, 
                    currency='{self.currency}')'''