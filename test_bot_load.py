#test_bot_load.py

# import threading
# import time
# import telebot
# from config import TG_API_KEY
#
# bot = telebot.TeleBot(TG_API_KEY)
#
#
# def simulate_user(i):
#     try:
#         class MockUser:
#             id = 123456789 + i
#             username = f"user_{i}"
#             first_name = f"Test{i}"
#
#         class MockMessage:
#             from_user = MockUser()
#             chat = type('obj', (object,), {'id': 123456789 + i})
#             text = "/start"
#
#         msg = MockMessage()
#         bot.process_new_messages([type('obj', (object,), {'message': msg})])
#         print(f"Пользователь {i} обработан")
#         time.sleep(0.3)  # Добавляем задержку между запросами
#     except Exception as e:
#         print(f"Ошибка в пользователе {i}: {e}")
#
#
# if __name__ == "__main__":
#     print("Запуск нагрузочного теста...")
#
#     threads = []
#     for i in range(10):  # Уменьшил количество для стабильности
#         t = threading.Thread(target=simulate_user, args=(i,))
#         threads.append(t)
#         t.start()
#         time.sleep(0.1)
#
#     for t in threads:
#         t.join()
#
#     print("Тест завершён")