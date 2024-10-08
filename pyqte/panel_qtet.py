from rpy2.robjects import r, Formula
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Activate the conversion of pandas DataFrames to R DataFrame
pandas2ri.activate()

# Import the 'qte' package from R
qte = importr('qte')

class PanelQTETEstimator:
    def __init__(self, formula, data, t, tmin1, tmin2, idname, tname, xformla=None, probs=None, se=True, iters=100, method="pscore"):
        self.formula = Formula(formula)
        self.data = pandas2ri.py2rpy(data)
        self.t = t
        self.tmin1 = tmin1
        self.tmin2 = tmin2
        self.idname = idname
        self.tname = tname
        self.xformla = Formula(xformla) if xformla else None
        
        # Process 'probs' as a numeric vector in R
        if probs is None:
            self.probs = r.seq(0.05, 0.95, by=0.05)
        else:
            if len(probs) == 3:
                self.probs = r.seq(probs[0], probs[1], by=probs[2])
            else:
                self.probs = r.FloatVector(probs)
        
        self.se = se
        self.iters = iters
        self.method = method

    def fit(self):
        # Ensure all necessary parameters are provided
        if self.formula is None or self.data is None or self.t is None or self.tmin1 is None or self.tmin2 is None or self.idname is None or self.tname is None:
            raise ValueError("All required parameters must be provided and cannot be None.")

        # Call the 'panel_qtet' function from the 'qte' package
        if self.xformla:
            self.result = qte.panel_qtet(
                formla=self.formula,
                t=self.t,
                tmin1=self.tmin1,
                tmin2=self.tmin2,
                idname=self.idname,
                tname=self.tname,
                data=self.data,
                xformla=self.xformla,
                probs=self.probs,
                se=self.se,
                iters=self.iters,
                method=self.method
            )
        else:
            self.result = qte.panel_qtet(
                formla=self.formula,
                t=self.t,
                tmin1=self.tmin1,
                tmin2=self.tmin2,
                idname=self.idname,
                tname=self.tname,
                data=self.data,
                probs=self.probs,
                se=self.se,
                iters=self.iters,
                method=self.method
            )
        return self.result

    def summary(self):
        summary = r.summary(self.result)
        print(summary)
        return summary
        
    def plot(self):
        """
        Plot the QTET estimation results, replacing invalid values with zero.
        """
        qte_results = self.result

        tau = np.linspace(0.05, 0.95, len(qte_results.rx2('qte')))
        qte = np.array(qte_results.rx2('qte'))
        lower_bound = np.array(qte_results.rx2('qte.lower')) if self.se else None
        upper_bound = np.array(qte_results.rx2('qte.upper')) if self.se else None

        # Replace invalid values (NaN) with zero
        qte = np.nan_to_num(qte, nan=0.0)
        if self.se:
            lower_bound = np.nan_to_num(lower_bound, nan=0.0)
            upper_bound = np.nan_to_num(upper_bound, nan=0.0)

        plt.figure(figsize=(10, 6))
        plt.plot(tau, qte, 'o-', label="QTE")

        if self.se:
            plt.fill_between(tau, lower_bound, upper_bound, color='gray', alpha=0.2, label="95% CI")
        
        plt.axhline(y=0, color='r', linestyle='--', label="No Effect Line")
        plt.xlabel('Quantiles')
        plt.ylabel('QTE Estimates')
        plt.title('Quantile Treatment Effects (Panel QTET)')
        plt.legend()
        plt.grid(True)
        plt.show()

    def get_results(self):
        """
        Return the results as a pandas DataFrame.
        """
        results_data = {
            'Quantile': np.linspace(0.05, 0.95, len(self.result.rx2('qte'))),
            'QTE': np.array(self.result.rx2('qte'))
        }
        
        # Include confidence intervals only if standard errors were calculated
        if self.se:
            results_data['QTE Lower Bound'] = np.array(self.result.rx2('qte.lower'))
            results_data['QTE Upper Bound'] = np.array(self.result.rx2('qte.upper'))

        results_df = pd.DataFrame(results_data)
        return results_df
