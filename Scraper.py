import os
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

with open('categorias.txt') as file:
    categorias = file.readlines()

caminho_destino = "imagens"
N_EXEMPLOS = 500
URL_BASE = "https://www.google.com/search?q={}&tbm=isch"
driver = webdriver.Firefox()
wait = WebDriverWait(driver,10)

def salvar_fotos(categoria,pagina,n_exemplos=10):
    soup = bs(pagina,"html.parser")
    imgs = soup.find_all('img',class_='rg_i')

    for i in range(len(imgs)):
        img = imgs[i]
        filename = f"{categoria}_{i+1}.jpg"
        try:
            urlretrieve(img['src'],f"{caminho_destino}/{filename}")
        except Exception as e:
            print(e)

def obter_exemplos(categorias,caminho_destino):
    for nome in categorias:
        nome = nome.replace(" ","+")
        nome = nome.replace('\n','')
        url = URL_BASE.replace("{}",nome)
        driver.get(url)
        salvar_fotos(nome,driver.page_source)

try:
    obter_exemplos(categorias,caminho_destino)
except Exception as e:
    print(e)
finally:
    driver.close()
