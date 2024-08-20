import pandas as pd
import numpy as np
from rpy2.robjects import r, Formula
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
import matplotlib.pyplot as plt

# Ativar a conversão automática de pandas DataFrames para R data.frames
pandas2ri.activate()

# Importar o pacote qte do R
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
    covariates : list of str, optional
        List of covariates to include in the model.
    """

    def __init__(self, data, outcome, treatment, time_var, id_var, covariates=None):
        self.data = data
        self.outcome = outcome
        self.treatment = treatment
        self.time_var = time_var
        self.id_var = id_var
        self.covariates = covariates if covariates else []
        self.result = None
        self.info = {}

    def estimate(self, t, tmin1, tmin2, probs=None, se=True, iters=100, alp=0.05, method="logit", retEachIter=False, panel=True, cores=None):
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
        method : str, optional
            The method for estimating the propensity score (default is "logit").
        retEachIter : bool, optional
            Whether to return results for each bootstrap iteration (default is False).
        panel : bool, optional
            Whether the data is panel or repeated cross sections (default is True).
        cores : int, optional
            The number of cores to use for parallel processing (default is None).
        """
        r_formula = Formula(f"{self.outcome} ~ {self.treatment}")
        r_data = pandas2ri.py2rpy(self.data)

        additional_args = {
            't': t,
            'tmin1': tmin1,
            'tmin2': tmin2,
            'tname': self.time_var,
            'idname': self.id_var,
            'probs': r.seq(0.05, 0.95, 0.05) if probs is None else ro.FloatVector(probs),
            'se': se,
            'iters': iters,
            'alp': alp,
            'method': method,
            'retEachIter': retEachIter,
            'panel': panel,
            'cores': cores
        }

        if self.covariates:
            r_xformla = Formula(f"~ {' + '.join(self.covariates)}")
            additional_args['xformla'] = r_xformla

        self.result = qte.ddid2(
            formla=r_formula,
            data=r_data,
            **additional_args
        )

        # Armazenar os resultados na variável self.info para futura extração
        self.info['qte'] = np.array(self.result.rx2('qte'))
        self.info['ate'] = np.array(self.result.rx2('ate'))[0]
        self.info['probs'] = np.array(self.result.rx2('probs'))
        self.info['qte.se'] = np.array(self.result.rx2('qte.se')) if se else None
        self.info['qte.lower'] = np.array(self.result.rx2('qte.lower')) if se else None
        self.info['qte.upper'] = np.array(self.result.rx2('qte.upper')) if se else None

    def summary(self):
        """
        Generate a summary of the DDID2 estimation results.
        
        Returns:
        --------
        summary : str
            A summary of the DDID2 estimation results.
        """
        if self.result is None:
            raise ValueError("Model has not been fitted yet. Call `fit()` before calling `summary()`.")
        
        summary_str = "DDID2 Estimation Results:\n"
        summary_str += "Quantile Treatment Effects (QTE):\n"
        for prob, qte in zip(self.info['probs'], self.info['qte']):
            summary_str += f"Quantile {prob:.2f}: QTE = {qte:.4f}"
            if self.se:
                summary_str += f", SE = {self.info['qte.se'][int(prob*20)]:.4f}\n"
            else:
                summary_str += "\n"
        summary_str += f"\nAverage Treatment Effect (ATE): {self.info['ate']:.4f}\n"
        return summary_str

    def plot(self):
        """
        Plot the DDID2 estimation results.
        """
        if self.result is None:
            raise ValueError("Model has not been fitted yet. Call `fit()` before calling `plot()`.")
        
        quantiles = self.info['probs']
        qte_values = self.info['qte']

        plt.figure(figsize=(10, 6))
        plt.plot(quantiles, qte_values, 'o-', label="QTE")

        if self.se and 'qte.lower' in self.info and 'qte.upper' in self.info:
            plt.fill_between(quantiles, self.info['qte.lower'], self.info['qte.upper'], color='gray', alpha=0.2, label="95% CI")

        plt.axhline(y=0, color='r', linestyle='--', label="No Effect Line")
        plt.xlabel('Quantiles')
        plt.ylabel('QTE Estimates')
        plt.title('DDID2: Quantile Treatment Effects')
        plt.legend()
        plt.grid(True)
        plt.show()

    def get_results(self):
        """
        Return the estimation results as a DataFrame for further analysis.
        
        Returns:
        --------
        results_df : pandas.DataFrame
            A DataFrame containing the QTE, SE (if available), and confidence intervals (if available) for each quantile.
        """
        data = {
            'Quantile': self.info['probs'],
            'QTE': self.info['qte']
        }
        if self.se:
            data['QTE Lower Bound'] = self.info.get('qte.lower', np.full(len(self.info['probs']), np.nan))
            data['QTE Upper Bound'] = self.info.get('qte.upper', np.full(len(self.info['probs']), np.nan))
            data['SE'] = self.info.get('qte.se', np.full(len(self.info['probs']), np.nan))

        return pd.DataFrame(data)
