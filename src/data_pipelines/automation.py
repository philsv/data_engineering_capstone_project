"""
This is the main program that automates the data pipeline.
"""

import os

import ibm_db  # type: ignore
import mysql.connector  # type: ignore
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

MYSQL_PW = str(os.getenv("MYSQL_PW"))
if MYSQL_PW is None:
    raise ValueError("MYSQL_PW is not set in environment variables")

DSN_DATABASE = str(os.getenv("DSN_DATABASE"))
if DSN_DATABASE is None:
    raise ValueError("DSN_DATABASE is not set in environment variables")

DSN_HOSTNAME = str(os.getenv("DSN_HOSTNAME"))
DSN_PORT = str(os.getenv("DSN_PORT"))
DSN_UID = str(os.getenv("DSN_UID"))
DSN_PWD = str(os.getenv("DSN_PWD"))


def mysql_connect() -> mysql.connector.connection.MySQLConnection:
    """
    Connect to MySQL database and return a cursor object.
    """
    connection = mysql.connector.connect(
        user="root",
        password=MYSQL_PW,
        host="127.0.0.1",
        database="sales",
    )
    if connection:
        print("Connected to MySQL")
    return connection  # type: ignore


def db2_connect() -> ibm_db.IBM_DBConnection:
    """
    Connect to DB2 database and return a cursor object.
    """
    dsn = (
        "DRIVER={0};"
        "DATABASE={1};"
        "HOSTNAME={2};"
        "PORT={3};"
        "PROTOCOL={4};"
        "UID={5};"
        "PWD={6};"
        "SECURITY={7};"
    ).format(
        "{IBM DB2 ODBC DRIVER}",
        DSN_DATABASE,
        DSN_HOSTNAME,
        DSN_PORT,
        "TCPIP",
        DSN_UID,
        DSN_PWD,
        "SSL",
    )

    connection = ibm_db.connect(dsn, "", "")
    if connection:
        print(f"Connected to DB2 database: {DSN_DATABASE} ")
        print(f"as user: {DSN_UID}")
        print(f"on host: {DSN_HOSTNAME}")
    return connection


def get_last_rowid() -> int:
    """
    Get the last rowid from the sales_data table in the sales database on the MySQL staging data warehouse.
    """
    connection = db2_connect()
    
    SQL = "SELECT MAX(rowid) FROM sales_data"
    stmt = ibm_db.exec_immediate(connection, SQL)
    tuple = ibm_db.fetch_tuple(stmt)
    
    if not tuple:
        raise ValueError("No records in the sales_data table")
    return tuple[0]  # row_id


def get_latest_records(rowid: int) -> list:
    """
    Get the latest records from the sales_data table in the sales database on the MySQL staging data warehouse.
    """
    connection = mysql_connect()
    cursor = connection.cursor()
    
    if not rowid:
        SQL = "SELECT * FROM sales_data"
        
    SQL = "SELECT * FROM sales_data WHERE rowid >" + str(rowid)
    cursor.execute(SQL)
    return cursor.fetchall()  # last_row_id


def insert_records(records: list) -> None:
    """
    Insert records into the sales_data table in the sales database on the DB2 production data warehouse.
    """
    connection = db2_connect()
    
    if len(records) > 0:
        SQL = "INSERT INTO sales_data(rowid, product_id, customer_id, quantity) VALUES(?,?,?,?);"
        stmt = ibm_db.prepare(connection, SQL)
        for row in records:
            ibm_db.execute(stmt, row)
    return None


if __name__ == "__main__":
    last_row_id = get_last_rowid()
    print("Last row id on production datawarehouse = ", last_row_id)

    new_records = get_latest_records(last_row_id)
    print("New rows on staging datawarehouse = ", len(new_records))

    insert_records(new_records)
    print("New rows inserted into production datawarehouse = ", len(new_records))

    # disconnect from mysql warehouse
    mysql_connection = mysql_connect()
    mysql_connection.close()
    
    # disconnect from DB2 or PostgreSql data warehouse
    ibm_connection = db2_connect()
    ibm_db.close(ibm_connection)
