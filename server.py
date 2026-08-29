# server.py

import os
import sys

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Import existing chatbot logic
from app import run_agent, memory
from tools import get_summary, add_expense, delete_expense

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

@app.route("/")
def read_index():
    return send_from_directory('static', 'index.html')

@app.route("/api/chat", methods=['POST'])
def chat_endpoint():
    data = request.json
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"error": "Message is required"}), 400
        
    # Run the agent (which might use tools)
    response_text = run_agent(user_message)
    
    return jsonify({"response": response_text})

@app.route("/api/expenses", methods=['GET'])
def expenses_endpoint():
    summary = get_summary("all")
    return jsonify(summary)

if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    PORT = 8000
    print(f" * Serving Budget Assistant on http://127.0.0.1:{PORT}")
    print(" * Ready! Open http://localhost:8000 in your browser.")
    server = make_server("0.0.0.0", PORT, app)
    server.serve_forever()
