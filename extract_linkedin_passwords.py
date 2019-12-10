def get_password(line, delimiter):
    return line.split(delimiter)[1].replace('\r', '')


def write_password(line, delimiter, out_file):
    password = get_password(line, delimiter)
    if len(password) > 0:
        out_file.write(password)


out_file = open('/media/discoD/Mestrado/NoLeak/Passwords/linkedin_passwords.txt', mode='w')
count = 0
with open('/media/discoD/Mestrado/NoLeak/Passwords/68_linkedin_found_hash_plain.txt', mode='r') as leak_file:
    for hash_password in leak_file:
        if ':' in hash_password:
            out_file.write(hash_password[41:])
            count += 1
            if count % 10000 == 0:
                print('Written %d passwords' % count)
        else:
            print('Separator not found in line %s' % hash_password)
    print('Finished writing %d passwords' % count)
out_file.close()
