from fastapi import APIRouter, Depends, status
from typing import List
from pydantic import UUID4

# in project
from api.dependencies import get_mongo_db, get_redis_session
from domain.value_objects import vo_User, vo_Job, vo_JobCreate, vo_Task
from .users import current_active_user
from infrastructure.MongoDB_repo import MongoDB_repo
from infrastructure.Redis_repo import Redis_repo

router = APIRouter()


@router.get("/jobs/{job_id}", tags=["jobs"], response_model=vo_Job)
def get_job(job_id: UUID4,
            user: vo_User = Depends(current_active_user),
            db=Depends(get_mongo_db)):
    mongo_repo = MongoDB_repo(db)
    return mongo_repo.get_job(user.id, job_id)


@router.get("/jobs", tags=["jobs"], response_model=List[vo_Job])
def list_jobs(user: vo_User = Depends(current_active_user),
              db=Depends(get_mongo_db)):
    mongo_repo = MongoDB_repo(db)
    return mongo_repo.list_jobs(user.id)


@router.post("/jobs",
             tags=["jobs"],
             status_code=status.HTTP_201_CREATED,
             response_model=vo_Job)
def add_job(msg: vo_JobCreate,
            user: vo_User = Depends(current_active_user),
            db=Depends(get_mongo_db)):
    mongo_repo = MongoDB_repo(db)
    job = vo_Job(**msg.dict(), by_user_id=user.id)
    this_job = mongo_repo.add_job(user.id, job)
    return this_job


@router.post("/jobs/{job_id}/run", tags=["jobs"], response_model=vo_Job)
def run_job(job_id: UUID4,
            user: vo_User = Depends(current_active_user),
            db=Depends(get_mongo_db),
            session=Depends(get_redis_session)):
    mongo_repo = MongoDB_repo(db)
    redis_repo = Redis_repo(session)
    job = mongo_repo.get_job(user.id, job_id)
    for task_id in job['tasks_id']:
        task = mongo_repo.get_task(user.id, task_id)
        redis_repo.publish(str(user.id), vo_Task(**task))
    return job


@router.put("/jobs/{job_id}", tags=["jobs"], response_model=vo_Job)
def update_job(job_id: UUID4,
               msg: vo_JobCreate,
               user: vo_User = Depends(current_active_user),
               db=Depends(get_mongo_db)):
    mongo_repo = MongoDB_repo(db)
    return mongo_repo.update_job(user.id, job_id, msg)


@router.delete("/jobs/{job_id}", tags=["jobs"])
def delete_job(job_id: UUID4,
               user: vo_User = Depends(current_active_user),
               db=Depends(get_mongo_db)):
    mongo_repo = MongoDB_repo(db)
    mongo_repo.delete_job(user.id, job_id)
    return None
