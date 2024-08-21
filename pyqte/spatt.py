import pandas as pd
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects import Formula

# Activate the automatic conversion of pandas DataFrames to R data.frames
pandas2ri.activate()

# Import the R 'qte' package
qte = importr('qte')

class SpATTEstimator:
    def __init__(self, formula, data, t, tmin1, tname, xformla=None, w=None, panel=False, idname=None, 
                 iters=100, alp=0.05, method="logit", se=True, 
                 retEachIter=False, seedvec=None, pl=False, cores=2):
        self.formula = Formula(formula)
        self.data = pandas2ri.py2rpy(data)
        self.t = t
        self.tmin1 = tmin1
        self.tname = tname
        self.xformla = Formula(xformla) if xformla else None
        self.w = ro.FloatVector(w) if w is not None else None
        self.panel = panel
        self.idname = idname
        self.iters = iters
        self.alp = alp
        self.method = method
        self.se = se
        self.retEachIter = retEachIter
        self.seedvec = ro.FloatVector(seedvec) if seedvec is not None else None
        self.pl = pl
        self.cores = cores
        self.result = None

    def fit(self):
        """
        Estimate the Spatial Average Treatment on the Treated (SpATT) effect.
        """
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
            additional_args['xformla'] = self.xformla
        
        if self.w is not None:
            additional_args['w'] = self.w

        if self.idname:
            additional_args['idname'] = self.idname
        
        if self.seedvec is not None:
            additional_args['seedvec'] = self.seedvec

        if self.panel:
            additional_args['panel'] = self.panel

        self.result = qte.spatt(
            formla=self.formula,
            data=self.data,
            **additional_args
        )

    def summary(self):
        """
        Print a summary of the SpATT estimation result.
        """
        if self.result is None:
            raise ValueError("Model has not been fitted yet. Call `fit()` before calling `summary()`.")
        
        ate = self.result.rx2('ate')[0]  # Extract the ATE
        print(f"Average Treatment Effect: {ate:.2f}")
