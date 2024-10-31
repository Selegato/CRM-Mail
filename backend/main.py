from app.db import init_mongo_db
from app.logger import logger
from app.routes import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    init_mongo_db()
except Exception as e:
    logger.critical(f"Error initializing MongoDB init_mongo_db", {e})

app = FastAPI()

# cors config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# router for routes
app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    port = 8001
    uvicorn.run(app, host="0.0.0.0", port=port)
    print(f"Server running on port {port}")
