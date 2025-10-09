import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import equipment_router
from error_handlers import handle_internal_provisioning_error
from config import Settings

app = FastAPI()
settings = Settings()

app.add_middleware(CORSMiddleware, allow_origins=["*"])

app.include_router(equipment_router)
app.add_exception_handler(Exception, handle_internal_provisioning_error)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.app_host, port=settings.app_port)
