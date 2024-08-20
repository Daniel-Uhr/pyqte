import pandas as pd
import numpy as np
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects import Formula
import matplotlib.pyplot as plt

# Ativar a conversão automática de pandas DataFrames para R data.frames
pandas2ri.activate()

# Importar o pacote qte do R
qte = importr('qte')

class MDiDEstimator:
    """
    MDiDEstimator is used to estimate Quantile Difference-in-Differences (MDiD) effects using the R 'qte' package via rpy2.
    """
    
    def __init__(self, formula, data, t, tmin1, idname, tname, probs=[0.05, 0.95, 0.05], se=True, iters=100, xformla=None, panel=False, alp=0.05, retEachIter=False):
        self.formula = formula
        self.data = data
        self.t = t
        self.tmin1 = tmin1
        self.idname = idname
        self.tname = tname
        self.probs = np.arange(probs[0], probs[1] + probs[2], probs[2]) if len(probs) == 3 else probs
        self.se = se
        self.iters = iters
        self.xformla = xformla
        self.panel = panel
        self.alp = alp
        self.retEachIter = retEachIter
        self.result = None

    def fit(self):
        r_formula = Formula(self.formula)
        r_data = pandas2ri.py2rpy(self.data)
        
        additional_args = {
            't': self.t,
            'tmin1': self.tmin1,
            'tname': self.tname,
            'idname': self.idname,
            'probs': ro.FloatVector(self.probs),
            'se': self.se,
            'iters': self.iters,
            'alp': self.alp,
            'retEachIter': self.retEachIter,
            'panel': self.panel
        }

        if self.xformla:
            r_xformla = Formula(self.xformla)
            additional_args['xformla'] = r_xformla
        
        self.result = qte.MDiD(
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
        mdid = np.array(self.result.rx2('qte'))

        plt.figure(figsize=(10, 6))
        plt.plot(tau, mdid, 'o-', label="MDiD")

        if self.se:
            if 'qte.lower' in self.result.names and 'qte.upper' in self.result.names:
                lower_bound = np.array(self.result.rx2('qte.lower'))
                upper_bound = np.array(self.result.rx2('qte.upper'))
                if np.issubdtype(lower_bound.dtype, np.number) and np.issubdtype(upper_bound.dtype, np.number):
                    plt.fill_between(tau, lower_bound, upper_bound, color='gray', alpha=0.2, label="95% CI")
                else:
                    print("Intervalos de confiança contêm valores não numéricos. Plotagem omitida.")
            else:
                print("Intervalos de confiança não estão disponíveis. Plotando apenas os valores de QTE.")

        plt.axhline(y=0, color='r', linestyle='--', label="No Effect Line")
        plt.xlabel('Quantiles')
        plt.ylabel('MDiD Estimates')
        plt.title('Median Difference-in-Differences (MDiD) Estimates')
        plt.legend()
        plt.grid(True)
        plt.show()

    def get_results(self):
        """
        Retorna os resultados como um DataFrame pandas para análises adicionais.
        """
        if self.result is None:
            raise ValueError("Model has not been fitted yet. Call `fit()` before calling `get_results()`.")

        data = {
            'Quantile': np.array(self.probs),
            'MDiD': np.array(self.result.rx2('qte')),
            'MDiD Lower Bound': np.array(self.result.rx2('qte.lower')) if 'qte.lower' in self.result.names else None,
            'MDiD Upper Bound': np.array(self.result.rx2('qte.upper')) if 'qte.upper' in self.result.names else None,
        }
        return pd.DataFrame(data)


