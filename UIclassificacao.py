import os,sys
from functools import partial
from tkinter import Tk, ttk, N,W,E,S, IntVar
from PIL import Image,ImageTk, ImageOps

class Classificador:
    def __init__(self,diretorio):
        self.diretorio = diretorio
        self.root = Tk()
        self.root.geometry("800x800")
        self.root.columnconfigure(0,weight=1)
        self.root.rowconfigure(0,weight=1)
        mainframe = ttk.Frame(self.root,padding=12)
        mainframe.grid(column=0,row=0,sticky=(N,W,E,S))

        mainframe.columnconfigure(0,weight=1)
        mainframe.rowconfigure(0,weight=1)

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
        self.root.mainloop()

    def mostrar_imagem(self):
        loaded_image = Image.open(
        os.path.join(self.diretorio,self.files[self.current_image_index])
        )
        loaded_image = ImageOps.contain(loaded_image,(760,760))
        image = ImageTk.PhotoImage(
        loaded_image
        )
        self.image_label.configure(image=image)
        self.image_label.image = image

    def proxima_imagem(self):
        self.current_image_index += 1
        self.mostrar_imagem()

diretorio = sys.argv[1]
classificador = Classificador(diretorio)
