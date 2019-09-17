from pathlib import Path
from html import parser
import fire, csv, pickle, utils, time


def get_pwd_array(password, max_length):
    password += '`' * (max_length - len(password))
    char_pwd = [char for char in password]
    return tuple(char_pwd)


def evaluate_all_passwords(source_path, out_path, lms_path, max_length=20, batch_size=10000):
    source_path = Path(source_path)
    out_path = Path(out_path)

    with open(Path(lms_path), 'rb') as out:
        true_char_ngram_lms = pickle.load(out, encoding='latin1')

    counter = 0
    counter_written = 0
    start_time = time.time()
    with source_path.open(mode='r', encoding='utf8') as source:
        with out_path.open(mode='w', encoding='utf8') as out:

            fields = ['js1', 'js2', 'js3', 'js4']
            w = csv.DictWriter(out, [i for i in fields], delimiter=',', extrasaction='ignore',
                               quoting=csv.QUOTE_MINIMAL)
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
                if counter % 500000 == 0:
                    passwords_per_second = float(counter) / (time.time() - start_time)
                    print('%d divergences from %d wrote to %s at %.2f passwords per second rate' % (
                        counter_written, counter, out_path, passwords_per_second))

            pwd_dict = {}
            counter_written += len(batch)

            for i in range(4):
                lm = utils.NgramLanguageModel(i + 1, batch, tokenize=False)
                pwd_dict['js{}'.format(i + 1)] = lm.js_with(true_char_ngram_lms[i])
            _ = w.writerow(pwd_dict)
            passwords_per_second = float(counter) / (time.time() - start_time)
            print('%d divergences from %d wrote to %s at %.2f passwords per second rate' % (
                counter_written, counter, out_path, passwords_per_second))

        print('%s divergences from %d were wrote to file: %s' % (counter_written, counter, out_path))
        out.close()
    source.close()


if __name__ == '__main__': fire.Fire(evaluate_all_passwords)
