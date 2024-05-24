from infrastructure.interface import I_QueueRepo
from domain.value_objects import vo_Task
from walrus import Database


class Redis_repo(I_QueueRepo):
    def __init__(self, session: Database):
        self.session = session

    def publish(self, queue_name: str, task: vo_Task):
        self.session.set(str(task.id), task.json())
        self.session.lpush(queue_name, str(task.id))
