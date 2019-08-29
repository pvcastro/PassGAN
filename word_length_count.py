from collections import defaultdict
from pathlib import Path
import fire
from pprint import pprint


def get_word_counts(file_path, big_path, lower_limit=100):
    d = defaultdict(int)
    file_path = Path(file_path)
    big_path = Path(big_path)

    with big_path.open(mode='w', encoding='utf8', errors='ignore') as out:

        with file_path.open(mode='r', encoding='utf8', errors='ignore') as file:
            count_written = 0
            count = 0
            for idx, line in enumerate(file):
                size = len(line)
                d[size] += 1  # observe this bit carefully

                if size > lower_limit:
                    out.write(line + '\n\n')
                    count_written += 1
                    if count % 1000 == 0:
                        print('Wrote %s' % line)

                count += 1
                if count % 100000 == 0:
                    print('Counted %d lines in %s file' % (count, file_path.name))

        print('Counted %d lines in %s file' % (count, file_path.name))
    print('Wrote %d big passwords to %s file' % (count_written, big_path.name))

    out.close()
    file.close()

    pprint(d)


if __name__ == '__main__': fire.Fire(get_word_counts)
