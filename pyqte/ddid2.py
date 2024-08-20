import pandas as pd
import numpy as np
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri, Formula
from rpy2.robjects.packages import importr
import matplotlib.pyplot as plt

# Ativar a conversão automática de pandas DataFrames para R data.frames
pandas2ri.activate()

# Importar o pacote qte do R
qte = importr('qte')

class DDID2Estimator:
    def __init__(self, data, outcome, treatment, time_var, id_var, t, tmin1, probs=None, se=True, iters=100, alp=0.05, method="logit", retEachIter=False, panel=True, cores=None, covariates=None):
        self.data = data
        self.outcome = outcome
        self.treatment = treatment
        self.time_var = time_var
        self.id_var = id_var
        self.t = t
        self.tmin1 = tmin1
        self.probs = probs if probs else np.arange(0.05, 1, 0.05)
        self.se = se
        self.iters = iters
        self.alp = alp
        self.method = method
        self.retEachIter = retEachIter
        self.panel = panel
        self.cores = cores
        self.covariates = covariates if covariates else []
        self.result = None

    def fit(self):
        r_formula = Formula(f"{self.outcome} ~ {self.treatment}")
        r_data = pandas2ri.py2rpy(self.data)
        
        additional_args = {
            't': self.t,
            'tmin1': self.tmin1,
            'tname': self.time_var,
            'idname': self.id_var,
            'probs': ro.FloatVector(self.probs),
            'se': self.se,
            'iters': self.iters,
            'alp': self.alp,
            'method': self.method,
            'retEachIter': self.retEachIter,
            'panel': self.panel,
            'cores': self.cores
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
            raise ValueError("Model has not been fitted yet. Call `fit()` before calling `summary()`.")
        summary = ro.r.summary(self.result)
        print(summary)
        return summary

    def plot(self):
        if self.result is None:
            raise ValueError("Model has not been fitted yet. Call `fit()` before calling `plot()`.")
        
        tau = np.array(self.probs)
        qte = np.array(self.result.rx2('qte'))

        plt.figure(figsize=(10, 6))
        plt.plot(tau, qte, 'o-', label="DDID2")

        if self.se:
            if 'qte.lower' in self.result.names and 'qte.upper' in self.result.names:
                lower_bound = np.array(self.result.rx2('qte.lower'))
                upper_bound = np.array(self.result.rx2('qte.upper'))
                if np.issubdtype(lower_bound.dtype, np.number) and np.issubdtype(upper_bound.dtype, np.number):
                    plt.fill_between(tau, lower_bound, upper_bound, color='gray', alpha=0.2, label="95% CI")
                else:
                    print("Intervalos de confiança contêm valores não numéricos. Plotagem omitida.")
            else:
                print("Intervalos de confiança não estão disponíveis. Plotando apenas os valores de DDID2.")

        plt.axhline(y=0, color='r', linestyle='--', label="No Effect Line")
        plt.xlabel('Quantiles')
        plt.ylabel('DDID2 Estimates')
        plt.title('Difference-in-Differences with Two Differences (DDID2)')
        plt.legend()
        plt.grid(True)
        plt.show()

    def get_results(self):
        """Retorna os resultados em um DataFrame para análise posterior."""
        if self.result is None:
            raise ValueError("Model has not been fitted yet. Call `fit()` before calling `get_results()`.")

        results = {
            'Quantile': self.probs,
            'QTE': np.array(self.result.rx2('qte'))
        }

        if self.se:
            if 'qte.lower' in self.result.names and 'qte.upper' in self.result.names:
                results['QTE Lower Bound'] = np.array(self.result.rx2('qte.lower'))
                results['QTE Upper Bound'] = np.array(self.result.rx2('qte.upper'))

        return pd.DataFrame(results)
