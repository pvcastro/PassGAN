from collections import defaultdict
from pathlib import Path
import fire
from pprint import pprint


def get_word_counts(file_path):
    d = defaultdict(int)
    file_path = Path(file_path)

    with file_path.open(mode='r', encoding='utf8', errors='ignore') as file:
        count_total = 0
        count = 0
        for idx, line in enumerate(file):
            d[len(line)] += 1  # observe this bit carefully
            count += 1
            if count % 100000 == 0:
                print('Counted %d lines in %s file' % (count, file_path.name))

    pprint(d)


if __name__ == '__main__': fire.Fire(get_word_counts)
