from flask import Flask, Blueprint, render_template, request, jsonify
import os
import json
import openai
from dotenv import load_dotenv
from chess_coach.database_connectors.sqlite_db import SQLiteDatabaseConnection
from chess_coach.stockfish.handlers import StockfishPool
from chess_coach.gpt.api import ask_gpt
from chess_coach.prompting.move_suggestion import next_move_advice
from chess_coach.stockfish.utilities import is_valid_fen
from chess_coach.gpt.queue import new_task
from chess_coach.settings import ROOT_DIR
import threading

gpt_queue_lock = threading.Lock()

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

    return jsonify(results), 200

@bp.route('/ask-form')
def ask_form():
    return render_template('ask_gpt.html')

def threaded_ask_coach(task_file_name, prompt):
    gpt_response = ask_gpt(prompt)
    gpt_summary = gpt_response[1 + gpt_response.find("__SUMMARY__") + len("__SUMMARY__"):].strip()

    with gpt_queue_lock:
        with open(f"workspace/gpt_queue/{task_file_name}", "w") as f:
            f.write(gpt_summary)

@bp.route('/ask-coach', methods=['POST', 'OPTIONS'])
def ask_coach():
    if request.method == 'OPTIONS':
        return jsonify({"message": "OK"}), 200

    fen = request.json.get('fen')
    elo = request.json.get('elo')

    if not is_valid_fen(fen):
        return jsonify({"error": f"Invalid fen: {fen}"}), 400

    prompt = next_move_advice(sf_pool, elo, fen)
    print("\n>>>>> PROMPT TO GPT\n")
    print(prompt)
    print("\n<<<<<<<< END PROMPT TO GPT?\n")

    task_file_name = new_task()

    t = threading.Thread(target=threaded_ask_coach, args=(task_file_name, prompt))
    t.start()

    return jsonify({"data": {"task_id": task_file_name}}), 202

@bp.route('/get-gpt-response/<task_id>', methods=['GET', 'OPTIONS'])
def get_task_status(task_id):
    if request.method == 'OPTIONS':
        return jsonify({"message": "OK"}), 200

    try:
        with gpt_queue_lock:
            with open(f"workspace/gpt_queue/{task_id}", "r") as f:
                result = f.read()

        if not result:
            return jsonify({'status': 'running'}), 202
        else:
            return jsonify({'status': 'done', 'result': result}), 200
    except FileNotFoundError:
        return jsonify({'status': 'not found'}), 404

with app.app_context():
    app.register_blueprint(bp, url_prefix='/chess-llm-coach-api')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
