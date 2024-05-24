from fastapi import APIRouter, Depends, status
from typing import List, Optional
from pydantic import UUID4

# in project
from api.dependencies import get_mongo_db
from domain.value_objects import vo_User, vo_Task, vo_TaskCreate, vo_TaskUpdate
from .users import current_active_user
from infrastructure.MongoDB_repo import MongoDB_repo

router = APIRouter()


@router.get("/tasks/{task_id}", tags=["tasks"], response_model=vo_Task)
def get_task(task_id: UUID4,
             user: vo_User = Depends(current_active_user),
             db=Depends(get_mongo_db)):
    mongo_repo = MongoDB_repo(db)
    return mongo_repo.get_task(user.id, task_id)


@router.post("/tasks",
             tags=["tasks"],
             status_code=status.HTTP_201_CREATED,
             response_model=vo_Task)
def add_task(msg: vo_TaskCreate,
             user: vo_User = Depends(current_active_user),
             db=Depends(get_mongo_db)):
    mongo_repo = MongoDB_repo(db)
    task = vo_Task(**msg.dict(), by_user_id=user.id)
    return mongo_repo.add_task(user.id, task)


@router.put("/tasks/{task_id}", tags=["tasks"], response_model=vo_Task)
def update_task(task_id: UUID4,
                msg: vo_TaskUpdate,
                user: vo_User = Depends(current_active_user),
                db=Depends(get_mongo_db)):
    mongo_repo = MongoDB_repo(db)
    return mongo_repo.update_task(user.id, task_id, msg)


@router.delete("/tasks/{task_id}", tags=["tasks"])
def delete_task(task_id: UUID4,
                user: vo_User = Depends(current_active_user),
                db=Depends(get_mongo_db)):
    mongo_repo = MongoDB_repo(db)
    mongo_repo.delete_task(user.id, task_id)
    return None


@router.get("/tasks", tags=["tasks"], response_model=List[vo_Task])
def list_tasks(user: vo_User = Depends(current_active_user),
               db=Depends(get_mongo_db),
               status: Optional[str] = None):
    mongo_repo = MongoDB_repo(db)
    return mongo_repo.list_tasks(user.id, status)
