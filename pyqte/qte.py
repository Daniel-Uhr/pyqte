import pandas as pd
import numpy as np
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects.conversion import localconverter
import matplotlib.pyplot as plt

# Activate the automatic conversion of pandas DataFrame to R DataFrame
pandas2ri.activate()

# Import the qte package from R
qte = importr('qte')

class QTEEstimator:
    def __init__(self, formula, xformla=None, data=None, probs=[0.05, 0.95, 0.05], se=False, iters=100):
        self.formula = formula
        self.xformla = xformla
        self.data = data

        if isinstance(probs, list) and len(probs) == 3:
            self.probs = ro.FloatVector(np.arange(probs[0], probs[1] + probs[2], probs[2]))
        else:
            self.probs = ro.FloatVector(probs)
            
        self.se = se
        self.iters = iters

    def fit(self):
        with localconverter(ro.default_converter + pandas2ri.converter):
            r_data = ro.conversion.py2rpy(self.data)

        # Call the qte function from the R qte package
        if self.xformla is not None:
            result = qte.ci_qte(
                formla=ro.Formula(self.formula),
                xformla=ro.Formula(self.xformla),
                data=r_data,
                probs=self.probs,
                se=self.se,
                iters=self.iters
            )
        else:
            result = qte.ci_qte(
                formla=ro.Formula(self.formula),
                data=r_data,
                probs=self.probs,
                se=self.se,
                iters=self.iters
            )

        self.result = result

    def summary(self):
        summary = ro.r.summary(self.result)
        print(summary)
        return summary

    def plot(self):
        tau = np.array(self.probs)
        qte = np.array(self.result.rx2('qte'))

        # Verificar se se=True para plotar com intervalos de confiança
        if self.se:
            # Verificar se os intervalos de confiança existem e são numéricos
            if 'qte.lower' in self.result.names and 'qte.upper' in self.result.names:
                lower_bound = np.array(self.result.rx2('qte.lower'))
                upper_bound = np.array(self.result.rx2('qte.upper'))

                # Verificar se os valores de lower_bound e upper_bound são válidos para plotagem
                if np.issubdtype(lower_bound.dtype, np.number) and np.issubdtype(upper_bound.dtype, np.number):
                    plt.figure(figsize=(10, 6))
                    plt.plot(tau, qte, 'o-', label="QTE")
                    plt.fill_between(tau, lower_bound, upper_bound, color='gray', alpha=0.2, label="95% CI")
                else:
                    print("Intervalos de confiança contêm valores não numéricos. Plotagem omitida.")
            else:
                print("Intervalos de confiança não estão disponíveis. Plotando apenas os valores de QTE.")
                plt.figure(figsize=(10, 6))
                plt.plot(tau, qte, 'o-', label="QTE")
        else:
            # Se se=False, plotar apenas os pontos sem intervalos de confiança
            plt.figure(figsize=(10, 6))
            plt.plot(tau, qte, 'o-', label="QTE")
        
        plt.axhline(y=0, color='r', linestyle='--', label="No Effect Line")
        plt.xlabel('Quantiles')
        plt.ylabel('QTE Estimates')
        plt.title('Quantile Treatment Effects (QTE)')
        plt.legend()
        plt.grid(True)
        plt.show()


