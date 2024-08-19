# pyqte

`pyqte` is a Python package designed to provide an interface for estimating Quantile Treatment Effects (QTE) using the R package `qte` via `rpy2`. This allows Python users to leverage the robust functionalities of the `qte` package without needing to directly interact with R.

## Installation

To install `pyqte`, you can clone the repository and install it using `pip`:

```bash
git clone https://github.com/Daniel-Uhr/pyqte.git
cd pyqte
pip install .
```

Make sure you have R installed along with the qte package and rpy2.

## Usage
Here’s a basic example of how to use pyqte to estimate Quantile Treatment Effects (QTE):

```
import pandas as pd
from pyqte.qte import QTEEstimator

# Load your data into a pandas DataFrame
df = pd.read_csv('path_to_your_data.csv')

# Initialize the QTE estimator
qte_estimator = QTEEstimator(data=df, outcome='outcome_column', treatment='treatment_column', quantiles=[0.1, 0.5, 0.9])

# Estimate QTE
qte_results = qte_estimator.estimate()

# Print the results
print(qte_results)

# Plot the QTE
qte_estimator.plot_qte(qte_results)
```
## Requirements

Python 3.6 or higher
R with the qte package installed
rpy2 for interfacing between Python and R
Other Python dependencies are listed in requirements.txt
License
This project is licensed under the MIT License. See the LICENSE file for details.

## Author
Daniel de Abreu Pereira Uhr - daniel.uhr@gmail.com

## Acknowledgments
I'd like to thank Brantly Callaway, the original author of the qte package in R (https://bcallaway11.github.io/qte/articles/R-QTEs.html), whose work this package relies on.
