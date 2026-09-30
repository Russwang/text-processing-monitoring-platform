from contextlib import closing
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from database import DB_PATH, init_db, pull

app = Flask(__name__)
CORS(app)
init_db()

@app.post('/saveText')
def save_text():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error='A JSON object is required'), 400
    text, custom_id = data.get('text'), data.get('id')
    if not isinstance(text, str) or not text.strip():
        return jsonify(error='Nonempty text is required'), 400
    if not isinstance(custom_id, str) or not custom_id.strip():
        return jsonify(error='Nonempty string ID is required'), 400
    try:
        with closing(sqlite3.connect(DB_PATH)) as conn, conn:
            conn.execute('INSERT INTO text_store (id, text) VALUES (?, ?)', (custom_id, text))
    except sqlite3.IntegrityError:
        return jsonify(error='ID already exists'), 409
    return jsonify(id=custom_id), 201

@app.get('/getText')
def get_text():
    text_id = request.args.get('id', '')
    if not text_id.strip():
        return jsonify(error='ID is required'), 400
    row = pull(text_id)
    if row is None:
        return jsonify(error='Text not found'), 404
    return jsonify(text=row[0])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
