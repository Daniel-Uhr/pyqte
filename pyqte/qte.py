import pandas as pd
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects.conversion import localconverter

# Ativando a conversão automática de pandas DataFrame para R DataFrame
pandas2ri.activate()

# Importando o pacote qte do R
qte = importr('qte')

class QTEEstimator:
    """
    QTEEstimator serves as an interface between Python and the R 'qte' package.
    It allows users to perform Quantile Treatment Effect estimation using R's
    capabilities but within a Python environment.

    Parameters:
    -----------
    formula : str
        A string representing the model formula (e.g., 're78 ~ treat').
    xformla : str
        A string representing the covariates formula (e.g., '~ age + education').
    data : pandas.DataFrame
        The dataset containing the variables specified in the formula.
    probs : list of float
        A list of quantiles at which to estimate the treatment effect.
    se : bool, optional
        Whether to compute standard errors (default is False).
    iters : int, optional
        Number of iterations for bootstrap standard errors (default is 100).

    Methods:
    --------
    fit()
        Fits the QTE model using the provided data and parameters.
    summary()
        Returns a summary of the fitted QTE model.
    plot()
        Generates a plot of the QTE results.
    """

    def __init__(self, formula, xformla, data, probs, se=False, iters=100):
        self.formula = formula
        self.xformla = xformla
        self.data = data
        self.probs = probs
        self.se = se
        self.iters = iters

    def fit(self):
        """
        Fits the QTE model using the R qte package. The data is converted
        to an R DataFrame and passed to the R function for estimation.
        """
        with localconverter(ro.default_converter + pandas2ri.converter):
            r_data = ro.conversion.py2rpy(self.data)

        # Chama a função ci_qte do pacote R qte
        result = qte.ci_qte(
            formla=ro.Formula(self.formula),
            xformla=ro.Formula(self.xformla),
            data=r_data,
            probs=ro.FloatVector(self.probs),
            se=self.se,
            iters=self.iters
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

