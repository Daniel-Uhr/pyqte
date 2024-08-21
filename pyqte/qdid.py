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
    def __init__(self, formula, data, t, tmin1, tname, idname=None, xformla=None, panel=False, se=True, alp=0.05, probs=None, iters=100, retEachIter=False, pl=False, cores=None):
        self.formula = Formula(formula)
        self.data = pandas2ri.py2rpy(data)
        self.t = t
        self.tmin1 = tmin1
        self.tname = tname
        self.idname = idname
        self.xformla = Formula(xformla) if xformla else None
        self.panel = panel
        self.se = se
        self.alp = alp
        self.iters = iters
        self.retEachIter = retEachIter
        self.pl = pl
        self.cores = cores

        # Processar 'probs' como um vetor numérico em R
        if probs is None:
            self.probs = r.seq(0.05, 0.95, by=0.05)
        else:
            if len(probs) == 3:
                self.probs = r.seq(probs[0], probs[1], by=probs[2])
            else:
                self.probs = r.FloatVector(probs)

    def fit(self):
        # Chamando a função QDiD do pacote qte do R
        if self.xformla:
            self.result = qte.QDiD(
                formla=self.formula,
                xformla=self.xformla,
                t=self.t,
                tmin1=self.tmin1,
                tname=self.tname,
                data=self.data,
                panel=self.panel,
                se=self.se,
                idname=self.idname,
                alp=self.alp,
                probs=self.probs,
                iters=self.iters,
                retEachIter=self.retEachIter,
                pl=self.pl,
                cores=self.cores
            )
        else:
            self.result = qte.QDiD(
                formla=self.formula,
                t=self.t,
                tmin1=self.tmin1,
                tname=self.tname,
                data=self.data,
                panel=self.panel,
                se=self.se,
                idname=self.idname,
                alp=self.alp,
                probs=self.probs,
                iters=self.iters,
                retEachIter=self.retEachIter,
                pl=self.pl,
                cores=self.cores
            )
        return self.result

    def summary(self):
        summary = r.summary(self.result)
        print(summary)
        return summary

    def plot(self):
        """
        Plota as estimativas do QDiD com intervalos de confiança, se disponíveis.
        """
        # Extraindo os dados do resultado
        tau = np.linspace(0.05, 0.95, len(self.result.rx2('qte')))
        qte = np.array(self.result.rx2('qte'))
        lower_bound = np.array(self.result.rx2('qte.lower')) if self.se else None
        upper_bound = np.array(self.result.rx2('qte.upper')) if self.se else None

        # Substituir valores inválidos (NaN) por zero
        qte = np.nan_to_num(qte, nan=0.0)
        if self.se:
            lower_bound = np.nan_to_num(lower_bound, nan=0.0)
            upper_bound = np.nan_to_num(upper_bound, nan=0.0)

        # Criar o gráfico
        plt.figure(figsize=(10, 6))
        plt.plot(tau, qte, 'o-', label="QTE")

        if self.se:
            plt.fill_between(tau, lower_bound, upper_bound, color='gray', alpha=0.2, label="95% CI")
        
        plt.axhline(y=0, color='r', linestyle='--', label="No Effect Line")
        plt.xlabel('Quantiles')
        plt.ylabel('QTE Estimates')
        plt.title('Quantile Treatment Effects (QDiD)')
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
            'QTE Lower Bound': np.array(self.result.rx2('qte.lower')) if self.se else np.nan,
            'QTE Upper Bound': np.array(self.result.rx2('qte.upper')) if self.se else np.nan
        })
        return results_df

