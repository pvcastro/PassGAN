import fire


def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


def print_percentage(lengths, up_to=10):
    total_passwords = sum(lengths)
    pct = []
    for i in range(0, 20):
        pct.append("{0:.5%}".format(float(lengths[i] / total_passwords)))
    print(pct)
    up_to_pct = float(sum(lengths[0:up_to]) / total_passwords)
    print('Percentage up to %s: %s' % (up_to, "{0:.5%}".format(up_to_pct)))


def print_password_sizes():
    lines = open('/media/discoD/Mestrado/NoLeak/password_length_count.txt', mode='r', encoding='utf8').readlines()
    chunks = list(divide_chunks(lines, 6))
    print(len(chunks))
    # generated_lines_by_size = {10000: 5, 100000: 7, 1000000: 9, 10000000: 11, 100000000: 13, 1000000000: 15}
    generated_lines_by_size = {1000000000: 5}
    length_by_size = {}
    linkedin_lengths, rockyou_lengths, passgan_lengths = [], [], []
    for idx, chunk in enumerate(chunks):
        # print('Printing quantity of passwords for length %s' % (idx + 1))
        chunk = [line.strip() for line in chunk]
        linkedin_size = chunk[1]
        linkedin_lengths.append(int(linkedin_size))
        rockyou_size = chunk[3]
        rockyou_lengths.append(int(rockyou_size))
        for size in generated_lines_by_size.keys():
            length_by_size[size] = chunk[generated_lines_by_size[size]]
        passgan_lengths.append(int(length_by_size[1000000000]))
        # print(linkedin_size, rockyou_size, length_by_size)
        # print("%s, %s, %s" % (linkedin_size, rockyou_size, length_by_size[1000000000]))
        print("{name: '%s',data: [%s, %s, %s]}, " % (idx + 1, linkedin_size, rockyou_size, length_by_size[1000000000]))
    print(linkedin_lengths)
    print(rockyou_lengths)
    print(passgan_lengths)
    print_percentage(linkedin_lengths)
    print_percentage(rockyou_lengths)
    print_percentage(passgan_lengths)


if __name__ == '__main__': fire.Fire(print_password_sizes)
