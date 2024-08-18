"""
pyqte - A Python package for Quantile Treatment Effects

This package provides various tools for estimating quantile treatment effects, including methods based on difference-in-differences, matching, and more.
"""

from .qte import QTEEstimator
from .qtet import QTETEstimator
from .qdid import QDiDEstimator
from .cic import CiCEstimator

__all__ = ["QTEEstimator", "QTETEstimator", "QDiDEstimator", "CiCEstimator"]
