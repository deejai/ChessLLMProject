from flask import Flask#, send_from_directory

app = Flask(__name__)

@app.route('/')
def serve_index():
    return "hi!!!"
    # return send_from_directory(directory='.', filename='index.html')
