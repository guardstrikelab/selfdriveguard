from abc import ABC, abstractmethod
from domain.value_objects import vo_ScenFolderDB, vo_ScenFolderCreate, vo_Scenario, vo_ScenarioDB, vo_ScenarioUpdate, vo_TaskCreate, vo_TaskUpdate, vo_JobCreate
from pydantic import UUID4


class I_DBRepo(ABC):

    # users
    @abstractmethod
    def set_root_folder(self, user_id: UUID4, folder: vo_ScenFolderDB):
        pass

    # folders
    @abstractmethod
    def add_folder(self, user_id: UUID4, parent_folder_id: UUID4,
                   folder: vo_ScenFolderCreate):
        pass

    @abstractmethod
    def delete_folder(self, user_id: UUID4, parent_folder_id: UUID4,
                      folder_id: UUID4):
        pass

    @abstractmethod
    def update_folder(self, user_id: UUID4, folder_id: UUID4,
                      folder: vo_ScenFolderCreate):
        pass

    @abstractmethod
    def get_folder(self, user_id: UUID4, folder_id: UUID4):
        pass

    @abstractmethod
    def move_folder(self, user_id: UUID4, parent_folder_id: UUID4,
                    folder_id: UUID4, another_folder_id: UUID4):
        pass

    # scenarios

    @abstractmethod
    def add_scenario(self, user_id: UUID4, folder_id: UUID4,
                     scenario: vo_ScenarioDB):
        pass

    @abstractmethod
    def update_scenario(self, user_id: UUID4, folder_id: UUID4,
                        scenario_id: UUID4, scenario: vo_ScenarioUpdate):
        pass

    @abstractmethod
    def get_scenario(self, user_id: UUID4, scenario_id: UUID4):
        pass

    @abstractmethod
    def delete_scenario(self, user_id: UUID4, folder_id: UUID4,
                        scenario_id: UUID4):
        pass

    @abstractmethod
    def move_scenario(self, user_id: UUID4, folder_id: UUID4,
                      scenario_id: UUID4, another_folder_id: UUID4):
        pass

    @abstractmethod
    def list_scenarios(self, user_id: UUID4, folder_id: UUID4,
                       recursive: bool):
        pass

    # tasks
    @abstractmethod
    def add_task(self, user_id: UUID4, task: vo_TaskCreate):
        pass

    @abstractmethod
    def delete_task(self, user_id: UUID4, task_id: UUID4):
        pass

    @abstractmethod
    def update_task(self, user_id: UUID4, task_id: UUID4, task: vo_TaskUpdate):
        pass

    @abstractmethod
    def get_task(self, user_id: UUID4, task_id: UUID4):
        pass

    @abstractmethod
    def list_tasks(self, user_id: UUID4, status: str):
        pass

    # jobs
    @abstractmethod
    def add_job(self, user_id: UUID4, job: vo_JobCreate):
        pass

    @abstractmethod
    def delete_job(self, user_id: UUID4, job_id: UUID4):
        pass

    @abstractmethod
    def update_job(self, user_id: UUID4, job_id: UUID4, job: vo_JobCreate):
        pass

    @abstractmethod
    def get_job(self, user_id: UUID4, job_id: UUID4):
        pass

    @abstractmethod
    def list_jobs(self, user_id: UUID4):
        pass


class I_QueueRepo(ABC):
    @abstractmethod
    def publish(self, queue_name, task):
        pass
