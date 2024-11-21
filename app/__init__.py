from fastapi import FastAPI, Request
import time
import logging


class CustomFastAPI(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set up logging
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            handlers=[
                                logging.FileHandler("app.log"),  # Log to a file
                                logging.StreamHandler()          # Also log to console
                            ])
        self.logger = logging.getLogger(__name__)

        @self.middleware("http")
        async def add_process_time_header(request: Request, call_next):
            start_time = time.perf_counter()
            self.logger.info(f"Request: {request.method} {request.url}")  # Log the request method and URL
            response = await call_next(request)
            process_time = time.perf_counter() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            self.logger.info(f"Processed {request.method} {request.url} in {process_time:.4f} secs")  # Log the processing time
            return response

        from .routers.pokemon import router as pokemon_router
        self.include_router(pokemon_router, prefix="/pokemon", tags=["Pokemon"])

        from .routers.pokemons import router as pokemons_router
        self.include_router(pokemons_router, prefix="/pokemons", tags=["Pokemon", "Pokemons"])

        from .routers.type import router as type_router
        self.include_router(type_router, prefix="/type", tags=["Type", "Pokemons"])

app = CustomFastAPI()
