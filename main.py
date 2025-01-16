import tkinter as tk
from tkinter import messagebox
import psycopg2


class DataBaseManager:
    def __init__(self):
        self.conn = None

    def connect(self, host, port, database, user, password):
        try:
            self.conn = psycopg2.connect(
                host='localhost',
                port=5432,
                database='tkinter_manager',
                user='admin',
                password='admin'
            )
        except Exception as e:
            messagebox.showerror("Грешка", f"Неуспешно свързване: {e}")

    def save_to_database(self, table, data):
        try:
            if not self.conn:
                raise Exception("Няма активна връзка към базата данни.")

            query = f"INSERT INTO {table} (name, age) VALUES ('{data[0]}', {data[1]});"

            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            cursor.close()

        except Exception as e:
            messagebox.showerror("Грешка", f"Неуспешно запазване: {e}")

    def show_all(self, table):
        try:
            if not self.conn:
                raise Exception("Няма активна връзка към базата данни.")

            query = f"SELECT * FROM {table};"

            cursor = self.conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()

            return rows

        except Exception as e:
            messagebox.showerror("Грешка", f"Неуспешно показване: {e}")

    def show_database_text(self, table):
        try:
            if not self.conn:
                raise Exception("Няма активна връзка към базата данни.")

            query = f"SELECT * FROM {table}"

            cursor = self.conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()

            return rows

        except Exception as e:
            messagebox.showerror('Грешка', f"Неуспешно показване: {e}")


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.db_manager = DataBaseManager()
        self.db_manager.connect(host="localhost", port=5432, database="tkinter_manager", user="admin", password="admin")
        self.create_widgets()

    def create_widgets(self):
        # Главен етикет
        self.label = tk.Label(self, text="ADR Information", font=("Arial", 14))
        self.label.grid(row=0, column=0, columnspan=4, pady=10)

        # Етикет и поле за име
        self.name_label = tk.Label(self, text="Име:", font=("Arial", 12))
        self.name_label.grid(row=1, column=0, sticky="e", padx=10, pady=5)

        self.name = tk.Entry(self, width=30)
        self.name.grid(row=1, column=1, padx=10, pady=5)

        # Етикет и поле за години
        self.age_label = tk.Label(self, text="Години:", font=("Arial", 12))
        self.age_label.grid(row=1, column=2, sticky="e", padx=10, pady=5)

        self.age = tk.Entry(self, width=30)
        self.age.grid(row=1, column=3, padx=10, pady=5)

        # Бутон за запазване
        self.button_save = tk.Button(self, text="Запази данните", command=self.on_button_save)
        self.button_save.grid(row=2, column=0, columnspan=2, pady=10)

        # Бутон за показване
        self.button_show = tk.Button(self, text="Покажи всички", command=self.on_button_show)
        self.button_show.grid(row=2, column=2, columnspan=2, pady=10)

        # Поле за показване на информация
        self.text_info = tk.Text(self, height=10, width=80, state="disabled")
        self.text_info.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

        self.button_show = tk.Button(self, text="Покажи базата", command=self.show_database)
        self.button_show.grid(row=4, column=2, columnspan=2, pady=10)

    def on_button_save(self):
        name = self.name.get()
        age = self.age.get()

        if name and age:
            try:
                self.db_manager.save_to_database('test', [name, age])
                messagebox.showinfo("Информация", "Данните бяха успешно запазени!")
            except Exception as e:
                messagebox.showerror("Грешка", f"Неуспешно запазване: {e}")
        else:
            messagebox.showerror("Грешка", "Моля, въведете текст!")

    def on_button_show(self):
        try:
            rows = self.db_manager.show_all('test')

            if rows:
                messagebox.showinfo("Информация", "Списък с данни:\n" + "\n"
                                    .join([f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}" for row in rows]))
            else:
                messagebox.showinfo("Информация", "Няма намерени данни.")
        except Exception as e:
            messagebox.showerror("Грешка", f"Неуспешно показване: {e}")

    def show_database(self):
        try:
            # Извличане на данни от базата
            rows = self.db_manager.show_all('test')

            # Активиране на текстовото поле за обновяване
            self.text_info.config(state="normal")
            self.text_info.delete("1.0", tk.END)  # Изчистване на предишния текст

            # Проверка за налични данни
            if rows:
                for row in rows:
                    self.text_info.insert(tk.END, f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}\n")
            else:
                self.text_info.insert(tk.END, "Няма намерени данни.\n")

            # Деактивиране на текстовото поле, за да се предотврати редактиране
            self.text_info.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Грешка", f"Неуспешно показване: {e}")


if __name__ == "__main__":
    app = Application()
    app.mainloop()
