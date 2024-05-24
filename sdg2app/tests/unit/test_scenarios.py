from fastapi.testclient import TestClient
import uuid
from fastapi.encoders import jsonable_encoder

# in project
try:
    from os.path import abspath, join, dirname
    import sys
    sys.path.insert(
        0, join(abspath((dirname(dirname(dirname(__file__))))), 'src'))
    from sdgApp.domain.value_objects import vo_Scenario, vo_ScenarioDB, vo_ScenarioCreate, vo_ScenarioUpdate, vo_ScenFolder, vo_ScenFolderDB, vo_ScenSubFolder, vo_ScenFolderCreate
except Exception as exception:
    print("Import Failed:{}".format(exception))


def test_get_scenario(app_and_db_and_user):
    app, mongoMockDB, user, _ = app_and_db_and_user
    # get test data
    this_scenario_db = mongoMockDB.db.scenarios.find_one({})
    this_scenario = vo_ScenarioDB(**this_scenario_db)

    # perform test
    with TestClient(app) as client:
        response = client.get("/scenarios/{}".format(str(this_scenario.id)))
    assert response.status_code == 200
    assert vo_ScenarioDB(**response.json()) == this_scenario

    # in_folder is in response
    in_folder_db = mongoMockDB.db.folders.find_one({
        "by_user_id":
        user.id,
        "scenarios_id":
        this_scenario.id
    })
    in_folder = vo_ScenSubFolder(**in_folder_db)
    assert in_folder == vo_Scenario(**response.json()).in_folder


def test_add_scenario(app_and_db_and_user):
    app, mongoMockDB, user, _ = app_and_db_and_user
    # get test data
    this_scenario_db = mongoMockDB.db.scenarios.find_one({})
    this_scenario = vo_ScenarioCreate(**this_scenario_db)
    this_scenario.name += "tail"

    # perform test
    # add this_scenario to rootfolder
    with TestClient(app) as client:
        response = client.post("/scen-folders/{}/scenarios".format(
            str(user.rootfolder)),
                               json=jsonable_encoder(this_scenario))
    assert response.status_code == 201

    # should return the created scenario
    new_scenario = vo_ScenarioDB(**response.json())
    assert vo_ScenarioCreate(**new_scenario.dict()) == this_scenario
    # check db data
    new_scenario_db = mongoMockDB.db.scenarios.find_one(
        {"id": new_scenario.id})
    assert new_scenario_db is not None

    # this scenario should be added to the folder's scenario list
    this_folder_db = mongoMockDB.db.folders.find_one({"id": user.rootfolder})
    assert new_scenario.id in this_folder_db['scenarios_id']


def test_list_scenarios(app_and_db_and_user):
    app, mongoMockDB, user, _ = app_and_db_and_user
    # get test data
    rootfolder_id = user.rootfolder
    rootfolder_db = mongoMockDB.db.folders.find_one({"id": user.rootfolder})

    # test recursive list
    with TestClient(app) as client:
        response = client.get(
            "/scen-folders/{}/scenarios?recursive=true".format(
                str(rootfolder_id)))
    assert response.status_code == 200
    scenarios_list_response = [vo_ScenarioDB(**s) for s in response.json()]

    def test_scenario_is_included(folder_db, scenarios_list_response):
        for scenario_id in folder_db['scenarios_id']:
            scenario_db = mongoMockDB.db.scenarios.find_one(
                {'id': scenario_id})
            assert vo_ScenarioDB(**scenario_db) in scenarios_list_response
        for subfolder_id in folder_db['subfolders_id']:
            subfolder_db = mongoMockDB.db.folders.find_one(
                {'id': subfolder_id})
            test_scenario_is_included(subfolder_db, scenarios_list_response)

    test_scenario_is_included(rootfolder_db, scenarios_list_response)

    # test not recursive list
    with TestClient(app) as client:
        response = client.get(
            "/scen-folders/{}/scenarios?recursive=true".format(
                str(rootfolder_id)))
    assert response.status_code == 200
    scenarios_list_response = [vo_ScenarioDB(**s) for s in response.json()]
    for scenario_id in rootfolder_db['scenarios_id']:
        scenario_db = mongoMockDB.db.scenarios.find_one({'id': scenario_id})
        assert vo_ScenarioDB(**scenario_db) in scenarios_list_response


def test_delete_scenario(app_and_db_and_user):
    app, mongoMockDB, user, _ = app_and_db_and_user
    # get test data

    rootfolder_id = user.rootfolder
    rootfolder = mongoMockDB.db.folders.find_one({"id": user.rootfolder})
    this_scenario_id = rootfolder['scenarios_id'][0]
    this_scenario = vo_ScenarioDB(
        **mongoMockDB.db.scenarios.find_one({'id': this_scenario_id}))

    # perform test
    # pass wrong folder
    fake_rootfolder_id = uuid.uuid4()
    with TestClient(app) as client:
        response = client.delete("/scen-folders/{}/scenarios/{}".format(
            str(fake_rootfolder_id), str(this_scenario_id)))
    assert response.status_code == 204
    assert mongoMockDB.db.scenarios.find_one({"id":
                                              this_scenario_id}) is not None

    # normal
    with TestClient(app) as client:
        response = client.delete("/scen-folders/{}/scenarios/{}".format(
            str(rootfolder_id), str(this_scenario_id)))
    assert response.status_code == 204
    assert mongoMockDB.db.scenarios.find_one({"id": this_scenario_id}) is None
    rootfolder = mongoMockDB.db.folders.find_one({"id": user.rootfolder})
    assert this_scenario_id not in rootfolder['scenarios_id']


def test_update_scenario(app_and_db_and_user):
    app, mongoMockDB, user, _ = app_and_db_and_user
    # get test data

    rootfolder_id = user.rootfolder
    rootfolder = mongoMockDB.db.folders.find_one({"id": user.rootfolder})
    this_scenario_id = rootfolder['scenarios_id'][0]
    this_scenario = vo_ScenarioUpdate(
        **mongoMockDB.db.scenarios.find_one({"id": this_scenario_id}))
    this_scenario.name += "tail"

    # perform test
    with TestClient(app) as client:
        response = client.put("/scen-folders/{}/scenarios/{}".format(
            str(rootfolder_id), str(this_scenario_id)),
                              json=jsonable_encoder(this_scenario))
    assert response.status_code == 200

    # should return the updated scenario
    new_scenario = vo_ScenarioDB(**response.json())
    assert vo_ScenarioUpdate(**new_scenario.dict()) == this_scenario
    this_scenario_db = mongoMockDB.db.scenarios.find_one(
        {"id": this_scenario_id})
    assert vo_ScenarioUpdate(**this_scenario_db) == this_scenario


def test_move_scenario(app_and_db_and_user):
    app, mongoMockDB, user, _ = app_and_db_and_user
    # get test data

    rootfolder_id = user.rootfolder
    rootfolder = mongoMockDB.db.folders.find_one({"id": user.rootfolder})
    subfolder_id = rootfolder['subfolders_id'][0]
    subfolder = mongoMockDB.db.folders.find_one({"id": subfolder_id})
    this_scenario_id = rootfolder['scenarios_id'][0]
    this_scenario = vo_ScenarioDB(
        **mongoMockDB.db.scenarios.find_one({'id': this_scenario_id}))

    # perform test

    assert this_scenario_id not in subfolder['scenarios_id']

    with TestClient(app) as client:
        response = client.patch(
            "/scen-folders/{}/scenarios/{}/move-to/another-folder/{}".format(
                str(rootfolder_id), str(this_scenario_id), str(subfolder_id)))
    assert response.status_code == 200

    rootfolder = mongoMockDB.db.folders.find_one({"id": user.rootfolder})
    assert this_scenario_id not in rootfolder['scenarios_id']

    subfolder = mongoMockDB.db.folders.find_one({"id": subfolder_id})
    another_folder = vo_ScenFolderDB(**response.json())
    assert another_folder == vo_ScenFolderDB(
        **subfolder)  # should return the another folder
    assert this_scenario_id in subfolder['scenarios_id']


def test_get_folder(app_and_db_and_user):
    app, mongoMockDB, _, _ = app_and_db_and_user
    # get test data
    this_folder_db = mongoMockDB.db.folders.find_one({})
    this_folder = vo_ScenFolderDB(**this_folder_db)

    # perform test
    with TestClient(app) as client:
        response = client.get("/scen-folders/{}".format(str(this_folder.id)))
    assert response.status_code == 200
    assert vo_ScenFolderDB(**response.json()) == this_folder

    # scenarios are in response
    first_scenario_db = mongoMockDB.db.scenarios.find_one(
        {'id': this_folder.scenarios_id[0]})
    first_scenario = vo_ScenarioDB(**first_scenario_db)
    assert first_scenario in vo_ScenFolder(**response.json()).scenarios

    # subfolders are in response
    first_subfolder_db = mongoMockDB.db.folders.find_one(
        {'id': this_folder.subfolders_id[0]})
    first_subfolder = vo_ScenSubFolder(**first_subfolder_db)
    assert first_subfolder in vo_ScenFolder(**response.json()).subfolders


def test_add_folder(app_and_db_and_user):
    app, mongoMockDB, user, _ = app_and_db_and_user
    # get test data
    this_folder_db = mongoMockDB.db.folders.find_one({})
    this_folder = vo_ScenFolderCreate(**this_folder_db)
    this_folder.name += "tail"
    parent_folder_id = this_folder_db['id']

    # perform test
    with TestClient(app) as client:
        response = client.post("/scen-folders/{}/sub-folders".format(
            str(parent_folder_id)),
                               json=jsonable_encoder(this_folder))
    assert response.status_code == 201

    # should return the created folder
    new_folder = vo_ScenFolderDB(**response.json())
    assert vo_ScenFolderCreate(**new_folder.dict()) == this_folder
    assert new_folder.by_user_id == user.id
    this_folder_db = mongoMockDB.db.folders.find_one({"id": new_folder.id})
    assert this_folder_db is not None

    # this folder should be added to parent folder's folder list
    parent_folder_db = mongoMockDB.db.folders.find_one(
        {"id": parent_folder_id})
    assert new_folder.id in parent_folder_db['subfolders_id']


def test_delete_folder(app_and_db_and_user):
    app, mongoMockDB, user, _ = app_and_db_and_user
    # get test data
    rootfolder_id = user.rootfolder
    rootfolder = mongoMockDB.db.folders.find_one({"id": user.rootfolder})
    this_folder_id = rootfolder['subfolders_id'][0]

    # perform test
    # pass wrong folder
    fake_rootfolder_id = uuid.uuid4()
    with TestClient(app) as client:
        response = client.delete("/scen-folders/{}/sub-folders/{}".format(
            str(fake_rootfolder_id), str(this_folder_id)))
    assert response.status_code == 204
    assert mongoMockDB.db.folders.find_one({"id": this_folder_id}) is not None

    # delete root folder
    with TestClient(app) as client:
        response = client.delete("/scen-folders/{}/sub-folders/{}".format(
            str(rootfolder_id), str(rootfolder_id)))
    assert response.status_code == 409
    assert mongoMockDB.db.folders.find_one({"id": rootfolder_id}) is not None

    # normal
    with TestClient(app) as client:
        response = client.delete("/scen-folders/{}/sub-folders/{}".format(
            str(rootfolder_id), str(this_folder_id)))
    assert response.status_code == 204
    print(mongoMockDB.db.folders.find_one({"id": this_folder_id}))
    assert mongoMockDB.db.folders.find_one({"id": this_folder_id}) is None
    rootfolder = mongoMockDB.db.folders.find_one({"id": user.rootfolder})
    assert this_folder_id not in rootfolder['subfolders_id']


def test_update_folder(app_and_db_and_user):
    app, mongoMockDB, user, _ = app_and_db_and_user
    # get test data
    rootfolder_id = user.rootfolder
    rootfolder_db = mongoMockDB.db.folders.find_one({"id": user.rootfolder})
    this_folder_id = rootfolder_db['subfolders_id'][0]
    this_folder = vo_ScenFolderCreate(
        **mongoMockDB.db.folders.find_one({"id": this_folder_id}))
    this_folder.name += "tail"

    # perform test
    # update rootfolder
    with TestClient(app) as client:
        response = client.put("/scen-folders/{}".format(str(rootfolder_id)),
                              json=jsonable_encoder(this_folder))
    assert response.status_code == 409
    now_rootfolder_db = mongoMockDB.db.folders.find_one(
        {"id": user.rootfolder})
    assert now_rootfolder_db["name"] == rootfolder_db['name']

    # normal
    with TestClient(app) as client:
        response = client.put("/scen-folders/{}".format(str(this_folder_id)),
                              json=jsonable_encoder(this_folder))
    assert response.status_code == 200
    # should return the updated folder
    new_this_folder = vo_ScenFolderDB(**response.json())
    assert vo_ScenFolderCreate(**new_this_folder.dict()) == this_folder
    new_this_folder_db = mongoMockDB.db.folders.find_one(
        {"id": this_folder_id})
    assert vo_ScenFolderCreate(**new_this_folder_db) == this_folder


def test_move_folder(app_and_db_and_user):
    app, mongoMockDB, user, _ = app_and_db_and_user
    # get test data

    rootfolder_id = user.rootfolder
    rootfolder_db = mongoMockDB.db.folders.find_one({"id": user.rootfolder})
    subfolder_1_id = rootfolder_db['subfolders_id'][0]
    subfolder_2_id = rootfolder_db['subfolders_id'][1]
    subfolder_2_db = mongoMockDB.db.folders.find_one({"id": subfolder_2_id})

    # perform test
    # move subfolder_1 from rootfolder to subfolder_2

    assert subfolder_1_id not in subfolder_2_db['subfolders_id']

    # move rootfolder

    with TestClient(app) as client:
        response = client.patch(
            "/scen-folders/{}/sub-folders/{}/move-to/another-folder/{}".format(
                str(rootfolder_id), str(rootfolder_id), str(subfolder_2_id)))
    assert response.status_code == 409
    assert rootfolder_id not in subfolder_2_db['subfolders_id']

    # normal

    with TestClient(app) as client:
        response = client.patch(
            "/scen-folders/{}/sub-folders/{}/move-to/another-folder/{}".format(
                str(rootfolder_id), str(subfolder_1_id), str(subfolder_2_id)))
    assert response.status_code == 200

    # subfolder_1_id should be removed from rootfolder
    rootfolder_db = mongoMockDB.db.folders.find_one({"id": user.rootfolder})
    assert subfolder_1_id not in rootfolder_db['subfolders_id']

    # should return the another-folder
    subfolder_2_db = mongoMockDB.db.folders.find_one({"id": subfolder_2_id})
    another_folder = vo_ScenFolderDB(**response.json())
    assert another_folder == vo_ScenFolderDB(**subfolder_2_db)
    # subfolder_1_id should be added to subfolder_2
    assert subfolder_1_id in subfolder_2_db['subfolders_id']
