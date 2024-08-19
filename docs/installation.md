# Installation Guide

## Prerequisites

Before installing the `pyqte` package, ensure you have the following prerequisites installed:

- **Python 3.7 or higher**
- **R and Rpy2**: The package depends on `R` and `rpy2` to interface with the `qte` package in R. Ensure R is installed on your system, and the `rpy2` package is available.

### Installing R and Rpy2

1. **Install R**: Follow the instructions on [CRAN](https://cran.r-project.org/) to install R on your system.

2. **Install Rpy2**: You can install `rpy2` using pip:

```bash
pip install rpy2
```

Install the R qte package: Once R is installed, you can install the qte package by running the following command in your R console:

```R
install.packages("qte")
```

Installing the pyqte package
You can install the pyqte package from the source or via pip if it has been published on PyPI.

Installing from Source
Clone the repository:

```bash
git clone https://github.com/Daniel-Uhr/pyqte.git
cd pyqte
```

Install the package:

```bash
pip install .
```

Installing via pip
If pyqte is available on PyPI, you can install it directly using pip:

```bash
pip install pyqte
```

Verifying the Installation
After installation, you can verify that the package is working correctly by running the included tests:

```bash
pytest tests/
```

If all tests pass, your installation is successful, and you can start using the pyqte package.

Troubleshooting

If you encounter issues during installation, ensure that all prerequisites are correctly installed, especially the rpy2 package and the qte package in R. Refer to the documentation for these tools for troubleshooting tips.