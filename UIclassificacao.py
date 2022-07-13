import os,sys
from functools import partial
from tkinter import Tk, ttk, N,W,E,S, IntVar, Toplevel, StringVar, Listbox
from PIL import Image,ImageTk, ImageOps

from dataset import Dataset

class Classificador:
    def __init__(self,diretorio):
        self.diretorio = diretorio
        self.categoria = None
        self.root = Tk()

        self.dataset = Dataset(diretorio)
        self.root.geometry("800x800")
        self.root.columnconfigure(0,weight=1)
        self.root.rowconfigure(0,weight=1)
        self.mainframe = ttk.Frame(self.root,padding=12)
        self.mainframe.grid(column=0,row=0,sticky=(N,W,E,S))

        self.mainframe.columnconfigure(0,weight=1)
        self.mainframe.rowconfigure(0,weight=1)

        self.current_image_index = 0

        self.image_label = ttk.Label(self.mainframe)
        self.image_label.grid(column=0,row=0,sticky=(N,W,E,S))
        self.criar_botoes()

        self.root.bind('d',self.descartar_imagem)
        self.root.bind('<Delete>',self.descartar_imagem)
        self.root.bind('<Right>',self.proxima_imagem)
        self.root.bind('<Left>',self.imagem_anterior)

        self.selecionar_categoria()
        self.root.mainloop()

    def definir_categoria(self,categoria):
        self.categoria = categoria
        self.files = [file for file in os.listdir(os.path.join(self.diretorio,self.categoria)) if not os.path.isdir(os.path.join(self.diretorio,self.categoria,file))]
        self.files = sorted(self.files,key=len)
        self.mostrar_imagem()

    def selecionar_categoria(self):
        def dismiss():
            w.grab_release()
            w.destroy()

        def confirmar():
            categoria = self.dataset.categorias[listbox.curselection()[0]]
            self.definir_categoria(categoria)
            dismiss()

        w = Toplevel(self.root)
        categoriasVar = StringVar(value=self.dataset.categorias)
        listbox = Listbox(w,listvariable=categoriasVar)
        listbox.grid(row=0,column=0)
        confirm = ttk.Button(
            w,
            text="OK",
            command=confirmar
        )
        confirm.grid(column=0,row=1,sticky=(W,E))
        w.protocol("WM_DELETE_WINDOW",dismiss)
        w.transient(self.root)
        w.wait_visibility()
        w.grab_set()
        w.wait_window()

    def criar_botoes(self):
        botoes = ttk.Frame(self.mainframe)
        botoes.grid(row=1,column=0,sticky=(W,E))
        botoes.columnconfigure(0,weight=1)
        botoes.columnconfigure(1,weight=1)
        botoes.columnconfigure(2,weight=1)

        botao_anterior = ttk.Button(
        botoes,
        text="Anterior",
        command=self.imagem_anterior
        )
        botao_anterior.grid(column=0,row=0,sticky=W)

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
            os.path.join(self.diretorio,self.categoria,self.files[self.current_image_index])
        )
        loaded_image = ImageOps.contain(loaded_image,(760,760))
        image = ImageTk.PhotoImage(
            loaded_image
        )
        self.image_label.configure(image=image)
        self.image_label.image = image

    def descartar_imagem(self,*args):
        self.dataset.descartar_imagem(
            self.categoria,
            self.files[self.current_image_index]
        )
        del self.files[self.current_image_index]
        self.mostrar_imagem()

    def proxima_imagem(self,*args):
        self.current_image_index += 1
        self.mostrar_imagem()

    def imagem_anterior(self,*args):
        self.current_image_index -= 1
        self.mostrar_imagem()

diretorio = sys.argv[1]
classificador = Classificador(diretorio)
