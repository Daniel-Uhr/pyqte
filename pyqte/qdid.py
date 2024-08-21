import pandas as pd
import numpy as np
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri, Formula, FloatVector
from rpy2.robjects.packages import importr
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
                self.probs = FloatVector(probs)

    def fit(self):
        # Construir os argumentos da função, omitindo aqueles que são None
        args = {
            'formla': self.formula,
            't': self.t,
            'tmin1': self.tmin1,
            'tname': self.tname,
            'data': self.data,
            'panel': self.panel,
            'se': self.se,
            'alp': self.alp,
            'probs': self.probs,
            'iters': self.iters,
            'retEachIter': self.retEachIter,
            'pl': self.pl,
            'cores': self.cores
        }
        if self.xformla:
            args['xformla'] = self.xformla
        if self.idname:
            args['idname'] = self.idname

        try:
            # Chamando a função QDiD do pacote qte do R
            self.result = qte.QDiD(**{k: v for k, v in args.items() if v is not None})
        except Exception as e:
            raise RuntimeError(f"Erro ao executar o estimador QDiD: {e}")
        return self.result

    def summary(self):
        try:
            summary = r.summary(self.result)
            print(summary)
            return summary
        except Exception as e:
            raise RuntimeError(f"Erro ao gerar o sumário: {e}")

    def plot(self):
        """
        Plota as estimativas do QDiD com intervalos de confiança, se disponíveis.
        """
        try:
            # Extraindo os dados do resultado
            tau = np.linspace(0.05, 0.95, len(self.result.rx2('qte')))
            qte = np.nan_to_num(np.array(self.result.rx2('qte')), nan=0.0)
            lower_bound = upper_bound = None
            
            if self.se:
                lower_bound = np.nan_to_num(np.array(self.result.rx2('qte.lower')), nan=0.0)
                upper_bound = np.nan_to_num(np.array(self.result.rx2('qte.upper')), nan=0.0)

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
        except Exception as e:
            raise RuntimeError(f"Erro ao plotar os resultados: {e}")

    def get_results(self):
        """
        Retorna os resultados como um DataFrame do pandas.
        """
        try:
            results_df = pd.DataFrame({
                'Quantile': np.linspace(0.05, 0.95, len(self.result.rx2('qte'))),
                'QTE': np.nan_to_num(np.array(self.result.rx2('qte')), nan=0.0),
                'QTE Lower Bound': np.nan_to_num(np.array(self.result.rx2('qte.lower')), nan=0.0) if self.se else np.nan,
                'QTE Upper Bound': np.nan_to_num(np.array(self.result.rx2('qte.upper')), nan=0.0) if self.se else np.nan
            })
            return results_df
        except Exception as e:
            raise RuntimeError(f"Erro ao obter os resultados: {e}")
