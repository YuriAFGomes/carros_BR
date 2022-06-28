import os, shutil
from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from Scraper import listar_imgs,obter_imgs,salvar_fotos,obter_exemplos
from config import SCRAPER_TEST_CONFIG

class TestScraper(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.categorias = ['Chevrolet Opala 1977','Ford Corcel 1977']
        if 'imagens_teste' not in os.listdir():
            os.mkdir('imagens_teste')
        cls.url = SCRAPER_TEST_CONFIG['url_base'].replace(
        "{}","Chevrolet+Opala+1977"
        )
        cls.driver.get(cls.url)
        cls.source = cls.driver.page_source

    def test_listar_imgs(self):
        imgs = listar_imgs(self.source)
        self.assertTrue(len(imgs)>20)

    def test_obter_imgs(self):
        imgs = obter_imgs(self.url,150,self.driver)
        self.assertTrue(len(imgs)>=150)

    def test_salvar_fotos(self):
        salvar_fotos(
        self.url,
        'imagens_teste',
        'Chevrolet Opala 1977',
        10,
        self.driver
        )
        self.assertTrue('Chevrolet Opala 1977' in os.listdir('imagens_teste'))
        self.assertEqual(
        10,
        len(os.listdir('imagens_teste/Chevrolet Opala 1977'))
        )

    def test_obter_exemplos(self):
        obter_exemplos(
            SCRAPER_TEST_CONFIG['url_base'],
            self.categorias,
            SCRAPER_TEST_CONFIG['caminho_destino'],
            SCRAPER_TEST_CONFIG['n_exemplos']
        )
        self.assertTrue('imagens_teste' in os.listdir())
        self.assertEqual(2,len(os.listdir('imagens_teste')))
        self.assertTrue('Chevrolet Opala 1977' in os.listdir('imagens_teste'))
        self.assertTrue('Ford Corcel 1977' in os.listdir('imagens_teste'))
        self.assertEqual(
        10,
        len(os.listdir('imagens_teste/Chevrolet Opala 1977'))
        )
        self.assertEqual(10,len(os.listdir('imagens_teste/Ford Corcel 1977')))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree('imagens_teste')
        cls.driver.close()
