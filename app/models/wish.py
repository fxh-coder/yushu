from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc, func
from app.models.base import Base, db
from sqlalchemy.orm import relationship

from app.spider.yushu_book import YuShuBook
from app.libs.enums import PendingStatus

class Wish(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))
    launched = Column(Boolean, default=False)
    
    @classmethod
    def get_user_wishes(cls, uid):
        wishes = Wish.query.filter_by(uid=uid, launched=False, status=PendingStatus.Waiting.value).order_by(
            desc(Wish.create_time)).all()
        return wishes

    @classmethod
    def get_gifts_counts(cls, isbn_list):
        from app.models.gift import Gift
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(
                                    Gift.launched == False,
                                    Gift.isbn.in_(isbn_list),
                                    Gift.status == 1).group_by(
                            Gift.isbn).all()
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

    @property
    def book(self):
        yuhsu_book = YuShuBook()
        yuhsu_book.search_by_isbn(self.isbn)
        return yuhsu_book.first
