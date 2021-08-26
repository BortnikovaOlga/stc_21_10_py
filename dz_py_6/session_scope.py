from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from models import engine

Session = scoped_session(sessionmaker(autoflush=True, autocommit=False, bind=engine))


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
