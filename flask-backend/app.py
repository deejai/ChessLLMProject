from flask import Flask, Blueprint, render_template, request
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

openai.api_key = os.environ["OPENAI_API_KEY"]

sqlite_db = SQLiteDatabaseConnection("db.sqlite3")

sf_pool = StockfishPool(size=5)

CORS_ALLOWED_ORIGINS = ["http://localhost:8080", "https://robotchesscoach.com"]

def add_cors_headers(response):
    origin = request.headers.get('Origin')

    if origin and origin in CORS_ALLOWED_ORIGINS:
        response.headers.add("Access-Control-Allow-Origin", origin)

        # Dynamically set allowed methods
        allowed_methods = []
        for rule in app.url_map.iter_rules():
            if request.path == rule.rule:
                allowed_methods.extend(rule.methods)

        response.headers.add("Access-Control-Allow-Methods", ", ".join(allowed_methods))

    response.headers.add("Access-Control-Allow-Headers", "Authorization, Content-Type")
    return response

app.after_request(add_cors_headers)

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

@bp.route('/ask-coach', methods=['POST', 'OPTIONS'])
def ask_coach():
    if request.method == 'OPTIONS':
        # Preflight request. Reply successfully:
        response = app.response_class(
            response=json.dumps({"message": "OK"}),
            status=200,
            mimetype='application/json'
        )

        return response

    fen = request.json.get('fen')
    elo = request.json.get('elo')

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

    # gpt_response: str = ask_gpt(prompt)
    gpt_summary: str = "hi"#gpt_response[gpt_response.find("__SUMMARY__") + len("__SUMMARY__"):].strip()

    response = app.response_class(
        response=json.dumps({"data": {"response": gpt_summary}}),
        status=200,
        mimetype='application/json'
    )

    response.headers.add("Access-Control-Allow-Origin", "https://robotchesscoach.com")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Authorization, Content-Type")

    return response

with app.app_context():
    app.register_blueprint(bp, url_prefix='/chess-llm-coach-api')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
