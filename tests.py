import os
from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


from Scraper import listar_imgs,obter_imgs
from config import SCRAPER_TEST_CONFIG

class TestScraper(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        categorias = ['Chevrolet Opala 1977','Ford Corcel 1977']
        if 'imagens_teste' not in os.listdir():
            os.mkdir('imagens_teste')
        cls.url = SCRAPER_TEST_CONFIG['url_base'].replace("{}","Chevrolet+Opala+1977")
        cls.driver.get(cls.url)
        cls.source = cls.driver.page_source

    def test_listar_imgs(self):
        imgs = listar_imgs(self.source)
        self.assertTrue(len(imgs)>20)

    def test_obter_imgs(self):
        imgs = obter_imgs(self.url,150,self.driver)
        self.assertTrue(len(imgs)>=150)

    @classmethod
    def tearDownClass(cls):
        os.rmdir('imagens_teste')
        cls.driver.close()
