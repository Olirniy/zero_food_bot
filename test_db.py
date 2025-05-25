from storage.db_session import DBSession
from config import SQL_DATA
from models.order import Order
from models.enums import OrderStatus
import pytest


def test_connection():
    print("\n=== Testing DB Connection ===")
    db = DBSession()
    try:
        conn = db.get_session()

        # Проверка users
        conn.execute("SELECT 1 FROM users LIMIT 1")
        print("✅ Table 'users' exists")

        # Тест записи/чтения
        conn.execute(
            "INSERT INTO users (telegram_id, username) VALUES (?, ?)",
            (999999, "test_user")
        )
        user = conn.execute(
            "SELECT id FROM users WHERE telegram_id = ?",
            (999999,)
        ).fetchone()

        assert user is not None, "Пользователь не создан"
        print(f"✅ User test passed (ID: {user[0]})")

        # Очистка
        conn.execute("DELETE FROM users WHERE telegram_id = 999999")
        conn.commit()

    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise
    finally:
        db.close()


def test_orders():
    print("\n=== Testing Orders ===")
    db = DBSession()
    try:
        from storage.order_storage import OrderStorage
        storage = OrderStorage(db, SQL_DATA)

        # Test
        order = Order(id=0, user_id=1, status=OrderStatus.IN_CART, payment_method=None, created_at=None)
        storage.save(order)

        loaded = storage.load_by_user(1)
        assert len(loaded) > 0, "Заказ не сохранён"
        assert loaded[0].status == OrderStatus.IN_CART, "Некорректный статус"

        print(f"✅ Order test passed (ID: {loaded[0].id})")

    except Exception as e:
        print(f"❌ Order test failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    test_connection()
    test_orders()
    print("=== All tests passed ===")


if __name__ == "__main__":
    test_connection()


