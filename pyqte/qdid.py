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

class QDiDEstimator:
    """
    O QDiDEstimator é utilizado para estimar os efeitos Quantile Difference-in-Differences (QDiD)
    utilizando o pacote 'qte' do R via rpy2.
    
    Atributos:
    ----------
    formula : str
        A fórmula representando a relação entre as variáveis dependentes e independentes.
    data : pandas.DataFrame
        O dataset contendo as variáveis usadas na fórmula.
    t : int
        O período de tempo após o tratamento.
    tmin1 : int
        O período de tempo antes do tratamento.
    idname : str
        O nome da coluna representando o identificador único de cada unidade.
    tname : str
        O nome da coluna representando os períodos de tempo.
    probs : list
        A lista de quantis nos quais estimar o efeito do tratamento.
    se : bool
        Se deve ou não calcular os erros padrão.
    iters : int
        O número de iterações bootstrap para calcular os erros padrão.
    """
    
    def __init__(self, formula, data, t, tmin1, idname, tname, probs=[0.05, 0.5, 0.95], se=True, iters=100):
        self.formula = formula
        self.data = data
        self.t = t
        self.tmin1 = tmin1
        self.idname = idname
        self.tname = tname
        self.probs = probs
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
                               idname=self.idname, tname=self.tname, probs=ro.FloatVector(self.probs),
                               se=self.se, iters=self.iters)

        # Extrair os resultados em um dicionário
        results = {
            'qdid': np.array(qdid_result.rx2('QTE')),
            'probs': self.probs
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
        summary_str += "Quantiles: " + str(self.probs) + "\n"
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
        
        plt.errorbar(self.probs, results['qdid'], yerr=results.get('se', None), fmt='o', capsize=5)
        plt.xlabel('Quantiles')
        plt.ylabel('QDiD Estimates')
        plt.title('Quantile Difference-in-Differences (QDiD) Estimates')
        plt.grid(True)
        plt.show()
