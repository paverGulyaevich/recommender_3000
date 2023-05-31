from database import Base, SessionLocal  # Import Base model from database.py module
from sqlalchemy import Text, Integer, Column  # Import types
from sqlalchemy.orm import relationship


# Create class Post inherited from Base class
class Post(Base):
    __tablename__ = "post_text_df"  # Define the table name
    __table_args__ = {"schema": "public"}  # Define the table schema
    # Define attributes of the class according to the table column names
    id = Column(Integer, primary_key=True, name='post_id')
    text = Column(Text, name="text")
    topic = Column(Text, name="topic")


    def __repr__(self):
        return f"Post(id={self.id}, topic={self.topic})"


# if __name__ == '__main__':
#     with SessionLocal() as session:
#         business_topics = session.query(Post).filter(Post.topic == 'business').order_by(Post.id.desc()).limit(10).all()
#         print([b_topic.id for b_topic in business_topics])