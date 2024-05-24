from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import UUID4
from typing import List

# in project
from api.dependencies import get_mongo_db
from domain.value_objects import vo_User, enum_Map
from .users import current_active_user
from infrastructure.MongoDB_repo import MongoDB_repo

router = APIRouter()


@router.get("/maps", tags=["maps"], response_model=List[str])
def list_maps(user: vo_User = Depends(current_active_user)):
    # TODO: write maps into database
    map_list = [item.value for item in list(enum_Map)]
    return map_list
