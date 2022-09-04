from fastapi import FastAPI, Depends

from config.appConf import Settings
from config.loggingConf import LogConfig
from source.models.auth.auth_controller import get_user
from source.models.azure.storage_router import storageRouter
from source.models.google_router import googleRouter
from source.models.patterns.pattern_router import patternRouter

from source.models.steam.steam_router import steamRouter


app = FastAPI(title=Settings.PROJECT_NAME, version=Settings.PROJECT_VERSION,
              middleware=Settings.middleware, swagger_ui_parameters=Settings.swagger_ui_parameters,
              swagger_ui_default_parameters=Settings.swagger_ui_default_parameters)

# Static Content Hosting Pattern


app.include_router(patternRouter, prefix='/v1')
app.include_router(googleRouter, prefix='/v1')
app.include_router(steamRouter, prefix='/v1')
app.include_router(storageRouter, prefix='/v1')



# Domain Name: https://hidden-inlet-35935.herokuapp.com/

@app.get("/api/me")
async def hello_user(user=Depends(get_user)):
    return {"msg": "Hello, {}".format(user['email']), "uid": user['uid']}
