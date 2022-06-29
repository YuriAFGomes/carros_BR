import os, traceback

from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from config import SCRAPER_CONFIG

def listar_imgs(source):
    soup = bs(source,"html.parser")
    imgs = soup.find_all('img',class_='rg_i')
    return imgs

def rolar_pagina(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        mais_resultados = driver.find_element(By.XPATH,"//input[@class='mye4qd']")
        mais_resultados.click()
    except:
        pass

def obter_imgs(url,n_exemplos,driver):
    driver.get(url)
    imgs = listar_imgs(driver.page_source)
    while len(imgs) < n_exemplos:
        print(len(imgs))
        rolar_pagina(driver)
        imgs = listar_imgs(driver.page_source)
    return imgs

def salvar_fotos(url_base,caminho_destino,categoria,n_exemplos,driver):
    categoria = categoria.replace('\n','')
    nome_url = categoria.replace(" ","+")
    url = url_base.replace("{}",nome_url)
    imgs = obter_imgs(url,n_exemplos,driver)

    if categoria not in os.listdir(caminho_destino):
        os.mkdir(f"{caminho_destino}/{categoria}")

    img_n=1
    for i in range(n_exemplos):
        img = imgs[i]
        filename = f"{img_n}.jpg"
        try:
            urlretrieve(img['src'],f"{caminho_destino}/{categoria}/{filename}")
            img_n+=1
        except:
            try:
                urlretrieve(
                img['data-src'],
                f"{caminho_destino}/{categoria}/{filename}"
                )
                img_n+=1
            except:
                traceback.print_exc()

def obter_exemplos(url_base,categorias,caminho_destino,n_exemplos):
    driver = webdriver.Firefox()

    if caminho_destino not in os.listdir():
        os.mkdir(caminho_destino)

    for nome in categorias:
        salvar_fotos(url_base,caminho_destino,nome,n_exemplos,driver)
    driver.close()

def main():
    with open('categorias.txt') as file:
        categorias = file.readlines()

    try:
        obter_exemplos(
            SCRAPER_CONFIG['url_base'],
            categorias,
            SCRAPER_CONFIG['caminho_destino'],
            SCRAPER_CONFIG['n_exemplos']
        )
    except:
        traceback.print_exc()

if __name__ == '__main__':
    main()
