# Файл добавлен в .gitignore

from storage.db_session import init_db

if __name__ == "__main__":
    init_db()
    print("Таблицы созданы!")