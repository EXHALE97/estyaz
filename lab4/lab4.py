import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox
from wordcloud import WordCloud
from tkinter import filedialog as fd
from wiki_ru_wordnet import WikiWordnet


def info():
    messagebox.askquestion("Help", "1. Введите одно слово или откройте файл с одним словом.\n"
                                   "2. Нажмите кнопку 'Анализ'.\n"
                                   "3. Посмотрите на картинку.", type='ok')


def open_html_file():
    file_name = fd.askopenfilename(filetypes=(("HTML files", "*.html"),))
    if file_name != '':
        with open(file_name, 'r', encoding='utf-8') as file:
            text = file.read()
            calculated_text.delete(1.0, END)
            calculated_text.insert(1.0, text)


def check_word(word):
    list_symbol = list(word)
    for i in list_symbol:
        if i == ' ':
            return False
    return True


def view_window():
    text = calculated_text.get(1.0, END)
    text = text.replace('\n', '')
    if text != '':
        check = check_word(text)
        if not check:
            messagebox.showwarning('!', 'Необходимо ввести одно слово', type='ok')
        else:
            wiki_wordnet = WikiWordnet()
            syn=wiki_wordnet.get_synsets(text.lower())
            text = ''
            for l in syn[0].get_words():
                text += l.lemma() + ' '
            for i in wiki_wordnet.get_hyponyms(syn[0]):
                for hyponym in i.get_words():
                    text += hyponym.lemma() + ' '
            for j in wiki_wordnet.get_hypernyms(syn[0]):
                for hypernym in j.get_words():
                    text += hypernym.lemma() + ' '
            wordcloud = WordCloud(
                relative_scaling=1.0,
            ).generate(text)
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.show()


root = Tk()
root.resizable(width=False, height=False)
root.geometry("420x80+300+300")

mainmenu = Menu(root)
root.config(menu=mainmenu)

filemenu = Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Открыть файл с текстом", command=open_html_file)

helpmenu = Menu(mainmenu, tearoff=0)
helpmenu.add_command(label="Помощь", command=info)

mainmenu.add_cascade(label='Файл', menu=filemenu)
mainmenu.add_cascade(label='Справка', menu=helpmenu)

label = Label(root, text='Введите слово:')
label.pack(side=TOP)

calculated_text = Text(root, height=1, width=40)
calculated_text.pack(side=TOP)

button1 = Button(text="Анализ", width=10, command=view_window)
button1.pack(side=TOP)

root.mainloop()
