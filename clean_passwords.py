import string
from pathlib import Path

base_path = '/media/discoD/Mestrado/NoLeak/'

source_path = base_path + 'passwordsAppendSorted.txt'
# source_path = base_path + 'invalid_sample.txt'
target_valid_path = base_path + 'valid_per_unicode.txt'
target_invalid_path = base_path + 'invalid_per_unicode.txt'


def is_valid(s):
    return s.translate(None, string.punctuation).isalnum()


def contains_invalid_unicode_characters(string_value):
    for c in string_value:
        if ord(c) > 255 or ord(c) < 32:
            return True
    return False


invalid_txt = Path(target_invalid_path).open(mode='w', encoding='utf8', errors='ignore')
valid_txt = Path(target_valid_path).open(mode='w', encoding='utf8', errors='ignore')

with Path(source_path).open(mode='r', encoding='utf8', errors='ignore') as sample_txt:
    count_total = 0
    count = 0
    for idx, line in enumerate(sample_txt):
        line = line.strip()
        if len(line) > 0:
            # if not is_valid(line.replace(' ', '')) and contains_invalid_unicode_characters(line.replace(' ', '')):
            if contains_invalid_unicode_characters(line.replace(' ', '')):
                invalid_txt.write(line + '\n')
                count += 1
                if count % 100000 == 0:
                    print('Wrote %d lines in invalid file from a total of %d lines' % (count, count_total))
            else:
                valid_txt.write(line + '\n')
        count_total += 1
    print('Wrote %d lines in invalid file from a total of %d lines' % (count, count_total))
invalid_txt.close()
valid_txt.close()
sample_txt.close()
