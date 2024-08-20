import pandas as pd
import numpy as np
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects.conversion import localconverter
import matplotlib.pyplot as plt

# Activate the automatic conversion of pandas DataFrame to R DataFrame
pandas2ri.activate()

# Import the qte package from R
qte = importr('qte')

class QTEEstimator:
    def __init__(self, formula, xformla, data, probs=[0.05, 0.95, 0.05], se=True, iters=100, method='logit', w=None, pl=False, cores=2):
        self.formula = formula
        self.xformla = xformla
        self.data = data
        self.method = method
        self.w = w
        self.pl = pl
        self.cores = cores

        # Handle the probs argument to create a sequence
        if isinstance(probs, list) and len(probs) == 3:
            self.probs = ro.FloatVector(np.arange(probs[0], probs[1] + probs[2], probs[2]))
        else:
            self.probs = ro.FloatVector(probs)
            
        self.se = se
        self.iters = iters

    def fit(self):
        with localconverter(ro.default_converter + pandas2ri.converter):
            r_data = ro.conversion.py2rpy(self.data)

        # Prepare additional arguments based on presence
        additional_args = {}
        if self.w is not None:
            additional_args['w'] = ro.FloatVector(self.w)
        if self.pl:
            additional_args['pl'] = True
            additional_args['cores'] = self.cores

        # Call the qte function from the R qte package
        result = qte.ci_qte(
            formla=ro.Formula(self.formula),
            xformla=ro.Formula(self.xformla),
            data=r_data,
            probs=self.probs,
            se=self.se,
            iters=self.iters,
            method=self.method,
            **additional_args  # Add additional args if provided
        )

        self.result = result

    def summary(self):
        summary = ro.r.summary(self.result)
        print(summary)
        return summary

    def plot(self):
        tau = np.array(self.probs)
        qte = np.array(self.result.rx2('qte'))
        lower_bound = np.array(self.result.rx2('qte.lower'))
        upper_bound = np.array(self.result.rx2('qte.upper'))

        plt.figure(figsize=(10, 6))
        plt.plot(tau, qte, 'o-', label="QTE")
        plt.fill_between(tau, lower_bound, upper_bound, color='gray', alpha=0.2, label="95% CI")
        plt.axhline(y=0, color='r', linestyle='--', label="No Effect Line")
        plt.xlabel('Quantiles')
        plt.ylabel('QTE Estimates')
        plt.title('Quantile Treatment Effects (QTE)')
        plt.legend()
        plt.grid(True)
        plt.show()

