from flask_mail import Message
from app import mail
from flask import  render_template
from app import app


# More details here on flask mail docs: https://pythonhosted.org/Flask-Mail/
def send_email(sender, receiver, subject, text_body, html_body):
    msg = Message(sender=sender, recipients=receiver, subject=subject)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_password_reset_email(user):
    token = user.get_password_reset_token()
    send_email(subject= "Reset you password -- Dev Blog!!",
               sender=app.config['ADMINS'],
               receiver=user.email,
               text_body= render_template('email/reset_password.txt', token=token, user=user),
               html_body=render_template('email/reset_password.html', token=token, user=user)
               )