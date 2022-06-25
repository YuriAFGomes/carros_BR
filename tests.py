import os
from unittest import TestCase
from selenium import webdriver

from Scraper import fetch_imgs
from config import SCRAPER_TEST_CONFIG

class TestScraper(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        categorias = ['Chevrolet Opala 1977','Ford Corcel 1977']
        os.mkdir('imagens_teste')
        url = SCRAPER_TEST_CONFIG['url_base'].replace("{}","Chevrolet+Opala+1977")
        cls.driver.get(url)
        cls.source = cls.driver.page_source

    def test_fetch_imgs(self):
        imgs = fetch_imgs(self.source)
        self.assertEqual('list',type(imgs))

    @classmethod
    def tearDownClass(cls):
        os.rmdir('imagens_teste')
        cls.driver.close()
