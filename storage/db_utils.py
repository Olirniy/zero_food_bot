from functools import wraps
from storage.db_session import DBSession
from config import SQL_DATA

_db = DBSession(SQL_DATA["db_path"])

def with_db_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            _db.get_session().commit()
            return result
        except Exception as e:
            _db.get_session().rollback()
            raise e
        finally:
            _db.close()
    return wrapper