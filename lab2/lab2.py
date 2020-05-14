# Imports
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox
from html.parser import HTMLParser
import operator
from functools import reduce

file_name = ''
all_words = []


class Parser(HTMLParser):
    def handle_data(self, data):
        all_words.append(data)


def calculate_distance(a, b):
    n, m = len(a), len(b)
    if n > m:
        a, b = swap(a, b)
        n, m = swap(n, m)

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


def swap(a, b):
    return [b, a]


def get_html_filename():
    global file_name
    file_name = fd.askopenfilename(filetypes=(("HTML files", "*.html"),))


def get_data_from_input(input):
    return input.get(1.0, END)


def separate_words(sentence):
    return sentence.replace('\n', '').split(' ')


def process():
    if file_name != '':
        incorrect_word = get_data_from_input(text_from_input)
        incorrect_word = incorrect_word.replace('\n', '')
        count_errors = get_data_from_input(text_from_input_2)
        count_errors = count_errors.replace('\n', '')
        if count_errors != '' and incorrect_word != '':
            list_box.delete(0, END)
            with open(file_name, 'r', encoding='utf-8') as file:
                source_html = file.read()
                parser = Parser()
                parser.feed(source_html)
                list_word = [word for word in reduce(operator.concat, list(map(separate_words, all_words))) if
                             word != '']
                dict_words_and_errors = {}
                for word in list_word:
                    errors = calculate_distance(incorrect_word.lower(), word.lower())
                    dict_words_and_errors.update({word: errors})
                list_with_tuple = list(dict_words_and_errors.items())
                list_with_tuple.sort(key=lambda i: i[1])
                for word in list_with_tuple[::-1]:
                    if int(word[1]) < int(count_errors) + 1:
                        list_box.insert(0, str(word[0]) + ' ' + str(word[1]))


def info():
    messagebox.askquestion(
        "Help",
        "1. Открыть файл с правильными словами\n"
        "2. Ввести неправильное слово\n"
        "3. Ввести количество допустимых ошибок\n", type='ok')


# GUI configuration
root = Tk()

mainmenu = Menu(root)
root.config(menu=mainmenu)

filemenu = Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Открыть файл со словами", command=get_html_filename)

helpmenu = Menu(mainmenu, tearoff=0)
helpmenu.add_command(label="Помощь", command=info)

mainmenu.add_cascade(label='Файл', menu=filemenu)
mainmenu.add_cascade(label='Справка', menu=helpmenu)

root.resizable(width=False, height=False)
root.geometry("400x250")

label = Label(root, width=30, text='Введите слово:')
label.grid(row=1, column=0)

text_from_input = Text(root, height=1, width=20)
text_from_input.grid(row=1, column=1, sticky='nsew', columnspan=3)

label2 = Label(root, width=30, text='Введите количество ошибок:')
label2.grid(row=2, column=0)

text_from_input_2 = Text(root, height=1, width=5)
text_from_input_2.grid(row=2, column=1, sticky='nsew', columnspan=3)

# Event handlers
b1 = Button(text="Обнаружение ошибок", command=process, highlightbackground='grey')
b1.grid(row=3, column=1)

list_box = Listbox(root, height=10, width=65)
scrollbar = Scrollbar(root, command=list_box.yview)
scrollbar.grid(row=4, column=4, sticky='nsew')

list_box.grid(row=4, column=0, sticky='nsew', columnspan=3)
list_box.configure(yscrollcommand=scrollbar.set)

root.mainloop()
