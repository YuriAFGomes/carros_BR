import os,sys
from functools import partial
from tkinter import Tk, ttk, N,W,E,S, IntVar
from PIL import Image,ImageTk, ImageOps

from dataset import Dataset

class Classificador:
    def __init__(self,diretorio):
        self.diretorio = diretorio
        self.root = Tk()
        self.root.geometry("800x800")
        self.root.columnconfigure(0,weight=1)
        self.root.rowconfigure(0,weight=1)
        self.mainframe = ttk.Frame(self.root,padding=12)
        self.mainframe.grid(column=0,row=0,sticky=(N,W,E,S))

        self.mainframe.columnconfigure(0,weight=1)
        self.mainframe.rowconfigure(0,weight=1)

        self.files = [file for file in os.listdir(self.diretorio) if not os.path.isdir(os.path.join(self.diretorio,file))]
        print(self.files)
        self.current_image_index = 0

        self.image_label = ttk.Label(self.mainframe)
        self.image_label.grid(column=0,row=0,sticky=(N,W,E,S))
        self.mostrar_imagem()
        self.criar_botoes()

        self.root.bind('d',self.descartar_imagem)
        self.root.bind('<Right>',self.proxima_imagem)

        self.root.mainloop()

    def criar_botoes(self):
        botoes = ttk.Frame(self.mainframe)
        botoes.grid(row=1,column=0,sticky=(W,E))
        botoes.columnconfigure(0,weight=1)
        botoes.columnconfigure(1,weight=1)
        botoes.columnconfigure(2,weight=1)

        botao_proxima = ttk.Button(
        botoes,
        text="Próxima",
        command=self.proxima_imagem
        )
        botao_proxima.grid(column=2,row=0,sticky=E)

        botao_descartar = ttk.Button(
        botoes,
        text="Descartar (D)",
        command=self.descartar_imagem
        )
        botao_descartar.grid(column=1,row=0)


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

    def atualizar_nomes_imagens(self):
        for file in self.files[self.current_image_index:]:
            new_name = f"000{int(file.split('.')[0])-1}.jpg"[-8:]
            os.rename(
                os.path.join(self.diretorio,file),
                os.path.join(self.diretorio,new_name)
            )

    def descartar_imagem(self,*args):
        n_descartadas = len(os.listdir(
            os.path.join(self.diretorio,"descartadas")
        )) + 1
        os.rename(
        os.path.join(self.diretorio,self.files[self.current_image_index]),
        os.path.join(self.diretorio,"descartadas",f"000{n_descartadas}.jpg"[-8:]),
        )
        del self.files[self.current_image_index]
        self.atualizar_nomes_imagens()
        self.mostrar_imagem()

    def proxima_imagem(self,*args):
        self.current_image_index += 1
        self.mostrar_imagem()

diretorio = sys.argv[1]
classificador = Classificador(diretorio)
