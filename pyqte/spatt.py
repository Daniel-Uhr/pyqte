import pandas as pd
import numpy as np
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects import Formula, FloatVector
import matplotlib.pyplot as plt

# Activate the automatic conversion of pandas DataFrames to R data.frames
pandas2ri.activate()

# Import the R 'qte' package
qte = importr('qte')

class SpATT_Estimator:
    """
    SpATT_Estimator is used to estimate Spatial Average Treatment on the Treated (SpATT)
    effects using the R 'qte' package via rpy2.
    """
    
    def __init__(self, formula, data, t, tmin1, tname, xformla=None, w=None, panel=False, idname=None, 
                 iters=100, alp=0.05, method="logit", plot=False, se=True, 
                 retEachIter=False, seedvec=None, pl=False, cores=2):
        self.formula = formula
        self.data = data
        self.t = t
        self.tmin1 = tmin1
        self.tname = tname
        self.xformla = xformla
        self.w = w
        self.panel = panel
        self.idname = idname
        self.iters = iters
        self.alp = alp
        self.method = method
        self.plot = plot
        self.se = se
        self.retEachIter = retEachIter
        self.seedvec = seedvec
        self.pl = pl
        self.cores = cores
        self.result = None
        self.info = {}

    def fit(self):
        r_formula = Formula(self.formula)
        r_data = pandas2ri.py2rpy(self.data)
        
        additional_args = {
            't': self.t,
            'tmin1': self.tmin1,
            'tname': self.tname,
            'se': self.se,
            'iters': self.iters,
            'alp': self.alp,
            'method': self.method,
            'plot': self.plot,
            'retEachIter': self.retEachIter,
            'pl': self.pl,
            'cores': self.cores
        }

        if self.xformla:
            additional_args['xformla'] = Formula(self.xformla)
        
        if self.w is not None:
            additional_args['w'] = FloatVector(self.w)

        if self.idname:
            additional_args['idname'] = self.idname
        
        if self.seedvec is not None:
            additional_args['seedvec'] = FloatVector(self.seedvec)

        if self.panel:
            additional_args['panel'] = self.panel

        self.result = qte.spatt(
            formla=r_formula,
            data=r_data,
            **additional_args
        )
        self._extract_info()

    def _extract_info(self):
        self.info['qte'] = np.array(self.result.rx2('qte'))
        self.info['probs'] = np.array(self.result.rx2('probs'))

        if self.se:
            self.info['qte.lower'] = np.array(self.result.rx2('qte.lower'))
            self.info['qte.upper'] = np.array(self.result.rx2('qte.upper'))
        else:
            self.info['qte.lower'] = None
            self.info['qte.upper'] = None

    def summary(self):
        if self.result is None:
            raise ValueError("Model has not been fitted yet. Call `fit()` before calling `summary()`.")
        summary = ro.r.summary(self.result)
        print(summary)
        return summary

    def plot(self):
        if self.result is None:
            raise ValueError("Model has not been fitted yet. Call `fit()` before calling `plot()`.")
        
        tau = self.info['probs']
        qte = self.info['qte']

        plt.figure(figsize=(10, 6))
        plt.plot(tau, qte, 'o-', label="SpATT")

        if self.se:
            if self.info['qte.lower'] is not None and self.info['qte.upper'] is not None:
                lower_bound = self.info['qte.lower']
                upper_bound = self.info['qte.upper']
                plt.fill_between(tau, lower_bound, upper_bound, color='gray', alpha=0.2, label="95% CI")
            else:
                print("Confidence intervals are not available. Plotting only QTE values.")

        plt.axhline(y=0, color='r', linestyle='--', label="No Effect Line")
        plt.xlabel('Quantiles')
        plt.ylabel('SpATT Estimates')
        plt.title('Spatial Average Treatment on the Treated (SpATT)')
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



