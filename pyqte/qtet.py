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
r = ro.r  # Acessando o ambiente R diretamente

class QTETEstimator:
    def __init__(self, data, formula, t=None, tmin1=None, tmin2=None, idname=None, tname=None, probs=None, iters=100, se=True, method='logit'):
        self.data = pandas2ri.py2rpy(data)  # Convertendo o DataFrame pandas para um DataFrame R
        self.formula = formula
        self.t = t
        self.tmin1 = tmin1
        self.tmin2 = tmin2
        self.idname = idname
        self.tname = tname
        
        # Se probs for uma lista de três elementos, interpretar como uma sequência
        if isinstance(probs, list) and len(probs) == 3:
            self.probs = r.seq(probs[0], probs[1], probs[2])
        else:
            self.probs = ro.FloatVector(probs)  # Caso contrário, usar como está

        self.se = se
        self.iters = iters
        self.method = method

    def estimate(self):
        r_formula = Formula(self.formula)
        result = qte.ci_qtet(
            formla=r_formula,
            data=self.data,
            probs=self.probs,
            se=self.se,
            iters=self.iters,
            method=self.method
        )
        return result

    def summary(self):
        result = self.estimate()
        summary = r.summary(result)
        print(summary)

    def plot(self, result=None):
        if result is None:
            result = self.estimate()

        tau = np.linspace(0.05, 0.95, len(result.rx2('qte')))
        qte = np.array(result.rx2('qte'))
        lower_bound = np.array(result.rx2('qte.lower'))
        upper_bound = np.array(result.rx2('qte.upper'))

        plt.figure(figsize=(10, 6))
        plt.plot(tau, qte, 'o-', label="QTE")
        plt.fill_between(tau, lower_bound, upper_bound, color='gray', alpha=0.2, label="95% CI")
        plt.axhline(y=0, color='r', linestyle='--', label="No Effect Line")
        plt.xlabel('Quantiles')
        plt.ylabel('QTE Estimates')
        plt.title('Quantile Treatment Effects (QTET)')
        plt.legend()
        plt.grid(True)
        plt.show()

