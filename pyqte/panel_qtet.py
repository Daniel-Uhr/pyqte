from rpy2.robjects import r, Formula
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri

# Ativar a conversão automática de pandas DataFrame para R DataFrame
pandas2ri.activate()

# Importar o pacote qte do R
qte = importr('qte')

class PanelQTETEstimator:
    """
    PanelQTETEstimator estima o Efeito Quantílico do Tratamento sobre os Tratados (QTET)
    utilizando dados em painel com o pacote 'qte' do R via rpy2.
    """

    def __init__(self, formula, data, t, tmin1, tmin2, idname, tname, probs, se=False, iters=100, method="pscore"):
        self.formula = Formula(formula)
        self.data = pandas2ri.py2rpy(data)
        self.t = t
        self.tmin1 = tmin1
        self.tmin2 = tmin2
        self.idname = idname
        self.tname = tname
        self.probs = probs
        self.se = se
        self.iters = iters
        self.method = method
        self.result = None  # Para armazenar os resultados da estimativa

    def fit(self):
        """
        Estimar o QTET para os quantis especificados.
        """
        # Chamando a função 'panel_qtet' do pacote qte do R
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
        """
        Exibir um sumário dos resultados da estimativa QTET.
        """
        if self.result is None:
            raise ValueError("O modelo não foi ajustado. Por favor, execute o método 'fit()' primeiro.")
        summary = r['summary'](self.result)
        print(summary)
        return summary
     
    def plot(self):
        """
        Plota os resultados da estimativa QTET.
        """
        qte_results = self.result

        tau = np.linspace(0.05, 0.95, len(qte_results.rx2('qte')))
        qte = np.array(qte_results.rx2('qte'))
        lower_bound = np.array(qte_results.rx2('qte.lower'))
        upper_bound = np.array(qte_results.rx2('qte.upper'))

        plt.figure(figsize=(10, 6))
        plt.plot(tau, qte, 'o-', label="QTE")
        plt.fill_between(tau, lower_bound, upper_bound, color='gray', alpha=0.2, label="95% CI")
        plt.axhline(y=0, color='r', linestyle='--', label="No Effect Line")
        plt.xlabel('Quantiles')
        plt.ylabel('QTE Estimates')
        plt.title('Quantile Treatment Effects (Panel QTET)')
        plt.legend()
        plt.grid(True)
        plt.show()

