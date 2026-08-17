from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

from config import PASSWORD_POSTGRESQL

engine = create_engine(
    f"postgresql+psycopg2://postgres:{PASSWORD_POSTGRESQL}@localhost:5432/postgres_flask",
)

db_session = scoped_session(sessionmaker(bind=engine))


class Base(DeclarativeBase):
    pass
