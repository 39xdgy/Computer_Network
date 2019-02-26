import smtplib

from email.mime.text import MIMEText



textfile = "textfile.txt"
me = "jwang20@cornellcollege.edu"
you = "39xdgy@gmail.com"
host = 'smtp.gmail.com:587'


with open(textfile) as fp:
    msg = MIMEText(fp.read())

print(msg)



msg['subject'] = 'The contents of %s' % textfile
msg['From'] = you
msg['To'] = me

#print(msg)


s = smtplib.SMTP(host)
s.starttls()
s.login('39xdgy@gmail.com', 'Jasonwang1575')
s.send_message(msg)
s.quit()

print("Successfully sended")
