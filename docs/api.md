# pyqte API Documentation

## Overview

The `pyqte` package provides a Python interface to estimate Quantile Treatment Effects (QTE) and related metrics using the underlying R `qte` package. This documentation provides an overview of the classes and functions available in `pyqte`.

## Classes

### `QTEEstimator`

**Description**: Estimates Quantile Treatment Effects (QTE).

**Parameters**:
- `data`: pandas.DataFrame - The dataset containing the outcome variable, treatment indicator, and covariates.
- `outcome`: str - The name of the outcome variable.
- `treatment`: str - The name of the treatment indicator variable.
- `quantiles`: list of float - The list of quantiles at which to estimate the treatment effect.

**Methods**:
- `estimate()`: Estimates the QTE for the specified quantiles.
- `plot_qte(qte_results)`: Plots the estimated QTEs.

### `QTETEstimator`

**Description**: Estimates Quantile Treatment Effects on the Treated (QTET) using panel data.

**Parameters**: 
- `formula`: str - The formula specifying the model.
- `t`: int - The treatment time period.
- `tmin1`: int - The pre-treatment time period.
- `tmin2`: int - The baseline time period.
- `idname`: str - The individual identifier.
- `tname`: str - The time period identifier.
- `data`: pandas.DataFrame - The dataset containing the variables.
- `probs`: list of float - The list of quantiles at which to estimate the treatment effect.
- `se`: bool - Whether to calculate standard errors.
- `iters`: int - The number of bootstrap iterations.
- `panel`: bool - Indicates if the data is panel data.

**Methods**:
- `estimate()`: Estimates the QTET for the specified quantiles.
- `plot_qtet(qtet_results)`: Plots the estimated QTETs.

### `QDiDEstimator`

**Description**: Estimates Quantile Treatment Effects using Difference-in-Differences (DiD).

**Parameters**:
- Similar to `QTETEstimator`.

**Methods**:
- `estimate()`: Estimates the DiD for the specified quantiles.
- `plot_qdid(qdid_results)`: Plots the estimated DiD results.

### `SpATT`

**Description**: Estimates Spatial Average Treatment Effects (SpATT).

**Parameters**:
- Similar to `QTEEstimator`, but adapted for spatial data.

**Methods**:
- `estimate()`: Estimates the SpATT for the specified quantiles.
- `plot_spatt(spatt_results)`: Plots the estimated SpATT results.

## Helper Functions

### `prepare_r_data`

**Description**: Converts a pandas DataFrame to an R dataframe.

**Parameters**:
- `dataframe`: pandas.DataFrame - The DataFrame to be converted.

**Returns**: R dataframe.

### `create_formula`

**Description**: Creates an R formula from dependent and independent variables.

**Parameters**:
- `dependent_var`: str - The name of the dependent variable.
- `independent_vars`: list of str - The list of independent variables.

**Returns**: rpy2.robjects.Formula.

### `calculate_summary_statistics`

**Description**: Calculates summary statistics for a pandas DataFrame.

**Parameters**:
- `dataframe`: pandas.DataFrame - The DataFrame for which to calculate summary statistics.

**Returns**: pandas.DataFrame containing the summary statistics.

### `bootstrap_sample`

**Description**: Generates bootstrap samples from a pandas DataFrame.

**Parameters**:
- `dataframe`: pandas.DataFrame - The DataFrame to bootstrap.
- `n`: int - The number of bootstrap samples to generate.

**Returns**: List of pandas.DataFrame containing the bootstrap samples.

### `calculate_confidence_intervals`

**Description**: Calculates confidence intervals for the mean of a pandas DataFrame.

**Parameters**:
- `data`: pandas.DataFrame - The data for which to calculate confidence intervals.
- `alpha`: float - The significance level for the confidence interval.

**Returns**: pandas.DataFrame containing the confidence intervals.

## Examples

Refer to the `examples.md` file for practical examples of how to use the `pyqte` package.

## Conclusion

This API documentation provides an overview of the classes and functions available in `pyqte`. For detailed use cases and advanced functionalities, refer to the examples and additional documentation files.

