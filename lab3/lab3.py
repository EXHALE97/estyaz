# Imports
import nltk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd
from pymorphy2 import MorphAnalyzer

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

DOT = '.'
COMMA = ','
GRAMMAR_RULES = r"""
        P: {<PRCL|PREP>}
        V: {<VERB|INFN>}
        N: {<NOUN|NPRO>}
        PP: {<P><N>}
        NP: {<N|PP>+<ADJF|NUMR>+}
        NP: {<ADJF|NUMR>+<N|PP>+}
        VP: {<NP|N><V>}
        VP: {<VP><NP|N|GRND|PRTS|ADVB>}
        VP: {<NP|N|GRND|PRTS|ADVB><VP>}
        VP: {<VP><PP>}
        """
rp = nltk.RegexpParser(GRAMMAR_RULES)
analyzer = MorphAnalyzer()


def open_html_file():
    file_name = fd.askopenfilename(filetypes=(("HTML files", "*.html"),))
    if file_name != '':
        html_file = open(file_name, 'r', encoding='utf-8')
        data = html_file.read()
        calculated_text.delete(1.0, END)
        calculated_text.insert(1.0, data)
        html_file.close()


def info():
    messagebox.askquestion(
        "Help",
        "1. Открыть HTML-файл / ввести текст\n"
        "2. Нажать 'Построить'\n", type='ok')


def draw_tree():
    text = calculated_text.get(1.0, END)
    text = text.replace('\n', '')
    if text != '':
        list_word_with_tag = []
        for sentence in nltk.sent_tokenize(text.lower()):
            for word in nltk.word_tokenize(sentence):
                parse_word = analyzer.parse(word)[0]
                if parse_word.tag.POS:
                    list_word_with_tag.append((word, parse_word.tag.POS))
        result = rp.parse(list_word_with_tag)
        result.draw()


# GUI configuration
root = Tk()
root.resizable(width=False, height=False)
root.geometry("420x150+600+300")

mainmenu = Menu(root)
root.config(menu=mainmenu)

filemenu = Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Открыть файл с текстом", command=open_html_file)

helpmenu = Menu(mainmenu, tearoff=0)
helpmenu.add_command(label="Помощь", command=info)

mainmenu.add_cascade(label='Файл', menu=filemenu)
mainmenu.add_cascade(label='Справка', menu=helpmenu)

label = Label(root, text='Введите текст:')
label.pack(side=TOP)

calculated_text = Text(root, height=5, width=40)
calculated_text.pack(side=TOP)

b1 = Button(text="Построить", width=10, command=draw_tree)
b1.pack(side=TOP)
root.mainloop()
