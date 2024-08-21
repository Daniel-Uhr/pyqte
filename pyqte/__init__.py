from .qte import QTEEstimator
from .qtet import QTETEstimator
from .qdid import QDiDEstimator
from .cic import CiCEstimator
from .mdid import MDiDEstimator
from .spatt import SpATTEstimator
from .ddid2 import DDID2Estimator 
from .helper_functions import compute_ci_qte, compute_panel_qtet, compute_diff_se, plot_qte

__all__ = [
    'QTEEstimator',
    'QTETEstimator',
    'QDiDEstimator',
    'CiCEstimator',
    'MDiDEstimator',
    'SpATTEstimator',
    'DDID2Estimator',  # Incluindo DDID2Estimator
    'compute_ci_qte',
    'compute_panel_qtet',
    'compute_diff_se',
    'plot_qte',
]

# Metadata
__version__ = '0.1.0'
__author__ = 'Daniel de Abreu Pereira Uhr'
__email__ = 'daniel.uhr@gmail.com'
