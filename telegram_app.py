from menu import display_menu
import os
import json
import time
import random
from pyrogram import Client, errors
from pathlib import Path

# Путь к папке с данными аккаунтов
BASE_PATH = Path(os.getenv('BASE_PATH', Path.home() / 'Desktop' / 'TG_Bot'))
ACCOUNTS_PATH = BASE_PATH / 'Data' / 'Accounts'


def load_json_data(filename):
    """Загрузка данных из файла JSON."""
    with open(ACCOUNTS_PATH / filename, "r", encoding="utf-8") as file:
        return json.load(file)


def perform_actions(client, account_data, groups_data):
    """Выполнение действий с аккаунтом: вступление в группы, отправка сообщений и т.д."""
    for group in groups_data["groups_to_write"]:
        try:
            # Отправка сообщения в группу
            client.send_message(group, random.choice(account_data["messages"]))
            time.sleep(account_data["message_interval"] * 60)  # Задержка в минутах
        except errors.UserBannedInChannel:
            print(f"Пользователь заблокирован в группе {group}. Перемещение в список для выхода.")
            groups_data["groups_to_leave"].append(group)
        except Exception as e:
            print(f"Ошибка при отправке сообщения в группу {group}: {e}")

    for group in groups_data["groups_to_leave"]:
        try:
            # Выход из группы
            client.leave_chat(group)
            print(f"Успешно покинул группу {group}")
        except Exception as e:
            print(f"Ошибка при выходе из группы {group}: {e}")


def main():
    action = display_menu()
    if action == "1":
        # Ваш текущий код для работы с аккаунтами
        ...
    elif action == "2":
        # Здесь будет код для других функций, которые вы добавите позже
        pass
    else:
        print("Выбрано неверное действие!")

    # Получение списка доступных аккаунтов
    available_accounts = [f.stem for f in ACCOUNTS_PATH.glob("*.json") if f.stem not in ['my_groups', 'my_groups2']]

    # Если нет доступных аккаунтов, завершить программу
    if not available_accounts:
        print("Нет доступных аккаунтов!")
        return

    print("Доступные аккаунты:")
    for idx, account in enumerate(available_accounts, 1):
        print(f"{idx}. {account}")

    # Запрос на выбор аккаунтов
    selected_accounts_indices = input("Введите номера аккаунтов для запуска через пробел (например, '1 2'): ").split()

    # Фильтрация выбранных аккаунтов
    selected_accounts = [available_accounts[int(idx) - 1] for idx in selected_accounts_indices if idx.isdigit() and 0 < int(idx) <= len(available_accounts)]

    # Если ни один аккаунт не выбран, завершить программу
    if not selected_accounts:
        print("Неверный номер аккаунта!")
        return

    # Запуск выбранных аккаунтов
    for account_name in selected_accounts:
        account_data = load_json_data(f"{account_name}.json")
        groups_data = load_json_data(account_data["groups_file"])

        with Client(account_name, account_data["api_id"], account_data["api_hash"]) as client:
            perform_actions(client, account_data, groups_data)


if __name__ == "__main__":
    main()
