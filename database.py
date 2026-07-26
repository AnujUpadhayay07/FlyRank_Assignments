from sqlmodel import SQLModel, create_engine

DATABASE_URL = "sqlite:///tasks.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

def create_db():
    SQLModel.metadata.create_all(engine)