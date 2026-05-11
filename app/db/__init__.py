from app.db.base import Base
from app.db.models import *
from app.db.session import engine, get_db, SessionLocal

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        from app.db.seed import seed_initial_data
        seed_initial_data(db)
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    print("Base de datos inicializada.")