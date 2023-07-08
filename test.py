import smtplib
import ssl

sender = 'matin.arno4646@outlook.com'
password = '34129093428198matin'
receiver = 'matin.geralt6565@gmail.com'
message = f"""From: From Person <matin.arno4646@outlook.com>
To: To Person <matin.geralt6565@gmail.com>
Subject: SMTP e-mail test\n\n"""
context = ssl.create_default_context()
smtp = smtplib.SMTP('smtp-mail.outlook.com', 587)
smtp.ehlo()
smtp.starttls(context=context)
smtp.ehlo()
smtp.login(sender, password)
smtp.sendmail(sender, receiver, message.encode("utf-8"))
print('email sent!')