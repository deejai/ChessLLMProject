from flask import Flask, Blueprint, render_template
import os
import json

from database_connectors.sqlite_db import SQLiteDatabaseConnection

bp = Blueprint('chess-llm-coach-api', __name__, template_folder='templates')
app = Flask(__name__)

sqlite_db = SQLiteDatabaseConnection("db.sqlite3")

@bp.route('/')
def hello_world():
    return render_template('hello.html')

@bp.route('/test')
def test():
    results = sqlite_db.execute_query("SELECT * FROM table2")

    response = app.response_class(
        response=json.dumps(results),
        status=200,
        mimetype='application/json'
    )

    print(results)

    return response

with app.app_context():
    app.register_blueprint(bp, url_prefix='/chess-llm-coach-api')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
