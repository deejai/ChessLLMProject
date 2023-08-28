import pyodbc
import os

class SQLServerDatabaseConnection:
    def __init__(self):
        self.conn = None
        self.connect()

    def connect(self):
        db_host = os.getenv('SQLSERVER_DB_HOST')
        db_port = os.getenv('SQLSERVER_DB_PORT')
        db_user = os.getenv('SQLSERVER_DB_USER')
        db_password = os.getenv('SQLSERVER_DB_PASSWORD')
        db_name = os.getenv('SQLSERVER_DB_NAME')

        conn_str = (
            f"Driver={{ODBC Driver 17 for SQL Server}};"
            f"Server={db_host},{db_port};"
            f"Database={db_name};"
            f"UID={db_user};"
            f"PWD={db_password};"
            f"Encrypt=yes;"
        )

        try:
            self.conn = pyodbc.connect(conn_str)
            print("Connected to the database.")

        except Exception as e:
            print("Error connecting to the database.", e)
            self.conn = None

    def execute_query(self, query):
        if self.conn is None:
            self.connect()

        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                cursor.execute(query)
                self.conn.commit()

            except Exception as e:
                print("An error occurred executing the query.", e)
                self.conn = None
                self.connect()

# Usage
# db = SQLServerDatabaseConnection()
# db.execute_query("YOUR SQL QUERY HERE")
