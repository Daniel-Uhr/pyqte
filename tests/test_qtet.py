import unittest
import pandas as pd
from pyqte.qtet import QTETEstimator
from pyqte.helper_functions import prepare_r_data, create_formula

class TestQTETEstimator(unittest.TestCase):

    def setUp(self):
        # Setup a basic test DataFrame
        data = {
            'id': [1, 2, 3, 4],
            'year': [1975, 1975, 1978, 1978],
            'treat': [0, 1, 0, 1],
            're': [5000, 7000, 6000, 8000],
            'age': [22, 23, 24, 25],
            'education': [12, 12, 14, 14],
            'black': [1, 0, 1, 0],
            'hispanic': [0, 1, 0, 1],
            'married': [0, 1, 0, 1],
            'nodegree': [1, 0, 1, 0]
        }
        self.df = pd.DataFrame(data)
        self.r_df = prepare_r_data(self.df)

    def test_qtet_basic(self):
        formula = create_formula('re', ['treat', 'age', 'education', 'black', 'hispanic', 'married', 'nodegree'])
        estimator = QTETEstimator(
            formula=formula,
            t=1978,
            tmin1=1975,
            idname='id',
            tname='year',
            data=self.r_df,
            probs=[0.1, 0.5, 0.9],
            se=True,
            iters=10,
            panel=True
        )
        result = estimator.estimate()
        self.assertIsNotNone(result)
        # Assert expected structure and values in the result
        self.assertIn('Quantile', result.columns)
        self.assertIn('QTE', result.columns)
        self.assertIn('Std. Error', result.columns)

    def test_qtet_with_covariates(self):
        formula = create_formula('re', ['treat', 'age', 'education', 'black'])
        estimator = QTETEstimator(
            formula=formula,
            t=1978,
            tmin1=1975,
            idname='id',
            tname='year',
            data=self.r_df,
            probs=[0.1, 0.5, 0.9],
            se=True,
            iters=10,
            panel=True
        )
        result = estimator.estimate()
        self.assertIsNotNone(result)
        # Check the results for correct dimensions and presence of quantiles
        self.assertEqual(result.shape[0], 3)  # There should be 3 quantiles
        self.assertTrue(all(result['Quantile'].isin([0.1, 0.5, 0.9])))

if __name__ == '__main__':
    unittest.main()


