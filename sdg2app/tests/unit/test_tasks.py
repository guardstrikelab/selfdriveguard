from fastapi.testclient import TestClient
import uuid
from fastapi.encoders import jsonable_encoder

# in project
try:
    from os.path import abspath, join, dirname
    import sys
    sys.path.insert(
        0, join(abspath((dirname(dirname(dirname(__file__))))), 'src'))
    from sdgApp.domain.value_objects import vo_Task, vo_TaskCreate, vo_TaskUpdate
except Exception as exception:
    print("Import Failed:{}".format(exception))


def test_get_task(app_and_db_and_user):
    app, mongoMockDB, _, _ = app_and_db_and_user
    # get test data
    this_task_db = mongoMockDB.db.tasks.find_one({})
    this_task = vo_Task(**this_task_db)

    # perform test
    with TestClient(app) as client:
        response = client.get("/tasks/{}".format(str(this_task.id)))
    assert response.status_code == 200
    assert vo_Task(**response.json()) == this_task


def test_add_task(app_and_db_and_user):
    app, mongoMockDB, _, _ = app_and_db_and_user
    # get test data
    this_task_db = mongoMockDB.db.tasks.find_one({})
    this_task = vo_TaskCreate(**this_task_db)
    this_task.time_limit = 120
    # perform test
    with TestClient(app) as client:
        response = client.post("/tasks", json=jsonable_encoder(this_task))
    assert response.status_code == 201
    new_task = vo_Task(**response.json())
    assert vo_TaskCreate(**new_task.dict()) == this_task
    new_task_db = mongoMockDB.db.tasks.find_one({"id": new_task.id})
    assert new_task_db is not None

    # test use_scenario is None
    this_task.use_scenario = None
    with TestClient(app) as client:
        response = client.post("/tasks", json=jsonable_encoder(this_task))
    assert response.status_code == 201
    new_task = vo_Task(**response.json())
    assert new_task.use_scenario is not None

    # test use_scenario is None and no use_scenario_id
    this_task.use_scenario = None
    this_task.use_scenario_id = None
    with TestClient(app) as client:
        response = client.post("/tasks", json=jsonable_encoder(this_task))
    assert response.status_code == 201
    assert response.json() is None


def test_delete_task(app_and_db_and_user):
    app, mongoMockDB, user, _ = app_and_db_and_user
    # get test data
    this_task_db = mongoMockDB.db.tasks.find_one({})

    # delete task
    with TestClient(app) as client:
        response = client.delete("/tasks/{}".format(str(this_task_db["id"])))
    assert response.status_code == 200
    assert mongoMockDB.db.tasks.find_one({"id": this_task_db["id"]}) is None


def test_update_task(app_and_db_and_user):
    app, mongoMockDB, user, _ = app_and_db_and_user

    # get test data
    this_task_db = mongoMockDB.db.tasks.find_one({})
    this_task = vo_TaskUpdate(
        **mongoMockDB.db.tasks.find_one({"id": this_task_db["id"]}))
    this_task.time_limit = 120
    # perform test
    with TestClient(app) as client:
        response = client.put("/tasks/{}".format(str(this_task_db["id"])),
                              json=jsonable_encoder(this_task))
    assert response.status_code == 200

    # should return the updated task
    new_task = vo_Task(**response.json())
    assert vo_TaskUpdate(**new_task.dict()) == this_task
    this_task_db = mongoMockDB.db.tasks.find_one({"id": this_task_db["id"]})
    assert vo_TaskUpdate(**this_task_db) == this_task


def test_list_tasks(app_and_db_and_user):
    app, mongoMockDB, user, _ = app_and_db_and_user
    # get test data
    task_collection = mongoMockDB.db.tasks
    task_list = list(task_collection.find({"by_user_id": user.id}))

    # perform test
    with TestClient(app) as client:
        response = client.get("/tasks")
    assert response.status_code == 200
    task_list_response = [vo_Task(**t) for t in response.json()]
    assert len(task_list) == len(response.json())
    for task in task_list:
        assert vo_Task(**task) in task_list_response
