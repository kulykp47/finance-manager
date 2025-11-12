import csv
from datetime import datetime
from enum import Enum

class TransactionType(Enum):
    INCOME = "Доход"
    EXPENSE = "Расход"

class Category:
    def __init__(self, name, type):
        self.name = name
        self.type = type

class Transaction:
    def __init__(self, amount, category, date, description=""):
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

class FinanceManager:
    def __init__(self, filename="transactions.csv"):
        self.filename = filename
        self.transactions = []
        self.categories = [
            Category("Зарплата", TransactionType.INCOME),
            Category("Инвестиции", TransactionType.INCOME),
            Category("Продукты", TransactionType.EXPENSE),
            Category("Транспорт", TransactionType.EXPENSE),
            Category("Развлечения", TransactionType.EXPENSE)
        ]
        self.load_from_file()

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.save_to_file()

    def delete_transaction(self, index):
        if 0 <= index < len(self.transactions):
            del self.transactions[index]
            self.save_to_file()

    def get_balance(self):
        income = sum(t.amount for t in self.transactions 
                    if t.category.type == TransactionType.INCOME)
        expenses = sum(t.amount for t in self.transactions 
                      if t.category.type == TransactionType.EXPENSE)
        return income - expenses

    def get_category_summary(self):
        summary = {}
        for transaction in self.transactions:
            cat_name = transaction.category.name
            if cat_name not in summary:
                summary[cat_name] = 0
            if transaction.category.type == TransactionType.INCOME:
                summary[cat_name] += transaction.amount
            else:
                summary[cat_name] -= transaction.amount
        return summary

    def save_to_file(self):
        with open(self.filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Amount', 'Category', 'Type', 'Date', 'Description'])
            for transaction in self.transactions:
                writer.writerow([
                    transaction.amount,
                    transaction.category.name,
                    transaction.category.type.value,
                    transaction.date,
                    transaction.description
                ])

    def load_from_file(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    category = next((cat for cat in self.categories 
                                   if cat.name == row['Category']), None)
                    if category:
                        transaction = Transaction(
                            amount=float(row['Amount']),
                            category=category,
                            date=row['Date'],
                            description=row['Description']
                        )
                        self.transactions.append(transaction)
        except FileNotFoundError:
            self.transactions = []
