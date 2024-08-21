import pandas as pd
import numpy as np
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects import Formula
from rpy2.robjects.conversion import localconverter
import matplotlib.pyplot as plt

# Activate the automatic conversion of pandas DataFrames to R DataFrames
pandas2ri.activate()

# Import the qte package from R
qte = importr('qte')

class QTEEstimator:
    def __init__(self, formula, xformla=None, data=None, probs=[0.05, 0.95, 0.05], se=False, iters=100):
        self.formula = formula
        self.xformla = xformla
        self.data = data

        if isinstance(probs, list) and len(probs) == 3:
            self.probs = ro.FloatVector(np.arange(probs[0], probs[1] + probs[2], probs[2]))
        else:
            self.probs = ro.FloatVector(probs)
            
        self.se = se
        self.iters = iters
        self.info = {}

    def fit(self):
        with localconverter(ro.default_converter + pandas2ri.converter):
            r_data = ro.conversion.py2rpy(self.data)

        # Call the ci_qte function from the R qte package
        if self.xformla is not None:
            self.result = qte.ci_qte(
                formla=ro.Formula(self.formula),
                xformla=ro.Formula(self.xformla),
                data=r_data,
                probs=self.probs,
                se=self.se,
                iters=self.iters
            )
        else:
            self.result = qte.ci_qte(
                formla=ro.Formula(self.formula),
                data=r_data,
                probs=self.probs,
                se=self.se,
                iters=self.iters
            )

        self._extract_info()

    def _extract_info(self):
        """Extract information from the R result object."""
        self.info['qte'] = np.array(self.result.rx2('qte'))
        self.info['probs'] = np.array(self.probs)
        
        if self.se:
            self.info['qte.lower'] = np.array(self.result.rx2('qte.lower'))
            self.info['qte.upper'] = np.array(self.result.rx2('qte.upper'))
        else:
            self.info['qte.lower'] = None
            self.info['qte.upper'] = None

    def summary(self):
        """Print a summary of the results."""
        summary = ro.r.summary(self.result)
        print(summary)
        return summary

    def plot(self):
        """Plot the Quantile Treatment Effects (QTE) with optional confidence intervals."""
        tau = self.info['probs']
        qte = self.info['qte']

        if self.se and self.info['qte.lower'] is not None and self.info['qte.upper'] is not None:
            lower_bound = self.info['qte.lower']
            upper_bound = self.info['qte.upper']

            plt.figure(figsize=(10, 6))
            plt.plot(tau, qte, 'o-', label="QTE")
            plt.fill_between(tau, lower_bound, upper_bound, color='gray', alpha=0.2, label="95% CI")
        else:
            plt.figure(figsize=(10, 6))
            plt.plot(tau, qte, 'o-', label="QTE")
        
        plt.axhline(y=0, color='r', linestyle='--', label="No Effect Line")
        plt.xlabel('Quantiles')
        plt.ylabel('QTE Estimates')
        plt.title('Quantile Treatment Effects (QTE)')
        plt.legend()
        plt.grid(True)
        plt.show()

    def get_results(self):
        """Create a pandas DataFrame with the estimated results."""
        df = pd.DataFrame({
            'Quantile': self.info['probs'],
            'QTE': self.info['qte']
        })
        
        if self.se and self.info['qte.lower'] is not None and self.info['qte.upper'] is not None:
            df['QTE Lower Bound'] = self.info['qte.lower']
            df['QTE Upper Bound'] = self.info['qte.upper']
        
        return df

