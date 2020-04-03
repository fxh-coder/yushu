from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc, func
from app.models.base import Base, db
from app.spider.yushu_book import YuShuBook
from sqlalchemy.orm import relationship
from flask import current_app
from app.libs.enums import PendingStatus


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))
    launched = Column(Boolean, default=False)
    
    def is_yourself_gift(self, uid):
        return True if self.uid == uid else False

    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False, status=PendingStatus.Waiting.value).order_by(
            desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        from app.models.wish import Wish
        # 根据传入的一组isbn，到Wish表中计算出某个礼物的wish心愿数量
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
                                    Wish.launched == False,
                                    Wish.isbn.in_(isbn_list),
                                    Wish.status == 1).group_by(
                            Wish.isbn).all()
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

    @property
    def book(self):
        yuhsu_book = YuShuBook()
        yuhsu_book.search_by_isbn(self.isbn)
        return yuhsu_book.first

    @classmethod
    def recent(cls):
        recent_gift = Gift.query.filter_by(
            status=PendingStatus.Waiting.value,
            launched=False).group_by(
            Gift.isbn).order_by(
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()

        return recent_gift
