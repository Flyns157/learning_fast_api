from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from fastapi import FastAPI, Request
import logging
import time

__version__ = "1.0.0"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class CustomFastAPI(FastAPI):
    def __init__(self, title: str = "Pokemon-CustomFastAPI", version: str = __version__, *args, **kwargs):
        super().__init__(title=title, version=version, *args, **kwargs)


        def setup_logging(self):
            # Set up logging
            logging.basicConfig(level=logging.INFO,
                                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                handlers=[
                                    logging.FileHandler("app.log"),  # Log to a file
                                    logging.StreamHandler()          # Also log to console
                                ])
            self.logger = logging.getLogger(__name__)


        def add_middleware(self):
            @self.middleware("http")
            async def add_process_time_header(request: Request, call_next):
                start_time = time.perf_counter()
                self.logger.info(f"Request: {request.method} {request.url}")  # Log the request method and URL
                response = await call_next(request)
                process_time = time.perf_counter() - start_time
                response.headers["X-Process-Time"] = str(process_time)
                self.logger.info(f"Processed {request.method} {request.url} in {process_time:.4f} secs")  # Log the processing time
                return response


        def add_routers(self):
            from .routers.auth import router as auth_router
            self.include_router(auth_router, tags=["Auth"])
            
            from .routers.pokemon import router as pokemon_router
            self.include_router(pokemon_router, tags=["Pokemon"])

            from .routers.pokemons import router as pokemons_router
            self.include_router(pokemons_router, tags=["Pokemons"])

            from .routers.type import router as type_router
            self.include_router(type_router, tags=["Type"])


        # Call the functions to set up logging, middleware, and routers
        setup_logging(self)
        add_middleware(self)
        add_routers(self)

app = CustomFastAPI()
