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
    def __init__(self, formula, data, probs=None, se=True, iters=100, xformla=None, method='logit'):
        self.formula = formula
        self.data = data
        # Se probs for uma lista de três elementos, interprete como início, fim, incremento
        if probs and len(probs) == 3:
            self.probs = np.arange(probs[0], probs[1] + probs[2], probs[2])
        else:
            self.probs = probs if probs is not None else np.arange(0.05, 1, 0.05)
        self.se = se
        self.iters = iters
        self.xformla = xformla
        self.method = method

    def fit(self):
        r_formula = Formula(self.formula)
        r_data = pandas2ri.py2rpy(self.data)

        if self.xformla:
            r_xformla = Formula(self.xformla)
            self.result = qte.ci_qtet(
                formla=r_formula,
                xformla=r_xformla,
                data=r_data,
                probs=ro.FloatVector(self.probs),
                se=self.se,
                iters=self.iters,
                method=self.method
            )
        else:
            self.result = qte.ci_qtet(
                formla=r_formula,
                data=r_data,
                probs=ro.FloatVector(self.probs),
                se=self.se,
                iters=self.iters,
                method=self.method
            )

    def summary(self):
        summary = ro.r.summary(self.result)
        print(summary)
        return summary

    def plot(self):
        # Extraindo os dados do resultado
        tau = np.linspace(self.probs[0], self.probs[-1], len(self.result.rx2('qte')))
        qte = np.array(self.result.rx2('qte'))
        lower_bound = np.array(self.result.rx2('qte.lower'))
        upper_bound = np.array(self.result.rx2('qte.upper'))

        # Criar o gráfico
        plt.figure(figsize=(10, 6))
        plt.plot(tau, qte, 'o-', label="QTET")
        plt.fill_between(tau, lower_bound, upper_bound, color='gray', alpha=0.2, label="95% CI")
        plt.axhline(y=0, color='r', linestyle='--', label="No Effect Line")
        plt.xlabel('Quantiles')
        plt.ylabel('QTET Estimates')
        plt.title('Quantile Treatment Effects on the Treated (QTET)')
        plt.legend()
        plt.grid(True)
        plt.show()
