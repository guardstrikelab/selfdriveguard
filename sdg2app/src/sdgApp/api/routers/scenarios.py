from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import UUID4
from typing import List

# in project
from api.dependencies import get_mongo_db
from domain.value_objects import vo_User, vo_Scenario, vo_ScenarioDB, vo_ScenarioCreate, vo_ScenarioUpdate, vo_ScenFolder, vo_ScenFolderDB, vo_ScenFolderCreate
from .users import current_active_user
from infrastructure.MongoDB_repo import MongoDB_repo

router = APIRouter()


@router.get("/scenarios/{scenario_id}",
            tags=["scenarios"],
            response_model=vo_Scenario)
def get_scenario(scenario_id: UUID4,
                 user: vo_User = Depends(current_active_user),
                 db=Depends(get_mongo_db)):
    mongo_repo = MongoDB_repo(db)
    return mongo_repo.get_scenario(user.id, scenario_id)


@router.get("/scen-folders/{folder_id}/scenarios",
            tags=["scenarios"],
            response_model=List[vo_ScenarioDB])
def list_scenarios(folder_id: UUID4,
                   recursive: bool = True,
                   user: vo_User = Depends(current_active_user),
                   db=Depends(get_mongo_db)):
    mongo_repo = MongoDB_repo(db)
    return mongo_repo.list_scenarios(user.id, folder_id, recursive)


@router.post("/scen-folders/{folder_id}/scenarios",
             tags=["scenarios"],
             status_code=status.HTTP_201_CREATED,
             response_model=vo_Scenario)
def add_scenario(folder_id: UUID4,
                 msg: vo_ScenarioCreate,
                 user: vo_User = Depends(current_active_user),
                 db=Depends(get_mongo_db)):
    mongo_repo = MongoDB_repo(db)
    scenario = vo_ScenarioDB(**msg.dict(), by_user_id=user.id)
    return mongo_repo.add_scenario(user.id, folder_id, scenario)


@router.put("/scen-folders/{folder_id}/scenarios/{scenario_id}",
            tags=["scenarios"],
            response_model=vo_Scenario)
def update_scenario(folder_id: UUID4,
                    scenario_id: UUID4,
                    msg: vo_ScenarioUpdate,
                    user: vo_User = Depends(current_active_user),
                    db=Depends(get_mongo_db)):
    mongo_repo = MongoDB_repo(db)
    return mongo_repo.update_scenario(user.id, folder_id, scenario_id, msg)


@router.patch(
    "/scen-folders/{folder_id}/scenarios/{scenario_id}/move-to/another-folder/{another_folder_id}",
    tags=["scenarios"],
    response_model=vo_ScenFolder)
def move_scenario(folder_id: UUID4,
                  scenario_id: UUID4,
                  another_folder_id: UUID4,
                  user: vo_User = Depends(current_active_user),
                  db=Depends(get_mongo_db)):
    mongo_repo = MongoDB_repo(db)
    return mongo_repo.move_scenario(user.id, folder_id, scenario_id,
                                    another_folder_id)


@router.delete("/scen-folders/{folder_id}/scenarios/{scenario_id}",
               tags=["scenarios"],
               status_code=status.HTTP_204_NO_CONTENT)
def delete_scenario(folder_id: UUID4,
                    scenario_id: UUID4,
                    user: vo_User = Depends(current_active_user),
                    db=Depends(get_mongo_db)):
    mongo_repo = MongoDB_repo(db)
    mongo_repo.delete_scenario(user.id, folder_id, scenario_id)
    return None


@router.get("/scen-folders/{folder_id}",
            tags=["scen-folders"],
            response_model=vo_ScenFolder)
def get_folder(folder_id: UUID4,
               user: vo_User = Depends(current_active_user),
               db=Depends(get_mongo_db)):
    mongo_repo = MongoDB_repo(db)
    return mongo_repo.get_folder(user.id, folder_id)


@router.post("/scen-folders/{parent_folder_id}/sub-folders",
             tags=["scen-folders"],
             status_code=status.HTTP_201_CREATED,
             response_model=vo_ScenFolder)
def add_folder(parent_folder_id: UUID4,
               msg: vo_ScenFolderCreate,
               user: vo_User = Depends(current_active_user),
               db=Depends(get_mongo_db)):
    mongo_repo = MongoDB_repo(db)
    folder = vo_ScenFolderDB(**msg.dict(), by_user_id=user.id)
    return mongo_repo.add_folder(user.id, parent_folder_id, folder)


@router.put("/scen-folders/{folder_id}",
            tags=["scen-folders"],
            response_model=vo_ScenFolder)
def update_folder(folder_id: UUID4,
                  msg: vo_ScenFolderCreate,
                  user: vo_User = Depends(current_active_user),
                  db=Depends(get_mongo_db)):
    mongo_repo = MongoDB_repo(db)
    if user.rootfolder == folder_id:
        raise HTTPException(status_code=409,
                            detail="Root folder can not be updated")
    else:
        return mongo_repo.update_folder(user.id, folder_id, msg)


@router.patch(
    "/scen-folders/{parent_folder_id}/sub-folders/{folder_id}/move-to/another-folder/{another_folder_id}",
    tags=["scen-folders"],
    response_model=vo_ScenFolder)
def move_folder(parent_folder_id: UUID4,
                folder_id: UUID4,
                another_folder_id: UUID4,
                user: vo_User = Depends(current_active_user),
                db=Depends(get_mongo_db)):
    mongo_repo = MongoDB_repo(db)
    if user.rootfolder == folder_id:
        raise HTTPException(status_code=409,
                            detail="Root folder can not be moved")
    else:
        return mongo_repo.move_folder(user.id, parent_folder_id, folder_id,
                                      another_folder_id)


@router.delete("/scen-folders/{parent_folder_id}/sub-folders/{folder_id}",
               tags=["scen-folders"],
               status_code=status.HTTP_204_NO_CONTENT)
def delete_folder(parent_folder_id: UUID4,
                  folder_id: UUID4,
                  user: vo_User = Depends(current_active_user),
                  db=Depends(get_mongo_db)):
    mongo_repo = MongoDB_repo(db)
    if user.rootfolder == folder_id:
        raise HTTPException(status_code=409,
                            detail="Root folder can not be deleted")
    mongo_repo.delete_folder(user.id, parent_folder_id, folder_id)
    return None
