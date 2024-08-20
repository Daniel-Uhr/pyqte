import pandas as pd
import numpy as np
from rpy2.robjects import r, Formula
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
import rpy2.robjects as ro
import matplotlib.pyplot as plt

# Ativar a conversão de pandas DataFrames para R data.frames
pandas2ri.activate()

# Importar o pacote qte do R
qte = importr('qte')

class DDID2Estimator:
    def __init__(self, data, outcome, treatment, time_var, id_var, covariates=None):
        self.data = pandas2ri.py2rpy(data)
        self.outcome = outcome
        self.treatment = treatment
        self.time_var = time_var
        self.id_var = id_var
        self.covariates = covariates if covariates else []
        self.result = None

    def estimate(self, t, tmin1, probs=None, se=True, iters=100, alp=0.05, method='logit', retEachIter=False, panel=True, cores=1):
        r_formula = Formula(f"{self.outcome} ~ {self.treatment}")
        r_data = self.data
        
        additional_args = {
            't': t,
            'tmin1': tmin1,
            'tname': self.time_var,
            'idname': self.id_var,
            'probs': r.seq(0.05, 0.95, 0.05) if probs is None else ro.FloatVector(probs),
            'se': se,
            'iters': iters,
            'alp': alp,
            'method': method,
            'retEachIter': retEachIter,
            'panel': panel,
            'cores': cores
        }

        if self.covariates:
            r_xformla = Formula(f"~ {' + '.join(self.covariates)}")
            additional_args['xformla'] = r_xformla

        self.result = qte.ddid2(
            formla=r_formula,
            data=r_data,
            **additional_args
        )

    def summary(self):
        if self.result is None:
            raise ValueError("O modelo ainda não foi ajustado. Chame `fit()` antes de chamar `summary()`.")
        summary = r.summary(self.result)
        print(summary)
        return summary

    def plot(self):
        if self.result is None:
            raise ValueError("O modelo ainda não foi ajustado. Chame `fit()` antes de chamar `plot()`.")
        
        tau = np.array(self.result.rx2('probs'))
        qte = np.array(self.result.rx2('qte'))

        plt.figure(figsize=(10, 6))
        plt.plot(tau, qte, 'o-', label="DDID2")

        if self.result.rx2('qte.se') is not None:
            lower_bound = np.array(self.result.rx2('qte.lower'))
            upper_bound = np.array(self.result.rx2('qte.upper'))
            if np.issubdtype(lower_bound.dtype, np.number) and np.issubdtype(upper_bound.dtype, np.number):
                plt.fill_between(tau, lower_bound, upper_bound, color='gray', alpha=0.2, label="95% CI")

        plt.axhline(y=0, color='r', linestyle='--', label="No Effect Line")
        plt.xlabel('Quantiles')
        plt.ylabel('DDID2 Estimates')
        plt.title('Difference-in-Differences with Two Differences (DDID2)')
        plt.legend()
        plt.grid(True)
        plt.show()

    def get_results(self):
        if self.result is None:
            raise ValueError("O modelo ainda não foi ajustado. Chame `fit()` antes de chamar `get_results()`.")
        
        df = pd.DataFrame({
            'Quantile': np.array(self.result.rx2('probs')),
            'QTE': np.array(self.result.rx2('qte'))
        })

        if self.result.rx2('qte.se') is not None:
            df['QTE Lower Bound'] = np.array(self.result.rx2('qte.lower'))
            df['QTE Upper Bound'] = np.array(self.result.rx2('qte.upper'))

        return df

