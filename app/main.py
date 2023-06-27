from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post , user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


#models.Base.metadata.create_all(bind=engine)
# we don;t need this now because alembic is taling care of generating tabesl

app = FastAPI()

#origins = ["https://www.google.com","https://www.youtube.com"] 
# of all the domains that can talk to the api

origins = ["*"] # fro every single domain

app.add_middleware(
    CORSMiddleware, # func that runs before everu request, it persofms soem form of action
    allow_origins = origins,
    allow_credentials=True,# we can also allow specif HTTPs methods. ex we can allow only get requests
    allow_methods=["*"],#
    allow_headers=["*"],#
)
 
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello Wordls"}