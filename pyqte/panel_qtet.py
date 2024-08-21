from rpy2.robjects import r, Formula
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Ativar a conversão pandas para R DataFrame
pandas2ri.activate()

# Importar o pacote 'qte' do R
qte = importr('qte')

class PanelQTETEstimator:
    def __init__(self, formula, data, t, tmin1, tmin2, idname, tname, xformla=None, probs=None, se=False, iters=100, method="pscore"):
        self.formula = Formula(formula)
        self.data = pandas2ri.py2rpy(data)
        self.t = t
        self.tmin1 = tmin1
        self.tmin2 = tmin2
        self.idname = idname
        self.tname = tname
        self.xformla = Formula(xformla) if xformla else None

        # Processar 'probs' como um vetor numérico em R
        if probs is None:
            self.probs = r.seq(0.05, 0.95, by=0.05)
        else:
            if len(probs) == 3:
                self.probs = r.seq(probs[0], probs[1], by=probs[2])
            else:
                self.probs = r.FloatVector(probs)

        self.se = se
        self.iters = iters
        self.method = method
        self.result = None

    def fit(self):
        if self.formula is None or self.data is None or self.t is None or self.tmin1 is None or self.tmin2 is None or self.idname is None or self.tname is None:
            raise ValueError("Todos os parâmetros obrigatórios devem ser fornecidos e não devem ser None.")

        # Chamando a função 'panel_qtet' do pacote 'qte'
        self.result = qte.panel_qtet(
            formla=self.formula,
            t=self.t,
            tmin1=self.tmin1,
            tmin2=self.tmin2,
            idname=self.idname,
            tname=self.tname,
            data=self.data,
            xformla=self.xformla,
            probs=self.probs,
            se=self.se,
            iters=self.iters,
            method=self.method
        )
        return self.result

    def summary(self):
        if self.result is None:
            raise ValueError("O modelo ainda não foi ajustado. Chame `fit()` antes de chamar `summary()`.")
        summary = r.summary(self.result)
        print(summary)
        return summary

    def plot(self):
        """
        Plota os resultados da estimativa QTET.
        """
        if self.result is None:
            raise ValueError("O modelo ainda não foi ajustado. Chame `fit()` antes de chamar `plot()`.")
        
        qte_results = self.result

        tau = np.linspace(0.05, 0.95, len(qte_results.rx2('qte')))
        qte = np.array(qte_results.rx2('qte'))
        lower_bound = np.array(qte_results.rx2('qte.lower'))
        upper_bound = np.array(qte_results.rx2('qte.upper'))

        # Verificar se os valores são numéricos e válidos
        if np.issubdtype(qte.dtype, np.number) and np.issubdtype(lower_bound.dtype, np.number) and np.issubdtype(upper_bound.dtype, np.number):
            plt.figure(figsize=(10, 6))
            plt.plot(tau, qte, 'o-', label="QTE")
            plt.fill_between(tau, lower_bound, upper_bound, color='gray', alpha=0.2, label="95% CI")
            plt.axhline(y=0, color='r', linestyle='--', label="No Effect Line")
            plt.xlabel('Quantiles')
            plt.ylabel('QTE Estimates')
            plt.title('Quantile Treatment Effects (Panel QTET)')
            plt.legend()
            plt.grid(True)
            plt.show()
        else:
            print("Os dados contêm valores não numéricos ou inválidos. A plotagem foi omitida.")

    def get_results(self):
        """
        Retorna os resultados como um DataFrame do pandas.
        """
        if self.result is None:
            raise ValueError("O modelo ainda não foi ajustado. Chame `fit()` antes de chamar `get_results()`.")
        
        results_df = pd.DataFrame({
            'Quantile': np.linspace(0.05, 0.95, len(self.result.rx2('qte'))),
            'QTE': np.array(self.result.rx2('qte')),
            'QTE Lower Bound': np.array(self.result.rx2('qte.lower')),
            'QTE Upper Bound': np.array(self.result.rx2('qte.upper'))
        })
        return results_df
