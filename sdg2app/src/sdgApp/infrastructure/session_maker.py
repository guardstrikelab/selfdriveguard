from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from pymongo.database import Database
from pymongo import MongoClient
import walrus
from typing import Tuple
from common.conf_parser import get_conf
'''redis session'''


def redis_session() -> walrus.Database:
    conf = get_conf()
    host = str(conf['Queue Redis']['host'])
    port = int(conf['Queue Redis']['port'])
    db = int(conf['Queue Redis']['db'])
    password = str(conf['Queue Redis']['password'])
    session = walrus.Database(host=host,
                              port=port,
                              db=db,
                              decode_responses=True,
                              password=password)
    session.ping()
    return session


'''mongo session'''


def mongo_session() -> Tuple[MongoClient, Database]:
    conf = get_conf()
    uri = conf['DB Mongo']['connection_string']
    db_name = str(conf['DB Mongo']['db_name'])
    client = MongoClient(uri, uuidRepresentation="standard")
    db = client[db_name]
    return client, db


'''user session'''


def mongo_user_session(
) -> Tuple[AsyncIOMotorDatabase, AsyncIOMotorCollection]:
    conf = get_conf()
    uri = conf['DB Mongo']['connection_string']
    db_name = str(conf['DB Mongo']['db_name'])
    client = AsyncIOMotorClient(uri, uuidRepresentation="standard")
    db = client[db_name]
    collection = db['users']
    return db, collection
