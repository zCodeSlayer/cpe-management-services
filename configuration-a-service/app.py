import uvicorn
from fastapi import FastAPI

from routes import equipment_router
from error_handlers import handle_internal_provisioning_error

app = FastAPI()

app.include_router(equipment_router)
app.add_exception_handler(Exception, handle_internal_provisioning_error)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
