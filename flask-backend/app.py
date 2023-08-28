from flask import Flask, Blueprint, render_template, jsonify, request
from flask_cors import CORS
import os
import json
import openai
from dotenv import load_dotenv
from database_connectors.sqlite_db import SQLiteDatabaseConnection

load_dotenv()

bp = Blueprint('chess-llm-coach-api', __name__, template_folder='templates')
app = Flask(__name__)
CORS(app, resources={r"/chess-llm-coach-api/*": {"origins": "robotchesscoach.com"}})

openai.api_key = os.getenv("OPENAI_API_KEY")

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
    return response

@bp.route('/ask', methods=['POST'])
def ask_gpt():
    user_input = request.json.get('prompt')
    model_engine = "gpt-4.0"
    conversation = [
        {"role": "user", "content": user_input}
    ]
    openai_response = openai.ChatCompletion.create(
        model=model_engine,
        messages=conversation
    )
    gpt_response = openai_response['choices'][0]['message']['content']

    response = app.response_class(
        response=json.dumps({"data": {"response": gpt_response}}),
        status=200,
        mimetype='application/json'
    )

    return response

@bp.route('/ask-form')
def ask_form():
    return render_template('ask_gpt.html')

with app.app_context():
    app.register_blueprint(bp, url_prefix='/chess-llm-coach-api')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
