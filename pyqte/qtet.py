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
    """
    QTETEstimator is used to estimate Quantile Treatment Effects on the Treated (QTET) 
    using panel data with Difference in Differences (DiD) assumptions.
    """

    def __init__(self, data, formula, t, tmin1, tmin2, idname, tname, probs, iters=100, se=True, method='qr'):
        self.data = data
        self.formula = formula
        self.t = t
        self.tmin1 = tmin1
        self.tmin2 = tmin2
        self.idname = idname
        self.tname = tname
        self.probs = probs
        self.iters = iters
        self.se = se
        self.method = method

    def estimate(self):
        """
        Estimate the QTET for the specified quantiles.
        """
        # Convertendo o DataFrame pandas para um DataFrame R
        r_data = pandas2ri.py2rpy(self.data)

        # Criando a fórmula no formato do R
        r_formula = Formula(self.formula)

        # Chamando a função do R para estimar o QTET
        result = qte.panel_qtet(
            formla=r_formula,
            t=self.t,
            tmin1=self.tmin1,
            tmin2=self.tmin2,
            tname=self.tname,
            idname=self.idname,
            data=r_data,
            probs=ro.FloatVector(self.probs),
            iters=self.iters,
            se=self.se,
            method=self.method
        )
        return result

    def summary(self):
        """
        Display a summary of the QTET estimation result.
        """
        result = self.estimate()
        summary = r.summary(result)
        print(summary)
        return summary

    def plot(self):
        """
        Plot the estimated QTET.
        """
        result = self.estimate()

        # Extraindo os dados do resultado
        tau = np.linspace(0.05, 0.95, len(result.rx2('qte')))
        qte = np.array(result.rx2('qte'))
        lower_bound = np.array(result.rx2('qte.lower'))
        upper_bound = np.array(result.rx2('qte.upper'))

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
