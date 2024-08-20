import pandas as pd
import numpy as np
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects.conversion import localconverter
import matplotlib.pyplot as plt

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
    probs : list of float or None
        A list of quantiles at which to estimate the treatment effect, or None to use default.
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

    def __init__(self, formula, xformla, data, probs=None, se=False, iters=100):
        self.formula = formula
        self.xformla = xformla
        self.data = data
        self.probs = probs if probs is not None else np.arange(0.05, 1.00, 0.05)
        self.se = se
        self.iters = iters
        self.result = None

    def fit(self):
        """
        Fits the QTE model using the R qte package. The data is converted
        to an R DataFrame and passed to the R function for estimation.
        """
        with localconverter(ro.default_converter + pandas2ri.converter):
            r_data = ro.conversion.py2rpy(self.data)

        # Chama a função ci_qte do pacote R qte
        self.result = qte.ci_qte(
            formla=ro.Formula(self.formula),
            xformla=ro.Formula(self.xformla),
            data=r_data,
            probs=ro.FloatVector(self.probs),
            se=self.se,
            iters=self.iters
        )

    def summary(self):
        """
        Returns a summary of the QTE results by calling the R summary function.
        """
        return ro.r.summary(self.result)

    def plot(self):
        """
        Generates a plot of the QTE results using Matplotlib.
        """
        if self.result is None:
            raise ValueError("No results to plot. Please run the 'fit' method first.")

        # Extrair os resultados
        qte = np.array(self.result.rx2('qte'))
        qte_lower = np.array(self.result.rx2('qte.lower'))
        qte_upper = np.array(self.result.rx2('qte.upper'))
        tau = np.linspace(0.05, 0.95, len(qte))

        # Plotar os resultados
        plt.figure(figsize=(10, 6))
        plt.plot(tau, qte, 'o-', label="QTE")
        plt.fill_between(tau, qte_lower, qte_upper, color='gray', alpha=0.2, label="95% CI")
        plt.axhline(y=0, color='r', linestyle='--', label="No Effect Line")
        plt.xlabel('Quantiles')
        plt.ylabel('QTE Estimates')
        plt.title('Quantile Treatment Effects (QTE)')
        plt.legend()
        plt.grid(True)
        plt.show()

