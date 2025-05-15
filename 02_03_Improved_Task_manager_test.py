import pytest
import mysql.connector
from test_init import create_test_tables

@pytest.fixture(scope="session", autouse=True)
def vytvoreni_test_db():
    create_test_tables()

@pytest.fixture(scope="module")
def db_connection():
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "1111",
        database = "taskmanager_test"
    )
    yield conn
    conn.close()