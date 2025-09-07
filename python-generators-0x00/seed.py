import pymysql
from mysql.connector import errorcode
import csv
import uuid

def connect_db():
    """Connects to the MySQL server (without selecting a DB)."""
    try:
        connection = pymysql.connect(
            host="localhost",
            user="alx_user",      # change if needed
            password="alx_pass",  # change if needed
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return connection
    except Exception as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    """Creates the ALX_prodev database if it does not exist."""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev ready.")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    finally:
        cursor.close()
        
def connect_to_prodev():
    """Connects directly to the ALX_prodev database."""
    try:
        connection = pymysql.connect(
            host="localhost",
            user="alx_user",
            password="alx_pass",
            database="ALX_prodev",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return connection
    except Exception as err:
        print(f"Error: {err}")
        return None

def create_table(connection):
    """Creates the user_data table if it does not exist."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        age DECIMAL NOT NULL,
        INDEX (user_id)
    )
    """
    cursor = connection.cursor()
    try:
        cursor.execute(create_table_query)
        print("Table user_data is ready.")
    except mysql.connector.Error as err:
        print(f"Failed creating table: {err}")
    finally:
        cursor.close()

def insert_data(connection, data):
    """Inserts data into user_data table if not exists."""
    insert_query = """
    INSERT IGNORE INTO user_data (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    """
    cursor = connection.cursor()
    try:
        cursor.executemany(insert_query, data)
        connection.commit()
        print(f"Inserted {cursor.rowcount} rows.")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    finally:
        cursor.close()

def load_csv_data(csv_file):
    """Loads data from user_data.csv"""
    data = []
    with open(csv_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_id = str(uuid.uuid4())
            name = row["name"]
            email = row["email"]
            age = row["age"]
            data.append((user_id, name, email, age))
    return data
