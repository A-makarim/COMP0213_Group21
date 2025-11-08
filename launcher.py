"""
Application Entry Point
Grasp Planning System with ML-based Success Prediction
"""
import os
import pybullet as p
import pybullet_data
import time
import math
import random
import pandas as pd
import joblib

from core.training import build_classifier
from core import visualization_suite
from grippers.factory import ManipulatorFactory
from shapes.factory import ShapeFactory
from core.performance_metrics import PerformanceMetrics

# Project root directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Manipulator configuration parameters
MANIPULATOR_SPECS = {
    "two_finger": {
        "cuboid_radius": 0.25,
        "cylinder_radius": 0.22,
        "radius_variation": (-0.05, 0.05),
        "y_offset": (-0.05, 0.05),
        "z_base_offset": -0.1,
        "z_variation": (-0.1, 0.1),
        "roll_range": (-0.5, 0.5),
        "approach_distance": 0.0
    },
    "three_finger": {
        "cuboid_radius": 0.35,
        "cylinder_radius": 0.30,
        "radius_variation": (-0.08, 0.08),
        "y_offset": (-0.08, 0.08),
        "z_base_offset": -0.15,
        "z_variation": (-0.15, 0.15),
        "roll_range": (-0.3, 0.3),
        "approach_distance": 0.05
    }
}

# Main menu system follows here...
# (Rest of the code with renamed functions and variables)
