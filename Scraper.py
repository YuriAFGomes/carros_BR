from urllib.request import urlopen
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

def salvar_fotos(pagina,n_exemplos):
    html = pagina.read().decode('utf-8')
    soup = bs(html,"html.parser")

def obter_exemplos(nomes,destino=None):
    for nome in nomes:
        nome = nome.replace(" ","+")
        url = URL_BASE.replace("{}",nome)
        driver.get(url)
        print(driver.page_source)

obter_exemplos(nomes_dos_carros)
