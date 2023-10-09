import os
from pathlib import Path
import json

BASE_PATH = Path(os.getenv('BASE_PATH', Path.home() / 'Desktop' / 'TG_Bot'))
ACCOUNTS_PATH = BASE_PATH / 'Data' / 'Accounts'

def display_menu():
    available_accounts = [f.stem for f in ACCOUNTS_PATH.glob("*.json")]

    if not available_accounts:
        print("Нет доступных аккаунтов!")
        return

    print("Доступные аккаунты:")
    for idx, account in enumerate(available_accounts, 1):
        print(f"{idx}. {account}")

    selected_account_index = input("Выберите номер аккаунта для запуска: ")

    if selected_account_index.isdigit() and 0 < int(selected_account_index) <= len(available_accounts):
        selected_account = available_accounts[int(selected_account_index) - 1]
        print(f"Selected account: {selected_account}")
        return selected_account
    else:
        print("Неверный номер аккаунта!")
        return

if __name__ == "__main__":
    display_menu()
