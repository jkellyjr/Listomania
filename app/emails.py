# listomania/app/emails.py
# email framework

from flask_mail import Message
from app import app, mail
from flask import render_template
from config import ADMINS
from threading import Thread
from .decorators import async

# implement threading
@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


# generic email
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject = subject, sender = sender, recipients = recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(app, msg)


# email notification for new follower
def follower_notification(followed, follower):
    send_email("[listomania] %s is now following you!" % follower.name, ADMINS[0], [followed.email],
        render_template("follower_email.txt", user = followed, follower = follower),
        render_template("follower_email.html", user = followed, follower = follower))
