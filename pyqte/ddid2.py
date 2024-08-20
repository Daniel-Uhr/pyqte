import pandas as pd
import numpy as np
from rpy2.robjects import Formula
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
import matplotlib.pyplot as plt

# Ativando a conversão automática de pandas DataFrames para R data.frames
pandas2ri.activate()

# Importando o pacote qte do R
qte = importr('qte')

class DDID2Estimator:
    def __init__(self, formula, data, t, tmin1, tname, idname=None, xformla=None, probs=[0.05, 0.95, 0.05], 
                 se=True, iters=100, alp=0.05, method='logit', retEachIter=False, panel=True, dropalwaystreated=True, 
                 seedvec=None, pl=False, cores=None):
        self.formula = formula
        self.xformla = xformla
        self.data = data
        self.t = t
        self.tmin1 = tmin1
        self.tname = tname
        self.idname = idname
        
        # Processar 'probs' como um vetor numérico em R
        if isinstance(probs, list) and len(probs) == 3:
            self.probs = np.arange(probs[0], probs[1] + probs[2], probs[2])
        else:
            self.probs = probs
        
        self.se = se
        self.iters = iters
        self.alp = alp
        self.method = method
        self.retEachIter = retEachIter
        self.panel = panel
        self.dropalwaystreated = dropalwaystreated
        self.seedvec = seedvec
        self.pl = pl
        self.cores = cores
        self.result = None

    def fit(self):
        r_formula = Formula(self.formula)
        r_data = pandas2ri.py2rpy(self.data)
        
        additional_args = {
            't': self.t,
            'tmin1': self.tmin1,
            'tname': self.tname,
            'panel': self.panel,
            'dropalwaystreated': self.dropalwaystreated,
            'se': self.se,
            'iters': self.iters,
            'alp': self.alp,
            'method': self.method,
            'retEachIter': self.retEachIter,
            'pl': self.pl,
            'cores': self.cores
        }

        if self.xformla:
            r_xformla = Formula(self.xformla)
            additional_args['xformla'] = r_xformla
        
        if self.idname:
            additional_args['idname'] = self.idname
        
        if self.seedvec is not None:
            additional_args['seedvec'] = self.seedvec

        self.result = qte.ddid2(
            formla=r_formula,
            data=r_data,
            probs=np.array(self.probs),
            **additional_args
        )

    def summary(self):
        if self.result is None:
            raise ValueError("Model has not been fitted yet. Call `fit()` before calling `summary()`.")
        summary = ro.r.summary(self.result)
        print(summary)
        return summary

    def plot(self):
        if self.result is None:
            raise ValueError("Model has not been fitted yet. Call `fit()` before calling `plot()`.")
        
        tau = np.array(self.probs)
        qte = np.array(self.result.rx2('qte'))

        plt.figure(figsize=(10, 6))
        plt.plot(tau, qte, 'o-', label="DDID2")

        if self.se:
            if 'qte.lower' in self.result.names and 'qte.upper' in self.result.names:
                lower_bound = np.array(self.result.rx2('qte.lower'))
                upper_bound = np.array(self.result.rx2('qte.upper'))
                if np.issubdtype(lower_bound.dtype, np.number) and np.issubdtype(upper_bound.dtype, np.number):
                    plt.fill_between(tau, lower_bound, upper_bound, color='gray', alpha=0.2, label="95% CI")
                else:
                    print("Intervalos de confiança contêm valores não numéricos. Plotagem omitida.")
            else:
                print("Intervalos de confiança não estão disponíveis. Plotando apenas os valores de QTE.")

        plt.axhline(y=0, color='r', linestyle='--', label="No Effect Line")
        plt.xlabel('Quantiles')
        plt.ylabel('DDID2 Estimates')
        plt.title('Quantile Treatment Effects on the Treated (DDID2)')
        plt.legend()
        plt.grid(True)
        plt.show()

    def get_results(self):
        if self.result is None:
            raise ValueError("Model has not been fitted yet. Call `fit()` before calling `get_results()`.")

        # Extrair os resultados e convertê-los em um DataFrame
        qte = np.array(self.result.rx2('qte'))
        probs = np.array(self.result.rx2('probs'))

        # Verificar se existem intervalos de confiança
        if 'qte.lower' in self.result.names and 'qte.upper' in self.result.names:
            lower_bound = np.array(self.result.rx2('qte.lower'))
            upper_bound = np.array(self.result.rx2('qte.upper'))
        else:
            lower_bound = upper_bound = np.zeros_like(qte)

        results_df = pd.DataFrame({
            'Quantile': probs,
            'QTE': qte,
            'QTE Lower Bound': lower_bound,
            'QTE Upper Bound': upper_bound
        })

        return results_df
