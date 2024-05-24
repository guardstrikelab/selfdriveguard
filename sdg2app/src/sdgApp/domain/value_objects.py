from pydantic import BaseModel, UUID4, validator
from typing import List, Optional, Any
from enum import Enum
from fastapi_users import models
import uuid


class vo_ScenFolderBase(BaseModel):
    name: str
    desc: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "folder_name",
                "desc": "Something about this folder"
            }
        }


class vo_ScenSubFolder(vo_ScenFolderBase):
    id: UUID4

    class Config:
        schema_extra = {
            "example": {
                **vo_ScenFolderBase.__config__.schema_extra['example'], "id":
                uuid.uuid4()
            }
        }


class enum_Language(str, Enum):
    cartel = 'cartel'
    scenic = 'scenic'


class enum_Map(str, Enum):
    Town01 = 'Town01'
    Town02 = 'Town02'
    Town03 = 'Town03'
    Town04 = 'Town04'
    Town05 = 'Town05'
    Town06 = 'Town06'
    Town07 = 'Town07'
    Town08 = 'Town08'
    Town09 = 'Town09'
    Town10 = 'Town10'


class vo_ScenarioBase(BaseModel):
    script: str
    language: enum_Language
    map_name: enum_Map
    name: str
    desc: Optional[str] = None
    tags: Optional[List[str]] = []
    categories: Optional[List[str]] = []

    class Config:
        schema_extra = {
            "example": {
                "script": "This is a demo script",
                "language": enum_Language.cartel,
                "map_name": enum_Map.Town03,
                "name": "Demo No.1",
                "desc": "A normal scenario desc(optional)",
                "tags": ['tag1', 'tag2'],
                "categories": ['cat1', 'cat2']
            }
        }


class vo_ScenarioCreate(vo_ScenarioBase):
    pass


class vo_ScenarioUpdate(vo_ScenarioBase):
    pass


class vo_ScenarioDB(vo_ScenarioBase):
    id: Optional[UUID4]
    by_user_id: UUID4

    @validator("id", pre=True, always=True)
    def default_id(cls, v):
        return v or uuid.uuid4()

    class Config:
        schema_extra = {
            "example": {
                **vo_ScenarioBase.__config__.schema_extra['example'],
                "id": uuid.uuid4(),
                "by_user_id": uuid.uuid4()
            }
        }


class vo_Scenario(vo_ScenarioDB):
    in_folder: vo_ScenSubFolder

    class Config:
        schema_extra = {
            "example": {
                **vo_ScenarioDB.__config__.schema_extra['example'], "in_folder":
                vo_ScenSubFolder.__config__.schema_extra['example']
            }
        }


class vo_ScenFolderCreate(vo_ScenFolderBase):
    pass


class vo_ScenFolderUpdate(vo_ScenFolderBase):
    pass


class vo_ScenFolderDB(vo_ScenFolderBase):
    id: Optional[UUID4]
    scenarios_id: Optional[List[UUID4]] = []
    subfolders_id: Optional[List[UUID4]] = []
    by_user_id: UUID4

    @validator("id", pre=True, always=True)
    def default_id(cls, v):
        return v or uuid.uuid4()

    class Config:
        schema_extra = {
            "example": {
                **vo_ScenFolderBase.__config__.schema_extra['example'], "id":
                uuid.uuid4(),
                "scenarios_id": [uuid.uuid4(), uuid.uuid4()],
                "subfolders_id": [uuid.uuid4(), uuid.uuid4()],
                "by_user_id": uuid.uuid4()
            }
        }


class vo_ScenFolder(vo_ScenFolderDB):
    scenarios: Optional[List[vo_ScenarioDB]] = []
    subfolders: Optional[List[vo_ScenSubFolder]] = []

    class Config:
        schema_extra = {
            "example": {
                **vo_ScenFolderDB.__config__.schema_extra['example'],
                "id": uuid.uuid4(),
                "scenarios": [vo_ScenarioDB.__config__.schema_extra['example']],
                "subfolders": [vo_ScenSubFolder.__config__.schema_extra['example']]
            }
        }


class enum_Ads(str, Enum):
    autoware = 'autoware'
    pylot = 'pylot'


class vo_TaskBase(BaseModel):
    use_scenario_id: Optional[UUID4]
    use_scenario: Optional[vo_ScenarioDB]
    ads: enum_Ads
    time_limit: int

    @validator('time_limit')
    def time_limit_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('must > 0')
        return v

    class Config:
        schema_extra = {
            "example": {
                "use_scenario_id": uuid.uuid4(),
                "use_scenario": vo_ScenarioDB.__config__.schema_extra['example'],
                "ads": enum_Ads.autoware,
                "time_limit": 100
            }
        }


class vo_TaskCreate(vo_TaskBase):
    pass


class vo_TaskUpdate(vo_TaskBase):
    status: str = "Ready"
    result: Optional[Any] = None  # TODO: result object
    by_job_id: Optional[UUID4] = None

    class Config:
        schema_extra = {
            "example": {
                **vo_TaskBase.__config__.schema_extra['example'],
                "status": "Ready",
                "result": "Result things",
                "by_job_id": uuid.uuid4()
            }
        }


class vo_Task(vo_TaskUpdate):
    id: Optional[UUID4] = None
    by_user_id: UUID4
    by_job_id: Optional[UUID4] = None

    @validator("id", pre=True, always=True)
    def default_id(cls, v):
        return v or uuid.uuid4()

    class Config:
        schema_extra = {
            "example": {
                **vo_TaskUpdate.__config__.schema_extra['example'],
                "id": uuid.uuid4(),
                "by_user_id": uuid.uuid4(),
                "by_job_id": uuid.uuid4(),
            }
        }


class vo_JobBase(BaseModel):
    desc: str
    tasks_id: Optional[List[UUID4]] = []

    class Config:
        schema_extra = {
            "example": {
                "desc": "A brief desc",
                "tasks_id": [uuid.uuid4(), uuid.uuid4()]
            }
        }


class vo_JobCreate(vo_JobBase):
    pass


class vo_Job(vo_JobBase):
    id: Optional[UUID4] = None
    by_user_id: UUID4
    tasks: Optional[List[vo_Task]]
    status: Optional[str] = "Ready"

    @validator("id", pre=True, always=True)
    def default_id(cls, v):
        return v or uuid.uuid4()

    class Config:
        schema_extra = {
            "example": {
                **vo_JobBase.__config__.schema_extra['example'],
                "id": uuid.uuid4(),
                "by_user_id": uuid.uuid4(),
                "tasks": [vo_Task.__config__.schema_extra['example']]
            }
        }


class vo_User(models.BaseUser):
    rootfolder: Optional[UUID4] = None


class vo_UserCreate(models.BaseUserCreate):
    pass


class vo_UserUpdate(vo_User, models.BaseUserUpdate):
    pass


class vo_UserDB(vo_User, models.BaseUserDB):
    pass
