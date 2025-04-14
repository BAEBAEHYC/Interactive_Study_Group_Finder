from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles  

from db import engine, Base 
from routers import studentinfo, friendslist, subjects, users, meetings, groups, search

app = FastAPI()

# API가 먼저 처리되도록 정적 파일은 /static 경로로 이동
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


templates = Jinja2Templates(directory="templates")


Base.metadata.create_all(bind=engine)


app.include_router(studentinfo.router)
app.include_router(friendslist.router)
app.include_router(subjects.router)
app.include_router(users.router)
app.include_router(meetings.router)
app.include_router(groups.router)
app.include_router(search.router)


@app.get("/")
def root():
    return {"message": "Study Buddy API is running"}
