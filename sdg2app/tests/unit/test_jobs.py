from fastapi.testclient import TestClient
import uuid
from fastapi.encoders import jsonable_encoder

# in project
try:
    from os.path import abspath, join, dirname
    import sys
    sys.path.insert(
        0, join(abspath((dirname(dirname(dirname(__file__))))), 'src'))
    from sdgApp.domain.value_objects import vo_User, vo_Job, vo_JobCreate, vo_Task
except Exception as exception:
    print("Import Failed:{}".format(exception))


def test_get_job(app_and_db_and_user):
    app, mongoMockDB, _, _ = app_and_db_and_user
    # get test data
    this_job_db = mongoMockDB.db.jobs.find_one({})
    this_job = vo_Job(**this_job_db)
    # perform test
    with TestClient(app) as client:
        response = client.get("/jobs/{}".format(str(this_job.id)))
    assert response.status_code == 200
    new_response = response.json()
    del new_response["tasks"]
    assert vo_Job(**new_response) == this_job


def test_add_job(app_and_db_and_user):
    app, mongoMockDB, user, _ = app_and_db_and_user
    # get test data
    this_job_db = mongoMockDB.db.jobs.find_one({})
    this_job = vo_JobCreate(**this_job_db)
    this_job.desc = "This is a job"
    # perform test
    with TestClient(app) as client:
        response = client.post("/jobs", json=jsonable_encoder(this_job))
    assert response.status_code == 201
    for task in response.json()["tasks"]:
        assert "by_job_id" in task
    # should return the created job
    new_job = vo_Job(**response.json())
    assert vo_JobCreate(**new_job.dict()) == this_job
    # check db data
    new_job_db = mongoMockDB.db.jobs.find_one({"id": new_job.id})
    assert new_job_db is not None
    with TestClient(app) as client:
        response = client.delete("/jobs/{}".format(str(this_job_db["id"])))
    assert response.status_code == 200
    assert mongoMockDB.db.jobs.find_one({"id": this_job_db["id"]}) is None


def test_delete_job(app_and_db_and_user):
    app, mongoMockDB, user, _ = app_and_db_and_user
    # get test data
    this_job_db = mongoMockDB.db.jobs.find_one({})
    with TestClient(app) as client:
        response = client.delete("/jobs/{}".format(str(this_job_db["id"])))
    assert response.status_code == 200
    assert mongoMockDB.db.jobs.find_one({"id": this_job_db["id"]}) is None


def test_update_job(app_and_db_and_user):
    app, mongoMockDB, user, _ = app_and_db_and_user
    # get test data
    this_job_db = mongoMockDB.db.jobs.find_one({})
    this_job = vo_JobCreate(**this_job_db)
    this_job.desc = "This is a job"
    # add job
    with TestClient(app) as client:
        response = client.post("/jobs", json=jsonable_encoder(this_job))
    assert response.status_code == 201
    for task in response.json()["tasks"]:
        assert "by_job_id" in task
    old_job = response.json()
    old_job["tasks_id"].pop()
    old_job["tasks"].pop()
    # perform test
    with TestClient(app) as client:
        response = client.put("/jobs/{}".format(str(old_job["id"])),
                              json=jsonable_encoder(vo_JobCreate(**old_job)))
    assert response.status_code == 200
    response_job = vo_Job(**response.json())
    assert vo_Job(**old_job) == response_job


def test_list_jobs(app_and_db_and_user):
    app, mongoMockDB, user, _ = app_and_db_and_user
    # get test data
    job_collection = mongoMockDB.db.jobs
    job_list = list(job_collection.find({"by_user_id": user.id}))
    # perform test
    with TestClient(app) as client:
        response = client.get("/jobs")
    assert response.status_code == 200
    job_list_response = [vo_Job(**t) for t in response.json()]
    assert len(job_list) == len(response.json())
    assert job_list_response[0].tasks is not None
    job_list_response[0].tasks = None
    for job in job_list:
        assert vo_Job(**job) in job_list_response


def test_run_job(app_and_db_and_user):
    app, mongoMockDB, user, fake_redis = app_and_db_and_user
    # get test data
    this_job_db = mongoMockDB.db.jobs.find_one({})
    this_job = vo_Job(**this_job_db)
    # perform test
    with TestClient(app) as client:
        response = client.post("/jobs/{}/run".format(str(this_job.id)))
    assert response.status_code == 200
    new_response = response.json()
    del new_response["tasks"]
    assert vo_Job(**new_response) == this_job
    for task_id in this_job.dict()['tasks_id']:
        assert fake_redis.get(str(task_id)) is not None
