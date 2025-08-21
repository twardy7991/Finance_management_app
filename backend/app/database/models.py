from datetime import date, datetime
from typing import List
from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, VARCHAR, TEXT, DATE, NUMERIC, INTEGER, ARRAY, JSON, TIMESTAMP   

from app.db import Base

### CLASS MAPPING THE users TABLE ###

class User(Base):

    __tablename__ = 'users'
    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] =  mapped_column(VARCHAR(100), nullable=False)
    surname: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    telephone: Mapped[str] = mapped_column(VARCHAR(20), nullable=True)
    address: Mapped[str] = mapped_column(TEXT(), nullable=True)
    
    credential: Mapped['Credential'] = relationship(back_populates="user")
    operations: Mapped[List['Operation']] = relationship(back_populates="user")
    
    # needed for testing
    def is_equal(self, other) -> bool:
        return (
            self.name == other.name and 
            self.surname == other.surname and 
            self.telephone == other.telephone and 
            self.address == other.address
        )    
        
    def __repr__(self):
        
        return f'''User(id={self.user_id})" 
                    name={self.name}
                    surname={self.surname}
                    telephone={self.telephone}
                    address={self.address}
            '''
    
### CLASS MAPPING THE credentials TABLE ###  

class Credential(Base):
    
    __tablename__ = 'credentials'
    credential_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    username: Mapped[str] = mapped_column(VARCHAR(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(VARCHAR(77), unique=True, nullable=False)
    
    user: Mapped['User'] = relationship(back_populates="credential")
        
        
    # needed for testing
    def is_equal(self, other, context=None) -> bool:
        return (
            self.user_id == other.user_id and
            self.username == other.username and 
            (context.verify(other.password, self.password) if context else other.password == self.password)
        )      
    
    def __repr__(self):
        return f'''Credential(credential_id={self.credential_id}, 
                    user_id={self.user_id}, 
                    username='{self.username}'
                    password='{self.password}')'''

### CLASS MAPPING THE financial_operations TABLE ###

class Operation(Base):
    
    __tablename__ = 'financial_operations'
    operation_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    operation_date: Mapped[date] = mapped_column(DATE, nullable=False)
    category: Mapped[str] = mapped_column(VARCHAR(50), nullable=True)
    description: Mapped[str] = mapped_column(TEXT(), nullable=True)
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
                    
### CLASS MAPPING THE sessions TABLE ###

from app.db import Base_auth

class UserSession(Base_auth):
    
    __tablename__ = 'sessions'
    id : Mapped[int] = mapped_column(primary_key=True)
    session_id : Mapped[str] = mapped_column(VARCHAR(100))
    user_id : Mapped[int] = mapped_column(INTEGER)
    created_at : Mapped[datetime] = mapped_column(TIMESTAMP)
    expires_at : Mapped[datetime] = mapped_column(TIMESTAMP)
    last_active : Mapped[datetime] = mapped_column(TIMESTAMP)
    roles : Mapped[List] = mapped_column(ARRAY(TEXT))
    session_metadata : Mapped[dict] = mapped_column(JSON) 
    
    def is_equal(self, other) -> bool:
        return (
            self.session_id == other.session_id and
            self.user_id == other.user_id and
            self.created_at == other.created_at and
            self.expires_at == other.expires_at and
            self.last_active == other.last_active and
            self.roles == other.roles and 
            self.session_metadata == other.session_metadata
        )  
    
    def __repr__(self):
        return f'''UserSession(
                    id={self.id}
                    session_id={self.session_id}, 
                    user_id={self.user_id}, 
                    created_at={self.created_at}, 
                    expires_at={self.expires_at}, 
                    last_active={self.last_active}, 
                    roles={self.roles},
                    session_metadata={self.session_metadata})'''