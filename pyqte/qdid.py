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

class QDiDEstimator:
    def __init__(self, formula, data, t, tmin1, idname, tname, probs=None, se=True, iters=100):
        self.formula = formula
        self.data = pandas2ri.py2rpy(data[data[tname].isin([tmin1, t])])  # Filtrando os dados
        self.t = t
        self.tmin1 = tmin1
        self.idname = idname
        self.tname = tname
        
        # Se probs for uma lista de três elementos, interpretá-la como uma sequência R
        if isinstance(probs, list) and len(probs) == 3:
            self.probs = r.seq(probs[0], probs[1], probs[2])
        else:
            self.probs = probs  # caso contrário, use como está

        self.se = se
        self.iters = iters

    def estimate(self):
        """
        Estima os efeitos do QDiD.

        Retorna:
        --------
        results : dict
            Um dicionário contendo os efeitos estimados do QDiD e, se solicitado, os erros padrão.
        """
        # Preparar a fórmula para R
        r_formula = Formula(self.formula)

        # Chama a função QDiD do pacote qte do R
        qdid_result = qte.QDiD(r_formula, data=self.data, t=self.t, tmin1=self.tmin1,
                               idname=self.idname, tname=self.tname, probs=self.probs,
                               se=self.se, iters=self.iters, panel=True)

        return qdid_result

    def summary(self):
        """
        Fornece um resumo dos resultados de estimativa QDiD.
        
        Retorna:
        --------
        summary : ListVector
            Um resumo dos resultados do QDiD em formato ListVector.
        """
        qdid_result = self.estimate()
        summary = r.summary(qdid_result)
        return summary

    def plot(self):
        """
        Plota as estimativas do QDiD com intervalos de confiança, se disponíveis.
        """
        summary = self.summary()

        # Extraindo os dados do summary
        tau = list(summary.rx2('tau'))
        qte = list(summary.rx2('QTE'))
        std_error = list(summary.rx2('Std. Error'))

        # Substituir valores nulos (NULLType) por 0
        std_error = [0 if v is None else v for v in std_error]

        # Construindo o intervalo de confiança
        lower_bound = np.array(qte) - 1.96 * np.array(std_error)
        upper_bound = np.array(qte) + 1.96 * np.array(std_error)

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

