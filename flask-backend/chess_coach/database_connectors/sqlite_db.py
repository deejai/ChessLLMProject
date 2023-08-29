import sqlite3
import threading

class SQLiteDatabaseConnection:
    _local_storage = threading.local()

    def __init__(self, db_path):
        self.db_path = db_path

    def _get_connection(self):
        conn = getattr(self._local_storage, 'conn', None)
        if conn is None:
            try:
                conn = sqlite3.connect(self.db_path)
                print("Connected to the SQLite database.")
                setattr(self._local_storage, 'conn', conn)

            except Exception as e:
                print(f"Error connecting to the SQLite database: {repr(e)}")
                conn = None

        return conn

    def execute_query(self, query):
        conn = self._get_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute(query)
                if query.strip().lower().startswith('select'):
                    return cursor.fetchall()
                conn.commit()
            except Exception as e:
                print(f"An error occurred executing the query.: {repr(e)}")
                conn = None
