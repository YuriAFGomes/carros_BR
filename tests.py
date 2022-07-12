import os, shutil, time
from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from scraper import listar_imgs,obter_imgs,salvar_fotos,obter_exemplos
from config import SCRAPER_TEST_CONFIG
from dataset import Dataset

class TestScraper(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.categorias = ['Chevrolet Opala 1977','Ford Corcel 1977']
        cls.diretorio = SCRAPER_TEST_CONFIG['caminho_destino']
        if cls.diretorio not in os.listdir():
            os.mkdir(cls.diretorio)
        cls.url = SCRAPER_TEST_CONFIG['url_base'].replace(
        "{}","Chevrolet+Opala+1977"
        )
        cls.driver.get(cls.url)
        cls.source = cls.driver.page_source
        cls.dataset = Dataset(SCRAPER_TEST_CONFIG['caminho_destino'])

    def test_listar_imgs(self):
        imgs = listar_imgs(self.source)
        self.assertTrue(len(imgs)>20)

    def test_obter_imgs(self):
        imgs = obter_imgs(self.url,150,self.driver)
        self.assertTrue(len(imgs)>=150)

    def test_obter_1500_imgs(self):
        imgs = obter_imgs(self.url,1500,self.driver)
        self.assertTrue(len(imgs)>=500)

    def test_salvar_fotos(self):
        salvar_fotos(
        self.url,
        'Chevrolet Opala 1977',
        10,
        self.driver,
        self.dataset
        )
        self.assertTrue('Chevrolet Opala 1977' in os.listdir('imagens_teste'))
        self.assertTrue(
        len(os.listdir('imagens_teste/Chevrolet Opala 1977')) >= 7
        )

    def test_nao_salvar_foto_repetida(self):
        url = SCRAPER_TEST_CONFIG['url_base'].replace(
        "{}","Volkswagen SP2"
        )

        img = obter_imgs(self.url,1,self.driver)[0]
        imgs = [img,img]
        self.dataset.adicionar_imagens(imgs,"Volkswagen SP2",2)
        self.assertEqual(2,len(os.listdir("imagens_teste/Volkswagen SP2")))

    def test_nome_arquivo_salvo(self):
        dataset = Dataset('test_assets')

        salvar_fotos(
            SCRAPER_TEST_CONFIG['url_base'],
            "Gurgel Motomachine",
            1,
            self.driver,
            dataset
        )
        self.assertEqual(3,len(os.listdir("test_assets/Gurgel Motomachine")))
        self.assertTrue('2.jpg' in os.listdir("test_assets/Gurgel Motomachine"))
        self.assertTrue('1.jpg' in os.listdir("test_assets/Gurgel Motomachine"))

    def test_obter_exemplos(self):
        obter_exemplos(
            SCRAPER_TEST_CONFIG['url_base'],
            self.categorias,
            SCRAPER_TEST_CONFIG['n_exemplos'],
            self.dataset
        )
        self.assertTrue('imagens_teste' in os.listdir())
        self.assertTrue(2<=len(os.listdir('imagens_teste')))
        self.assertTrue('Chevrolet Opala 1977' in os.listdir('imagens_teste'))
        self.assertTrue('Ford Corcel 1977' in os.listdir('imagens_teste'))
        self.assertEqual(
        11,
        len(os.listdir('imagens_teste/Chevrolet Opala 1977'))
        )
        self.assertEqual(11,len(os.listdir('imagens_teste/Ford Corcel 1977')))

    def test_mais_resultados(self):
        imgs = obter_imgs(self.url,500,self.driver)
        self.assertTrue(len(imgs)>=500)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree('imagens_teste')
        try:
            os.remove("test_assets/Gurgel Motomachine/2.jpg")
        except:
            pass
        cls.driver.close()

class TestDataset(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.diretorio = SCRAPER_TEST_CONFIG['caminho_destino']
        if cls.diretorio not in os.listdir():
            os.mkdir(cls.diretorio)
        cls.dataset = Dataset(SCRAPER_TEST_CONFIG['caminho_destino'])
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree('imagens_teste')

    def setUp(self):
        try:
            os.mkdir(os.path.join(self.diretorio,"Gurgel X15"))
        except:
            pass
    def tearDown(self):
        shutil.rmtree(os.path.join(self.diretorio,"Gurgel X15"))

    def test_renomear_arquivos(self):
        src = "test_assets/gurgel x15.jpg"
        caminho = os.path.join(self.diretorio,"Gurgel X15")
        shutil.copy(src,os.path.join(caminho,"1.jpg"))
        shutil.copy(src,os.path.join(caminho,"3.jpg"))
        shutil.copy(src,os.path.join(caminho,"4.jpg"))

        self.dataset.renomear_arquivos("Gurgel X15",1)
        dir = os.listdir(caminho)
        self.assertEqual(3,len(dir))
        self.assertTrue('1.jpg' in dir)
        self.assertTrue('2.jpg' in dir)
        self.assertTrue('3.jpg' in dir)
        self.assertTrue('4.jpg' not in dir)

    def test_descartar_imagem(self):
        src = "test_assets/gurgel x15.jpg"
        caminho = os.path.join(self.diretorio,"Gurgel X15")
        shutil.copy(src,os.path.join(caminho,"1.jpg"))
        shutil.copy(src,os.path.join(caminho,"2.jpg"))
        shutil.copy(src,os.path.join(caminho,"3.jpg"))

        os.mkdir(os.path.join(caminho,"descartadas"))

        dir = os.listdir(caminho)
        self.dataset.descartar_imagem("Gurgel X15",'2.jpg')

        self.assertEqual(1,len(os.listdir(os.path.join(caminho,"descartadas"))))
        self.assertEqual(3,len(os.listdir(caminho)))
        self.assertTrue("3.jpg" not in os.listdir(caminho))
        self.assertTrue("2.jpg" in os.listdir(caminho))

        self.dataset.descartar_imagem("Gurgel X15",'1.jpg')

        self.assertEqual(2,len(os.listdir(caminho)))
        self.assertEqual(2,len(os.listdir(os.path.join(caminho,"descartadas"))))
        self.assertTrue("2.jpg" not in os.listdir(caminho))
        self.assertTrue("1.jpg" in os.listdir(caminho))

        print(os.listdir(os.path.join(caminho,"descartadas")))
        self.assertTrue("2.jpg" in os.listdir(os.path.join(caminho,"descartadas")))
        self.assertTrue("1.jpg" in os.listdir(os.path.join(caminho,"descartadas")))

    def test_comparar_imagens(self):
        comparacao = self.dataset.comparar_imagens(
            "test_assets/belle belinha.jpg",
            "test_assets/belle belinha reduzido.jpg"
        )
        end = time.time()
        self.assertTrue(comparacao)
