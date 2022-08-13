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