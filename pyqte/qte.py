import pandas as pd
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects.conversion import localconverter

# Activate the automatic conversion of pandas DataFrame to R DataFrame
pandas2ri.activate()

# Import the qte package from R
qte = importr('qte')

class QTEEstimator:
    """
    QTEEstimator serves as an interface between Python and the R 'qte' package.
    It allows users to perform Quantile Treatment Effect estimation using R's
    capabilities but within a Python environment.

    Parameters:
    -----------
    formula : str
        A string representing the model formula (e.g., 're ~ treat').
    data : pandas.DataFrame
        The dataset containing the variables specified in the formula.
    probs : list of float
        A list of quantiles at which to estimate the treatment effect.
    t : int
        The treatment time period.
    tmin1 : int
        The pre-treatment time period.
    idname : str
        The name of the identifier variable for the panel data.
    tname : str
        The name of the time variable in the dataset.
    se : bool, optional
        Whether to compute standard errors (default is False).
    iters : int, optional
        Number of iterations for bootstrap standard errors (default is 100).
    panel : bool, optional
        Whether the data is panel data (default is False).

    Methods:
    --------
    fit()
        Fits the QTE model using the provided data and parameters.
    summary()
        Returns a summary of the fitted QTE model.
    plot()
        Generates a plot of the QTE results.
    """

    def __init__(self, formula, data, probs, t, tmin1, idname, tname, se=False, iters=100, panel=False):
        self.formula = formula
        self.data = data
        self.probs = probs
        self.t = t
        self.tmin1 = tmin1
        self.idname = idname
        self.tname = tname
        self.se = se
        self.iters = iters
        self.panel = panel

    def fit(self):
        """
        Fits the QTE model using the R qte package. The data is converted
        to an R DataFrame and passed to the R function for estimation.
        """
        with localconverter(ro.default_converter + pandas2ri.converter):
            r_data = ro.conversion.py2rpy(self.data)

        # Call the qte function from the R qte package
        result = ci.qte(
            formula=self.formula,
            data=r_data,
            probs=ro.FloatVector(self.probs),
            t=self.t,
            tmin1=self.tmin1,
            idname=self.idname,
            tname=self.tname,
            se=self.se,
            iters=self.iters,
            panel=self.panel
        )

        self.result = result

    def summary(self):
        """
        Returns a summary of the QTE results by calling the R summary function.
        """
        return ro.r.summary(self.result)

    def plot(self):
        """
        Generates a plot of the QTE results using the R plot function.
        """
        ro.r.plot(self.result)
