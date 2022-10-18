import os

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware


class Settings:
    PROJECT_NAME: str = "GameWiki"
    PROJECT_VERSION: str = "0.5.1"

    swagger_ui_parameters = {
        "syntaxHighlight.theme": "obsidian"
    }
    swagger_ui_default_parameters = {
        "dom_id": "#swagger-ui",
        "layout": "BaseLayout",
        "deepLinking": True,
        "showExtensions": True,
        "showCommonExtensions": True,
    }

    # API_URL = "http://127.0.0.1:8000"
    API_URL = "https://hidden-inlet-35935.herokuapp.com/"

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    STEAM_API_KEY = os.getenv("STEAM_API_KEY")
    AZURE_CLOUD_STORAGE_NAME = os.getenv("AZURE_CLOUD_STORAGE_NAME")
    AZURE_CLOUD_STORAGE_KEY = os.getenv("AZURE_CLOUD_STORAGE_KEY")
    AZURE_CLOUD_STORAGE_CONNECTION_STRING = os.getenv("AZURE_CLOUD_STORAGE_CONNECTION_STRING")
    TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
    TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")

    origins = [
        "*",
        "https://hidden-inlet-35935.herokuapp.com/",
        "http://localhost:4200",
        "http://127.0.0.1:8000",

    ]
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
            expose_headers=['*']
        )
    ]
