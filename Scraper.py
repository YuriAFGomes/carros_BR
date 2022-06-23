from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
nomes_dos_carros = [
"jeep willys",
# "volkswagen fusca",
# "chevrolet chevette",
# "chevrolet monza",
# "volkswagen gol",
# "fiat palio",
# "chevrolet onix"
]

N_EXEMPLOS = 500
URL_BASE = "https://www.google.com/search?q={}&tbm=isch"
driver = webdriver.Firefox()
wait = WebDriverWait(driver,10)

def salvar_fotos(pagina,n_exemplos=10):
    soup = bs(pagina,"html.parser")
    imgs = soup.find_all('img',class_='rg_i')

    for i in range(len(imgs)):
        img = imgs[i]
        filename = f"car_{i+1}.jpg"
        try:
            urlretrieve(img['src'],f"imagens/{filename}")
        except:
            pass

def obter_exemplos(nomes,destino=None):
    for nome in nomes:
        nome = nome.replace(" ","+")
        url = URL_BASE.replace("{}",nome)
        driver.get(url)
        salvar_fotos(driver.page_source)
        # print(driver.page_source)

obter_exemplos(nomes_dos_carros)

driver.close()
