from flask_mail import Message
from app import mail


def send_email(sender, receiver, subject, text_body, html_body):
    msg = Message(recipients=receiver, subject=subject, sender=sender)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
