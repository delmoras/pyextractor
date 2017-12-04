#!/usr/bin/python3

from imapclient import IMAPClient
import pyzmail , imaplib , pprint ,sys
from validate_email import validate_email
imaplib._MAXLINE = 10000000


if len(sys.argv) != 4:
    print("Usage:\n    %s <server> <username> <password>" % (sys.argv[0][sys.argv[0].rfind("\\") + 1:]))
    sys.exit()


emailFile = 'emails-export.txt'
serverName = str(sys.argv[1])
username = str(sys.argv[2])
password = str(sys.argv[3])


server = IMAPClient(serverName, use_uid=True)
server.login(username,password)
select_info = server.select_folder('INBOX',readonly=True)
print('%d messages in found in INBOX' % select_info[b'EXISTS'])
print('Exporting..')

#get ids of inbox messages
uids = server.search('ALL')


for val in uids:
     rawMessages = server.fetch([val], ['BODY[]','FLAGS'])
     message = pyzmail.PyzMessage.factory(rawMessages[val][b'BODY[]'])
     address =  message.get_address('reply-to')
     print(address[0])
     is_valid = validate_email(address[0])
     if is_valid == True and address[0] != '':
         with open(emailFile, 'a') as out:
            out.write(address[0].lower() + '\n')

print("Done !")