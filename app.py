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
# true_char_ngram_lms = None
max_length = 20
batch_size = 10000
threshold = 0.3


@app.route('/evaluate', methods=['GET', 'POST'])
def evaluate():
    password = request.args.get('password', None)
    ngrams = request.args.get('ngrams', default=1, type=int)

    js_divergences = evaluate_single_password(true_char_ngram_lms=true_char_ngram_lms, password=password, ngrams=ngrams,
                                              max_length=max_length, batch_size=batch_size)

    for i in range(ngrams):
        key = 'js{}'.format(i + 1)
        ref_key = 'ref_' + key
        ref_thresh_key = 'ref_thresh_' + key
        diagnostic_key = 'diag_' + key
        divergence, reference_divergence = js_divergences[key], js_divergences[ref_key]
        ref_threshold_divergence = reference_divergence * (1 + threshold)
        js_divergences[ref_thresh_key] = ref_threshold_divergence
        if divergence > ref_threshold_divergence:
            diagnostic = 'A senha se diverge mais das conhecidas pela GAN, e mais segura'
        else:
            diagnostic = 'A senha esta mais semelhante as conhecidas pela GAN, e mais fraca'
        js_divergences[diagnostic_key] = diagnostic

    return jsonify(js_divergences)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
