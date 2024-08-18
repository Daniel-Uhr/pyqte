import numpy as np
import pandas as pd
from scipy.stats import norm
from statsmodels.regression.quantile_regression import QuantReg

class CiCEstimator:
    """
    CiCEstimator is used to estimate Quantile Treatment Effects using the Change in Changes (CiC) method.
    
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
        Estimate the Quantile Treatment Effects using CiC for the specified quantiles.
        
        Returns:
        --------
        cic_results : pandas.DataFrame
            A DataFrame containing the estimated Quantile Treatment Effects and their standard errors.
        """
        cic_results = []
        
        for quantile in self.quantiles:
            pre_treated_data = self.data[(self.data[self.treatment] == 1) & (self.data[self.time] == 0)]
            post_treated_data = self.data[(self.data[self.treatment] == 1) & (self.data[self.time] == 1)]
            pre_control_data = self.data[(self.data[self.treatment] == 0) & (self.data[self.time] == 0)]
            post_control_data = self.data[(self.data[self.treatment] == 0) & (self.data[self.time] == 1)]
            
            model_pre_control = QuantReg(pre_control_data[self.outcome], pre_control_data[self.covariates])
            result_pre_control = model_pre_control.fit(q=quantile)
            
            model_post_control = QuantReg(post_control_data[self.outcome], post_control_data[self.covariates])
            result_post_control = model_post_control.fit(q=quantile)
            
            model_pre_treated = QuantReg(pre_treated_data[self.outcome], pre_treated_data[self.covariates])
            result_pre_treated = model_pre_treated.fit(q=quantile)
            
            # Calculate the Change in Changes for the treated group
            cic = result_pre_treated.predict(self.data[self.covariates]) + (result_post_control.predict(self.data[self.covariates]) - result_pre_control.predict(self.data[self.covariates]))
            
            qtete_diff = result_post_control.params - cic
            
            cic_results.append({
                "Quantile": quantile,
                "CiC Estimate": qtete_diff[self.covariates[0]],  # Focusing on the first covariate for simplicity
                "Std. Error": np.sqrt(result_post_control.bse[self.covariates[0]]**2 + result_pre_control.bse[self.covariates[0]]**2)
            })
        
        return pd.DataFrame(cic_results)

    def plot_cic(self, cic_results):
        """
        Plot the estimated CiC Quantile Treatment Effects.
        
        Parameters:
        -----------
        cic_results : pandas.DataFrame
            The DataFrame containing the estimated CiC QTETs to be plotted.
        """
        import matplotlib.pyplot as plt
        
        plt.errorbar(cic_results["Quantile"], cic_results["CiC Estimate"], yerr=cic_results["Std. Error"], fmt='o')
        plt.xlabel("Quantile")
        plt.ylabel("CiC Estimate")
        plt.title("Quantile Treatment Effects using Change in Changes (CiC)")
        plt.show()

