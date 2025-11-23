from django.test import TestCase
from ..models import Celulares
from django.db import IntegrityError
from django.core.files.uploadedfile import SimpleUploadedFile


class CelularesUnitTest(TestCase):

    def setUp(self):
        self.dados_validos = {
            "nome": "Iphone 15",
            "marca": "Apple",
            "preco": 4999.99,
            "descricao": "Celular top de linha",
        }

    def test_criacao_celular_valido(self):
        celular = Celulares.objects.create(**self.dados_validos)

        self.assertEqual(celular.nome, "Iphone 15")
        self.assertEqual(celular.marca, "Apple")
        self.assertEqual(float(celular.preco), 4999.99)
        self.assertEqual(celular.descricao, "Celular top de linha")

    def test_criacao_celular_sem_campos_opcionais(self):
        dados = {"nome": "Galaxy S23", "marca": "Samsung", "preco": 3599.90}
        celular = Celulares.objects.create(**dados)

        self.assertIsNone(celular.descricao)
        self.assertFalse(celular.foto.name)
        self.assertIsNotNone(celular.data_criacao)

    def test_campos_obrigatorios(self):
        celular_sem_nome = Celulares(marca="Xiaomi", preco=1999.99)
        with self.assertRaises(Exception):
            celular_sem_nome.full_clean()

        celular_sem_marca = Celulares(nome="Teste", preco=1999.99)
        with self.assertRaises(Exception):
            celular_sem_marca.full_clean()

    def test_metodo_str(self):
        celular = Celulares.objects.create(**self.dados_validos)
        expected_str = (
            f"{celular.marca} {celular.nome}"  # O PROBLEMA - ESPAÇO ENTRE AS CHAVES
        )

        self.assertEqual(str(celular), expected_str)
        self.assertEqual(str(celular), "Apple Iphone 15")  # Este já está correto

    def test_ordenacao_padrao(self):
        celular1 = Celulares.objects.create(
            nome="Celular Antigo", marca="Teste", preco=1000.00
        )
        celular2 = Celulares.objects.create(
            nome="Celular Novo", marca="Teste", preco=2000.00
        )

        celulares = Celulares.objects.all()
        self.assertEqual(celulares[0], celular1)
        self.assertEqual(celulares[1], celular2)

    def test_data_criacao_automatica(self):
        celular = Celulares.objects.create(
            **self.dados_validos
        )  # "celulares" para "Celulares"
        self.assertIsNotNone(celular.data_criacao)
