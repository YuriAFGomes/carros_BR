import os, traceback, time

from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import SCRAPER_CONFIG

def fetch_imgs(source):
    soup = bs(source,"html.parser")
    imgs = soup.find_all('img',class_='rg_i')
    return imgs

def salvar_fotos(url_base,caminho_destino,categoria,n_exemplos):
    categoria = categoria.replace('\n','')
    nome_url = categoria.replace(" ","+")
    url = url_base.replace("{}",nome_url)
    driver.get(url)
    imgs = fetch_imgs(driver.page_source)

    while len(imgs) < n_exemplos+50:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        imgs = fetch_imgs(driver.page_source)

    if categoria not in os.listdir(caminho_destino):
        os.mkdir(f"{caminho_destino}/{categoria}")

    img_n=1
    for i in range(len(imgs)):
        img = imgs[i]
        filename = f"{img_n}.jpg"
        try:
            urlretrieve(img['src'],f"{caminho_destino}/{categoria}/{filename}")
            img_n+=1
        except:
            try:
                urlretrieve(img['data-src'],f"{caminho_destino}/{categoria}/{filename}")
                img_n+=1
            except:
                traceback.print_exc()

def obter_exemplos(url_base,categorias,caminho_destino,n_exemplos):
    for nome in categorias:
        salvar_fotos(url_base,caminho_destino,nome,n_exemplos)

def main():
    with open('categorias.txt') as file:
        categorias = file.readlines()
    driver = webdriver.Firefox()
    wait = WebDriverWait(driver,10)
    try:
        obter_exemplos(
            SCRAPER_CONFIG['url_base'],
            categorias,
            SCRAPER_CONFIG['caminho_destino'],
            SCRAPER_CONFIG['n_exemplos']
        )
    except:
        traceback.print_exc()
    finally:
        driver.close()

if __name__ == '__main__':
    main()
