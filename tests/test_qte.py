import unittest
from pyqte import qte, qtet, ddid2, qdid, cic

class TestQteFunctions(unittest.TestCase):

    def setUp(self):
        # Configurações iniciais antes de cada teste
        self.data = ...  # Um exemplo de conjunto de dados de teste
        self.params = {
            'formula': 'outcome ~ treatment',
            't': 1978,
            'tmin1': 1975,
            'idname': 'id',
            'tname': 'year',
            'data': self.data,
            'probs': [0.1, 0.5, 0.9],
            'se': True,
            'iters': 10,
            'panel': True
        }

    def test_qte(self):
        result = qte(**self.params)
        self.assertIsNotNone(result)
        # Adicione mais asserções para validar o resultado esperado

    def test_qtet(self):
        result = qtet(**self.params)
        self.assertIsNotNone(result)
        # Adicione mais asserções para validar o resultado esperado

    def test_ddid2(self):
        result = ddid2(**self.params)
        self.assertIsNotNone(result)
        # Adicione mais asserções para validar o resultado esperado

    def test_qdid(self):
        result = qdid(**self.params)
        self.assertIsNotNone(result)
        # Adicione mais asserções para validar o resultado esperado

    def test_cic(self):
        result = cic(**self.params)
        self.assertIsNotNone(result)
        # Adicione mais asserções para validar o resultado esperado

if __name__ == '__main__':
    unittest.main()


