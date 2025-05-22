# test_bot_load.py

# import threading
# import telebot
# from config import TG_API_KEY
#
# bot = telebot.TeleBot(TG_API_KEY)
#
# def simulate_user(i):
#     # Имитируем вход пользователя
#     class MockUser:
#         id = 123456789 + i
#         username = f"user_{i}"
#         first_name = f"Test{i}"
#
#     class MockMessage:
#         from_user = MockUser()
#         chat = type('obj', (object,), {'id': 123456789 + i})
#
#     msg = MockMessage()
#     bot.process_new_messages([msg])
#     print(f"Пользователь {i} обработан")
#
# if __name__ == "__main__":
#     threads = []
#     for i in range(20):  # имитация 20 пользователей
#         t = threading.Thread(target=simulate_user, args=(i,))
#         threads.append(t)
#         t.start()
#
#     for t in threads:
#         t.join()
#
#     print("Тест завершён")