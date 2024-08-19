import unittest
from pyqte.qte import QTEEstimator
import pandas as pd

class TestQTEEstimator(unittest.TestCase):

    def setUp(self):
        # Setup de um dataframe de teste básico
        data = {
            're': [100, 200, 300, 400],
            'treat': [1, 0, 1, 0],
        }
        self.df = pd.DataFrame(data)

    def test_qte_basic(self):
        estimator = QTEEstimator(data=self.df, outcome='re', treatment='treat', quantiles=[0.1, 0.5, 0.9])
        result = estimator.estimate()
        self.assertIsNotNone(result)
        # Testes específicos com base no que é esperado do resultado

if __name__ == '__main__':
    unittest.main()

