import tkinter as tk
from tkinter import scrolledtext
import requests
from bs4 import BeautifulSoup

def parse_websites():
    urls = text_area.get("1.0", tk.END).splitlines()

    for url in urls:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            title = soup.title.string if soup.title else 'N/A'
            description = soup.find('meta', {'name': 'description'})['content'] if soup.find('meta', {'name': 'description'}) else 'N/A'
            h1 = soup.find('h1').text if soup.find('h1') else 'N/A'

            result_text.insert(tk.END, f"URL: {url}\nTitle: {title}\nDescription: {description}\nH1: {h1}\n\n")
        except Exception as e:
            result_text.insert(tk.END, f"Error parsing {url}: {str(e)}\n\n")

# Создаем графический интерфейс
root = tk.Tk()
root.title("Web Page Parser")

# Создаем текстовое поле для ввода урлов
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
text_area.pack(pady=10)

# Создаем кнопку СТАРТ
start_button = tk.Button(root, text="START", command=parse_websites)
start_button.pack()

# Создаем текстовое поле для вывода результата
result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
result_text.pack(pady=10)

# Запускаем главный цикл программы
root.mainloop()
