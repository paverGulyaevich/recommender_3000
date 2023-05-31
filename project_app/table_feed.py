from database import Base, SessionLocal
from table_post import Post
from table_user import User
from sqlalchemy import Integer, Text, TIMESTAMP, Column, ForeignKey, func
from sqlalchemy.orm import relationship


class Feed(Base):
    __tablename__ = "feed_data"
    __table_args__ = {"schema": "public"}
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    post_id = Column(Integer, ForeignKey(Post.id), primary_key=True)
    action = Column(Text)
    time = Column(TIMESTAMP, name='timestamp')
    user = relationship("User")
    post = relationship("Post")

    # def __repr__(self):
    #     return f"Feed(user_id={self.user_id}, post_id={self.post_id}, action={self.action}, time={self.time})"


if __name__ == "__main__":
    with SessionLocal() as db:
        result = db.query(Feed.post_id) \
            .filter(Feed.action == 'like') \
            .group_by(Feed.post_id) \
            .order_by(func.count(Feed.user_id).desc()).limit(10).all()
        print(result)
