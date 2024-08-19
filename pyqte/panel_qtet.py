from rpy2.robjects import r, Formula
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri

# Activate the pandas conversion for rpy2
pandas2ri.activate()

# Import the R 'qte' package
qte = importr('qte')

class PanelQTET_Estimator:
    """
    PanelQTET_Estimator is used to estimate the Quantile Treatment Effect on the Treated (QTET)
    using panel data with the R 'qte' package via rpy2.
    
    Attributes:
    -----------
    formula : str
        The formula representing the relationship between the dependent and independent variables.
    data : pandas.DataFrame
        The dataset containing the variables used in the formula.
    t : int
        The third time period in the sample where treated units receive treatment.
    tmin1 : int
        The second time period in the sample, which should be a pre-treatment period.
    tmin2 : int
        The first time period in the sample, which should be a pre-treatment period.
    idname : str
        The name of the column representing the unique identifier for each unit.
    tname : str
        The name of the column representing the time periods.
    probs : list
        A vector of values between 0 and 1 to compute the QTET at.
    se : bool
        Whether to compute standard errors.
    iters : int
        The number of bootstrap iterations to compute standard errors.
    method : str
        The method for including covariates, either "QR" for quantile regression or "pscore" for propensity score.
    """

    def __init__(self, formula, data, t, tmin1, tmin2, idname, tname, probs, se=False, iters=100, method="pscore"):
        self.formula = Formula(formula)
        self.data = pandas2ri.py2rpy(data)
        self.t = t
        self.tmin1 = tmin1
        self.tmin2 = tmin2
        self.idname = idname
        self.tname = tname
        self.probs = probs
        self.se = se
        self.iters = iters
        self.method = method

    def estimate(self):
        """
        Estimate the Quantile Treatment Effect on the Treated (QTET) using panel data.

        Returns:
        --------
        result : R object
            The result of the Panel QTET estimation, which can be further processed or summarized.
        """
        result = qte.panel_qtet(self.formula, t=self.t, tmin1=self.tmin1, tmin2=self.tmin2,
                                idname=self.idname, tname=self.tname, data=self.data,
                                probs=self.probs, se=self.se, iters=self.iters, method=self.method)
        return result

    def summary(self, result):
        """
        Print a summary of the Panel QTET estimation result.

        Parameters:
        -----------
        result : R object
            The result from the Panel QTET estimation to be summarized.
        """
        return r['summary'](result)
    
    def plot(self, result):
        """
        Plot the Panel QTET estimation results.

        Parameters:
        -----------
        result : R object
            The result from the Panel QTET estimation to be plotted.
        """
        r['plot'](result)

