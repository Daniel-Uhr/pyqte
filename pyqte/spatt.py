import pandas as pd
import numpy as np
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects import Formula, FloatVector

# Activate the automatic conversion of pandas DataFrames to R data.frames
pandas2ri.activate()

# Import the R 'qte' package
qte = importr('qte')

class SpATT_Estimator:
    """
    SpATT_Estimator is used to estimate Spatial Average Treatment on the Treated (SpATT)
    effects using the R 'qte' package via rpy2.
    """
    
    def __init__(self, formula, data, t, tmin1, tname, xformla=None, w=None, panel=False, idname=None, 
                 iters=100, alp=0.05, method="logit", se=True, 
                 retEachIter=False, seedvec=None, pl=False, cores=2):
        self.formula = formula
        self.data = data
        self.t = t
        self.tmin1 = tmin1
        self.tname = tname
        self.xformla = xformla
        self.w = w
        self.panel = panel
        self.idname = idname
        self.iters = iters
        self.alp = alp
        self.method = method
        self.se = se
        self.retEachIter = retEachIter
        self.seedvec = seedvec
        self.pl = pl
        self.cores = cores
        self.result = None
        self.info = {}

    def fit(self):
        r_formula = Formula(self.formula)
        r_data = pandas2ri.py2rpy(self.data)
        
        additional_args = {
            't': self.t,
            'tmin1': self.tmin1,
            'tname': self.tname,
            'se': self.se,
            'iters': self.iters,
            'alp': self.alp,
            'method': self.method,
            'retEachIter': self.retEachIter,
            'pl': self.pl,
            'cores': self.cores
        }

        if self.xformla:
            additional_args['xformla'] = Formula(self.xformla)
        
        if self.w is not None:
            additional_args['w'] = FloatVector(self.w)

        if self.idname:
            additional_args['idname'] = self.idname
        
        if self.seedvec is not None:
            additional_args['seedvec'] = FloatVector(self.seedvec)

        if self.panel:
            additional_args['panel'] = self.panel

        self.result = qte.spatt(
            formla=r_formula,
            data=r_data,
            **additional_args
        )
        self._extract_info()

    def _extract_info(self):
        self.info['qte'] = np.array(self.result.rx2('qte'))
        self.info['probs'] = np.array(self.result.rx2('probs'))

        if self.se:
            self.info['qte.lower'] = np.array(self.result.rx2('qte.lower'))
            self.info['qte.upper'] = np.array(self.result.rx2('qte.upper'))
        else:
            self.info['qte.lower'] = None
            self.info['qte.upper'] = None

    def summary(self):
        if self.result is None:
            raise ValueError("Model has not been fitted yet. Call `fit()` before calling `summary()`.")
        summary = ro.r.summary(self.result)
        print(summary)
        return summary



