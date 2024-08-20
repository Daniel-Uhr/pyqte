from rpy2.robjects import r, Formula
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Ativar a conversão de pandas DataFrame para R DataFrame
pandas2ri.activate()

# Importar o pacote 'qte' do R
qte = importr('qte')

class PanelQTETEstimator:
    def __init__(self, formula, data, t, tmin1, tmin2, idname, tname, probs=None, se=True, iters=100, method="pscore", alp=0.05, retEachIter=False, pl=False, cores=None):
        self.formula = Formula(formula)
        self.data = pandas2ri.py2rpy(data)
        self.t = t
        self.tmin1 = tmin1
        self.tmin2 = tmin2
        self.idname = idname
        self.tname = tname
        self.se = se
        self.iters = iters
        self.method = method
        self.alp = alp
        self.retEachIter = retEachIter
        self.pl = pl
        self.cores = cores

        # Processar 'probs' como um vetor numérico em R
        if probs is None:
            self.probs = r.seq(0.05, 0.95, by=0.05)
        else:
            if len(probs) == 3:
                self.probs = r.seq(probs[0], probs[1], by=probs[2])
            else:
                self.probs = r.FloatVector(probs)

    def fit(self):
        self.result = qte.panel_qtet(
            formla=self.formula,
            t=self.t,
            tmin1=self.tmin1,
            tmin2=self.tmin2,
            idname=self.idname,
            tname=self.tname,
            data=self.data,
            probs=self.probs,
            se=self.se,
            iters=self.iters,
            method=self.method,
            alp=self.alp,
            retEachIter=self.retEachIter,
            pl=self.pl,
            cores=self.cores
        )
        return self.result

    def summary(self):
        if not hasattr(self, 'result'):
            raise ValueError("Model has not been fitted yet. Call `fit()` before calling `summary()`.")
        summary = r.summary(self.result)
        print(summary)
        return summary

    def plot(self):
        if not hasattr(self, 'result'):
            raise ValueError("Model has not been fitted yet. Call `fit()` before calling `plot()`.")
        
        tau = np.array(self.probs)
        qte = np.array(self.result.rx2('qte'))

        plt.figure(figsize=(10, 6))
        plt.plot(tau, qte, 'o-', label="QTE")

        if self.se:
            if 'qte.lower' in self.result.names and 'qte.upper' in self.result.names:
                lower_bound = np.array(self.result.rx2('qte.lower'))
                upper_bound = np.array(self.result.rx2('qte.upper'))
                plt.fill_between(tau, lower_bound, upper_bound, color='gray', alpha=0.2, label="95% CI")
            else:
                print("Intervalos de confiança não estão disponíveis. Plotando apenas os valores de QTE.")

        plt.axhline(y=0, color='r', linestyle='--', label="No Effect Line")
        plt.xlabel('Quantiles')
        plt.ylabel('QTE Estimates')
        plt.title('Quantile Treatment Effects (Panel QTET)')
        plt.legend()
        plt.grid(True)
        plt.show()

    def get_results(self):
        if not hasattr(self, 'result'):
            raise ValueError("Model has not been fitted yet. Call `fit()` before calling `get_results()`.")

        data = {
            'Quantile': np.array(self.probs),
            'QTET': np.array(self.result.rx2('qte')),
            'QTET Lower Bound': np.array(self.result.rx2('qte.lower')) if 'qte.lower' in self.result.names else None,
            'QTET Upper Bound': np.array(self.result.rx2('qte.upper')) if 'qte.upper' in self.result.names else None,
        }
        return pd.DataFrame(data)

