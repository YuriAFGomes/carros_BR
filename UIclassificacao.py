import os, json, sys
from functools import partial
from tkinter import Tk, ttk, N,W,E,S, IntVar, Toplevel, StringVar, Listbox
from PIL import Image,ImageTk, ImageOps

from dataset import Dataset

class Classificador:
    def __init__(self,diretorio):
        self.diretorio = diretorio
        self.categoria = None
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW",self.sair)

        self.dataset = Dataset(diretorio)
        self.root.geometry("800x800")
        self.root.columnconfigure(0,weight=1)
        self.root.rowconfigure(0,weight=1)
        self.mainframe = ttk.Frame(self.root,padding=12)
        self.mainframe.grid(column=0,row=0,sticky=(N,W,E,S))

        self.mainframe.columnconfigure(0,weight=1)
        self.mainframe.rowconfigure(1,weight=1)

        self.carregar_progresso()
        self.progressoVar = StringVar()
        self.image_label = ttk.Label(
            self.mainframe,
            textvariable=self.progressoVar,
            compound='top'
        )
        self.image_label.grid(column=0,row=1,sticky=(N,W,E,S))
        self.criar_botoes()
        self.selecionar_categoria()
        self.root.mainloop()

    def carregar_progresso(self):
        if 'progresso.json' in os.listdir(self.diretorio):
            with open(os.path.join(self.diretorio,'progresso.json')) as f:
                self.progresso = json.load(f)
        else:
            self.progresso = {}

    def salvar_progresso(self):
        self.progresso[self.categoria] = max(0,self.current_image_index - 1)
        with open(os.path.join(self.diretorio,'progresso.json'),'w') as f:
            json.dump(self.progresso,f)

    def sair(self):
        self.root.destroy()
        self.salvar_progresso()

    def atualizar_files(self):
        dir = os.listdir(os.path.join(self.diretorio,self.categoria))
        self.files = [file for file in dir if not os.path.isdir(os.path.join(self.diretorio,self.categoria,file))]
        self.files = sorted(self.files,key=len)

    def definir_categoria(self,categoria):
        if categoria in self.progresso:
            self.current_image_index = self.progresso[categoria]
        else:
            self.current_image_index = 0

        self.categoria = categoria

        self.atualizar_files()
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

    def trocar_categoria(self):
        self.salvar_progresso()
        self.selecionar_categoria()

    def criar_botoes(self):
        mudar_categoria = ttk.Button(
            self.mainframe,
            text="Mudar categoria",
            command=self.trocar_categoria
        )
        mudar_categoria.grid(row=0,column=0,sticky=E)

        botoes = ttk.Frame(self.mainframe)
        botoes.grid(row=2,column=0,sticky=(W,E))
        botoes.columnconfigure(0,weight=1)
        # botoes.columnconfigure(1,weight=1)
        # botoes.columnconfigure(2,weight=1)
        botoes.columnconfigure(3,weight=1)

        botao_anterior = ttk.Button(
            botoes,
            text="Anterior",
            command=self.imagem_anterior
        )
        botao_anterior.grid(column=0,row=0,sticky=W)

        botao_desfazer = ttk.Button(
            botoes,
            text="Desfazer (U)",
            command = self.desfazer
        )
        botao_desfazer.grid(row=0,column=1)

        botao_descartar = ttk.Button(
            botoes,
            text="Descartar (D)",
            command=self.descartar_imagem
        )
        botao_descartar.grid(column=2,row=0)

        botao_proxima = ttk.Button(
            botoes,
            text="Próxima",
            command=self.proxima_imagem
        )
        botao_proxima.grid(column=3,row=0,sticky=E)

        self.root.bind('d',self.descartar_imagem)
        self.root.bind('u',self.desfazer)
        self.root.bind('<Delete>',self.descartar_imagem)
        self.root.bind('<Right>',self.proxima_imagem)
        self.root.bind('<Left>',self.imagem_anterior)

    def atualizar_progresso(self):
        self.progressoVar.set(f"{self.current_image_index+1}/{len(self.files)}")

    def mostrar_imagem(self):
        loaded_image = Image.open(
            os.path.join(
                self.diretorio,
                self.categoria,
                self.files[self.current_image_index]
            )
        )
        loaded_image = ImageOps.contain(loaded_image,(760,760))
        image = ImageTk.PhotoImage(
            loaded_image
        )
        self.image_label.configure(image=image)
        self.image_label.image = image
        self.atualizar_progresso()

    def desfazer(self,*args):
        dir = os.path.join(self.diretorio,self.categoria)
        descartadas = os.listdir(
            os.path.join(dir,'descartadas')
        )
        if len(descartadas) == 0:
            return
        ultima = sorted(descartadas,key=len)[-1]
        novo_nome = f"{len(self.files)+1}.jpg"
        os.rename(
            os.path.join(dir,'descartadas',ultima),
            os.path.join(dir,novo_nome)
        )
        self.atualizar_files()
        self.atualizar_progresso()

    def proxima_imagem(self,*args):
        self.current_image_index = (self.current_image_index + 1)%len(self.files)
        self.mostrar_imagem()

    def descartar_imagem(self,*args):
        self.dataset.descartar_imagem(
            self.categoria,
            self.files[self.current_image_index]
        )
        self.atualizar_files()
        self.current_image_index = self.current_image_index%len(self.files)
        self.mostrar_imagem()
  
    def imagem_anterior(self,*args):
        self.current_image_index = (self.current_image_index - 1)%len(self.files)
        self.mostrar_imagem()

diretorio = sys.argv[1]
classificador = Classificador(diretorio)
