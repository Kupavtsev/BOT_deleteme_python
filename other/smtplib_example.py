# skipped your comments for readability
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

me = "support@deleteme.ru"
my_password = r"example"
you = "oleg.k@dot-tech.ru"

msg = MIMEMultipart('alternative')
msg['Subject'] = "Alert"
msg['From'] = me
msg['To'] = you

html = '<html><body><p>Hi, I have the following alerts for you!</p></body></html>'
part2 = MIMEText(html, 'html')

msg.attach(part2)

# Send the message via gmail's regular server, over SSL - passwords are being sent, afterall
# s = smtplib.SMTP_SSL('smtp.gmail.com')
s = smtplib.SMTP_SSL('smtp.yandex.ru:465')
# uncomment if interested in the actual smtp conversation
# s.set_debuglevel(1)
# do the smtp auth; sends ehlo if it hasn't been sent already
s.login(me, my_password)

s.sendmail(me, you, msg.as_string())
s.quit()