from flask import Flask
import os
import json

from database_connectors.sqlite_db import SQLiteDatabaseConnection

app = Flask(__name__)

sqlite_db = SQLiteDatabaseConnection("db.sqlite3")

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/test')
def test():
    results = sqlite_db.execute_query("SELECT * FROM table2")

    response = app.response_class(
        response=json.dumps(results),
        status=200,
        mimetype='application/json'
    )

    print(results)

    return response

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
