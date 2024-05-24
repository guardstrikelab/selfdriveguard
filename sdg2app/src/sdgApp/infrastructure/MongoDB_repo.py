from infrastructure.interface import I_DBRepo
from pydantic import UUID4
from pymongo.database import Database
from domain.value_objects import vo_Task

MONGO_IP = '127.0.0.1'
MONGO_PORT = 27017
DB_NAME = "sdgApp"


class MongoDB_repo(I_DBRepo):
    def __init__(self, db: Database):
        self.db = db

    def set_root_folder(self, user_id, folder):
        query = {"id": user_id}
        update = {"$set": {"rootfolder": folder['id']}}
        result = self.db.users.update_one(query, update)
        # TODO: exception handler

    # folders

    def add_folder(self, user_id, parent_folder_id, folder):
        collection = self.db.folders
        result = collection.insert_one(folder.dict())
        if parent_folder_id:
            query = {"id": parent_folder_id, "by_user_id": user_id}
            update = {"$addToSet": {"subfolders_id": folder.id}}
            collection.update_one(query, update)
        return self.get_folder(user_id, folder.id)

    def delete_folder(self, user_id, parent_folder_id, folder_id):
        parent_folder = self.get_folder(user_id, parent_folder_id)
        if parent_folder and (folder_id in parent_folder['subfolders_id']):
            self.db.folders.delete_many({
                'id': folder_id,
                'by_user_id': user_id
            })
            self.db.folders.update_one({"id": parent_folder_id},
                                       {"$pull": {
                                           'subfolders_id': folder_id
                                       }})
        else:
            print("folder error not find or not include")

    def update_folder(self, user_id, folder_id, folder):
        result = self.db.folders.update_one(
            {
                'id': folder_id,
                'by_user_id': user_id
            }, {'$set': folder.dict()})
        if result.matched_count == 1 and result.modified_count == 1:
            return self.get_folder(user_id, folder_id)
        else:
            return None

    def move_folder(self, user_id, parent_folder_id, folder_id,
                    another_folder_id):
        collection = self.db.folders
        result = collection.update_one(
            {
                "id": parent_folder_id,
                "by_user_id": user_id
            }, {"$pull": {
                "subfolders_id": folder_id
            }})
        if result.matched_count == 1 and result.modified_count == 1:
            result = collection.update_one(
                {
                    "id": another_folder_id,
                    "by_user_id": user_id
                }, {"$addToSet": {
                    "subfolders_id": folder_id
                }})
            if result.matched_count == 1 and result.modified_count == 1:
                return self.get_folder(user_id, another_folder_id)
        return None

    def get_folder(self, user_id, folder_id):
        collection = self.db.folders
        folder = collection.find_one({"by_user_id": user_id, "id": folder_id})
        if folder is not None:
            folder['scenarios'] = list(
                self.db.scenarios.find({'id': {
                    '$in': folder['scenarios_id']
                }}))
            folder['subfolders'] = list(
                self.db.folders.find({'id': {
                    '$in': folder['subfolders_id']
                }}))
        return folder

    # scenarios

    def add_scenario(self, user_id, folder_id, scenario):
        # get folder
        folder = self.db.folders.find_one({
            "by_user_id": user_id,
            "id": folder_id
        })
        if folder:
            # create new scenario and append it to folder
            self.db.scenarios.insert_one(scenario.dict())
            query = {"id": folder['id']}
            update = {"$addToSet": {"scenarios_id": scenario.id}}
            self.db.folders.update_one(query, update)
            return self.get_scenario(user_id, scenario.id)

    def update_scenario(self, user_id, folder_id, scenario_id, scenario):
        #TODO: verify scenario is in this folder
        result = self.db.scenarios.update_one(
            {
                'id': scenario_id,
                'by_user_id': user_id
            }, {'$set': scenario.dict()})
        if result.matched_count == 1 and result.modified_count == 1:
            return self.get_scenario(user_id, scenario_id)
        else:
            return None

    def move_scenario(self, user_id, folder_id, scenario_id,
                      another_folder_id):
        collection = self.db.folders
        result = collection.update_one({
            "id": folder_id,
            "by_user_id": user_id
        }, {"$pull": {
            "scenarios_id": scenario_id
        }})
        if result.matched_count == 1 and result.modified_count == 1:
            result = collection.update_one(
                {
                    "id": another_folder_id,
                    "by_user_id": user_id
                }, {"$addToSet": {
                    "scenarios_id": scenario_id
                }})
            if result.matched_count == 1 and result.modified_count == 1:
                return self.get_folder(user_id, another_folder_id)
        return None

    def get_scenario(self, user_id, scenario_id):
        scenario = self.db.scenarios.find_one({
            "by_user_id": user_id,
            "id": scenario_id
        })
        if scenario:
            in_folder = self.db.folders.find_one({
                "by_user_id": user_id,
                "scenarios_id": scenario_id
            })
            scenario["in_folder"] = in_folder
            return scenario
        else:
            return None

    def list_scenarios(self, user_id, folder_id, recursive):
        def get_folder_scenarios(folder_db, scenarios_list):
            if len(folder_db['scenarios']) > 0:
                scenarios_list += folder_db['scenarios']
            if len(folder_db['subfolders_id']) > 0:
                for subfolder_id in folder_db['subfolders_id']:
                    subfolder_db = self.get_folder(user_id, subfolder_id)
                    get_folder_scenarios(subfolder_db, scenarios_list)
            return scenarios_list

        if recursive:
            scenarios_list = []
            folder_db = self.get_folder(user_id, folder_id)
            return get_folder_scenarios(folder_db, scenarios_list)
        else:
            folder = self.get_folder(user_id, folder_id)
            return folder['scenarios']

    def delete_scenario(self, user_id, folder_id, scenario_id):
        folder = self.get_folder(user_id, folder_id)
        if folder and (scenario_id in folder['scenarios_id']):
            self.db.scenarios.delete_many({
                'id': scenario_id,
                'by_user_id': user_id
            })
            self.db.folders.update_one({
                "id": folder_id,
                "by_user_id": user_id
            }, {"$pull": {
                "scenarios_id": scenario_id
            }})
        else:
            print("folder error not find or not include")

    # tasks

    def add_task(self, user_id, task):
        collection = self.db.tasks
        if task.use_scenario is None:
            if task.use_scenario_id:
                scenario = self.get_scenario(user_id, task.use_scenario_id)
                task.use_scenario = scenario
            else:
                return None
        print(task.dict())
        result = collection.insert_one(task.dict())
        return self.get_task(user_id, task.id)

    def delete_task(self, user_id, task_id):
        self.db.tasks.delete_many({'id': task_id, 'by_user_id': user_id})

    def update_task(self, user_id, task_id, task):
        result = self.db.tasks.update_one(
            {
                'id': task_id,
                'by_user_id': user_id
            }, {'$set': task.dict()})
        if result.matched_count == 1 and result.modified_count == 1:
            return self.get_task(user_id, task_id)
        else:
            return None

    def get_task(self, user_id, task_id):
        collection = self.db.tasks
        task = collection.find_one({"by_user_id": user_id, "id": task_id})
        return task

    def list_tasks(self, user_id: UUID4, status):
        collection = self.db.tasks
        tasks = []
        query = {}
        if status:
            query['status'] = status
        for task in collection.find({"by_user_id": user_id, **query}):
            tasks.append(task)
        return tasks

    # jobs

    def add_job(self, user_id, job):
        self.db.jobs.insert_one(job.dict())
        this_job = self.get_job(user_id, job.id)
        for task in this_job["tasks"]:
            task["by_job_id"] = this_job["id"]
            self.update_task(user_id, task["id"], vo_Task(**task))
        return self.get_job(user_id, job.id)

    def delete_job(self, user_id, job_id):
        this_job = self.get_job(user_id, job_id)
        for task in this_job["tasks"]:
            if "by_job_id" in task.keys():
                del task["by_job_id"]
                self.update_task(user_id, task["id"], vo_Task(**task))
        self.db.jobs.delete_many({'id': job_id, 'by_user_id': user_id})

    def update_job(self, user_id, job_id, job):
        old_job = self.get_job(user_id, job_id)
        new_job = job.dict()
        task_id_diff = list(set(old_job["tasks_id"]) ^ set(new_job["tasks_id"]))
        for task_id in task_id_diff:
            task = self.get_task(user_id, task_id)
            if task.get("by_job_id"):
                del task["by_job_id"]
                self.update_task(user_id, task_id, vo_Task(**task))
            else:
                task["by_job_id"] = job_id
                self.update_task(user_id, task_id, vo_Task(**task))

        result = self.db.jobs.update_one({
            'id': job_id,
            'by_user_id': user_id
        }, {'$set': job.dict()})
        if result.matched_count == 1 and result.modified_count == 1:
            return self.get_job(user_id, job_id)
        else:
            return None

    def get_job(self, user_id, job_id):
        collection = self.db.jobs
        job = collection.find_one({"by_user_id": user_id, "id": job_id})
        job['tasks'] = []
        for task_id in job['tasks_id']:
            task = self.get_task(user_id, task_id)
            job['tasks'].append(task)
        return job

    def list_jobs(self, user_id: UUID4):
        collection = self.db.jobs
        jobs = []
        for job in collection.find({"by_user_id": user_id}):
            job['tasks'] = []
            for task_id in job['tasks_id']:
                task = self.get_task(user_id, task_id)
                job['tasks'].append(task)
                if task["status"] == "isRunning":
                    job["status"] = "Running"
            jobs.append(job)
        return jobs
