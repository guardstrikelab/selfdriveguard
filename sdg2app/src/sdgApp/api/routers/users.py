from fastapi import Request
from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import MongoDBUserDatabase

# in project
from domain.value_objects import vo_UserDB, vo_ScenFolderDB, vo_User, vo_UserCreate, vo_UserUpdate
from api.dependencies import get_user_collection, get_mongo_db_sync
from infrastructure.MongoDB_repo import MongoDB_repo

SECRET = "7165bf1355c0bddf29d0b6326af2ac9b6e876ee8514c93ae887796c540e33ddf"

# TODO: optimize the way to get db
user_db, collection = get_user_collection()
user_db = MongoDBUserDatabase(vo_UserDB, collection)


def on_after_register(user: vo_UserDB, request: Request):
    # create default root folder
    db = get_mongo_db_sync()
    mongo_repo = MongoDB_repo(db)
    folder = mongo_repo.add_folder(
        user.id, None, vo_ScenFolderDB(name="root", by_user_id=user.id))
    mongo_repo.set_root_folder(user.id, folder)


def on_after_forgot_password(user: vo_UserDB, token: str, request: Request):
    print(f"User {user.id} has forgot their password. Reset token: {token}")


def after_verification_request(user: vo_UserDB, token: str, request: Request):
    print(
        f"Verification requested for user {user.id}. Verification token: {token}"
    )


jwt_authentication = JWTAuthentication(secret=SECRET,
                                       lifetime_seconds=3600,
                                       tokenUrl="auth/jwt/login")

router = APIRouter()
fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    vo_User,
    vo_UserCreate,
    vo_UserUpdate,
    vo_UserDB,
)

# Depends
current_active_user = fastapi_users.current_user(active=True)

router.include_router(fastapi_users.get_auth_router(jwt_authentication),
                      prefix="/auth/jwt",
                      tags=["auth"])
router.include_router(fastapi_users.get_register_router(on_after_register),
                      prefix="/auth",
                      tags=["auth"])
router.include_router(
    fastapi_users.get_reset_password_router(
        SECRET, after_forgot_password=on_after_forgot_password),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(
        SECRET, after_verification_request=after_verification_request),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(fastapi_users.get_users_router(),
                      prefix="/users",
                      tags=["users"])
