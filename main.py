from fastapi import FastAPI
from router import (
    pcba_list,
    customer_list,
    hardware_settings,
    software_settings,
    customer_settings,
    note,
    create_project,
)
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Server Fan Project API",
    summary="Test API",
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pcba_list.router, prefix="/pcba-list")
app.include_router(customer_list.router, prefix="/customer-list")
app.include_router(hardware_settings.router, prefix="/hardware-settings")
app.include_router(software_settings.router, prefix="/software-settings")
app.include_router(customer_settings.router, prefix="/customer-settings")
app.include_router(note.router, prefix="/note")
app.include_router(create_project.router, prefix="/create-project")
