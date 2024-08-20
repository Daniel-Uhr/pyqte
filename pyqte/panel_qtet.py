from rpy2.robjects import r, Formula
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
import numpy as np
import matplotlib.pyplot as plt

# Ativar a conversão pandas para R DataFrame
pandas2ri.activate()

# Importar o pacote 'qte' do R
qte = importr('qte')

class PanelQTETEstimator:
    def __init__(self, formula, data, t, tmin1, tmin2, idname, tname, probs=None, se=False, iters=100, method="pscore", xformla=None):
        self.formula = Formula(formula)
        self.data = pandas2ri.py2rpy(data)
        self.t = t
        self.tmin1 = tmin1
        self.tmin2 = tmin2
        self.idname = idname
        self.tname = tname
        self.xformla = Formula(xformla) if xformla is not None else None

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

    def fit(self):
        additional_args = {}
        if self.xformla is not None:
            additional_args['xformla'] = self.xformla

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
            **additional_args
        )
        return self.result

    def summary(self):
        summary = r.summary(self.result)
        print(summary)
        return summary
        
    def plot(self):
        """
        Plota os resultados da estimativa QTET.
        """
        qte_results = self.result

        tau = np.linspace(0.05, 0.95, len(qte_results.rx2('qte')))
        qte = np.array(qte_results.rx2('qte'))
        lower_bound = np.array(qte_results.rx2('qte.lower'))
        upper_bound = np.array(qte_results.rx2('qte.upper'))

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

    def get_results(self):
        """
        Retorna os resultados como um DataFrame do pandas.
        """
        results_df = pd.DataFrame({
            'Quantile': np.linspace(0.05, 0.95, len(self.result.rx2('qte'))),
            'QTE': np.array(self.result.rx2('qte')),
            'QTE Lower Bound': np.array(self.result.rx2('qte.lower')),
            'QTE Upper Bound': np.array(self.result.rx2('qte.upper'))
        })
        return results_df
