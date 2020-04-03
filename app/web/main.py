from app.models.gift import Gift
from app.view_models.book import BookViewModel
from . import web
from flask import render_template
from flask_login import current_user

__author__ = 'fxh'


@web.route('/')
def index():
   recent_gifts = Gift.recent()
   books = [BookViewModel(gift.book) for gift in recent_gifts]
   return render_template('index.html', recent=books)


@web.route('/personal')
def personal_center():
   return render_template('personal.html', user=current_user.summary)
