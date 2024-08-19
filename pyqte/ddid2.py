import pandas as pd
from rpy2.robjects import r, Formula
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from .data_loader import prepare_r_data, create_formula

# Activate the pandas conversion to R dataframes
pandas2ri.activate()

# Import the necessary R packages
qte = importr('qte')

class DDID2Estimator:
    """
    DDID2Estimator is used to estimate the Difference-in-Differences with two differences (DDID2) effects.
    
    Attributes:
    -----------
    data : pandas.DataFrame
        The dataset containing the outcome variable, treatment indicator, and covariates.
    outcome : str
        The name of the outcome variable.
    treatment : str
        The name of the treatment indicator variable.
    time_var : str
        The name of the time variable.
    id_var : str
        The name of the individual identifier variable.
    """
    
    def __init__(self, data, outcome, treatment, time_var, id_var, covariates=None):
        self.data = prepare_r_data(data)
        self.outcome = outcome
        self.treatment = treatment
        self.time_var = time_var
        self.id_var = id_var
        self.covariates = covariates if covariates else []

    def estimate(self, t, tmin1, tmin2, probs=None, se=True, iters=100, alp=0.05):
        """
        Estimate the DDID2 effect.
        
        Parameters:
        -----------
        t : int
            The third time period (post-treatment).
        tmin1 : int
            The second time period (pre-treatment).
        tmin2 : int
            The first time period (pre-treatment).
        probs : list of float, optional
            The list of quantiles at which to estimate the treatment effect.
        se : bool, optional
            Whether to compute standard errors (default is True).
        iters : int, optional
            The number of bootstrap iterations for standard errors (default is 100).
        alp : float, optional
            The significance level for confidence intervals (default is 0.05).
        
        Returns:
        --------
        results : dict
            A dictionary containing the estimated DDID2 effects and standard errors.
        """
        formula_str = f"{self.outcome} ~ {self.treatment}"
        formula = create_formula(self.outcome, [self.treatment] + self.covariates)
        
        ddid2_result = qte.ddid2(
            formla=Formula(formula_str),
            t=t,
            tmin1=tmin1,
            tmin2=tmin2,
            tname=self.time_var,
            idname=self.id_var,
            data=self.data,
            probs=r.probs if probs else r.seq(0.05, 0.95, 0.05),
            se=se,
            iters=iters,
            alp=alp
        )
        
        # Extract results from the R object
        qte_estimates = dict(zip(ddid2_result.rx2('probs'), ddid2_result.rx2('qte')))
        se_estimates = dict(zip(ddid2_result.rx2('probs'), ddid2_result.rx2('qte.se')))
        ate_estimate = ddid2_result.rx2('ate')[0]
        ate_se_estimate = ddid2_result.rx2('ate.se')[0]
        
        results = {
            'qte': qte_estimates,
            'qte.se': se_estimates,
            'ate': ate_estimate,
            'ate.se': ate_se_estimate
        }
        
        return results

    def summary(self, results):
        """
        Generate a summary of the DDID2 estimation results.
        
        Parameters:
        -----------
        results : dict
            The results from the DDID2 estimation.
        
        Returns:
        --------
        summary : str
            A summary of the DDID2 estimation results.
        """
        summary_str = "DDID2 Estimation Results:\n"
        summary_str += "Quantile Treatment Effects (QTE):\n"
        for prob, qte in results['qte'].items():
            summary_str += f"Quantile {prob:.2f}: QTE = {qte:.4f}, SE = {results['qte.se'][prob]:.4f}\n"
        summary_str += f"\nAverage Treatment Effect (ATE): {results['ate']:.4f}, SE: {results['ate.se']:.4f}\n"
        return summary_str

    def plot(self, results):
        """
        Plot the DDID2 estimation results.
        
        Parameters:
        -----------
        results : dict
            The results from the DDID2 estimation.
        """
        import matplotlib.pyplot as plt
        
        quantiles = list(results['qte'].keys())
        qte_values = list(results['qte'].values())
        qte_se_values = list(results['qte.se'].values())
        
        plt.errorbar(quantiles, qte_values, yerr=qte_se_values, fmt='o')
        plt.xlabel('Quantiles')
        plt.ylabel('QTE')
        plt.title('DDID2: Quantile Treatment Effects')
        plt.show()
