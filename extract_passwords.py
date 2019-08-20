def get_password(line, delimiter):
    return line.split(delimiter)[1].replace('\r', '')


def write_password(line, delimiter, out_file):
    password = get_password(line, delimiter)
    if len(password) > 0:
        out_file.write(password)


out_file = open('/media/discoD/Mestrado/NoLeak/passwords.txt', mode='w')
count = 0
with open('/media/discoD/Mestrado/NoLeak/leak00.txt', mode='r') as leak_file:
    for email_password in leak_file:
        if ':' in email_password and ';' in email_password:
            out_file.write(email_password)
            count += 1
            if count % 10000 == 0:
                print('Written %d passwords' % count)
    #     try:
    #         write_password(email_password, ':', out_file)
    #         count += 1
    #         if count % 10000 == 0:
    #             print 'Written %d passwords' % count
    #     except IndexError:
    #         print email_password
    #         try:
    #             write_password(email_password, ';', out_file)
    #             count += 1
    #             if count % 10000 == 0:
    #                 print 'Written %d passwords' % count
    #             continue
    #         except IndexError:
    #             print email_password
    #             continue
    print('Written %d passwords' % count)
out_file.close()
