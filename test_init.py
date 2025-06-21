from storage.db_session import DBSession
from repository.user_repo import UserRepository
from storage.user_storage import UserStorage
from config import SQL_DATA

def test_user_creation():
    db = DBSession()
    storage = UserStorage(db, SQL_DATA)
    repo = UserRepository(storage)

    user = repo.create(12345, "test_user")
    assert user.id > 0, "Пользователь не получил ID"
    print(f"✅ Тест пройден. Создан пользователь ID: {user.id}")

if __name__ == "__main__":
    test_user_creation()