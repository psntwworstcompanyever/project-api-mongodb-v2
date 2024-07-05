from motor.motor_asyncio import AsyncIOMotorClient
from environs import Env

env = Env()
env.read_env()  # read .env file, if it exists

client: "AsyncIOMotorClient" = None


def get_database():
    global client
    if client is None:
        client = AsyncIOMotorClient(env("MONGODB_URL"))
    return client.project_v2


def get_pcba_list():
    db = get_database()
    return db.get_collection("pcba_list")


def get_customer_list():
    db = get_database()
    return db.get_collection("customer_list")


def get_hw_settings():
    db = get_database()
    return db.get_collection("hardware_settings")


def get_sw_settings():
    db = get_database()
    return db.get_collection("software_settings")


def get_customer_settings():
    db = get_database()
    return db.get_collection("customer_settings")


def get_spec_note():
    db = get_database()
    return db.get_collection("spec_note")


def get_cell_table():
    db = get_database()
    return db.get_collection("cell_table")
