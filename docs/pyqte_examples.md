# pyqte


## Introduction

The following examples demonstrate how to use the `pyqte` package to estimate various Quantile Treatment Effects (QTE) using the interface provided by the package. These examples assume that you have installed the `pyqte` package and its dependencies as described in the [Installation Guide](installation.md).


### Data
* *lalonde_exp* - Lalonde’s Experimental Dataset
  * The cross sectional verion of the experimental part of the lalonde dataset. 
* *lalonde_exp_panel* - Lalonde’s Panel Experimental Dataset
  * The panel verion of the experimental part of the lalonde dataset. 
* *lalonde_psid* - Lalonde’s Observational Dataset
  * The cross sectional verion of the observational part of the lalonde dataset.
* *lalonde_psid_panel* - Lalonde’s Experimental Dataset
  * The panel verion of the observational part of the lalonde dataset.


### QTE - Quantile Treatment Effect (QTEEstimator)

This method implements estimates the Quantile Treatment Effect (QTE) under a Conditional Independence Assumption (sometimes this is called Selection on Observables) developed in Firpo (2007). This method using propensity score re-weighting and minimizes a check function to compute the QTET. Standard errors (if requested) are computed using the bootstrap.


* Firpo, Sergio. “Efficient Semiparametric Estimation of Quantile Treatment Effects.” Econometrica 75.1, pp. 259-276, 2015.



#### Without Covariates


```python
from pyqte.qte import QTEEstimator
import pandas as pd

lalonde_psid = pd.read_csv("https://github.com/Daniel-Uhr/data/raw/main/lalonde_psid.csv")

qte_estimator_1 = QTEEstimator(
    formula='re78 ~ treat', 
    xformla=None,  
    data=lalonde_psid, 
    probs=[0.05, 0.95, 0.05],  
    se=True,                  
    iters=100                 
)

qte_estimator_1.fit()
qte_estimator_1.summary()
qte_estimator_1.plot()
qte_estimator_1.get_results()
```
   
#### With Covariates


```python
from pyqte.qte import QTEEstimator
import pandas as pd

# Carregar os dados
lalonde_psid = pd.read_csv("https://github.com/Daniel-Uhr/data/raw/main/lalonde_psid.csv")

# Inicialize o estimador QTE com covariáveis adicionais
qte_estimator_2 = QTEEstimator(
    formula='re78 ~ treat', 
    xformla='~ age + I(age^2) + education + black + hispanic + married + nodegree',  # Covariáveis adicionais
    data=lalonde_psid, 
    probs=[0.05, 0.95, 0.05],  # Quantis de interesse
    se=True,                  # Não calcular erros padrão
    iters=100                  # Número de iterações do bootstrap
)

qte_estimator_2.fit()
qte_estimator_2.summary()
qte_estimator_2.plot()
qte_estimator_2.get_results()
```


### QTET - Quantile Treatment Effect on the Treated (QTETEstimator)

This method implements estimates the Quantile Treatment Effect on the Treated (QTET) under a Conditional Independence Assumption (sometimes this is called Selection on Observables) developed in Firpo (2007). This method using propensity score re-weighting and minimizes a check function to compute the QTET. Standard errors (if requested) are computed using the bootstrap.

* Firpo, Sergio. “Efficient Semiparametric Estimation of Quantile Treatment Effects.” Econometrica 75.1, pp. 259-276, 2015.


```python
from pyqte.qtet import QTETEstimator
import pandas as pd

# Carregar os dados
lalonde_psid = pd.read_csv("https://github.com/Daniel-Uhr/data/raw/main/lalonde_psid.csv")

# Inicializar o estimador QTET sem covariáveis
qtet_estimator_1 = QTETEstimator(
    formula='re78 ~ treat', 
    xformla=None,  # Sem covariáveis adicionais
    data=lalonde_psid, 
    probs=[0.05, 0.95, 0.05],   # Quantis de interesse
    se=True,                    # Não calcular erros padrão
    iters=10                    # Número de iterações do bootstrap
)

qtet_estimator_1.fit()
qtet_estimator_1.summary()
qtet_estimator_1.plot()
qtet_estimator_1.get_results()
```



```python
from pyqte.qtet import QTETEstimator
import pandas as pd

# Carregar os dados
lalonde_psid = pd.read_csv("https://github.com/Daniel-Uhr/data/raw/main/lalonde_psid.csv")

# Inicializar o estimador QTET com covariáveis
qtet_estimator_2 = QTETEstimator(
    formula='re78 ~ treat', 
    xformla='~ age + I(age**2) + education + black + hispanic + married + nodegree', 
    data=lalonde_psid, 
    probs=[0.05, 0.95, 0.05],  # Quantis de interesse
    se=True,                  # Não calcular erros padrão
    iters=100                  # Número de iterações do bootstrap
)

qtet_estimator_2.fit()
qtet_estimator_2.summary()
qtet_estimator_2.plot()
qtet_estimator_2.get_results()
```


### CIC - Changes-in-Changes (CiCEstimator)

CiCEstimator computes the Quantile Treatment Effect on the Treated (QTET) using the method of Athey and Imbens (2006). CiC is a Difference in Differences type method. It requires having two periods of data that can be either repeated cross sections or panel data. The method can accommodate conditioning on covariates though it does so in a restrictive way: It specifies a linear model for outcomes conditional on group-time dummies and covariates. Then, after residualizing (see details in Athey and Imbens (2006)), it computes the Change in Changes model based on these quasi-residuals.

* Athey, Susan andGuidoImbens. “Identification andInference in Nonlinear Difference-in-Differences Models.” Econometrica 74.2, pp. 431-497, 2006.


```python
from pyqte.cic import CiCEstimator
import pandas as pd

# Carregar os dados
lalonde_psid_panel = pd.read_csv("https://github.com/Daniel-Uhr/data/raw/main/lalonde_psid_panel.csv")

# Inicialize o estimador CiC com as mesmas configurações do exemplo em R
cic_estimator = CiCEstimator(
    formula='re ~ treat',
    data=lalonde_psid_panel,
    t=1978,
    tmin1=1975,
    tname='year',
    idname='id',
    xformla='~ age + I(age**2) + education + black + hispanic + married + nodegree',
    se=True,  # Não calcular erros padrão
    probs=[0.05, 0.95, 0.05],  # Quantis de interesse
    iters=10                  # Número de iterações do bootstrap
)

cic_estimator.fit()
summary_cic = cic_estimator.summary()
cic_estimator.plot()
cic_estimator.get_results()
```


### DDiD2 (DDiD2Estimator)

DDiD2Estimator computes the Quantile Treatment Effect on the Treated (QTET) using the method of Callaway, Li, and Oka (2015).


#### Without Covariates

```python
from pyqte.ddid2 import DDID2Estimator
import pandas as pd

lalonde_psid_panel = pd.read_csv("https://github.com/Daniel-Uhr/data/raw/main/lalonde_psid_panel.csv")

# Inicializar o estimador DDID2 com as mesmas configurações do exemplo em R
ddid2_estimator_1 = DDID2Estimator(
    formula='re ~ treat',
    data=lalonde_psid_panel,
    t=1978,
    tmin1=1975,
    tname='year',
    idname='id',
    se=True,
    probs=[0.05, 0.95, 0.05],
    iters=100
)

ddid2_estimator_1.fit()
ddid2_estimator_1.summary()
ddid2_estimator_1.plot()
ddid2_estimator_1.get_results()

```

#### With Covariates


```python
from pyqte.ddid2 import DDID2Estimator
import pandas as pd

# Carregar os dados
lalonde_psid_panel = pd.read_csv("https://github.com/Daniel-Uhr/data/raw/main/lalonde_psid_panel.csv")

# Inicializar o estimador DDID2 com fórmula e covariáveis
ddid2_estimator_2 = DDID2Estimator(
    formula='re ~ treat',
    xformla='~ age + I(age**2) + education + black + hispanic + married + nodegree',
    data=lalonde_psid_panel,
    t=1978,
    tmin1=1975,
    tname='year',
    idname='id',
    se=True,
    probs=[0.05, 0.95, 0.05],
    iters=10
)

ddid2_estimator_2.fit()
ddid2_estimator_2.summary()
ddid2_estimator_2.plot()
ddid2_estimator_2.get_results()
```

### MDID (MDiDEstimator)

MDiDEstimator is a Difference in Differences type method for computing the QTET. The method can accommodate conditioning on covariates though it does so in a restrictive way: It specifies a linear model for outcomes conditional on group-time dummies and covariates. Then, after residualizing (see details in Athey and Imbens (2006)), it computes the Change in Changes model based on these quasi-residuals.

* Athey, Susan andGuidoImbens. “Identification andInference in Nonlinear Difference-in-Differences Models.” Econometrica 74.2, pp. 431-497, 2006. 
* Thuysbaert, Bram. “Distributional Comparisons in Difference in Differences Models.” Working Paper, 2007.


```python
from pyqte.mdid import MDiDEstimator
import pandas as pd

# Carregar os dados
lalonde_psid_panel = pd.read_csv("https://github.com/Daniel-Uhr/data/raw/main/lalonde_psid_panel.csv")

# Inicializar o estimador MDiD com covariáveis
mdid_estimator = MDiDEstimator(
    formula='re ~ treat',
    xformla='~ age + I(age**2) + education + black + hispanic + married + nodegree',
    data=lalonde_psid_panel,
    t=1978,
    tmin1=1975,
    tname='year',
    idname='id',
    se=True,
    probs=[0.05, 0.95, 0.05]
)

mdid_estimator.fit()
mdid_estimator.summary()
mdid_estimator.plot()
mdid_estimator.get_results()
```


### Panel QTET - Panel Quantile Treatment Effect on the Treated (PanelQTETEstimator)

PanelQTETEstimator computes the Quantile Treatment Effect on the Treated (QTET) using the method of Callaway and Li (2015). This method should be used when the researcher wants to invoke a Difference in Differences assumption to identify the QTET. Relative to the other Difference in Differences methods available in the qte package, this method’s assumptions are more intuitively similar to the identifying assumptions used in identifying the Average Treatment Effect on the Treated (ATT). Additionally, this method can accommodate covariates in a more flexible way than the other Difference in Differences methods available. In order to accommodate covariates, the user should specify a vector x of covariate names. The user also may specify a method for estimating the propensity score. The default is logit. panel.qtet can only be used in some situations, however. The method requires three periods of panel data where individuals are not treated until the last period. The data should be formatted as a panel; the names of columns containing time periods and ids for each cross sectional unit need to be passed to the method.

* Callaway, Brantly and Tong Li. “Quantile Treatment Effects in Difference in Differences Models with Panel Data.” https://onlinelibrary.wiley.com/doi/full/10.3982/QE935.


```python
# Run the PanelQTETEstimator on the experimental data with no covariates
from pyqte.panel_qtet import PanelQTETEstimator
import pandas as pd

lalonde_psid_panel = pd.read_csv("https://github.com/Daniel-Uhr/data/raw/main/lalonde_psid_panel.csv")

pq1 = PanelQTETEstimator(
    formula='re ~ treat',
    data=lalonde_psid_panel,
    t=1978,
    tmin1=1975,
    tmin2=1974,
    tname='year',
    idname='id',
    se=True,
    probs=[0.05, 0.95, 0.05]
)

pq1.fit()
pq1.summary()
pq1.plot()
pq1.get_results()
```


```python
#Run the panel.qtet method on the observational data with no covariates
from pyqte.panel_qtet import PanelQTETEstimator
import pandas as pd

lalonde_psid_panel = pd.read_csv("https://github.com/Daniel-Uhr/data/raw/main/lalonde_psid_panel.csv")

pq2 = PanelQTETEstimator(
    formula='re ~ treat',
    data=lalonde_psid_panel,
    t=1978,
    tmin1=1975,
    tmin2=1974,
    tname='year',
    idname='id',
    se=True,  # Não calcular erros padrão
    probs=[0.05, 0.95, 0.05]  # Quantis de interesse
)

pq2.fit()
pq2.summary()
pq2.plot()
pq2.get_results()
```


```python
# Run the panel.qtet method on the observational data conditioning on age, education, black, hispanic, married, and nodegree. The propensity score will be estimated using the default logit method. 
from pyqte.panel_qtet import PanelQTETEstimator
import pandas as pd

lalonde_psid_panel = pd.read_csv("https://github.com/Daniel-Uhr/data/raw/main/lalonde_psid_panel.csv")

pq3 = PanelQTETEstimator(
    formula='re ~ treat',
    xformla='~ age + I(age**2) + education + black + hispanic + married + nodegree',  # Covariáveis
    data=lalonde_psid_panel,
    t=1978,
    tmin1=1975,
    tmin2=1974,
    tname='year',
    idname='id',
    se=True,                           
    iters=10,
    method="pscore",                    # propensity score (logit)
    probs=[0.05, 0.95, 0.05]            
)

pq3.fit()
pq3.summary()
pq3.plot()
pq3.get_results()
```


```python
# Covariates and Quantile Regression (qr)
from pyqte.panel_qtet import PanelQTETEstimator
import pandas as pd

lalonde_psid_panel = pd.read_csv("https://github.com/Daniel-Uhr/data/raw/main/lalonde_psid_panel.csv")

pq4 = PanelQTETEstimator(
    formula='re ~ treat',
    xformla='~ age + I(age**2) + education + black + hispanic + married + nodegree',  # Covariáveis
    data=lalonde_psid_panel,
    t=1978,
    tmin1=1975,
    tmin2=1974,
    tname='year',
    idname='id',
    se=True,  
    iters=10,
    method="qr",                        # Quantile Regression (qr)
    probs=[0.05, 0.95, 0.05]  
)

pq4.fit()
pq4.summary()
pq4.plot()
pq4.get_results()
```


### Quantile Difference-in-Differences (QDiD - QDiDEstimator)

QDiDEstimator is a Difference in Differences type method for computing the QTET. The method can accommodate conditioning on covariates though it does so in a restrictive way: It specifies a linear model for outcomes conditional on group-time dummies and covariates. Then, after residualizing (see details in Athey and Imbens (2006)), it computes the Change in Changes model based on these quasi-residuals.

* Athey, Susan andGuidoImbens. “Identification andInference in Nonlinear Difference-in-Differences Models.” Econometrica 74.2, pp. 431-497, 2006.


```python
## Run the Quantile Difference in Differences method conditioning on age, education, black, hispanic, married, and nodegree.
from pyqte.qdid import QDiDEstimator
import pandas as pd

lalonde_psid_panel = pd.read_csv("https://github.com/Daniel-Uhr/data/raw/main/lalonde_psid_panel.csv")

qdid_estimator = QDiDEstimator(
    formula='re ~ treat',
    xformla='~ age + I(age**2) + education + black + hispanic + married + nodegree',
    data=lalonde_psid_panel,
    t=1978,
    tmin1=1975,
    tname='year',
    idname='id',
    se=True,  # Não calcular erros padrão
    probs=[0.05, 0.95, 0.05],  # Quantis de interesse
    iters=10
)

qdid_estimator.fit()
qdid_estimator.summary()
qdid_estimator.plot()
qdid_estimator.get_results()
```


##### SpATT

* Abadie, Alberto. 2005. “Semiparametric Difference-in-Differences Estimators.” The Review of Economic Studies 72 (1): 1–19.


```python
from pyqte.spatt import SpATTEstimator
import pandas as pd

lalonde_psid_panel = pd.read_csv("https://github.com/Daniel-Uhr/data/raw/main/lalonde_psid_panel.csv")

# Inicializar o estimador SpATT sem covariáveis
spatt_estimator = SpATTEstimator(
    formula='re ~ treat',    # Fórmula especificando o resultado e o tratamento
    data=lalonde_psid_panel, # Conjunto de dados
    t=1978,                  # Período após o tratamento
    tmin1=1975,              # Período antes do tratamento
    tname='year',            # Nome da coluna que contém os períodos de tempo
    xformla=None,            # Nenhuma covariável adicional (x=NULL em R)
    idname='id',             # Nome da coluna que contém os identificadores únicos
    se=False                 # Não calcular erros padrão
)

spatt_estimator.fit()
spatt_estimator.summary()
```
