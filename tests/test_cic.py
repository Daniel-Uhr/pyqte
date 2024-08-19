import unittest
import pandas as pd
from pyqte.cic import CiCEstimator
from pyqte.helper_functions import prepare_r_data, create_formula

class TestCiCEstimator(unittest.TestCase):

    def setUp(self):
        # Setup a basic test DataFrame
        data = {
            'id': [1, 2, 3, 4, 5, 6],
            'year': [1974, 1974, 1975, 1975, 1978, 1978],
            'treat': [0, 1, 0, 1, 0, 1],
            're': [5000, 7000, 6000, 8000, 6500, 8500],
            'age': [22, 23, 24, 25, 26, 27],
            'education': [12, 12, 14, 14, 16, 16],
            'black': [1, 0, 1, 0, 1, 0],
            'hispanic': [0, 1, 0, 1, 0, 1],
            'married': [0, 1, 0, 1, 0, 1],
            'nodegree': [1, 0, 1, 0, 1, 0]
        }
        self.df = pd.DataFrame(data)
        self.r_df = prepare_r_data(self.df)

    def test_cic_basic(self):
        formula = create_formula('re', ['treat'])
        estimator = CiCEstimator(
            data=self.r_df,
            formula=formula,
            t=1978,
            tmin1=1975,
            tmin2=1974,
            idname='id',
            probs=[0.1, 0.5, 0.9],
            se=True,
            iters=10
        )
        result = estimator.estimate()
        self.assertIsNotNone(result)
        # Assert expected structure and values in the result
        self.assertIn('Quantile', result.columns)
        self.assertIn('QTE', result.columns)
        self.assertIn('Std. Error', result.columns)

    def test_cic_with_covariates(self):
        formula = create_formula('re', ['treat', 'age', 'education'])
        estimator = CiCEstimator(
            data=self.r_df,
            formula=formula,
            t=1978,
            tmin1=1975,
            tmin2=1974,
            idname='id',
            probs=[0.1, 0.5, 0.9],
            se=True,
            iters=10
        )
        result = estimator.estimate()
        self.assertIsNotNone(result)
        # Check the results for correct dimensions and presence of quantiles
        self.assertEqual(result.shape[0], 3)  # There should be 3 quantiles
        self.assertTrue(all(result['Quantile'].isin([0.1, 0.5, 0.9])))

if __name__ == '__main__':
    unittest.main()

