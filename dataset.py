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
    def __init__(self,destino=None):
        if destino is not None:
            self.destino = destino
            if destino not in os.listdir():
                os.mkdir(destino)
        self.limiar_similaridade = 0.95

    def definir_destino(self,destino):
        self.destino = destino
        if self.destino not in os.listdir():
            os.mkdir(self.destino)

    def comparar_imagens(self,imagem,imagem_2):
        imagem = imread(imagem)
        imagem_2 = imread(imagem_2)

        if imagem.size > imagem_2.size:
            imagem_maior = imagem
            imagem_menor = imagem_2
        else:
            imagem_maior = imagem_2
            imagem_menor = imagem

        imagem_menor = resize(imagem_menor,imagem_maior.shape)
        imagem_maior = img_as_float(imagem_maior)
        return structural_similarity(imagem_menor,imagem_maior,channel_axis=-1) > self.limiar_similaridade

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

        if not self.e_unico(file):
            os.remove(file)

    def adicionar_imagens(self,imgs,categoria,n_exemplos):
        if categoria not in os.listdir(self.destino):
            os.mkdir(f"{self.destino}/{categoria}")
            os.mkdir(f"{self.destino}/{categoria}/descartadas")

        img_n=1
        for i in range(n_exemplos):
            try:
                img = imgs[i]
            except:
                break
            filename = f"{img_n}.jpg"
            self.adicionar_imagem(img,categoria,filename)
            img_n+=1

if __name__ == "__main__":
    main()
