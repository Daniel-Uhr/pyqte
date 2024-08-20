import pandas as pd
import numpy as np
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects.conversion import localconverter
from rpy2.robjects import Formula
import matplotlib.pyplot as plt

# Ativando a conversão automática de pandas DataFrames para R data.frames
pandas2ri.activate()

# Importando o pacote qte do R
qte = importr('qte')

class PanelQTETEstimator:
    """
    PanelQTETEstimator é utilizado para estimar o Quantile Treatment Effect on the Treated (QTET)
    utilizando dados em painel com o pacote 'qte' do R via rpy2.

    Parâmetros:
    -----------
    formula : str
        A fórmula representando o relacionamento entre as variáveis dependentes e independentes.
    data : pandas.DataFrame
        O conjunto de dados contendo as variáveis usadas na fórmula.
    t : int
        O terceiro período de tempo na amostra onde as unidades tratadas recebem o tratamento.
    tmin1 : int
        O segundo período de tempo na amostra, que deve ser um período pré-tratamento.
    tmin2 : int
        O primeiro período de tempo na amostra, que deve ser um período pré-tratamento.
    idname : str
        O nome da coluna que representa o identificador único para cada unidade.
    tname : str
        O nome da coluna que representa os períodos de tempo.
    probs : list
        Um vetor de valores entre 0 e 1 para calcular o QTET.
    se : bool
        Se deve calcular os erros padrão.
    iters : int
        O número de iterações bootstrap para calcular os erros padrão.
    method : str
        O método para incluir covariáveis, "QR" para regressão quantílica ou "pscore" para escore de propensão.
    """

    def __init__(self, formula, data, t, tmin1, tmin2, idname, tname, probs, se=False, iters=100, method="pscore"):
        self.formula = Formula(formula)
        self.data = pandas2ri.py2rpy(data)
        self.t = t
        self.tmin1 = tmin1
        self.tmin2 = tmin2
        self.idname = idname
        self.tname = tname
        # Se probs for uma lista de três elementos, interpretá-la como uma sequência
        if isinstance(probs, list) and len(probs) == 3:
            self.probs = ro.FloatVector(np.arange(probs[0], probs[1] + probs[2], probs[2]))
        else:
            self.probs = ro.FloatVector(probs)  # Usar probs como está
        self.se = se
        self.iters = iters
        self.method = method

    def estimate(self):
        """
        Estima o QTET usando dados em painel.

        Retorna:
        --------
        result : objeto R
            O resultado da estimativa QTET, que pode ser processado ou resumido.
        """
        result = qte.panel_qtet(
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
            method=self.method
        )
        self.result = result
        return result

    def summary(self):
        """
        Exibe um resumo dos resultados da estimativa QTET.

        Retorna:
        --------
        summary : str
            Um resumo dos resultados QTET.
        """
        summary = ro.r.summary(self.result)
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

