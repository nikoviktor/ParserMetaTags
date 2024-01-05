# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import ttk
from bs4 import BeautifulSoup
import requests
import os
from openpyxl import Workbook

exel_list = []
# Получить путь к рабочему столу
current_directory = os.path.join(os.path.expanduser('~'), 'Desktop')

class ParserMetaTags:
    def __init__(self, root):
        self.root = root
        self.root.title("Парсер мета-тегов © Виктор Торгаш")
        self.root.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        # Список урлов
        self.url_label = tk.Label(self.root, text="Список урлов (чтобы вставить, переключите клавиатуру на EN)")
        self.url_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.url_textarea = scrolledtext.ScrolledText(self.root, width=60, height=5)
        self.url_textarea.grid(row=1, column=0, padx=10, pady=5, columnspan=2, sticky="nsew")

        # Кнопка СТАРТ
        self.start_button = tk.Button(self.root, text="СТАРТ", command=self.parse_url)
        self.start_button.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

        # Результат
        self.result_label = tk.Label(self.root, text="Результат")
        self.result_label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)

        self.result_textarea = scrolledtext.ScrolledText(self.root, width=60, height=10)
        self.result_textarea.grid(row=4, column=0, padx=10, pady=5, columnspan=2, sticky="nsew")

        # Прогресс бар
        self.progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=200, mode='determinate')
        self.progress_bar.grid(row=5, column=0, padx=10, pady=10, columnspan=2, sticky="nsew")

        # Размещение элементов по центру
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Обработчики клавиш
        #self.url_textarea.bind("<Control-v>", self.paste_text)
        #self.result_textarea.bind("<Control-v>", self.paste_text)

    def paste_text(self, event):
        text = self.root.clipboard_get()
        current_textarea = self.root.focus_get()

        if isinstance(current_textarea, tk.Text):
            current_textarea.insert(tk.INSERT, text)

    def parse_url(self):
        data = []
        urls = self.url_textarea.get("1.0", tk.END).splitlines()

        self.progress_bar['value'] = 0

        try:
            for i, url in enumerate(urls, 1):
                progress_value = (i / len(urls)) * 100
                self.progress_bar['value'] = progress_value
                self.root.update_idletasks()

                global exel_list
                exel_list = []
                data.append(self.get_title_from_url(url))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            self.progress_bar['value'] = 0
            self.export_to_excel(data, "output_metadata.xlsx")


    def export_to_excel(self, data, filename):
        # Сохранить файл
        excel_filepath = os.path.join(current_directory, filename)

        # Создаем новую книгу Excel
        workbook = Workbook()
        sheet = workbook.active

       # Заполняем лист данными из многомерного массива (если урлов много)
        for row_index, row in enumerate(data, start=1):
            for col_index, value in enumerate(row, start=1):
                sheet.cell(row=row_index, column=col_index, value=value)

        # Сохраняем книгу Excel
        workbook.save(excel_filepath)
        self.result_textarea.insert(tk.END, f"\n\nДанные успешно экспортированы в файл: {excel_filepath}")


    def get_title_from_url(self, url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            #headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
            response = requests.get(url, headers=headers, timeout=5)
            if(response.status_code == 200):
                soup = BeautifulSoup(response.text, 'html.parser')

                exel_list.append(url)

                if soup.findAll("title"):
                    title = soup.find("title").string
                    if title is not None: title = title.strip()
                    else: title = " "
                    exel_list.append(title)
                else:
                    title = " "
                    exel_list.append(title)

                if soup.findAll("h1"):
                    h1 = soup.find("h1").string
                    if h1 is not None: h1 = h1.strip()
                    else: h1 = " "
                    exel_list.append(h1)
                else:
                    h1 = " "
                    exel_list.append(h1)

                if soup.findAll("meta", attrs={"name": "description"}):
                    description = soup.find("meta", attrs={"name": "description"}).get("content")
                    if description is not None: description = description.strip()
                    else: description = " "
                    exel_list.append(description)
                else:
                    description = " "
                    exel_list.append(description)

        except requests.Timeout:
            print(f"Таймаут при запросе URL: {url}")
        except ConnectionRefusedError:
            print("Ошибка: Сервер отклонил соединение.")

        except Exception as e:
            print(f"Произошла ошибка: {e}")

        self.result_textarea.insert(tk.END, f"{exel_list}\n")
        return exel_list


if __name__ == "__main__":
    root = tk.Tk()
    app = ParserMetaTags(root)
    root.mainloop()
