import numpy as np
import pandas as pd
from scipy.stats import norm
from statsmodels.regression.quantile_regression import QuantReg

class QDiDEstimator:
    """
    QDiDEstimator is used to estimate Quantile Treatment Effects using a Quantile Difference-in-Differences approach.
    
    Attributes:
    -----------
    data : pandas.DataFrame
        The dataset containing the outcome variable, treatment indicator, time indicator, and covariates.
    outcome : str
        The name of the outcome variable.
    treatment : str
        The name of the treatment indicator variable.
    time : str
        The name of the time indicator variable.
    covariates : list of str
        The list of covariates to control for in the estimation.
    quantiles : list of float
        The list of quantiles at which to estimate the treatment effect.
    panel : bool
        Whether the data is panel data (True) or repeated cross-section (False).
    """
    
    def __init__(self, data, outcome, treatment, time, covariates, quantiles, panel=True):
        self.data = data
        self.outcome = outcome
        self.treatment = treatment
        self.time = time
        self.covariates = covariates
        self.quantiles = quantiles
        self.panel = panel
        
    def estimate(self):
        """
        Estimate the Quantile Treatment Effects using QDiD for the specified quantiles.
        
        Returns:
        --------
        qdid_results : pandas.DataFrame
            A DataFrame containing the estimated Quantile Treatment Effects and their standard errors.
        """
        qdid_results = []
        
        for quantile in self.quantiles:
            pre_treated_data = self.data[(self.data[self.treatment] == 1) & (self.data[self.time] == 0)]
            post_treated_data = self.data[(self.data[self.treatment] == 1) & (self.data[self.time] == 1)]
            pre_control_data = self.data[(self.data[self.treatment] == 0) & (self.data[self.time] == 0)]
            post_control_data = self.data[(self.data[self.treatment] == 0) & (self.data[self.time] == 1)]
            
            model_pre_treated = QuantReg(pre_treated_data[self.outcome], pre_treated_data[self.covariates])
            result_pre_treated = model_pre_treated.fit(q=quantile)
            
            model_post_treated = QuantReg(post_treated_data[self.outcome], post_treated_data[self.covariates])
            result_post_treated = model_post_treated.fit(q=quantile)
            
            model_pre_control = QuantReg(pre_control_data[self.outcome], pre_control_data[self.covariates])
            result_pre_control = model_pre_control.fit(q=quantile)
            
            model_post_control = QuantReg(post_control_data[self.outcome], post_control_data[self.covariates])
            result_post_control = model_post_control.fit(q=quantile)
            
            qtete_pre = result_pre_treated.params - result_pre_control.params
            qtete_post = result_post_treated.params - result_post_control.params
            
            qtete_diff = qtete_post - qtete_pre
            se_pre = np.sqrt(result_pre_treated.bse**2 + result_pre_control.bse**2)
            se_post = np.sqrt(result_post_treated.bse**2 + result_post_control.bse**2)
            se_diff = np.sqrt(se_pre**2 + se_post**2)
            
            qdid_results.append({
                "Quantile": quantile,
                "QDiD Estimate": qtete_diff[self.covariates[0]],  # Focusing on the first covariate for simplicity
                "Std. Error": se_diff[self.covariates[0]]
            })
        
        return pd.DataFrame(qdid_results)

    def plot_qdid(self, qdid_results):
        """
        Plot the estimated QDiD Quantile Treatment Effects.
        
        Parameters:
        -----------
        qdid_results : pandas.DataFrame
            The DataFrame containing the estimated QDiD QTETs to be plotted.
        """
        import matplotlib.pyplot as plt
        
        plt.errorbar(qdid_results["Quantile"], qdid_results["QDiD Estimate"], yerr=qdid_results["Std. Error"], fmt='o')
        plt.xlabel("Quantile")
        plt.ylabel("QDiD Estimate")
        plt.title("Quantile Treatment Effects using QDiD")
        plt.show()
