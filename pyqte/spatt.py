import numpy as np
import pandas as pd
from scipy import sparse
from scipy.spatial import distance_matrix

def compute_spatial_weights(data, coords, bandwidth=1.0, kernel='gaussian'):
    """
    Compute spatial weights for the given data based on coordinates.
    
    Parameters:
    -----------
    data : pandas.DataFrame
        The input data containing the variables of interest.
    coords : pandas.DataFrame
        The coordinates associated with each observation in `data`.
    bandwidth : float, optional
        The bandwidth parameter for the kernel function. Default is 1.0.
    kernel : str, optional
        The kernel function to use for computing weights. Options are 'gaussian', 'exponential', etc.
    
    Returns:
    --------
    weights_matrix : scipy.sparse.csr_matrix
        A sparse matrix containing the spatial weights.
    """
    distances = distance_matrix(coords.values, coords.values)
    
    if kernel == 'gaussian':
        weights = np.exp(-0.5 * (distances / bandwidth) ** 2)
    elif kernel == 'exponential':
        weights = np.exp(-distances / bandwidth)
    else:
        raise ValueError(f"Unknown kernel: {kernel}")
    
    # Normalize the weights so that rows sum to 1
    row_sums = weights.sum(axis=1)
    weights = weights / row_sums[:, np.newaxis]
    
    return sparse.csr_matrix(weights)

def spatt_model(y, X, W, lamb=0.5):
    """
    Fit a Spatial Autoregressive Treatment Effect (SPATT) model.
    
    Parameters:
    -----------
    y : numpy.ndarray
        The dependent variable.
    X : numpy.ndarray
        The independent variables.
    W : scipy.sparse.csr_matrix
        The spatial weights matrix.
    lamb : float, optional
        The spatial autoregressive parameter. Default is 0.5.
    
    Returns:
    --------
    results : dict
        A dictionary containing model parameters, residuals, and fit statistics.
    """
    n = len(y)
    I = sparse.eye(n)
    
    # Spatial lag of y
    Wy = W.dot(y)
    
    # Spatial lag of X
    WX = W.dot(X)
    
    # Spatial autoregressive model
    y_star = y - lamb * Wy
    X_star = X - lamb * WX
    
    # Ordinary least squares estimation
    beta_hat = np.linalg.inv(X_star.T.dot(X_star)).dot(X_star.T).dot(y_star)
    residuals = y_star - X_star.dot(beta_hat)
    sigma2 = (residuals.T.dot(residuals)) / (n - X.shape[1])
    
    # Returning results
    results = {
        'beta': beta_hat,
        'lambda': lamb,
        'sigma2': sigma2,
        'residuals': residuals
    }
    
    return results

def spatial_effects(W, treatment_effects):
    """
    Compute spatial effects given a spatial weights matrix and treatment effects.
    
    Parameters:
    -----------
    W : scipy.sparse.csr_matrix
        The spatial weights matrix.
    treatment_effects : numpy.ndarray
        The estimated treatment effects.
    
    Returns:
    --------
    spatial_effects : numpy.ndarray
        The spatial effects adjusted for neighborhood influence.
    """
    return W.dot(treatment_effects)

def summary_spatt(model_results):
    """
    Generate a summary of the SPATT model results.
    
    Parameters:
    -----------
    model_results : dict
        The results from the SPATT model fitting.
    
    Returns:
    --------
    summary : str
        A formatted summary of the model results.
    """
    beta = model_results['beta']
    lamb = model_results['lambda']
    sigma2 = model_results['sigma2']
    
    summary = f"Spatial Autoregressive Treatment Effect Model Summary\n"
    summary += f"--------------------------------------------\n"
    summary += f"Coefficients (Beta):\n"
    summary += "\n".join([f"  Beta[{i}]: {b}" for i, b in enumerate(beta)])
    summary += f"\nSpatial Autoregressive Parameter (Lambda): {lamb}\n"
    summary += f"Residual Variance (Sigma^2): {sigma2}\n"
    
    return summary
