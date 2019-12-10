import fire


def count_pwd(file):
    count = 0
    match = 0
    for password in open(file, mode='r', encoding='utf8', errors='ignore'):
        count += 1
        password = password.replace('\n', '')
        if len(password) > 20:
            match += 1
        if count % 1000000 == 0:
            print('Found %s passwords with size greater than 20 from %s count so far' % (match, count))
    print('Finished matching %s passwords from %s' % (match, count))


if __name__ == '__main__': fire.Fire(count_pwd)
