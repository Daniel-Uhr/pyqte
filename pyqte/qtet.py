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

class QTETEstimator:
    """
    QTETEstimator is used to estimate Quantile Treatment Effects on the Treated (QTET) 
    using panel data with Difference in Differences (DiD) assumptions.

    Attributes:
    -----------
    data : pandas.DataFrame
        The dataset containing the outcome variable, treatment indicator, and covariates.
    formula : str
        The formula representing the model to be estimated (e.g., 'outcome ~ treatment').
    t : int
        The time period when the treatment is applied.
    tmin1 : int
        The time period before the treatment is applied.
    tmin2 : int
        The time period before tmin1, used as an additional control.
    idname : str
        The name of the column that identifies individuals in the panel data.
    tname : str
        The name of the column that identifies the time periods in the panel data.
    probs : list of float
        The list of quantiles at which to estimate the treatment effect.
    iters : int
        The number of bootstrap iterations to compute standard errors.
    se : bool
        Whether to compute standard errors.
    """

    def __init__(self, data, formula, t, tmin1, tmin2, idname, tname, probs, iters=100, se=True, method='qr'):
        self.data = data
        self.formula = formula
        self.t = t
        self.tmin1 = tmin1
        self.tmin2 = tmin2
        self.idname = idname
        self.tname = tname
        self.probs = probs
        self.iters = iters
        self.se = se
        self.method = method

    def estimate(self):
        """
        Estimate the QTET for the specified quantiles.

        Returns:
        --------
        result : rpy2.robjects.vectors.ListVector
            A list containing the estimated QTETs and their standard errors.
        """
        # Convertendo o DataFrame pandas para um DataFrame R
        r_data = pandas2ri.py2rpy(self.data)

        # Criando a fórmula no formato do R
        r_formula = Formula(self.formula)

        # Chamando a função do R para estimar o QTET
        result = qte.panel_qtet(
            formla=r_formula,
            t=self.t,
            tmin1=self.tmin1,
            tmin2=self.tmin2,
            tname=self.tname,
            idname=self.idname,
            data=r_data,
            probs=ro.FloatVector(self.probs),
            iters=self.iters,
            se=self.se,
            method=self.method
        )
        return result

    def summary(self, result):
        """
        Display a summary of the QTET estimation result.

        Parameters:
        -----------
        result : rpy2.robjects.vectors.ListVector
            The result object from the estimate() method.
        """
        ro.r['summary'](result)

    def plot(self, result):
        """
        Plot the estimated QTET.

        Parameters:
        -----------
        result : rpy2.robjects.vectors.ListVector
            The result object from the estimate() method.
        """
        ro.r['plot'](result)
