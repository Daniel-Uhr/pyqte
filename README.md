# pyqte

`pyqte` is a Python package designed to provide an interface for estimating Quantile Treatment Effects (QTE) using the R package `qte` via `rpy2`. This allows Python users to leverage the robust functionalities of the `qte` package without needing to directly interact with R.

## Installation

To install `pyqte`, you can clone the repository and install it using `pip`:

```bash
git clone https://github.com/Daniel-Uhr/pyqte.git
cd pyqte
pip install .
```
or,

```bash
pip install git+https://github.com/Daniel-Uhr/pyqte.git
```

Make sure you have R installed along with the qte package and rpy2.

## Usage
Here’s a basic example of how to use pyqte to estimate Quantile Treatment Effects (QTE):

```
from pyqte.qte import QTEEstimator
import pandas as pd

# Load your data into a pandas DataFrame
lalonde_psid = pd.read_csv("https://github.com/Daniel-Uhr/data/raw/main/lalonde_psid.csv")

# Initialize the QTE estimator
qte_estimator_1 = QTEEstimator(
    formula='re78 ~ treat', 
    xformla=None,  
    data=lalonde_psid, 
    probs=[0.05, 0.95, 0.05],  
    se=True,                  
    iters=100                 
)

# Estimate QTE
qte_estimator_1.fit()

# Summary the results
qte_estimator_1.summary()

# Plot the QTE
qte_estimator_1.plot()

# Generate a data-frame with results
res_1 = qte_estimator_1.get_results()
```
## Requirements

Python 3.6 or higher
R with the qte package installed
rpy2 for interfacing between Python and R
Other Python dependencies are listed in requirements.txt

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Author
Daniel de Abreu Pereira Uhr - daniel.uhr@gmail.com

## Acknowledgments
I'd like to thank Brantly Callaway, the original author of the qte package in R (https://github.com/bcallaway11/qte), whose work this package relies on.
