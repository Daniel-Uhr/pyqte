import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def MDiD(y, X, D, T, group_name, time_name):
    """
    Implementa o estimador Mean Difference in Differences (MDiD).
    
    Parâmetros:
    -----------
    y : numpy.ndarray
        A variável dependente (outcome).
    X : numpy.ndarray
        As variáveis independentes (covariates).
    D : numpy.ndarray
        Indicador de tratamento (treat).
    T : numpy.ndarray
        Indicador de tempo (time).
    group_name : str
        Nome da coluna que indica o grupo (tratado ou controle).
    time_name : str
        Nome da coluna que indica o tempo (antes ou depois do tratamento).
    
    Retorna:
    --------
    results : dict
        Um dicionário contendo os coeficientes estimados, o erro padrão,
        e outras estatísticas de ajuste.
    """
    # Subdefinir os dados
    treated = (D == 1)
    control = (D == 0)
    post = (T == 1)
    pre = (T == 0)
    
    # Criar variáveis de interação
    interaction = D * T
    X_interaction = np.column_stack([X, interaction])
    
    # Regressão nos grupos e períodos
    model = LinearRegression().fit(X_interaction, y)
    beta = model.coef_
    intercept = model.intercept_
    
    # Previsões e cálculo do efeito médio do tratamento
    treated_post = X[treated & post]
    control_post = X[control & post]
    treated_pre = X[treated & pre]
    control_pre = X[control & pre]
    
    treated_effect = np.mean(y[treated & post]) - np.mean(y[treated & pre])
    control_effect = np.mean(y[control & post]) - np.mean(y[control & pre])
    
    MDiD_effect = treated_effect - control_effect
    
    # Estatísticas de ajuste
    residuals = y - model.predict(X_interaction)
    rss = np.sum(residuals ** 2)
    tss = np.sum((y - np.mean(y)) ** 2)
    r_squared = 1 - rss / tss
    
    # Retornando resultados
    results = {
        'beta': beta,
        'intercept': intercept,
        'MDiD_effect': MDiD_effect,
        'r_squared': r_squared,
        'residuals': residuals,
        'rss': rss,
        'tss': tss
    }
    
    return results

def summary_MDiD(model_results):
    """
    Gera um resumo dos resultados do modelo MDiD.
    
    Parâmetros:
    -----------
    model_results : dict
        Os resultados do ajuste do modelo MDiD.
    
    Retorna:
    --------
    summary : str
        Um resumo formatado dos resultados do modelo.
    """
    beta = model_results['beta']
    intercept = model_results['intercept']
    MDiD_effect = model_results['MDiD_effect']
    r_squared = model_results['r_squared']
    
    summary = f"Mean Difference in Differences (MDiD) Model Summary\n"
    summary += f"----------------------------------------------------\n"
    summary += f"Intercept: {intercept}\n"
    summary += f"Coefficients (Beta):\n"
    summary += "\n".join([f"  Beta[{i}]: {b}" for i, b in enumerate(beta)])
    summary += f"\nMean DiD Effect: {MDiD_effect}\n"
    summary += f"R-squared: {r_squared}\n"
    
    return summary

