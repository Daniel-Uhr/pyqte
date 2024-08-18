import numpy as np
import pandas as pd
from scipy import stats

def calculate_quantiles(data, probs):
    """
    Calculate quantiles for the given data and specified probabilities.
    
    Parameters:
    -----------
    data : array-like
        The data for which quantiles need to be calculated.
    probs : list or array-like
        A list or array of probabilities at which to calculate quantiles.
    
    Returns:
    --------
    quantiles : numpy.ndarray
        The calculated quantiles corresponding to the specified probabilities.
    """
    quantiles = np.quantile(data, probs)
    return quantiles

def bootstrap(data, func, iters=1000):
    """
    Perform bootstrap resampling on the data to estimate the sampling distribution of a statistic.
    
    Parameters:
    -----------
    data : array-like
        The data to bootstrap.
    func : function
        The statistic function to apply to the bootstrap samples.
    iters : int, optional
        The number of bootstrap iterations. Default is 1000.
    
    Returns:
    --------
    bootstrap_estimates : numpy.ndarray
        An array of the bootstrap estimates for each iteration.
    """
    n = len(data)
    bootstrap_estimates = np.zeros(iters)
    
    for i in range(iters):
        sample = np.random.choice(data, size=n, replace=True)
        bootstrap_estimates[i] = func(sample)
    
    return bootstrap_estimates

def calculate_confidence_interval(estimates, alpha=0.05):
    """
    Calculate a confidence interval for the bootstrap estimates.
    
    Parameters:
    -----------
    estimates : array-like
        The bootstrap estimates.
    alpha : float, optional
        The significance level for the confidence interval. Default is 0.05.
    
    Returns:
    --------
    ci_lower : float
        The lower bound of the confidence interval.
    ci_upper : float
        The upper bound of the confidence interval.
    """
    lower_bound = np.percentile(estimates, 100 * (alpha / 2))
    upper_bound = np.percentile(estimates, 100 * (1 - alpha / 2))
    return lower_bound, upper_bound

def weighted_quantile(values, quantiles, sample_weight=None, values_sorted=False, old_style=False):
    """
    Compute the weighted quantile of a given data set.
    
    Parameters:
    -----------
    values : array-like
        The data values.
    quantiles : array-like
        The quantiles to compute (should all be in the range [0, 1]).
    sample_weight : array-like, optional
        The weights of the data values. If None, equal weights are assumed.
    values_sorted : bool, optional
        If True, the values array is assumed to be sorted.
    old_style : bool, optional
        If True, use the "1-liner" method for computing quantiles, which is slightly less accurate.
    
    Returns:
    --------
    quantiles : numpy.ndarray
        The computed quantiles.
    """
    values = np.array(values)
    quantiles = np.array(quantiles)
    
    if sample_weight is None:
        sample_weight = np.ones(len(values))
    sample_weight = np.array(sample_weight)
    
    assert np.all(quantiles >= 0) and np.all(quantiles <= 1), "Quantiles should be in the range [0, 1]"
    
    if not values_sorted:
        sorter = np.argsort(values)
        values = values[sorter]
        sample_weight = sample_weight[sorter]
    
    weighted_quantiles = np.cumsum(sample_weight) - 0.5 * sample_weight
    weighted_quantiles /= np.sum(sample_weight)
    
    if old_style:
        return np.interp(quantiles, weighted_quantiles, values)
    else:
        return np.interp(quantiles, weighted_quantiles, values, left=values[0], right=values[-1])
