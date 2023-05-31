from database import Base, SessionLocal  # Import Base model from database.py module
from sqlalchemy import Text, Integer, Column, ForeignKey, TIMESTAMP  # Import types
from sqlalchemy.orm import relationship


# Create class Post inherited from Base class
class Post(Base):
    __tablename__ = "post"  # Define the table name
    __table_args__ = {"schema": "public"}  # Define the table schema
    # Define attributes of the class according to the table column names
    id = Column(Integer, primary_key=True, name='id')
    text = Column(Text, name="text")
    topic = Column(Text, name="topic")


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "public"}
    id = Column(Integer, primary_key=True, name="id")
    gender = Column(Integer, name="gender")
    age = Column(Integer, name="age")
    country = Column(Text, name="country")
    city = Column(Text, name="city")
    exp_group = Column(Integer, name="exp_group")
    os = Column(Text, name="os")
    source = Column(Text, name="source")


class Feed(Base):
    __tablename__ = "feed_data"
    __table_args__ = {"schema": "public"}
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    post_id = Column(Integer, ForeignKey(Post.id), primary_key=True)
    action = Column(Text)
    time = Column(TIMESTAMP, name='timestamp')
    user = relationship("User")
    post = relationship("Post")

#
# if __name__ == '__main__':
#     with SessionLocal() as db:
#         result = db.query(User).filter(User.id == 210).all()
#         for x in result:
#             print(x.id, x.country)