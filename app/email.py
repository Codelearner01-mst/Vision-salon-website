from flask_mail import Message
from flask import current_app,render_template
from threading import Thread
from . import mail

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)


def send_email(to,subject, template,sender,**kwargs):
    app = current_app._get_current_object()
    msg = Message(subject,[to],sender=sender)
    msg.body = render_template(template)
    msg.html  = render_template(template)
    thr = Thread(target=send_async_email, args=[app,msg])
    thr.start()
    return thr