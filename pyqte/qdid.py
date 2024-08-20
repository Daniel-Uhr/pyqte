import pandas as pd
import numpy as np
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects import Formula

# Ativando a conversão automática de pandas DataFrames para R data.frames
pandas2ri.activate()

# Importando o pacote qte do R
qte = importr('qte')
r = ro.r  # Acessando o ambiente R diretamente

class QDiDEstimator:
    def __init__(self, formula, data, t, tmin1, idname, tname, probs=None, se=True, iters=100):
        self.formula = formula
        self.data = pandas2ri.py2rpy(data[data[tname].isin([tmin1, t])])  # Filtrando os dados
        self.t = t
        self.tmin1 = tmin1
        self.idname = idname
        self.tname = tname
        self.probs = r.seq(probs[0], probs[1], probs[2]) if isinstance(probs, list) else probs
        self.se = se
        self.iters = iters

    def estimate(self):
        # Preparar a fórmula para R
        r_formula = Formula(self.formula)

        # Chama a função QDiD do pacote qte do R
        qdid_result = qte.QDiD(r_formula, data=self.data, t=self.t, tmin1=self.tmin1,
                               idname=self.idname, tname=self.tname, probs=self.probs,
                               se=self.se, iters=self.iters, panel=True)

        return qdid_result

    def summary(self):
        qdid_result = self.estimate()
        summary = r.summary(qdid_result)
        print(summary)

    def plot(self):
        """
        Plota as estimativas do QDiD com intervalos de confiança, se disponíveis.
        """
        qte_results = self.estimate()

        # Extraindo os dados do summary
        tau = list(qte_results.rx2('qte').names)
        qte = list(qte_results.rx2('qte'))
        lower_bound = list(qte_results.rx2('qte.lower'))
        upper_bound = list(qte_results.rx2('qte.upper'))

        # Convertendo tau de string para float
        tau = [float(t.replace('%', '')) / 100 for t in tau]

        # Criar o gráfico
        plt.figure(figsize=(10, 6))
        plt.plot(tau, qte, 'o-', label="QTE")
        plt.fill_between(tau, lower_bound, upper_bound, color='gray', alpha=0.2, label="95% CI")

        plt.axhline(y=0, color='r', linestyle='--', label="No Effect Line")
        plt.xlabel('Quantiles')
        plt.ylabel('QTE Estimates')
        plt.title('Quantile Treatment Effects (QDiD)')
        plt.legend()
        plt.grid(True)
        plt.show()
