import numpy as np
import pandas as pd
from scipy.stats import norm
from statsmodels.regression.quantile_regression import QuantReg

class QTEEstimator:
    """
    QTEEstimator is used to estimate Quantile Treatment Effects (QTE).
    
    Attributes:
    -----------
    data : pandas.DataFrame
        The dataset containing the outcome variable, treatment indicator, and covariates.
    outcome : str
        The name of the outcome variable.
    treatment : str
        The name of the treatment indicator variable.
    quantiles : list of float
        The list of quantiles at which to estimate the treatment effect.
    """
    
    def __init__(self, data, outcome, treatment, quantiles):
        self.data = data
        self.outcome = outcome
        self.treatment = treatment
        self.quantiles = quantiles
        
    def estimate(self):
        """
        Estimate the QTE for the specified quantiles.
        
        Returns:
        --------
        qte_results : pandas.DataFrame
            A DataFrame containing the estimated QTEs and their standard errors.
        """
        qte_results = []
        
        for quantile in self.quantiles:
            model = QuantReg(self.data[self.outcome], self.data[[self.treatment]])
            result = model.fit(q=quantile)
            
            qte = result.params[self.treatment]
            se = result.bse[self.treatment]
            
            qte_results.append({
                "Quantile": quantile,
                "QTE": qte,
                "Std. Error": se
            })
        
        return pd.DataFrame(qte_results)

    def plot_qte(self, qte_results):
        """
        Plot the estimated QTEs.
        
        Parameters:
        -----------
        qte_results : pandas.DataFrame
            The DataFrame containing the estimated QTEs to be plotted.
        """
        import matplotlib.pyplot as plt
        
        plt.errorbar(qte_results["Quantile"], qte_results["QTE"], yerr=qte_results["Std. Error"], fmt='o')
        plt.xlabel("Quantile")
        plt.ylabel("QTE")
        plt.title("Quantile Treatment Effects")
        plt.show()

from .data_loader import load_lalonde_data