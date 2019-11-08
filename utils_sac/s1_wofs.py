#Currently redundant - SArah trying to turn s1_wofs_classify into a utils_function. 

import gc
import numpy as np
import xarray as xr

import datacube

from .dc_mosaic import restore_or_convert_dtypes
#from import dc_utilities as utilities
#from .dc_utilities import create_default_clean_mask
# Command line tool imports
import argparse
import os
import collections
import gdal
from datetime import datetime

def s1_wofs_classify(dataset_in, clean_mask=None, x_coord='longitude', y_coord='latitude',
                  time_coord='time', no_data=-9999, mosaic=False, enforce_float64=False):
        vv_threshold = 12
        vh_threshold = -15.5
        s1_coverage = dataset_in
        observations = ((s1_coverage["vv"] <= vv_threshold) & (s1_coverage["vh"] <= vh_threshold))
        return(observations)