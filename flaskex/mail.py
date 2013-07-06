from smtplib import SMTP
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def rfc2047_header(str):
    return Header(str.encode('utf-8'), 'UTF-8').encode('utf-8')


def create_message(from_addr, to_addr, from_, to, subject, html):
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    # if email address encoded then attach local address
    message['From'] = "%s<%s>" % (rfc2047_header(from_), from_addr)
    message['To'] = "%s<%s>" % (rfc2047_header(to), to_addr)
    message.attach(MIMEText(html, 'html', 'utf-8'))
    return message


def send_mail(
    from_addr, from_, to_addr, to, subject, html, smtp=None,
    smtp_server='127.0.0.1'
):
    if smtp is None:
        smtp = SMTP(smtp_server)
        try:
            return send_mail(
                from_addr, from_, to_addr, to, subject, html, smtp
            )
        finally:
            smtp.quit()
    message = create_message(from_addr, to_addr, from_, to, subject, html)
    smtp.sendmail(from_addr, to_addr, message.as_string())
