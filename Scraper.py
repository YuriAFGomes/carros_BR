import os, traceback

from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from config import SCRAPER_CONFIG
from dataset import Dataset

def listar_imgs(source):
    soup = bs(source,"html.parser")
    imgs = soup.find_all('img',class_='rg_i')
    return imgs

def rolar_pagina(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        mais_resultados = driver.find_element(
        By.XPATH,
        "//input[@class='mye4qd']"
        )
        mais_resultados.click()
    except:
        pass

def obter_imgs(url,n_exemplos,driver):
    driver.get(url)
    imgs = listar_imgs(driver.page_source)
    while len(imgs) < n_exemplos:
        n_atual = len(imgs)
        rolar_pagina(driver)
        imgs = listar_imgs(driver.page_source)
        
    return imgs

def salvar_fotos(url_base,categoria,n_exemplos,driver,dataset):
    categoria = categoria.replace('\n','')
    nome_url = categoria.replace(" ","+")
    url = url_base.replace("{}",nome_url)
    imgs = obter_imgs(url,n_exemplos,driver)

    dataset.adicionar_imagens(imgs,categoria,n_exemplos)


def obter_exemplos(url_base,categorias,n_exemplos,dataset):
    driver = webdriver.Firefox()

    for nome in categorias:
        salvar_fotos(url_base,nome,n_exemplos,driver,dataset)
    driver.close()

def main():
    with open('categorias.txt') as file:
        categorias = file.readlines()
    dataset = Dataset(SCRAPER_CONFIG['caminho_destino'])
    try:
        obter_exemplos(
            SCRAPER_CONFIG['url_base'],
            categorias,
            SCRAPER_CONFIG['n_exemplos'],
            dataset
        )
    except:
        traceback.print_exc()

if __name__ == '__main__':
    main()
