from domain.value_objects import vo_Task
from infrastructure.session_maker import redis_session
from infrastructure.Redis_repo import Redis_repo
import uuid

one_task = vo_Task(use_scenario="this is a test",
                   ads="autoware",
                   time_limit=2,
                   status="ok",
                   id=uuid.uuid4(),
                   by_user_id=uuid.uuid4(),
                   result="done")

r = Redis_repo(redis_session())
r.publish("task", one_task)