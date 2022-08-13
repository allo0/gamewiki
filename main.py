
from fastapi import FastAPI

from config.appConf import Settings
from source.models.patterns.pattern_router import patternRouter

app = FastAPI(title=Settings.PROJECT_NAME, version=Settings.PROJECT_VERSION,
              swagger_ui_parameters=Settings.swagger_ui_parameters,
              swagger_ui_default_parameters=Settings.swagger_ui_default_parameters)


# Static Content Hosting Pattern
# Retry Pattern
# Circuit Breaker Pattern

app.include_router(patternRouter, prefix='/v1')
