import nltk
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation
from collections import defaultdict

nltk.download('punkt')
from tkinter import ttk
import tkinter as tk
from tkinter import *
import json
from tkinter import filedialog
from tkinter import messagebox

# Create lemmatizer and stopwords list
mystem = Mystem()
stopwords = set(stopwords.words("russian"))
not_words = [',', '.', '!', '?', '-', '+', '=', ':']
vocabulary = {}


# Tokens that does not contains stopwords and punctuation
def preprocess_text(text):
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in stopwords \
              and token != " " \
              and token.strip() not in punctuation]
    return tokens


def forms_of_words(text):
    forms = defaultdict(lambda: 0)
    tokens = nltk.word_tokenize(text.lower())
    tokens.sort()
    for token in tokens:
        if not token in not_words:
            forms[token] += 1

    for form in forms:
        count = forms[form]
        forms[form] = [count, '']
    return forms


def get_lexems(text):
    tokens = preprocess_text(text)
    tokens.sort()
    lexems = defaultdict(lambda: 0)
    for token in tokens:
        if not token in not_words:
            lexems[token] += 1
    return lexems


def process_text():
    input = text.get(1.0, END)
    forms = forms_of_words(input)
    lexems = get_lexems(input)
    vocabulary['forms'] = forms
    vocabulary['lexems'] = lexems
    for key, value in forms.items():
        tree.insert("", "end", text="%s" % key, values=('%s' % value[0], value[1]))
    for key, value in lexems.items():
        lexems_tree.insert("", "end", text="%s" % key, values=('%s' % value))


def add_note():
    text_field.pack()
    submit_button.pack()


def submit():
    notes = text_field.get(1.0, END)
    text_field.pack_forget()
    submit_button.pack_forget()

    item = tree.selection()
    value = tree.item(item)['values'][0]
    text = tree.item(item)['text']
    vocabulary['forms'][text][1] = notes
    tree.item(item, values=(value, notes))


def save_vocabulary():
    file_path = filedialog.asksaveasfilename()
    if file_path != '':
        f = open(file_path, "w")
        f.write(json.dumps(vocabulary))
        f.close()


def upload_vocabulary():
    file_path = filedialog.askopenfilename()
    if file_path != '':
        with open(file_path) as json_file:
            vocabulary = json.load(json_file)
        tree.delete(*tree.get_children())
        lexems_tree.delete(*lexems_tree.get_children())
        for key, value in vocabulary['forms'].items():
            tree.insert("", "end", text="%s" % key, values=('%s' % value[0], value[1]))
        for key, value in vocabulary['lexems'].items():
            lexems_tree.insert("", "end", text="%s" % key, values=('%s' % value))


def info():
    messagebox.askquestion(
        "Помощь",
        "Для запуска анализа текста: \n"
        "1. Ввести текст в окно\n"
        "2. Нажать 'запустить анализ текста'\n\n"
        "Для добавления записи для словоформы необходимо:\n"
        "1. В таблице словоформ кликнуть на необходимую."
        "2. Нажать Записи -> Добавить запись\n"
        "3. В появшиемся текстовом поле ввести необходимые данные.\n"
        "4. Нажать 'Добавить запись\n\n"
        "Для сохранения грамматики необходимо нажать Файл -> Импорт.\n\n"
        "Для того, чтобы открыть уже имеюющуюся грамматику (формата Json) необходимо нажать Файл -> Экспорт\n\n"
        "Сохранять файл можно в любом текстовом формате.", type='ok')


# GUI


root = tk.Tk()

mainmenu = Menu(root)
root.config(menu=mainmenu)

filemenu = Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Импорт словаря в файл", command=save_vocabulary)
filemenu.add_command(label="Экспорт словаря из файла", command=upload_vocabulary)

recordmenu = Menu(mainmenu, tearoff=0)
recordmenu.add_command(label="Добавить запись для словоформы", command=add_note)

helpmenu = Menu(mainmenu, tearoff=0)
helpmenu.add_command(label="Помощь", command=info)

mainmenu.add_cascade(label='Файл', menu=filemenu)
mainmenu.add_cascade(label='Записи', menu=recordmenu)
mainmenu.add_cascade(label='Справка', menu=helpmenu)

text_field = Text(width=70, height=5)
submit_button = Button(text='Добавить запись', width=30, height=2, command=submit)

frame = Frame()
frame.pack(side=TOP)

text = Text(frame, width=70, height=5)
text.pack()

button = Button(frame, width=30, height=2, text="Запустить анализ текста", command=process_text)
button.pack(side=TOP)

frame_button = Frame(frame)
frame_button.pack(side=RIGHT)

frame_tree = Frame()
frame_tree.pack(side=BOTTOM)

tree = ttk.Treeview(frame_tree, height=20)
tree.pack(side=LEFT)

lexems_tree = ttk.Treeview(frame_tree, height=20)
lexems_tree.pack(side=RIGHT)

lexems_tree["columns"] = ("#0", "#1")

lexems_tree.heading("#0", text="Лексемы", anchor=tk.W)
lexems_tree.heading("#1", text="Количество повторений", anchor=tk.W)

tree["columns"] = ("#1", "#2")

tree.heading("#0", text="Словоформы", anchor=tk.W)
tree.heading("#1", text="Количество повторений", anchor=tk.W)
tree.heading("#2", text="Записи", anchor=tk.W)

root.mainloop()
