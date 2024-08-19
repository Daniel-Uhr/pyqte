# Examples

## Introduction

The following examples demonstrate how to use the `pyqte` package to estimate various Quantile Treatment Effects (QTE) using the interface provided by the package. These examples assume that you have installed the `pyqte` package and its dependencies as described in the [Installation Guide](installation.md).

## Example 1: Estimating Basic QTE

This example demonstrates how to estimate the basic Quantile Treatment Effect (QTE) using the `QTEEstimator`.

```python
import pandas as pd
from pyqte.qte import QTEEstimator

# Load example data
data = pd.read_csv('path_to_your_data.csv')

# Define the outcome and treatment variables
outcome = 'outcome_variable'
treatment = 'treatment_variable'

# Create the estimator instance
qte_estimator = QTEEstimator(data=data, outcome=outcome, treatment=treatment, quantiles=[0.1, 0.5, 0.9])

# Estimate the QTE
qte_results = qte_estimator.estimate()

# Print the results
print(qte_results)

# Plot the results
qte_estimator.plot_qte(qte_results)
```

## Example 2: Estimating QTE with Panel Data
This example demonstrates how to estimate the Quantile Treatment Effect on the Treated (QTET) using panel data with the QTETEstimator.

```python	
from pyqte.qtet import QTETEstimator

# Define the necessary variables
formula = 'outcome ~ treatment'
params = {
    'formula': formula,
    't': 1978,
    'tmin1': 1975,
    'tmin2': 1974,
    'idname': 'id',
    'tname': 'year',
    'data': data,
    'probs': [0.1, 0.5, 0.9],
    'se': True,
    'iters': 100,
    'panel': True
}

# Create the estimator instance
qtet_estimator = QTETEstimator(**params)

# Estimate the QTET
qtet_results = qtet_estimator.estimate()

# Print the results
print(qtet_results)

# Plot the results
qtet_estimator.plot_qtet(qtet_results)
```
## Example 3: Estimating Difference-in-Differences (DID)
This example demonstrates how to estimate the Difference-in-Differences (DiD) using the QDiDEstimator.

```python
from pyqte.qdid import QDiDEstimator

# Define the necessary variables
formula = 'outcome ~ treatment'
params = {
    'formula': formula,
    't': 1978,
    'tmin1': 1975,
    'idname': 'id',
    'tname': 'year',
    'data': data,
    'probs': [0.1, 0.5, 0.9],
    'se': True,
    'iters': 100,
    'panel': True
}

# Create the estimator instance
qdid_estimator = QDiDEstimator(**params)

# Estimate the DiD
qdid_results = qdid_estimator.estimate()

# Print the results
print(qdid_results)

# Plot the results
qdid_estimator.plot_qdid(qdid_results)
```

## Example 4: Using Helper Functions
This example demonstrates how to use the helper functions provided in pyqte for data preparation and analysis.

```python
from pyqte.helper_functions import prepare_r_data, calculate_summary_statistics

# Prepare data for use with R
r_data = prepare_r_data(data)

# Calculate summary statistics
summary_stats = calculate_summary_statistics(data)
print(summary_stats)
```
## Conclusion

These examples provide a starting point for using the pyqte package. The package is flexible and can be adapted for various research needs, particularly in the field of econometrics. For more detailed use cases and advanced functionalities, refer to the full documentation.

This document provides practical examples of how to use the `pyqte` package to estimate Quantile Treatment Effects and other related metrics using Python. Each example illustrates the application of different estimators within the package, showcasing their functionality and output.
