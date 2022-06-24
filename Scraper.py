import os, traceback, time

from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

with open('categorias.txt') as file:
    categorias = file.readlines()

caminho_destino = "imagens"
N_EXEMPLOS = 50
URL_BASE = "https://www.google.com/search?q={}&tbm=isch"

driver = webdriver.Firefox()
wait = WebDriverWait(driver,10)

def fetch_imgs():
    time.sleep(0.3)
    source = driver.page_source
    soup = bs(source,"html.parser")
    imgs = soup.find_all('img',class_='rg_i')
    return imgs

def salvar_fotos(categoria,pagina,n_exemplos):
    categoria = categoria.replace('\n','')
    nome_url = categoria.replace(" ","+")
    url = URL_BASE.replace("{}",nome_url)
    driver.get(url)
    imgs = fetch_imgs()
    n_imgs = len(imgs)

    while n_imgs < n_exemplos+24:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        imgs = fetch_imgs()
        n_imgs = len(imgs)

    if categoria not in os.listdir(caminho_destino):
        os.mkdir(f"{caminho_destino}/{categoria}")

    for i in range(min(n_exemplos,len(imgs))):
        img = imgs[i]
        filename = f"{i+1}.jpg"
        try:
            urlretrieve(img['src'],f"{caminho_destino}/{categoria}/{filename}")
        except:
            pass

def obter_exemplos(categorias,caminho_destino,n_exemplos=50):
    for nome in categorias:
        salvar_fotos(nome,driver.page_source,n_exemplos)

try:
    obter_exemplos(categorias,caminho_destino)
except:
    traceback.print_exc()
finally:
    driver.close()
