from rpy2.robjects import r, Formula
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri, FloatVector
import pandas as pd

# Activate the pandas conversion for rpy2
pandas2ri.activate()

# Import the R 'qte' package
qte = importr('qte')

class SpATT_Estimator:
    """
    SpATT_Estimator is used to estimate Spatial Average Treatment on the Treated (SpATT)
    effects using the R 'qte' package via rpy2.
    
    Attributes:
    -----------
    formula : str
        The formula representing the relationship between the dependent and independent variables.
    xformla : str or None
        An optional formula for additional covariates to adjust for.
    data : pandas.DataFrame
        The dataset containing the variables used in the formula.
    t : int
        The time period after treatment.
    tmin1 : int
        The time period before treatment.
    tname : str
        The name of the column representing the time periods.
    w : array-like or None
        An optional vector of sampling weights.
    panel : bool
        Whether the data is panel or repeated cross sections.
    idname : str or None
        The name of the column representing the unique identifier for each unit.
    iters : int
        The number of bootstrap iterations to compute standard errors.
    alp : float
        The significance level used for constructing bootstrap confidence intervals.
    method : str
        The method for estimating the propensity score when covariates are included (e.g., "logit").
    plot : bool
        Whether or not to plot the estimated QTET.
    se : bool
        Whether to compute standard errors.
    retEachIter : bool
        Whether or not to return results from each iteration of the bootstrap procedure.
    seedvec : array-like or None
        Optional value to set a random seed, can be used in conjunction with bootstrapping standard errors.
    pl : bool
        Whether or not to compute bootstrap errors in parallel.
    cores : int or None
        The number of cores to use if computing bootstrap standard errors in parallel.
    """

    def __init__(self, formula, data, t, tmin1, tname, xformla=None, w=None, panel=False, idname=None, 
                 iters=100, alp=0.05, method="logit", plot=False, se=True, 
                 retEachIter=False, seedvec=None, pl=False, cores=2):
        self.formula = Formula(formula)
        self.data = pandas2ri.py2rpy(data)
        self.t = t
        self.tmin1 = tmin1
        self.tname = tname
        self.xformla = Formula(xformla) if xformla else None
        self.w = FloatVector(w) if w is not None else None
        self.panel = panel
        self.idname = idname
        self.iters = iters
        self.alp = alp
        self.method = method
        self.plot = plot
        self.se = se
        self.retEachIter = retEachIter
        self.seedvec = FloatVector(seedvec) if seedvec is not None else None
        self.pl = pl
        self.cores = cores

    def estimate(self):
        """
        Estimate the Spatial Average Treatment on the Treated (SpATT) effect.
        
        Returns:
        --------
        result : R object
            The result of the SpATT estimation, which can be further processed or summarized.
        """
        result = qte.spatt(
            formla=self.formula,
            xformla=self.xformla,
            t=self.t,
            tmin1=self.tmin1,
            tname=self.tname,
            data=self.data,
            w=self.w,
            panel=self.panel,
            idname=self.idname,
            iters=self.iters,
            alp=self.alp,
            method=self.method,
            plot=self.plot,
            se=self.se,
            retEachIter=self.retEachIter,
            seedvec=self.seedvec,
            pl=self.pl,
            cores=self.cores
        )
        return result

    def summary(self, result):
        """
        Print a summary of the SpATT estimation result.
        
        Parameters:
        -----------
        result : R object
            The result from the SpATT estimation to be summarized.
        """
        return r['summary'](result)
    
    def plot(self, result):
        """
        Plot the SpATT estimation results.
        
        Parameters:
        -----------
        result : R object
            The result from the SpATT estimation to be plotted.
        """
        r['plot'](result)

    def get_results(self, result):
        """
        Extract the results from the SpATT estimation and return as a pandas DataFrame.
        
        Parameters:
        -----------
        result : R object
            The result from the SpATT estimation from which to extract data.
        
        Returns:
        --------
        results_df : pandas.DataFrame
            A DataFrame containing the extracted results.
        """
        qte_values = np.array(result.rx2('qte'))
        probs = np.array(result.rx2('probs'))

        if self.se:
            lower_bound = np.array(result.rx2('qte.lower'))
            upper_bound = np.array(result.rx2('qte.upper'))
            results_df = pd.DataFrame({
                'Quantile': probs,
                'QTE': qte_values,
                'QTE Lower Bound': lower_bound,
                'QTE Upper Bound': upper_bound
            })
        else:
            results_df = pd.DataFrame({
                'Quantile': probs,
                'QTE': qte_values
            })
        
        return results_df


