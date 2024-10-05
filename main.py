import dotenv
from fastapi import FastAPI

from api import Handlers
from api.exception_handler import ExceptionMiddleware
from infrastructure.container import Container

dotenv.load_dotenv()

app = FastAPI()
app.container = Container()
app.add_middleware(ExceptionMiddleware)
for handler in Handlers.iterator():
    app.include_router(handler.router)
