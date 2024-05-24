'''read conf.ini'''
from infrastructure.session_maker import redis_session, mongo_session, mongo_user_session


async def get_redis_session():
    session = redis_session()
    try:
        yield session
    finally:
        session.close()


async def get_mongo_db():
    client, db = mongo_session()
    try:
        yield db
    finally:
        client.close()


def get_mongo_db_sync():
    client, db = mongo_session()
    return db


def get_user_collection():
    db, collection = mongo_user_session()
    return db, collection
