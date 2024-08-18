import numpy as np
import pandas as pd
from scipy.stats import norm
from statsmodels.regression.quantile_regression import QuantReg

class QTETEstimator:
    """
    QTETEstimator is used to estimate Quantile Treatment Effects on the Treated (QTET).
    
    Attributes:
    -----------
    data : pandas.DataFrame
        The dataset containing the outcome variable, treatment indicator, and covariates.
    outcome : str
        The name of the outcome variable.
    treatment : str
        The name of the treatment indicator variable.
    covariates : list of str
        The list of covariates to control for in the estimation.
    quantiles : list of float
        The list of quantiles at which to estimate the treatment effect.
    """
    
    def __init__(self, data, outcome, treatment, covariates, quantiles):
        self.data = data
        self.outcome = outcome
        self.treatment = treatment
        self.covariates = covariates
        self.quantiles = quantiles
        
    def estimate(self):
        """
        Estimate the QTET for the specified quantiles.
        
        Returns:
        --------
        qtete_results : pandas.DataFrame
            A DataFrame containing the estimated QTETs and their standard errors.
        """
        qtete_results = []
        
        for quantile in self.quantiles:
            treated_data = self.data[self.data[self.treatment] == 1]
            untreated_data = self.data[self.data[self.treatment] == 0]
            
            model_treated = QuantReg(treated_data[self.outcome], treated_data[self.covariates])
            result_treated = model_treated.fit(q=quantile)
            
            model_untreated = QuantReg(untreated_data[self.outcome], untreated_data[self.covariates])
            result_untreated = model_untreated.fit(q=quantile)
            
            qtete = result_treated.params - result_untreated.params
            se_treated = result_treated.bse
            se_untreated = result_untreated.bse
            se = np.sqrt(se_treated**2 + se_untreated**2)
            
            qtete_results.append({
                "Quantile": quantile,
                "QTET": qtete[self.covariates[0]],  # Focusing on the first covariate for simplicity
                "Std. Error": se[self.covariates[0]]
            })
        
        return pd.DataFrame(qtete_results)

    def plot_qtet(self, qtete_results):
        """
        Plot the estimated QTETs.
        
        Parameters:
        -----------
        qtete_results : pandas.DataFrame
            The DataFrame containing the estimated QTETs to be plotted.
        """
        import matplotlib.pyplot as plt
        
        plt.errorbar(qtete_results["Quantile"], qtete_results["QTET"], yerr=qtete_results["Std. Error"], fmt='o')
        plt.xlabel("Quantile")
        plt.ylabel("QTET")
        plt.title("Quantile Treatment Effects on the Treated")
        plt.show()
