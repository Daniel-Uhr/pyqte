import pandas as pd
import numpy as np
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects import Formula

# Activate the automatic conversion of pandas DataFrames to R data.frames
pandas2ri.activate()

# Import the qte package from R
qte = importr('qte')

class QDiDEstimator:
    """
    QDiDEstimator is used to estimate Quantile Difference-in-Differences (QDiD)
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
    probs : list
        The list of quantiles at which to estimate the treatment effect.
    se : bool
        Whether to compute standard errors.
    iters : int
        The number of bootstrap iterations to compute standard errors.
    """
    
    def __init__(self, formula, data, t, tmin1, idname, tname, probs=[0.05, 0.5, 0.95], se=True, iters=100):
        self.formula = formula
        self.data = data
        self.t = t
        self.tmin1 = tmin1
        self.idname = idname
        self.tname = tname
        self.probs = probs
        self.se = se
        self.iters = iters

    def estimate(self):
        """
        Estimate the QDiD effects.

        Returns:
        --------
        results : dict
            A dictionary containing the estimated QDiD effects and, if requested, the standard errors.
        """
        # Convert the pandas DataFrame to an R data.frame
        r_data = pandas2ri.py2rpy(self.data)

        # Prepare the formula for R
        r_formula = Formula(self.formula)

        # Call the qdid function from the R 'qte' package
        qdid_result = QDiD(r_formula, data=r_data, t=self.t, tmin1=self.tmin1,
                               idname=self.idname, tname=self.tname, probs=ro.FloatVector(self.probs),
                               se=self.se, iters=self.iters)

        # Extract the results into a dictionary
        results = {
            'qdid': np.array(qdid_result.rx2('QTE')),
            'probs': self.probs
        }

        if self.se:
            results['se'] = np.array(qdid_result.rx2('Std.Error'))

        return results

    def summary(self):
        """
        Provide a summary of the QDiD estimation results.
        
        Returns:
        --------
        summary : str
            A textual summary of the QDiD results.
        """
        results = self.estimate()
        summary_str = "Quantile Difference-in-Differences (QDiD) Results:\n"
        summary_str += "Quantiles: " + str(self.probs) + "\n"
        summary_str += "QDiD Estimates: " + str(results['qdid']) + "\n"
        
        if self.se:
            summary_str += "Standard Errors: " + str(results['se']) + "\n"
        
        return summary_str

    def plot(self):
        """
        Plot the QDiD estimates with confidence intervals if available.
        """
        import matplotlib.pyplot as plt

        results = self.estimate()
        
        plt.errorbar(self.probs, results['qdid'], yerr=results.get('se', None), fmt='o', capsize=5)
        plt.xlabel('Quantiles')
        plt.ylabel('QDiD Estimates')
        plt.title('Quantile Difference-in-Differences (QDiD) Estimates')
        plt.grid(True)
        plt.show()
