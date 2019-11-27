from pathlib import Path
from html import parser
import fire, csv, pickle, utils, time
from datetime import datetime
from pprint import pprint
import pandas as pd
import requests, json

gan_train_divergences_path = 'data/divergences_train.csv'
gan_generated_divergences_path = 'data/divergences_gan_gen.csv'


def get_reference_divergences(divergences_path):
    divergences = pd.read_csv(divergences_path).describe()

    def get_max_divergence(ngram):
        return divergences['js{}'.format(ngram)]['max']

    return {1: get_max_divergence(1), 2: get_max_divergence(2), 3: get_max_divergence(3), 4: get_max_divergence(4)}


max_train_divergences = get_reference_divergences(
    gan_train_divergences_path)  # {1: 0.218597, 2: 0.351165, 3: 0.411383, 4: 0.461548}
max_generated_divergences = get_reference_divergences(
    gan_generated_divergences_path)  # {: 0.186912, 2: 0.232348, 3: 0.285541, 4: 0.350717}


def log(message):
    print(datetime.now(), '-', message)


def load_char_ngram_model(lms_path):
    with open(Path(lms_path), 'rb') as f:
        log('Loading ngrams from %s' % lms_path)
        true_char_ngram_lms = pickle.load(f, encoding='latin1')
        log('Finished loading ngrams')
    return true_char_ngram_lms


def get_pwd_array(password, max_length):
    password += '`' * (max_length - len(password))
    char_pwd = [char for char in password]
    return tuple(char_pwd)


def evaluate_single_password(true_char_ngram_lms, password, max_length=20, batch_size=10000, ngrams=1):
    char_pwd = get_pwd_array(password, max_length)
    pwd_array = [tuple(char_pwd)] * batch_size

    result = {}

    for i in range(ngrams):
        log('Loading {}-gram from model for password {}'.format(i, password))
        lm = utils.NgramLanguageModel(i + 1, pwd_array, tokenize=False)
        log('Loaded {}-gram from model for password {}'.format(i, password))
        js_divergence = lm.js_with(true_char_ngram_lms[i])
        key = 'js{}'.format(i + 1)
        print(key, js_divergence)
        result[key] = js_divergence
        result['ref_' + key] = max_train_divergences[i + 1]

    pprint(result)

    return result


def evaluate_all_passwords(source_path, out_path, lms_path, max_length=20, batch_size=10000):
    source_path = Path(source_path)
    out_path = Path(out_path)

    with open(Path(lms_path), 'rb') as lms:
        log('Loading ngrams from %s' % lms_path)
        true_char_ngram_lms = pickle.load(lms, encoding='latin1')
        log('Finished loading ngrams')

    counter = 0
    counter_written = 0
    start_time = time.time()
    with source_path.open(mode='r', encoding='utf8') as source:
        with out_path.open(mode='w', encoding='utf8') as out:

            fields = ['js1', 'js2', 'js3', 'js4']
            w = csv.DictWriter(out, [i for i in fields], delimiter=',', extrasaction='ignore',
                               quoting=csv.QUOTE_MINIMAL)
            log('Created divergences file %s' % out_path)
            w.writeheader()

            batch = []

            for line in source:

                password = parser.unescape(line).strip()

                if len(password) <= max_length:

                    pwd_array = get_pwd_array(password, max_length)
                    batch.append(pwd_array)

                    if len(batch) == batch_size:
                        pwd_dict = {}
                        counter_written += len(batch)

                        for i in range(4):
                            lm = utils.NgramLanguageModel(i + 1, batch, tokenize=False)
                            pwd_dict['js{}'.format(i + 1)] = lm.js_with(true_char_ngram_lms[i])
                        _ = w.writerow(pwd_dict)

                        batch = []

                counter += 1
                if counter > 0 and counter % 100000 == 0:
                    passwords_per_second = float(counter) / (time.time() - start_time)
                    log('%d divergences from %d wrote to %s at %.2f passwords per second rate' % (
                        counter_written, counter, out_path, passwords_per_second))

            log('Finished reading lines from %s' % source_path)

            pwd_dict = {}
            counter_written += len(batch)

            for i in range(4):
                lm = utils.NgramLanguageModel(i + 1, batch, tokenize=False)
                pwd_dict['js{}'.format(i + 1)] = lm.js_with(true_char_ngram_lms[i])
            _ = w.writerow(pwd_dict)
            passwords_per_second = float(counter) / (time.time() - start_time)
            log('%d divergences from %d wrote to %s at %.2f passwords per second rate' % (
                counter_written, counter, out_path, passwords_per_second))

        log('%s divergences from %d were wrote to file: %s' % (counter_written, counter, out_path))
        out.close()
    source.close()


def flask_evaluation(password: str, ngrams: int):
    params = {'password': password, 'ngrams': ngrams}
    response = requests.get('http://0.0.0.0:5002/evaluate', params=params)
    print(json.loads(response.text))


if __name__ == '__main__': fire.Fire()
