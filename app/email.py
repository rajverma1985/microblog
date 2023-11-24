from flask_mail import Message
from flask import render_template
from app import app, mail


# More details here on flask mail docs: https://pythonhosted.org/Flask-Mail/
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject=subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


# Main function that will send email to the user.
def send_password_reset_email(user):
    token = user.get_password_reset_token()
    send_email("Reset you password -- Dev Blog!!",
               sender=app.config['ADMINS'],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token),
               html_body=render_template('email/reset_password.html', user=user, token=token)
               )
