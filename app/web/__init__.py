from flask import Blueprint, render_template

web = Blueprint('web', __name__)

@web.app_errorhandler(404)
def not_found(e):
    # 这里可以实现自己的处理方法，写入日志啊等等，都可以 
    return render_template('404.html'), 404

from app.web import book
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish
