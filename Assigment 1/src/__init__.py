"""
CV1 Assignment 1: Thin Lens Equation, Geometric Transformations, and OpenCV Basics

This package implements:
- Thin lens equation calculations
- Geometric transformations (2D and 3D)
- OpenCV image processing operations
"""

from . import thin_lens
from . import transformations
from . import opencv_operations

__all__ = [
    'thin_lens',
    'transformations',
    'opencv_operations',
]
