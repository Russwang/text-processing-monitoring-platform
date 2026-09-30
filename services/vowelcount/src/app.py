from flask import Flask, request, jsonify
from vowelcount import count_vowels
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def count_vowel():
    text = request.args.get('text', '')
    count = count_vowels(text)
    return jsonify({'answer': count})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
