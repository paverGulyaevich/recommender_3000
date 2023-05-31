from database import Base, SessionLocal
from sqlalchemy import Column, Integer, Text, func


class User(Base):
    __tablename__ = "user_data"
    __table_args__ = {"schema": "public"}
    id = Column(Integer, primary_key=True, name="user_id")
    gender = Column(Integer, name="gender")
    age = Column(Integer, name="age")
    country = Column(Text, name="country")
    city = Column(Text, name="city")
    exp_group = Column(Integer, name="exp_group")
    os = Column(Text, name="os")
    source = Column(Text, name="source")


# if __name__ == "__main__":
#     with SessionLocal() as session:
#         count_ = func.count(User.id)
#         result = session.query(User.country, User.os, count_) \
#             .filter(User.exp_group == 3) \
#             .group_by(User.country, User.os) \
#             .having(count_ > 100) \
#             .order_by(count_.desc()) \
#             .all()
#         print(result)
