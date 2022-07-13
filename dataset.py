import os, traceback
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
from skimage import img_as_float
from skimage.io import imread
from skimage.metrics import structural_similarity
from skimage.transform import resize
from PIL import Image
from urllib.request import urlretrieve


class Dataset:
    def __init__(self,destino):
        self.limiar_similaridade = 0.95
        self.destino = destino
        if not os.path.exists(destino):
            os.mkdir(destino)
        self.categorias = self.atualizar_categorias()

    def atualizar_categorias(self):
        categorias = os.listdir(self.destino)
        return categorias

    def comparar_imagens(self,imagem,imagem_2):
        imagem = imread(imagem,as_gray=True)
        imagem_2 = imread(imagem_2,as_gray=True)

        imagem = resize(imagem,(100,100,1))
        imagem_2 = resize(imagem_2,(100,100,1))
        return structural_similarity(imagem,imagem_2,channel_axis=-1) > self.limiar_similaridade

    def e_unico(self,caminho):
        caminho = Path(caminho)
        parent = Path(caminho).parent
        for caminho_2 in os.listdir(parent):
            caminho_2 = os.path.join(parent,caminho_2)
            if os.path.samefile(caminho,caminho_2):
                continue
            if os.path.isdir(caminho_2):
                continue
            if self.comparar_imagens(caminho,caminho_2):
                return False
        return True

    def adicionar_imagem(self,img,categoria,filename):
        caminho = f"{self.destino}/{categoria}/{filename}"
        try:
            file,info = urlretrieve(img['src'],caminho)
        except:
            try:
                file,info = urlretrieve(
                img['data-src'],
                caminho
                )
            except:
                traceback.print_exc()
        return file

    def renomear_arquivos(self,categoria,index=0):
        caminho = os.path.join(self.destino,categoria)
        for item in os.listdir(caminho)[index:]:
            if not os.path.isdir(os.path.join(caminho,item)):
                novo_nome = f"{int(item.split('.')[0])-1}.jpg"
                os.rename(
                    os.path.join(caminho,item),
                    os.path.join(caminho,novo_nome)
                )

    def descartar_imagem(self,categoria,filename):
        index_imagem = int(filename.split(".")[0])-1
        caminho_categoria = os.path.join(self.destino,categoria)
        n_descartadas = len(os.listdir(os.path.join(caminho_categoria,"descartadas")))
        novo_filename = f"{n_descartadas+1}.jpg"
        os.rename(
            os.path.join(caminho_categoria,filename),
            os.path.join(caminho_categoria,"descartadas",novo_filename)
        )
        self.renomear_arquivos(categoria,index_imagem)

    def adicionar_imagens(self,imgs,categoria,n_exemplos):
        if categoria not in os.listdir(self.destino):
            os.mkdir(f"{self.destino}/{categoria}")
            os.mkdir(f"{self.destino}/{categoria}/descartadas")
            self.atualizar_categorias()

        n_imagens_salvas = len(
        os.listdir(os.path.join(self.destino,categoria))
        ) - 1

        img_n = n_imagens_salvas + 1
        for i in range(n_exemplos):
            try:
                img = imgs[i]
            except:
                break
            filename = f"{img_n}.jpg"
            file = self.adicionar_imagem(img,categoria,filename)
            if not self.e_unico(file):
                os.remove(file)
                continue
            img_n+=1

if __name__ == "__main__":
    main()
