import pandas as pd
import numpy as np
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects import Formula
from rpy2.robjects.conversion import localconverter
import matplotlib.pyplot as plt

# Ativar a conversão automática de pandas DataFrames para R data.frames
pandas2ri.activate()

# Importar o pacote qte do R
qte = importr('qte')

class CiCEstimator:
    def __init__(self, formula, data, t, tmin1, tname, idname=None, xformla=None, probs=[0.05, 0.95, 0.05], se=True, iters=100, alp=0.05, panel=False, pl=False, cores=2, retEachIter=False):
        self.formula = formula
        self.data = data
        self.t = t
        self.tmin1 = tmin1
        self.tname = tname
        self.idname = idname
        self.xformla = xformla
        
        # Processar 'probs' como um vetor numérico em R
        if isinstance(probs, list) and len(probs) == 3:
            self.probs = ro.FloatVector(np.arange(probs[0], probs[1] + probs[2], probs[2]))
        else:
            self.probs = ro.FloatVector(probs)

        self.se = se
        self.iters = iters
        self.alp = alp
        self.panel = panel
        self.pl = pl
        self.cores = cores
        self.retEachIter = retEachIter

    def fit(self):
        with localconverter(ro.default_converter + pandas2ri.converter):
            r_data = ro.conversion.py2rpy(self.data)

        r_formula = Formula(self.formula)
        additional_args = {}

        if self.xformla:
            additional_args['xformla'] = Formula(self.xformla)

        if self.idname:
            additional_args['idname'] = self.idname

        if self.panel:
            additional_args['panel'] = self.panel

        # Chama a função CiC do pacote qte do R
        self.result = qte.CiC(
            formla=r_formula,
            t=self.t,
            tmin1=self.tmin1,
            tname=self.tname,
            data=r_data,
            probs=self.probs,
            se=self.se,
            iters=self.iters,
            alp=self.alp,
            pl=self.pl,
            cores=self.cores,
            retEachIter=self.retEachIter,
            **additional_args
        )

    def summary(self):
        summary = ro.r.summary(self.result)
        print(summary)
        return summary

    def plot(self):
        """
        Plota as estimativas do CiC com intervalos de confiança, se disponíveis.
        """
        tau = np.array(self.probs)
        cic = np.array(self.result.rx2('QTE'))

        if self.se:
            lower_bound = np.array(self.result.rx2('QTE.lower'))
            upper_bound = np.array(self.result.rx2('QTE.upper'))
            plt.figure(figsize=(10, 6))
            plt.plot(tau, cic, 'o-', label="CiC")
            plt.fill_between(tau, lower_bound, upper_bound, color='gray', alpha=0.2, label="95% CI")
        else:
            plt.figure(figsize=(10, 6))
            plt.plot(tau, cic, 'o-', label="CiC")
        
        plt.axhline(y=0, color='r', linestyle='--', label="No Effect Line")
        plt.xlabel('Quantiles')
        plt.ylabel('CiC Estimates')
        plt.title('Changes-in-Changes (CiC) Estimates')
        plt.legend()
        plt.grid(True)
        plt.show()

