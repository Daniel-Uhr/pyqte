import unittest
import pandas as pd
from pyqte.helper_functions import (
    prepare_r_data,
    create_formula,
    calculate_summary_statistics,
    bootstrap_sample,
    calculate_confidence_intervals,
    merge_dataframes,
    generate_quantile_regression_results
)
from statsmodels.regression.quantile_regression import QuantReg

class TestHelperFunctions(unittest.TestCase):

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

    def test_prepare_r_data(self):
        r_df = prepare_r_data(self.df)
        self.assertIsNotNone(r_df)
        # Additional checks to confirm the DataFrame has been converted correctly

    def test_create_formula(self):
        formula = create_formula('re', ['treat', 'age'])
        self.assertEqual(str(formula), 're ~ treat + age')

    def test_calculate_summary_statistics(self):
        summary = calculate_summary_statistics(self.df)
        self.assertIn('re', summary.columns)
        self.assertIn('age', summary.columns)
        self.assertEqual(summary.shape[1], self.df.shape[1])

    def test_bootstrap_sample(self):
        samples = bootstrap_sample(self.df, n=100)
        self.assertEqual(len(samples), 100)
        for sample in samples:
            self.assertEqual(sample.shape, self.df.shape)

    def test_calculate_confidence_intervals(self):
        intervals = calculate_confidence_intervals(self.df[['re']])
        self.assertIn('Lower Bound', intervals.columns)
        self.assertIn('Upper Bound', intervals.columns)
        self.assertEqual(intervals.shape[0], 1)  # Expect one row for the 're' column

    def test_merge_dataframes(self):
        df1 = self.df[['id', 're']]
        df2 = self.df[['id', 'age']]
        merged_df = merge_dataframes(df1, df2, on='id')
        self.assertEqual(merged_df.shape[0], self.df.shape[0])
        self.assertEqual(merged_df.shape[1], 3)  # id, re, and age

    def test_generate_quantile_regression_results(self):
        model = QuantReg(self.df['re'], self.df[['treat']])
        quantiles = [0.25, 0.5, 0.75]
        results = generate_quantile_regression_results(model, quantiles)
        self.assertEqual(len(results), 3)
        for q in quantiles:
            self.assertIn(q, results)
            self.assertIn('coefficients', results[q])
            self.assertIn('confidence_intervals', results[q])

if __name__ == '__main__':
    unittest.main()

