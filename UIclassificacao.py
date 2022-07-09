import os,sys
from functools import partial
from tkinter import Tk, ttk, N,W,E,S, IntVar
from PIL import Image,ImageTk

class Classificador:
    def __init__(self,diretorio):
        self.diretorio = diretorio
        self.root = Tk()

        mainframe = ttk.Frame(self.root,padding=12)
        mainframe.grid(column=0,row=0,sticky=(N,W,E,S))

        self.files = [file for file in os.listdir(self.diretorio) if not os.path.isdir(os.path.join(self.diretorio,file))]
        self.current_image_index = 0

        self.image_label = ttk.Label(mainframe)
        self.image_label.grid(column=0,row=0,sticky=(N,W,E,S))
        self.mostrar_imagem()

        botao_proxima = ttk.Button(
        mainframe,
        command=self.proxima_imagem
        )
        botao_proxima.grid(column=0,row=1,sticky=E)

    def mostrar_imagem(self):
        image = ImageTk.PhotoImage(
        Image.open(
        os.path.join(self.diretorio,self.files[self.current_image_index]))
        )
        self.image_label.configure(image=image)
        self.image_label.image = image

    def proxima_imagem(self):
        self.current_image_index += 1
        self.mostrar_imagem()

diretorio = sys.argv[1]
classificador = Classificador(diretorio)
classificador.root.mainloop()
