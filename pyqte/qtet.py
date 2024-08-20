import pandas as pd
import numpy as np
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects import Formula
import matplotlib.pyplot as plt

# Ativando a conversão automática de pandas DataFrames para R data.frames
pandas2ri.activate()

# Importando o pacote qte do R
qte = importr('qte')

class QTETEstimator:
    def __init__(self, formula, data, probs=None, se=True, iters=100, xformla=None, method='logit',
                 weights=None, alp=0.05, retEachIter=False, indsample=True, printIter=False, pl=False, cores=2):
        self.formula = formula
        self.data = data
        self.probs = np.arange(probs[0], probs[1] + probs[2], probs[2]) if probs and len(probs) == 3 else (probs if probs else np.arange(0.05, 1, 0.05))
        self.se = se
        self.iters = iters
        self.xformla = xformla
        self.method = method
        self.weights = weights
        self.alp = alp
        self.retEachIter = retEachIter
        self.indsample = indsample
        self.printIter = printIter
        self.pl = pl
        self.cores = cores
        self.result = None
        self.info = {}

    def fit(self):
        r_formula = Formula(self.formula)
        r_data = pandas2ri.py2rpy(self.data)
        
        additional_args = {
            'se': self.se,
            'iters': self.iters,
            'alp': self.alp,
            'method': self.method,
            'retEachIter': self.retEachIter,
            'indsample': self.indsample,
            'printIter': self.printIter,
            'pl': self.pl,
            'cores': self.cores
        }

        if self.xformla:
            r_xformla = Formula(self.xformla)
            additional_args['xformla'] = r_xformla
        
        if self.weights is not None:
            additional_args['w'] = ro.FloatVector(self.weights)

        self.result = qte.ci_qtet(
            formla=r_formula,
            data=r_data,
            probs=ro.FloatVector(self.probs),
            **additional_args
        )
        self._extract_info()

    def _extract_info(self):
        self.info['qte'] = np.array(self.result.rx2('qte'))
        self.info['probs'] = np.array(self.probs)
        
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
        
        tau = np.array(self.probs)
        qte = np.array(self.result.rx2('qte'))

        plt.figure(figsize=(10, 6))
        plt.plot(tau, qte, 'o-', label="QTET")

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
        plt.ylabel('QTET Estimates')
        plt.title('Quantile Treatment Effects on the Treated (QTET)')
        plt.legend()
        plt.grid(True)
        plt.show()

    def get_results(self):
        """Cria um DataFrame pandas com os resultados estimados."""
        df = pd.DataFrame({
            'Quantile': self.info['probs'],
            'QTE': self.info['qte']
        })
        
        if self.se and self.info['qte.lower'] is not None and self.info['qte.upper'] is not None:
            df['QTE Lower Bound'] = self.info['qte.lower']
            df['QTE Upper Bound'] = self.info['qte.upper']
        
        return df

