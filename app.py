#!/usr/bin/env python

import traceback

from flask import Flask, request, jsonify
from flask_cors import CORS

from password_evaluation import evaluate_single_password, load_char_ngram_model

import json

app = Flask(__name__)

CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

true_char_ngram_lms = load_char_ngram_model('ngram/true_char_ngram_lms.pickle')
max_length = 20
batch_size = 10000


@app.route('/evaluate', methods=['GET', 'POST'])
def evaluate():
    password = request.args.get('password', None)

    js_divergences = evaluate_single_password(true_char_ngram_lms=true_char_ngram_lms, password=password,
                                              max_length=max_length, batch_size=batch_size)

    return jsonify(js_divergences)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
