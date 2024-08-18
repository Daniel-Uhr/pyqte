# pyqte

`pyqte` is a Python package designed to estimate Quantile Treatment Effects (QTE) and related estimators for causal inference in observational studies, particularly in economics. This package provides several methods commonly used in econometrics to analyze the distributional impact of treatments, including the Quantile Treatment Effects on the Treated (QTET) under different assumptions.

## Features

- **QTE**: Estimate Quantile Treatment Effects for cases where treatment is randomly assigned or conditional on covariates.
- **QTET**: Estimate Quantile Treatment Effects on the Treated, using various methods like difference-in-differences.
- **QDiD**: Quantile Difference-in-Differences estimator.
- **DDID2**: Another variant of the Difference-in-Differences estimator.
- **CiC**: Change-in-Changes estimator.
- **Panel Data Support**: Methods for working with panel data, including checks and setup functions.

## Installation

To install the package, you can clone the repository and install it using `pip`:

```bash
git clone https://github.com/yourusername/pyqte.git
cd pyqte
pip install .
```

Usage
Here's an example of how to use the pyqte package:

```python
import pyqte as pq

# Example usage of the QTE estimator
result = pq.qte(formula='outcome ~ treatment', data=df, probs=[0.25, 0.5, 0.75])
print(result.summary())

# Plotting the QTE results
result.plot()
```	

Requirements
Python 3.x
numpy
pandas
statsmodels
matplotlib
These dependencies are listed in the requirements.txt file and will be installed automatically when you install the package.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Authors
Daniel de Abreu Pereira Uhr - Initial work and implementation
Brantly Callaway - Original R package implementation

Acknowledgments
This package is inspired by the R package qte and aims to provide similar functionality in Python. Special thanks to Brantly Callaway for his work on the original R package.


This `README.md` provides an overview of the package, installation instructions, usage examples, and credits. It’s a starting point and can be further customized to better fit your project needs.
