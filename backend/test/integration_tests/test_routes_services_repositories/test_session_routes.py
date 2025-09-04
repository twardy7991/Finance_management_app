from fastapi.testclient import TestClient
from fastapi import status

from app.main import app
from app.containers import Container
import pytest
from fastapi.testclient import TestClient

from sqlalchemy.orm import sessionmaker
from sqlalchemy import text


from sqlalchemy import Transaction, Connection
import pytest
from app.db import Database
import yaml
from contextlib import contextmanager

from app.db import Database
from app.auth.auth import AuthenticationTools
from app.services.utils.unit import UnitOfWorkUser, UnitOfWorkRegistration, UnitOfWorkCredential, UnitOfWorkOperation, UnitOfWorkSession
from app.services import SessionService, DataService, AuthenticationService, UserService


# @pytest.fixture(autouse=True)
# def clean_db(db):
#     yield
#     with db.create_connection() as connection:
#         connection.execute(text("DISCARD ALL"))
#         try:
#             with open("test_database/clean_db/clean_db_test.sql") as f:
#                 sql = f.read()
#             connection.execute(text(sql))
#             connection.commit()
#         finally:
#             connection.close()

# @pytest.fixture(autouse=True)
# def clean_db_auth(db_auth):
#     yield
#     with db_auth.create_connection() as connection:
#         connection.execute(text("DISCARD ALL"))
#         try:
#             with open("test_database/clean_db/clean_db_auth_test.sql") as f:
#                 sql = f.read()
#             connection.execute(text(sql))
#             connection.commit()
#         finally:
#             connection.close()


# @pytest.fixture
# def client():
#     yield TestClient(app)

# def test_register_login_user(client : TestClient):
    
#     register_request = {
#     "username" : "user3",
#     "password" : "password2",
#     "name" : "Jose",
#     "surname" : "Inverio",
#     "telephone" : "123456789",
#     "address" : "St. Michael street, 15/62 Warsaw"
#     }
    
#     response = client.post("/register", json=register_request)
    
#     assert response.status_code == status.HTTP_201_CREATED

#     login_request = {
#     "username" : "user3",
#     "password" : "password2"
#     }

#     response = client.post("/login", json=login_request)

#     assert response.status_code == status.HTTP_200_OK
    
#     assert isinstance(response.content, bytes)
    
#     #does not work for some reason
#     #assert len(response.content) == TOKEN_LEN
    
# def test_login_user(client : TestClient):
    
#     login_request = {
#     "username" : "admin",
#     "password" : "admin"
#     }

#     session_id = 'SCKXWjK7uIgKefL3tY8C862ny-t07I1Mn5Gx5DnwfPA'
    
#     response = client.post("/login", json=login_request)

#     assert response.status_code == status.HTTP_200_OK
    
#     assert isinstance(response.content, bytes)
