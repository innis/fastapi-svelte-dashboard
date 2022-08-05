from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import jwt

from functools import lru_cache
from . import config

@lru_cache()
def get_settings():
    conf = config.Settings()
    ret_setting = {}
    try:
        if conf.db_conn_token != None:
            db_conn_info = jwt.decode(conf.db_conn_token, "jwt_secret_token", algorithms="HS256")
            for k in db_conn_info.keys():
                setattr(conf, k, db_conn_info[k])
    except Exception as e:
        pass

    return conf

conf = get_settings()

db_name = f"fastapi_svelte_{conf.env}"

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{conf.db_user}:{conf.db_pass}@{conf.db_host}/{db_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"charset": "utf8"}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()