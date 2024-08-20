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
        self.data = data
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
        # Converter o pandas DataFrame para um R data.frame
        r_data = pandas2ri.py2rpy(self.data)

        # Preparar a fórmula para R
        r_formula = Formula(self.formula)

        # Chama a função QDiD do pacote qte do R
        qdid_result = qte.QDiD(r_formula, data=r_data, t=self.t, tmin1=self.tmin1,
                               idname=self.idname, tname=self.tname, probs=self.probs,
                               se=self.se, iters=self.iters, panel=True)

        # Extrair os resultados em um dicionário
        results = {
            'qdid': np.array(qdid_result.rx2('QTE')),
            'probs': np.array(self.probs)
        }

        if self.se:
            results['se'] = np.array(qdid_result.rx2('Std.Error'))

        return results

    def summary(self):
        """
        Fornece um resumo dos resultados de estimativa QDiD.
        
        Retorna:
        --------
        summary : str
            Um resumo textual dos resultados do QDiD.
        """
        results = self.estimate()
        summary_str = "Quantile Difference-in-Differences (QDiD) Results:\n"
        summary_str += "Quantiles: " + str(results['probs']) + "\n"
        summary_str += "QDiD Estimates: " + str(results['qdid']) + "\n"
        
        if self.se:
            summary_str += "Standard Errors: " + str(results['se']) + "\n"
        
        return summary_str

    def plot(self):
        """
        Plota as estimativas do QDiD com intervalos de confiança, se disponíveis.
        """
        import matplotlib.pyplot as plt

        results = self.estimate()
        
        plt.errorbar(results['probs'], results['qdid'], yerr=results.get('se', None), fmt='o', capsize=5)
        plt.xlabel('Quantiles')
        plt.ylabel('QDiD Estimates')
        plt.title('Quantile Difference-in-Differences (QDiD) Estimates')
        plt.grid(True)
        plt.show()

