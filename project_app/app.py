# Import all the libraries required
import os
import pandas as pd
import hashlib
from catboost import CatBoostClassifier, Pool
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, Text, Integer, Column, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from typing import List
from datetime import datetime
from pydantic import BaseModel
from loguru import logger

# Create a URL object to connect to Database
SQLALCHEMY_DATABASE_URL = "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml"
# Create an engine object and link it to the URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Instantiate a Session maker object used to create sessions with required parameters
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Create a parental class Base from which other ORM classes will inherit
Base = declarative_base()


# Create classes validating the output of a query
class PostGet(BaseModel):
    id: int
    text: str
    topic: str

    class Config:
        orm_mode = True


class Response(BaseModel):
    exp_group: str
    recommendations: List[PostGet]


# Create ORM classes from Database
class User(Base):
    __tablename__ = "user_data"  # Define table's name
    __table_args__ = {"schema": "public"}  # Define table's schema
    # Define class' attributes according to the DB's table column names
    id = Column(Integer, primary_key=True, name="user_id")
    gender = Column(Integer, name="gender")
    age = Column(Integer, name="age")
    country = Column(Text, name="country")
    city = Column(Text, name="city")
    exp_group = Column(Integer, name="exp_group")
    os = Column(Text, name="os")
    source = Column(Text, name="source")


class Post(Base):
    __tablename__ = "post_text_df"
    __table_args__ = {"schema": "public"}
    id = Column(Integer, primary_key=True, name='post_id')
    text = Column(Text, name="text")
    topic = Column(Text, name="topic")


class Feed(Base):
    __tablename__ = "feed_data"
    __table_args__ = {"schema": "public"}
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    post_id = Column(Integer, ForeignKey(Post.id), primary_key=True)
    action = Column(Text)
    time = Column(TIMESTAMP, name='timestamp')
    user = relationship("User")
    post = relationship("Post")


app = FastAPI()


# Function that facilitates downloading huge datasets to pandas by splitting them into batches/chunks
def batch_load_sql(query: str):
    engine = create_engine("postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml")
    conn = engine.connect().execution_options(
        stream_results=True)
    chunks = []
    for chunk_df in pd.read_sql(query, conn, chunksize=200000):
        chunks.append(chunk_df)
        logger.info(f'Got chunk: {len(chunk_df)}')
    conn.close()
    return pd.concat(chunks, ignore_index=True)


# Getting the control model path
def get_model_path_control(path: str) -> str:
    if os.environ.get("IS_LMS") == "1":
        model_path = '/workdir/user_input/model_control'
    else:
        model_path = path
    return model_path


# Getting the test model path
def get_model_path_test(path: str) -> str:
    if os.environ.get("IS_LMS") == "1":
        model_path = '/workdir/user_input/model_test'
    else:
        model_path = path
    return model_path


# Load-features function
def load_features():
    logger.info("loading liked posts")

    # Query unique entries post_id, user_id with likes
    liked_posts_query = """
    SELECT DISTINCT post_id, user_id
    FROM public.feed_data
    WHERE action = 'like'
    """
    liked_posts = batch_load_sql(liked_posts_query)

    logger.info('loading posts features with TF-IDF')

    # Query TF-IDF posts' features
    posts_features_tfidf = pd.read_sql(
        """
        SELECT *
        FROM public.pg_posts_features_tfidf
        """,
        con="postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml"
    )

    logger.info('loading posts features with BERT embeddings')

    # Query BERT posts' features
    posts_features_bertemb = pd.read_sql(
        """
        SELECT *
        FROM public.pg_posts_features_bertemb
        """,
        con="postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml"
    )

    logger.info("loading user features")

    # Query users' features
    user_features = pd.read_sql(
        """
        SELECT *
        FROM public.user_data
        """,
        con="postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml"
    )
    return [liked_posts, posts_features_tfidf, posts_features_bertemb, user_features]


# Load-models function
def load_models():
    # Specify the control model's path
    model_path_control = get_model_path_control("D:\start_ml\my_project\project_app\my_models\catboost_model_tfidf")
    # Specify the test model's path
    model_path_test = get_model_path_test("D:\start_ml\my_project\project_app\my_models\catboost_model_bertemb")

    loaded_model_control = CatBoostClassifier()
    loaded_model_test = CatBoostClassifier()
    loaded_model_control.load_model(model_path_control)
    loaded_model_test.load_model(model_path_test)
    return loaded_model_control, loaded_model_test


logger.info("loading model")
model_control = load_models()[0]  # loading control model
model_test = load_models()[1]  # loading test model
logger.info('loading features')
features = load_features()
logger.info('Service is up and running')


# Splitting users into test and control groups for A/B test
def get_exp_group(user_id: int, salt='my_salt', ab_size=50) -> str:
    encoded_id = int(hashlib.md5((str(user_id) + salt).encode()).hexdigest(), 16) % 100  # Encode user's id with salt
    if encoded_id >= ab_size:
        return 'test'
    else:
        return 'control'


# Get-recommended-feed function
def get_recommended_feed(id: int, time: datetime, limit: int):
    logger.info(f'user_id: {id}')
    logger.info('reading features')

    # Load users' features
    user_features = features[3].loc[features[3].user_id == id]
    user_features = user_features.drop('user_id', axis=1)

    # Load posts' features depending on the user's experimental group
    logger.info('dropping columns')
    exp_group = get_exp_group(id)
    if exp_group == 'control':
        posts_features = features[1].drop(['text'], axis=1)
        content = features[1][['post_id', 'text', 'topic']]
    elif exp_group == 'test':
        posts_features = features[2].drop(['text'], axis=1)
        content = features[1][['post_id', 'text', 'topic']]
    else:
        raise ValueError('unknown group')

    logger.info("zipping everything")
    # Concatenate users' and posts' features
    # Create a dictionary of user's features by the user's id
    add_user_features = dict(zip(user_features.columns,  # -> Get dict like:
                                 user_features.values[0]))  # {'gender': 1, 'age': 34, 'country': Russia...} and so on
    logger.info("assigning everything")
    # Assign data from the dict to posts_features table.
    user_posts_features = posts_features.assign(**add_user_features)  # ->all the posts with regard to a certain user id
    user_posts_features = user_posts_features.set_index('post_id')

    # Add time data to the features
    logger.info('add time info')
    user_posts_features['hour'] = time.hour
    user_posts_features['month'] = time.month

    # Get predicted probabilities that a certain user will like each of the posts
    logger.info('predicting')
    # Create Pool constructor to transform categorical features to numerical data.
    if exp_group == 'control':
        logger.info('applying model_control')
        pooled_features = Pool(user_posts_features,
                               cat_features=['topic', 'gender', 'country',
                                             'city', 'exp_group', 'hour', 'TextCluster',
                                             'month', 'os', 'source'])
        predicts = model_control.predict_proba(pooled_features)[:, 1]
    elif exp_group == 'test':
        logger.info('applying model_test')
        pooled_features = Pool(user_posts_features,
                               cat_features=['topic', 'gender', 'country',
                                             'city', 'exp_group', 'hour', 'TextCluster',
                                             'month', 'os', 'source'])
        predicts = model_test.predict_proba(pooled_features)[:, 1]
    else:
        raise ValueError('Unknown group')

    user_posts_features['predictions'] = predicts

    # Remove entries/posts from user_posts_features that were already liked by a user.
    # There should be only the posts that a user hasn't liked yet.
    logger.info('removing liked posts')
    liked_posts = features[0]
    liked_posts = liked_posts[liked_posts.user_id == id].post_id.values
    filtered_ = user_posts_features[~user_posts_features.index.isin(liked_posts)]

    # Recommend top-5 posts (with the highest probabilities of being liked) to a user
    recommended_posts = filtered_.sort_values('predictions')[-limit:].index

    return {'exp_group': exp_group,
            'recommendations': [
                PostGet(**{
                    "id": i,
                    "text": content[content.post_id == i].text.values[0],
                    "topic": content[content.post_id == i].topic.values[0]
                }) for i in recommended_posts
            ]
            }


# GET-request to obtain top-5 relevant posts that a user might like
@app.get("/post/recommendations", response_model=Response)
async def get_recommended_posts(
        id: int = 1000,
        time: datetime = datetime(year=2021, month=12, day=25),
        limit: int = 5
):
    if id not in features[3]['user_id'].values:
        raise HTTPException(status_code=404, detail="User not found")
    return get_recommended_feed(id, time, limit)
