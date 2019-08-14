import string

base_path = '/media/discoD/Mestrado/NoLeak/'

source_path = base_path + 'passwordsAppendSorted.txt'
target_path = base_path + 'invalid.txt'


def is_valid(s):
    return s.translate(None, string.punctuation).isalnum()


with open(target_path, mode='w') as invalid_txt:
    with open(source_path, mode='r') as sample_txt:
        count_total = 0
        count = 0
        for idx, line in enumerate(sample_txt):
            line = line.strip()
            if len(line) > 0:
                if not is_valid(line.replace(' ', '')):
                    invalid_txt.write(line + '\n')
                    count += 1
                    if count % 100000 == 0:
                        print('Wrote %d lines in invalid file from a total of %d lines' % (count, count_total))
            count_total += 1
        print('Wrote %d lines in invalid file from a total of %d lines' % (count, count_total))
invalid_txt.close()
sample_txt.close()
