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
        summary : str
            Um resumo textual dos resultados do QDiD.
        """
        qdid_result = self.estimate()
        summary = r.summary(qdid_result)
        print(summary)
        return summary

    def plot(self):
        """
        Plota as estimativas do QDiD com intervalos de confiança, se disponíveis.
        """
        import matplotlib.pyplot as plt
        
        # Estimando os resultados
        results = self.estimate()
        
        quantiles = results['probs']
        qte_estimates = results['qdid']
        std_errors = results.get('se', None)
        
        # Verificando os tamanhos das listas
        print("Tamanhos das listas:")
        print(f"Tamanho de quantiles: {len(quantiles)}")
        print(f"Tamanho de qte_estimates: {len(qte_estimates)}")
        if std_errors is not None:
            print(f"Tamanho de std_errors: {len(std_errors)}")
        
        # Criar o gráfico
        plt.figure(figsize=(10, 6))
        if std_errors is not None:
            plt.errorbar(quantiles, qte_estimates, yerr=std_errors, fmt='o', capsize=5, label="QTE with Std. Error")
        else:
            plt.plot(quantiles, qte_estimates, 'o-', label="QTE")
        
        plt.axhline(y=0, color='r', linestyle='--', label="No Effect Line")
        plt.xlabel('Quantiles')
        plt.ylabel('QTE Estimates')
        plt.title('Quantile Treatment Effects (QDiD)')
        plt.legend()
        plt.grid(True)
        plt.show()
