import unittest
from pyqte import qdid

class TestQdidFunction(unittest.TestCase):

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

    def test_qdid(self):
        result = qdid(**self.params)
        self.assertIsNotNone(result)
        # Adicione mais asserções para validar o resultado esperado

if __name__ == '__main__':
    unittest.main()

