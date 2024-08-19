from rpy2.robjects import r, Formula
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri

# Activate the pandas conversion for rpy2
pandas2ri.activate()

# Import the R 'qte' package
qte = importr('qte')

class SpATT_Estimator:
    """
    SpATT_Estimator is used to estimate Spatial Average Treatment on the Treated (SpATT)
    effects using the R 'qte' package via rpy2.
    
    Attributes:
    -----------
    formula : str
        The formula representing the relationship between the dependent and independent variables.
    data : pandas.DataFrame
        The dataset containing the variables used in the formula.
    t : int
        The time period after treatment.
    tmin1 : int
        The time period before treatment.
    idname : str
        The name of the column representing the unique identifier for each unit.
    tname : str
        The name of the column representing the time periods.
    se : bool
        Whether to compute standard errors.
    iters : int
        The number of bootstrap iterations to compute standard errors.
    """

    def __init__(self, formula, data, t, tmin1, idname, tname, se=False, iters=100):
        self.formula = Formula(formula)
        self.data = pandas2ri.py2rpy(data)
        self.t = t
        self.tmin1 = tmin1
        self.idname = idname
        self.tname = tname
        self.se = se
        self.iters = iters

    def estimate(self):
        """
        Estimate the Spatial Average Treatment on the Treated (SpATT) effect.

        Returns:
        --------
        result : R object
            The result of the SpATT estimation, which can be further processed or summarized.
        """
        result = qte.spatt(self.formula, t=self.t, tmin1=self.tmin1,
                           idname=self.idname, tname=self.tname,
                           data=self.data, se=self.se, iters=self.iters)
        return result

    def summary(self, result):
        """
        Print a summary of the SpATT estimation result.

        Parameters:
        -----------
        result : R object
            The result from the SpATT estimation to be summarized.
        """
        return r['summary'](result)
    
    def plot(self, result):
        """
        Plot the SpATT estimation results.

        Parameters:
        -----------
        result : R object
            The result from the SpATT estimation to be plotted.
        """
        r['plot'](result)

