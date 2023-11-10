"""
Script to connect to DB2 database and create a table and insert data into it.
"""

import os

import ibm_db  # type: ignore
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

if os.getenv("DSN_DATABASE") is None:
    raise ValueError("DSN_DATABASE is not set in environment variables")

if __name__ == "__main__":
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
        os.getenv("DSN_DATABASE"),
        os.getenv("DSN_HOSTNAME"),
        os.getenv("DSN_PORT"),
        "TCPIP",
        os.getenv("DSN_UID"),
        os.getenv("DSN_PWD"),
        "SSL",
    )

    conn = ibm_db.connect(dsn, "", "")
    print(
        "Connected to database: ",
        os.getenv("DSN_DATABASE"),
        "as user: ",
        os.getenv("DSN_UID"),
        "on host: ",
        os.getenv("DSN_HOSTNAME"),
    )
    SQL = """
    CREATE TABLE IF NOT EXISTS products
    (
        rowid INTEGER PRIMARY KEY NOT NULL,
        product varchar(255) NOT NULL,
        category varchar(255) NOT NULL
    )
    """
    create_table = ibm_db.exec_immediate(conn, SQL)
    print("Table created")

    SQL = "INSERT INTO products(rowid,product,category)  VALUES(?,?,?);"
    stmt = ibm_db.prepare(conn, SQL)
    row1 = (1, "Television", "Electronics")
    ibm_db.execute(stmt, row1)

    row2 = (2, "Laptop", "Electronics")
    ibm_db.execute(stmt, row2)

    row3 = (3, "Mobile", "Electronics")
    ibm_db.execute(stmt, row3)

    SQL = "SELECT * FROM products"
    stmt = ibm_db.exec_immediate(conn, SQL)
    tuple = ibm_db.fetch_tuple(stmt)
    while tuple != False:
        print(tuple)
        tuple = ibm_db.fetch_tuple(stmt)
    ibm_db.close(conn)
