# from storage.db_session import DBSession
# from config import SQL_DATA
#
#
# def test_connection():
#     print("\n=== Testing DB Connection ===")
#     db = DBSession(SQL_DATA["db_path"])
#     try:
#         conn = db.get_session()
#
#         # Проверка существования таблицы users
#         conn.execute("SELECT 1 FROM users LIMIT 1")
#         print("✅ Table 'users' exists")
#
#         # Тест записи
#         conn.execute(
#             "INSERT INTO users (telegram_id, username) VALUES (?, ?)",
#             (999999, "test_user")
#         )
#         print("✅ Write test passed")
#
#         # Тест чтения
#         user = conn.execute(
#             "SELECT id FROM users WHERE telegram_id = ?",
#             (999999,)
#         ).fetchone()
#         print(f"✅ Read test passed. User ID: {user[0]}")
#
#     except Exception as e:
#         print(f"❌ Test failed: {e}")
#     finally:
#         db.close()
#         print("=== Test completed ===")


if __name__ == "__main__":
    test_connection()


