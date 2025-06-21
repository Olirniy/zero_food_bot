from functools import wraps


# Заменим импорт на ленивую инициализацию
_db = None

def get_db():
    global _db
    if _db is None:
        from storage.db_session import DBSession
        _db = DBSession()
    return _db

def with_db_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        db = get_db()
        try:
            result = func(*args, **kwargs)
            db.get_session().commit()
            return result
        except Exception as e:
            db.get_session().rollback()
            raise e
    return wrapper