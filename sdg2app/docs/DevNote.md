## 参考资料
FastApi官方文档：https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/
MongoDB教程：https://www.tutorialspoint.com/mongodb
Pymongo 同步Python-MongoDB库：https://pymongo.readthedocs.io/en/stable/tutorial.html
Motor 异步Python-MongoDB库：https://motor.readthedocs.io/en/stable

## Dependencies
```
pytest
requests
pyyaml
'fastapi-users[mongodb]'
fastapi
'uvicorn[standard]'
```

## API 草稿
- GET /scenarios/{scenario_id}
return Scenario Object
- POST /folders/{folder_id}/scenarios
- DEL /folders/{folder_id}/scenarios/{scenario_id}
- PUT /folders/{folder_id}/scenarios/{scenario_id}
ScenarioUpdateModel: add targetFolderId
- GET /folders/{folder_id}
return folders
- POST /folders
- PUT /folders/{folder_id}
- DEL /folders/{folder_id}

## User System
使用fastapi-users库

## 数据库 Mongo

[设计文档](./sdgApp_DB.md)

数据库可视化管理：MongoDB Compass

阿里云MongoDB：
云数据库MongoDB版副本集。root密码
sdg##mongo**666

连接：
```
mongodb://sdg:sdg3App3@dds-2zeb146fafba16441401-pub.mongodb.rds.aliyuncs.com:3717,dds-2zeb146fafba16442383-pub.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-54022070
```

user
```
db.createUser(
  {
    user: "sdg",
    pwd: "sdg3App3",
    roles: [
       { role: "readWrite", db: "sdgApp" }
    ]
  }
)
```

## TODO
- 使用配置文件管理配置(城)

- 统一的异常处理和返回格式（扬）

- 依赖管理（城）

- redis队列管理(伟)

- 引擎调度器

- 数据库上云（阿里云MongoDB和redis）（扬）

- task、job的api（扬）

  

  ## 8月3日

1. redis 队列与用户绑定

