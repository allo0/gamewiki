from fastapi import FastAPI

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

app = FastAPI(swagger_ui_parameters=swagger_ui_parameters, swagger_ui_default_parameters=swagger_ui_default_parameters)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
