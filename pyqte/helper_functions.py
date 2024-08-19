import pandas as pd
import numpy as np
from rpy2.robjects import pandas2ri, Formula
from rpy2.robjects.packages import importr

# Activate the pandas conversion for rpy2
pandas2ri.activate()

# Import the necessary R packages
base = importr('base')
stats = importr('stats')

def prepare_r_data(dataframe):
    """
    Convert a pandas DataFrame to an R dataframe.
    
    Parameters:
    -----------
    dataframe : pandas.DataFrame
        The DataFrame to be converted.
    
    Returns:
    --------
    r_dataframe : R dataframe
        The converted R dataframe.
    """
    return pandas2ri.py2rpy(dataframe)

def create_formula(dependent_var, independent_vars):
    """
    Create an R formula from dependent and independent variables.
    
    Parameters:
    -----------
    dependent_var : str
        The name of the dependent variable.
    independent_vars : list of str
        The list of independent variables.
    
    Returns:
    --------
    formula : rpy2.robjects.Formula
        The created R formula.
    """
    formula_str = f"{dependent_var} ~ {' + '.join(independent_vars)}"
    return Formula(formula_str)

def calculate_summary_statistics(dataframe):
    """
    Calculate summary statistics for a pandas DataFrame.
    
    Parameters:
    -----------
    dataframe : pandas.DataFrame
        The DataFrame for which to calculate summary statistics.
    
    Returns:
    --------
    summary : pandas.DataFrame
        A DataFrame containing the summary statistics.
    """
    summary = dataframe.describe()
    return summary

def bootstrap_sample(dataframe, n=1000):
    """
    Generate bootstrap samples from a pandas DataFrame.
    
    Parameters:
    -----------
    dataframe : pandas.DataFrame
        The DataFrame to bootstrap.
    n : int, optional (default=1000)
        The number of bootstrap samples to generate.
    
    Returns:
    --------
    samples : list of pandas.DataFrame
        A list containing the bootstrap samples.
    """
    samples = [dataframe.sample(frac=1, replace=True) for _ in range(n)]
    return samples

def calculate_confidence_intervals(data, alpha=0.05):
    """
    Calculate confidence intervals for the mean of a pandas DataFrame.
    
    Parameters:
    -----------
    data : pandas.DataFrame
        The data for which to calculate confidence intervals.
    alpha : float, optional (default=0.05)
        The significance level for the confidence interval.
    
    Returns:
    --------
    intervals : pandas.DataFrame
        A DataFrame containing the lower and upper bounds of the confidence intervals.
    """
    mean = data.mean()
    std_err = data.sem()
    margin_of_error = std_err * stats.qnorm(1 - alpha / 2)
    
    lower_bound = mean - margin_of_error
    upper_bound = mean + margin_of_error
    
    intervals = pd.DataFrame({
        'Lower Bound': lower_bound,
        'Upper Bound': upper_bound
    })
    
    return intervals

def merge_dataframes(df1, df2, on):
    """
    Merge two pandas DataFrames on a common key.
    
    Parameters:
    -----------
    df1 : pandas.DataFrame
        The first DataFrame.
    df2 : pandas.DataFrame
        The second DataFrame.
    on : str
        The key column to merge on.
    
    Returns:
    --------
    merged_df : pandas.DataFrame
        The merged DataFrame.
    """
    merged_df = pd.merge(df1, df2, on=on)
    return merged_df

def generate_quantile_regression_results(model, quantiles):
    """
    Generate results from a quantile regression model.
    
    Parameters:
    -----------
    model : statsmodels.regression.quantile_regression.QuantReg
        The fitted quantile regression model.
    quantiles : list of float
        The list of quantiles to estimate.
    
    Returns:
    --------
    results : dict
        A dictionary containing the quantile estimates and confidence intervals.
    """
    results = {}
    for q in quantiles:
        res = model.fit(q=q)
        results[q] = {
            'coefficients': res.params,
            'confidence_intervals': res.conf_int()
        }
    return results

def compute_ci_qte(data, outcome, treatment, covariates=None):
    """
    Compute confidence intervals for QTE using the qte package.
    
    Parameters:
    -----------
    data : pandas.DataFrame
        The dataset containing the outcome variable, treatment indicator, and covariates.
    outcome : str
        The name of the outcome variable.
    treatment : str
        The name of the treatment indicator variable.
    covariates : list of str, optional
        A list of covariate names to include in the model.
    
    Returns:
    --------
    ci_results : dict
        A dictionary containing the confidence intervals for each quantile.
    """
    formula = f"{outcome} ~ {treatment}"
    if covariates:
        formula += " + " + " + ".join(covariates)
    
    formula = Formula(formula)
    r_data = pandas2ri.py2rpy(data)
    
    qte_results = qte.ci_qte(formula, data=r_data)
    
    ci_results = {
        'lower_bound': qte_results.rx2('lowerBound'),
        'upper_bound': qte_results.rx2('upperBound')
    }
    return ci_results


