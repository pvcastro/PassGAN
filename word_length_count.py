from collections import defaultdict
from pathlib import Path
import fire
from pprint import pprint
from html import parser


def get_word_counts(file_path, big_path, colon_path, pwd_path, lower_limit=100):
    d = defaultdict(int)
    file_path = Path(file_path)
    big_path = Path(big_path)
    colon_path = Path(colon_path)
    pwd_path = Path(pwd_path)

    colon_out = colon_path.open(mode='w', encoding='utf8', errors='ignore')
    big_out = big_path.open(mode='w', encoding='utf8', errors='ignore')
    pwd_out = pwd_path.open(mode='w', encoding='utf8', errors='ignore')

    with file_path.open(mode='r', encoding='utf8', errors='ignore') as file:
        count_written = 0
        count_colon = 0
        count_pwd = 0
        count = 0
        for idx, line in enumerate(file):
            line = parser.unescape(line)
            size = len(line)
            d[size] += 1  # observe this bit carefully

            if size > lower_limit:
                big_out.write(line + '\n')
                count_written += 1
                if count_written % 100000 == 0:
                    print('Wrote %d big passwords' % count_written)
            elif ':' in line:
                colon_out.write(line + '\n')
                count_colon += 1
                if count_colon % 1000 == 0:
                    print('Wrote %d passwords with colon' % count_colon)
            else:
                pwd_out.write(line)
                count_pwd += 1
                if count_pwd % 500000 == 0:
                    print('Wrote %d normal passwords' % count_pwd)

            count += 1
            if count % 500000 == 0:
                print('Counted %d lines in %s file' % (count, file_path.name))

        print('Counted %d lines in %s file' % (count, file_path.name))
        print('Wrote %d big passwords to %s file' % (count_written, big_path.name))
        print('Wrote %d passwords with colon to %s file' % (count_colon, colon_path.name))
        print('Wrote %d normal passwords to %s file' % (count_pwd, pwd_path.name))

    pwd_out.close()
    colon_out.close()
    big_out.close()
    file.close()

    pprint(d)


if __name__ == '__main__': fire.Fire(get_word_counts)
