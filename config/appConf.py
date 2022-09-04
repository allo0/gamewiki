from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware


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
    API_URL="https://hidden-inlet-35935.herokuapp.com/"

    STEAM_API_KEY = "7DC5A7A48F87A2A910FAB95D695D6B5B"
    AZURE_CLOUD_STORAGE_KEY = "MDEopau5hYvqXaXZS+mBqr3fuMUJnW2ZQi3UcjloZliX6+/YNPKdrcztwiOvnherbtL4RkBcl3jP+AStUo9vxg=="
    AZURE_CLOUD_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=gamewikistorage;AccountKey=MDEopau5hYvqXaXZS+mBqr3fuMUJnW2ZQi3UcjloZliX6+/YNPKdrcztwiOvnherbtL4RkBcl3jP+AStUo9vxg==;EndpointSuffix=core.windows.net"

    origins = [
        "*",
        "https://hidden-inlet-35935.herokuapp.com/",
        "https://hidden-inlet-35935.herokuapp.com/",
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
