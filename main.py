from fastapi import FastAPI, Depends
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

from config.appConf import Settings
from source.models.auth.auth_controller import get_user
from source.models.azure.storage_router import storageRouter
from source.models.google_router import googleRouter
from source.models.igdb.igdb_router import igdbRouter
from source.models.patterns.pattern_router import patternRouter

from source.models.steam.steam_router import steamRouter, get_recommendations

app = FastAPI(title=Settings.PROJECT_NAME, version=Settings.PROJECT_VERSION,
              middleware=Settings.middleware, swagger_ui_parameters=Settings.swagger_ui_parameters,
              swagger_ui_default_parameters=Settings.swagger_ui_default_parameters)
app.add_middleware(HTTPSRedirectMiddleware)

app.include_router(patternRouter, prefix='/v1')
app.include_router(googleRouter, prefix='/v1')
app.include_router(steamRouter, prefix='/v1',dependencies=[Depends(get_user)])
app.include_router(igdbRouter, prefix='/v1')
app.include_router(storageRouter, prefix='/v1')

