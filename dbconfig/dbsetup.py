from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_engine():
    # DB_URL = "sqlite:///./database/test.db"
    DB_URL = "mysql+pymysql://root:Welcome-1@backend_db:3306/testdb"
    engine = create_engine(DB_URL)
    return engine


def get_db():
    engine = get_engine()
    localsession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = localsession()
    try:
        yield db
    finally:
        db.close()
