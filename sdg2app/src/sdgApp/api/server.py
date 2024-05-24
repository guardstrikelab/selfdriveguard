from fastapi import FastAPI
import importlib
from fastapi.middleware.cors import CORSMiddleware
# in project
from api import routers

conn_factory = {}


def create_app() -> FastAPI:

    app = FastAPI(
        debug=True,
        title="SDG App",
        version="v2.0",
        description="Debug Mode",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_startend(app)

    return app


def register_startend(app: FastAPI) -> None:
    @app.on_event("startup")
    async def startup():
        # register routers
        for routermodule in routers.__all__:
            imported_module = importlib.import_module("api.routers." +
                                                      routermodule)
            app.include_router(imported_module.router)

    @app.on_event("shutdown")
    async def shutdown():
        for conn in conn_factory.values():
            conn.disconnect()
            print("{}  disconnected".format(conn))
