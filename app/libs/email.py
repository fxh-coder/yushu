
"""
to：发送对象
subject：标题
template：内容
"""
from threading import Thread
from app import mail
from flask_mail import Message
from flask import current_app, render_template

def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass

def send_email(to, subject, template, **kwargs):
    msg = Message('[鱼书]' + ' ' + subject,
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[to])
    msg.html = render_template(template, **kwargs)
    # 获取真实的app对象，不是代理对象，代理对象受线程影响，代理对象的id不一样
    app = current_app._get_current_object()

    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
