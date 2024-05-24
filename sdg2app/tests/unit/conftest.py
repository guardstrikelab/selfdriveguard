import pytest
from ..mock.mongo_mock_db import MongoMockDB
import fakeredis

# in project
try:
    from os.path import abspath, join, dirname
    import sys
    src_path = join(abspath((dirname(dirname(dirname(__file__))))), 'src')
    sys.path.insert(0, join(src_path, 'sdgApp'))
    from main import app
    from domain.value_objects import vo_User
    # from api.routers.users import current_active_user
    # from api.dependencies import get_mongo_db
    print(get_mongo_db)
except:
    print("Import Failed!")


@pytest.fixture(scope="function")
def app_and_db_and_user():
    # TODO: I have no idea but if current_active_user and get_mongo_db are not imported here
    # Aliyun Codeup's workflow won't find them as valid variables
    from api.routers.users import current_active_user
    from api.dependencies import get_mongo_db
    from api.dependencies import get_redis_session
    mongoMockDB = MongoMockDB()
    fake_redis = fakeredis.FakeRedis()

    async def override_get_mongo_db():
        yield mongoMockDB.db

    app.dependency_overrides[get_mongo_db] = override_get_mongo_db

    user_db = mongoMockDB.db.users.find_one({})
    user = vo_User(**user_db)

    async def override_current_active_user():
        yield user

    app.dependency_overrides[
        current_active_user] = override_current_active_user

    async def override_get_redis_session():
        yield fake_redis

    app.dependency_overrides[get_redis_session] = override_get_redis_session
    return app, mongoMockDB, user, fake_redis
