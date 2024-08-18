import unittest
from pyqte import qtet

class TestQtetFunction(unittest.TestCase):

    def setUp(self):
        # Configurações iniciais antes de cada teste
        self.data = pd.DataFrame({
            'id': [1, 1, 2, 2],
            'year': [1975, 1978, 1975, 1978],
            'outcome': [5, 15, 6, 14],
            'treatment': [0, 1, 0, 1]
        })
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

    def test_qtet(self):
        result = qtet(**self.params)
        self.assertIsNotNone(result)
        # Adicione mais asserções para validar o resultado esperado

if __name__ == '__main__':
    unittest.main()



