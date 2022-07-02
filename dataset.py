import os, traceback
import numpy as np
from urllib.request import urlretrieve

class Dataset:
    def __init__(self,destino=None):
        if destino is not None:
            self.destino = destino
            if destino not in os.listdir():
                os.mkdir(destino)

    def definir_destino(self,destino):
        self.destino = destino
        if self.destino not in os.listdir():
            os.mkdir(self.destino)

    def adicionar_imagem(self,img,categoria,filename):
        try:
            urlretrieve(img['src'],f"{self.destino}/{categoria}/{filename}")
        except:
            try:
                urlretrieve(
                img['data-src'],
                f"{self.destino}/{categoria}/{filename}"
                )
            except:
                traceback.print_exc()

    def adicionar_imagens(self,imgs,categoria,n_exemplos):
        if categoria not in os.listdir(self.destino):
            os.mkdir(f"{self.destino}/{categoria}")

        img_n=1
        for i in range(n_exemplos):
            img = imgs[i]
            filename = f"{img_n}.jpg"
            self.adicionar_imagem(img,categoria,filename)
            img_n+=1

if __name__ == "__main__":
    main()
