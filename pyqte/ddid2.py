import pandas as pd
import numpy as np
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri, Formula
from rpy2.robjects.packages import importr
from rpy2.robjects.conversion import localconverter
import matplotlib.pyplot as plt

# Ativando a conversão automática de pandas DataFrames para R data.frames
pandas2ri.activate()

# Importando o pacote qte do R
qte = importr('qte')

class DDID2Estimator:
    def __init__(self, data, outcome, treatment, time_var, id_var, covariates=None, se=True, iters=100, probs=[0.05, 0.95, 0.05], alp=0.05, method='logit', retEachIter=False, panel=True, cores=2):
        self.data = data
        self.outcome = outcome
        self.treatment = treatment
        self.time_var = time_var
        self.id_var = id_var
        self.covariates = covariates if covariates else []
        self.se = se
        self.iters = iters
        self.probs = np.arange(probs[0], probs[1] + probs[2], probs[2]) if len(probs) == 3 else probs
        self.alp = alp
        self.method = method
        self.retEachIter = retEachIter
        self.panel = panel
        self.cores = cores
        self.result = None

    def fit(self, t, tmin1):
        r_formula = Formula(f"{self.outcome} ~ {self.treatment}")
        r_data = pandas2ri.py2rpy(self.data)
        
        additional_args = {
            't': t,
            'tmin1': tmin1,
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
            lower_bound = np.array(self.result.rx2('qte.lower')) if 'qte.lower' in self.result.names else np.zeros(len(tau))
            upper_bound = np.array(self.result.rx2('qte.upper')) if 'qte.upper' in self.result.names else np.zeros(len(tau))

            plt.fill_between(tau, lower_bound, upper_bound, color='gray', alpha=0.2, label="95% CI")

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

        # Se os valores de intervalo de confiança forem None, considerá-los como zero
        lower_bound = np.array(self.result.rx2('qte.lower')) if 'qte.lower' in self.result.names else np.zeros(len(self.probs))
        upper_bound = np.array(self.result.rx2('qte.upper')) if 'qte.upper' in self.result.names else np.zeros(len(self.probs))

        results['QTE Lower Bound'] = lower_bound
        results['QTE Upper Bound'] = upper_bound

        return pd.DataFrame(results)

