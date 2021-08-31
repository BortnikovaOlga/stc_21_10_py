from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from models import engine

Session = scoped_session(sessionmaker(autoflush=True, autocommit=False, bind=engine))


@contextmanager
def session_scope():
    """Открывает и закрывает сессию."""
    session = Session()
    try:
        yield session
    except Exception as ex:
        session.rollback()
        raise ex
    finally:
        session.close()
