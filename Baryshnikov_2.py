import tkinter as tk
from tkinter import ttk, messagebox
import json
import requests

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("600x400")

        # Поля для выбора валют
        ttk.Label(root, text="Из:").grid(row=0, column=0, padx=5, pady=5)
        self.from_currency = ttk.Combobox(root, values=[])
        self.from_currency.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(root, text="В:").grid(row=1, column=0, padx=5, pady=5)
        self.to_currency = ttk.Combobox(root, values=[])
        self.to_currency.grid(row=1, column=1, padx=5, pady=5)

        # Поле ввода суммы
        ttk.Label(root, text="Сумма:").grid(row=2, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(root)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка конвертации
        self.convert_btn = ttk.Button(root, text="Конвертировать", command=self.convert_currency)
        self.convert_btn.grid(row=3, column=0, columnspan=2, pady=10)

        # Таблица истории
        self.history_tree = ttk.Treeview(root, columns=("From", "To", "Amount", "Result"), show="headings")
        self.history_tree.heading("From", text="Из валюты")
        self.history_tree.heading("To", text="В валюту")
        self.history_tree.heading("Amount", text="Сумма")
        self.history_tree.heading("Result", text="Результат")
        self.history_tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Загрузка данных
        self.load_currencies()
        self.load_history()
    def get_exchange_rate(self, from_curr, to_curr):
        try:
            # Замените YOUR_API_KEY на реальный ключ от сервиса
            url = f"https://api.exchangerate-api.com/v4/latest/{from_curr}"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200 and to_curr in data['rates']:
                return data['rates'][to_curr]
            else:
                messagebox.showerror("Ошибка", "Не удалось получить курс валюты")
                return None
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка подключения: {e}")
            return None
    def convert_currency(self):
        # Проверка корректности ввода
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Ошибка", "Сумма должна быть положительным числом")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное число")
            return

        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()

        if not from_curr or not to_curr:
            messagebox.showerror("Ошибка", "Выберите валюты")
            return

        # Получение курса
        rate = self.get_exchange_rate(from_curr, to_curr)
        if rate is None:
            return

        # Расчёт результата
        result = amount * rate

        # Добавление в историю
        self.add_to_history(from_curr, to_curr, amount, result)

        # Отображение результата
        messagebox.showinfo("Результат", f"{amount} {from_curr} = {result:.2f} {to_curr}")

    def add_to_history(self, from_curr, to_curr, amount, result):
        self.history_tree.insert("", "end", values=(from_curr, to_curr, f"{amount:.2f}", f"{result:.2f}"))
        self.save_history()
    def save_history(self):
        history = []
        for item in self.history_tree.get_children():
            values = self.history_tree.item(item)["values"]
            history.append(values)

        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=4)

    def load_history(self):
        try:
            with open("history.json", "r", encoding="utf-8") as f:
                history = json.load(f)
                for record in history:
                    self.history_tree.insert("", "end", values=record)
        except FileNotFoundError:
            pass  # Файл истории ещё не создаy
    def load_currencies(self):
        # Пример списка валют (можно расширить или получать из API)
        currencies = ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "RUB"]
        self.from_currency['values'] = currencies
        self.to_currency['values'] = currencies
if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()








