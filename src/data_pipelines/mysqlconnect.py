"""
Simple script to connect to MySQL database and create a table and insert data.
"""

import os

import mysql.connector  # type: ignore
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

MYSQL_PW = str(os.getenv("MYSQL_PW"))
if MYSQL_PW is None:
    raise ValueError("MYSQL_PW is not set in environment variables")

if __name__ == "__main__":
    connection = mysql.connector.connect(
        user="root",
        password=MYSQL_PW,
        host="127.0.0.1",
        database="sales",
    )
    cursor = connection.cursor()

    SQL = """
    CREATE TABLE IF NOT EXISTS products(

	rowid int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	product varchar(255) NOT NULL,
	category varchar(255) NOT NULL
	)
 	"""

    cursor.execute(SQL)
    print("Table created")

    SQL = """
 	INSERT INTO products(product,category)
	VALUES
	("Television","Electronics"),
	("Laptop","Electronics"),
	("Mobile","Electronics")
	"""

    cursor.execute(SQL)
    connection.commit()

    SQL = "SELECT * FROM products"
    cursor.execute(SQL)

    for row in cursor.fetchall():
        print(row)
    connection.close()
