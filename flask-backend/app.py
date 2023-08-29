from flask import Flask, Blueprint, render_template, jsonify, request
from flask_cors import CORS
import os
import json
import openai
from dotenv import load_dotenv
from chess_coach.database_connectors.sqlite_db import SQLiteDatabaseConnection
from chess_coach.stockfish.handlers import StockfishPool
from chess_coach.gpt.api import ask_gpt
from chess_coach.prompting.move_suggestion import next_move_advice
from chess_coach.stockfish.utilities import is_valid_fen

load_dotenv()

bp = Blueprint('chess-llm-coach-api', __name__, template_folder='templates')
app = Flask(__name__)
CORS(app, resources={r"/chess-llm-coach-api/*": {"origins": "robotchesscoach.com"}})

openai.api_key = os.environ["OPENAI_API_KEY"]

sqlite_db = SQLiteDatabaseConnection("db.sqlite3")

sf_pool = StockfishPool(size=5)

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

@bp.route('/ask-form')
def ask_form():
    return render_template('ask_gpt.html')

@bp.route('/ask-coach', methods=['POST'])
def ask_coach():
    fen = request.json.get('fen')
    elo = 1000

    if not is_valid_fen(fen):
        return app.response_class(
            response=json.dumps({"error": f"Invalid fen: {fen}"}),
            status=400,
            mimetype='application/json'
        )

    prompt = next_move_advice(sf_pool, elo, fen)
    print("\n>>>>> PROMPT TO GPT\n")
    print(prompt)
    print("\n<<<<<<<< END PROMPT TO GPT\n")

    gpt_response = ask_gpt(prompt)

    response = app.response_class(
        response=json.dumps({"data": {"response": gpt_response}}),
        status=200,
        mimetype='application/json'
    )

    return response

with app.app_context():
    app.register_blueprint(bp, url_prefix='/chess-llm-coach-api')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
